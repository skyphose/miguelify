#!/usr/bin/env python3
"""Flag mechanical assistant-tells in public-facing text, and private-string leaks.

Usage:  voicecheck.py FILE [FILE...]
        voicecheck.py --tracked        every file git tracks in the current repo
        voicecheck.py --git            author, committer and message of every commit
                                       on the current branch
        voicecheck.py --pro FILE...    professional register (pro/SKILL.md): standard
                                       caps and apostrophes, plus post-template hooks
        git diff --cached --name-only | xargs voicecheck.py

The flags combine. `voicecheck.py --tracked --git` is the pre-push check.

Regex only. It catches the tells that can be counted and nothing else. A clean
run is a floor, not a passing grade -- the judgment calls (honest claims, the
who-it-is-not-for paragraph, cutting a restating conclusion) still need a human
or a careful read. See ../SKILL.md.

If ../references/private.md exists it is also a leak list: every backticked string
under its "## Leak list" heading is grepped for in every file, including this
skill's own, and in commit metadata under --git. Leaks are reported separately and
set the exit status to 2, because a leak is a publish-blocker and a hype word is
not. The check refuses to run at all if private.md has itself been committed.

Anything shaped like an email, a home path, an IP, a token, a bearer header, a private
key or a credential assignment is reported as a possible leak whether or not a list
exists, and exits 1 with a "review" line. Placeholders in angle brackets, example.com
addresses and GitHub noreply addresses are not counted.

Exit: 0 clean, 1 voice findings or possible leaks, 2 listed leak or a committed private.md.
"""
import json
import os
import re
import subprocess
import sys

HYPE = (r"delve|leverage|robust|seamless|elevate|unlock|harness|empower|streamline|"
        r"effortless|comprehensive|cutting-edge|game.changer|powerhouse|"
        r"revolutioniz|transformative|blazing|supercharge|unparalleled|"
        r"meticulous|testament to|dive in|deep dive into the")

CHECKS = [
    # (id, severity, regex, message)
    ("emdash",   "high", r"[—–]",
     "em/en dash: {em_dash} in {messages} typed messages. The measured form is a spaced hyphen ' - '."),
    ("emoji",    "high", r"[\U0001F300-\U0001FAFF\U00002600-\U000027BF️]",
     "emoji: {emoji} in {messages} typed messages, none in anything shipped."),
    ("claude",   "high", r"Co-Authored-By:\s*Claude|Claude-Session:|Generated with \[?Claude",
     "Claude attribution: never in public repos. Standing preference."),
    ("british",  "med",  r"\b(licence|colour|favour|centre|metre|millimetre|organis\w+|analyse)\b",
     "British spelling: {british} in {messages} typed messages. The corpus is American."),
    ("hype",     "med",  HYPE,
     "hype word with no number behind it."),
    ("whether",  "med",  r"[Ww]hether you'?re (a|an|new|just|looking)",
     "'whether you're X or Y' construction."),
    ("filler",   "med",  r"[Ii]n today'?s .{0,20}world|[Ii]n an era of|"
                         r"[Aa]t the end of the day|[Ll]et'?s dive",
     "filler opener/closer."),
    ("intro",    "med",  r"^#{0,3}\s*Introducing\b",
     "'Introducing' opener: name the thing instead."),
    ("titlecase","low",  r"^#{1,6} (?:[A-Z][a-z]+ ){2,}[A-Z][a-z]+\s*$",
     "Title Case heading: headings are lowercase like the rest of the prose."),
    ("arrow",    "low",  r"→",
     "Unicode arrow: shipped commits and docs use ASCII '->'."),
    ("bang",     "low",  r"!(?!\[|=|\]|\))",
     "exclamation mark: {bang} in {messages} typed messages. Almost always cut."),
    ("labelbul", "low",  r"^\s*[-*] \*\*[A-Z][^*]{1,30}:\*\*",
     "bolded-label bullet: fine occasionally, not as the house format."),
    ("formal",   "med",  r"\b(?:repositor(?:y|ies)|utili[sz](?:e|es|ed|ing|ation)|approximately|"
                         r"in order to|kindly|README files?|prior to|subsequently)\b",
     "formal word with 0 uses in {messages} typed messages: repo not repository, use not "
     "utilize, about not approximately, before not prior to."),
]

CHECKS += [
    # Decided from A/B samples on 2026-09-14: contractions as typed, no apostrophe;
    # figures plain, not bold; short sentences, fragments allowed.
    ("apostrophe", "med",
     r"\b(?:don|doesn|didn|isn|aren|wasn|weren|can|won|wouldn|couldn|shouldn|hasn|haven|hadn)'t\b|"
     r"\b(?:it|that|what|there|here|let)'s\b|\bi'(?:m|ve|ll|d)\b|\b(?:you|we|they)'(?:re|ve|ll|d)\b",
     "apostrophe in a contraction: the corpus types dont, isnt, youre, lets. "
     "{apostrophe} apostrophes in {messages} typed messages."),
    ("uncontracted", "low",
     r"\b(?:do not|does not|did not|is not|are not|was not|cannot|you are|i am|that is|there is|it is)\b",
     "uncontracted form: contract it as typed, with no apostrophe. dont, isnt, youre, thats."),
    ("boldnum", "low", r"\*\*[^*\n]*\d[^*\n]*\*\*",
     "bold figure: numbers are plain, with spaced units. Chosen from A/B samples."),
]

# The patterns Wikipedia's AI-cleanup project catalogs at WP:AISIGNS
# (Wikipedia:Signs_of_AI_writing, read 2026-11-09). references/ai-tells.md has each
# one with its fix. These are signs of a deeper problem (a generic claim standing in
# for a specific one), so the message says what to put back, not just what to cut.
AI_VOCAB = (r"\bAdditionally,|\balign(?:s|ed)? with\b|\bbolster(?:s|ed|ing)?\b|\bcrucial\b|"
            r"\bemphasiz(?:e|es|ed|ing)\b|\benduring\b|\benhanc(?:e|es|ed|ing)\b|"
            r"\bfoster(?:s|ed|ing)?\b|\bgarner(?:s|ed|ing)?\b|"
            r"\bhighlight(?:s|ed|ing)? (?:the|its|their|how|a|an)\b|\binterplay\b|"
            r"\bintricat(?:e|ies)\b|\blandscape\b|\bpivotal\b|\bshowcas(?:e|es|ed|ing)\b|"
            r"\btapestry\b|\bunderscor(?:e|es|ed|ing)\b|\bvaluable\b|\bvibrant\b|"
            r"\bnestled\b|\bin the heart of\b|\bgroundbreaking\b|\brenowned\b|"
            r"\bdiverse array\b|\bcommitment to\b|\bexemplif(?:y|ies|ied)\b|\bprofound\b|"
            r"\bmultifaceted\b|\bquietly\b|\buniversally\b|\bdependable\b|\bboasts?\b")

CHECKS += [
    ("aivocab", "med", AI_VOCAB,
     "ai vocabulary (WP:AIWORDS). one is a coincidence, several is the strongest tell "
     "there is. say the plain thing: has, is, shows, important, or the number."),
    ("legacy", "med",
     r"\b(?:stands|serves) as (?:a|an) (?:testament|reminder|symbol)|\btestament to\b|"
     r"\b(?:pivotal|crucial|vital|key|significant|important) (?:role|moment|turning point)\b|"
     r"\bplays? an? (?:\w+ )?role in\b|\breflects? (?:a |the )?broader\b|\bsetting the stage\b|"
     r"\bmark(?:s|ed|ing) a (?:\w+ )?(?:shift|turning point|milestone)\b|\bevolving landscape\b|"
     r"\bindelible mark\b|\bdeeply rooted\b|\b(?:enduring|lasting) (?:legacy|impact|influence)\b|"
     r"\bfocal point\b|\bcontribut(?:es|ed|ing) to the broader\b",
     "puffed-up significance (WP:AILEGACY). nobody asked what it symbolizes. cut it, or "
     "replace it with what the thing actually does, with a number."),
    ("ingtail", "med",
     r", (?:highlighting|underscoring|emphasizing|reflecting|showcasing|symbolizing|ensuring|"
     r"fostering|cultivating|contributing to|enhancing|demonstrating|solidifying|"
     r"embodying|reinforcing|signaling)\b",
     "trailing '-ing' analysis (WP:SUPERFICIAL): a clause tacked on to say why a fact "
     "matters. end the sentence at the fact."),
    ("copula", "low",
     r"\b(?:serves|stands|functions|operates|acts) as (?:a|an|the)\b|"
     r"\b(?:features|offers) (?:a|an|two|three|four|five|several|multiple|\d)\b|\brefers to the\b",
     "'serves as' / 'features a' for is / has (WP:AINOCOPULA). say 'is' and 'has'."),
    ("negpar", "med",
     r"(?i)\bnot only\b[^.]{0,80}\bbut\b|\bnot just\b|\bmore than just\b|"
     r"\b(?:it'?s|its|is|isn'?t|this is|that'?s|thats) not (?:a|an|about|merely|simply)\b"
     r"[^.]{0,60}[,;]\s*(?:but|it'?s|its|it is)\b|"
     r"\bno [^,.]{1,30}, no [^,.]{1,30}, (?:just|only)\b",
     "negative parallelism, 'not X, but Y' (WP:AIPARALLEL). nobody said it was X. "
     "say what it is."),
    ("ratherthan", "low", r"\b[Rr]ather than\b",
     "'Y rather than X' (WP:AIPARALLEL), the 2026 form of the same move. fine once for a "
     "real choice between two options, a tell as a habit."),
    ("vague", "med",
     r"\b(?:[Mm]any|[Ss]ome|[Mm]ost|[Ss]everal) (?:users|people|players|makers|reviewers|"
     r"critics|experts|observers|developers|commenters|printers)\b (?:report|say|find|note|"
     r"agree|argue|have|praise|describe)|\b[Ee]xperts (?:say|argue|agree|note|suggest)\b|"
     r"\b[Oo]bservers have\b|\b[Ii]ndustry reports\b|\bwidely (?:regarded|considered|praised|"
     r"seen|recognized)\b",
     "vague attribution (WP:AIWEASEL). who, how many, and where. name them or cut it."),
    ("connect", "low",
     r"\b(?:is|are|was|were|became|been|be|being) (?:closely |widely |often )?associated with\b|"
     r"\bin connection with\b|\bin association with\b",
     "'associated with' instead of the actual relationship (WP:AICONNECT). made it, "
     "uses it, runs it: say which."),
    ("disclaim", "med",
     r"\b[Ii]t'?s (?:important|worth|crucial) (?:to )?(?:note|noting|remember|mention)|"
     r"\b[Ii]t is (?:important|worth|crucial) to (?:note|remember|mention)|"
     r"\b[Bb]ased on (?:the )?available information\b|"
     r"\bnot (?:widely|publicly|extensively|well) (?:documented|available|disclosed|known)\b|"
     r"\b(?:limited|scarce) in (?:the )?(?:provided|available)\b|"
     r"\bshould be (?:treated|read|seen|understood|viewed|taken) as\b|"
     r"\bdoes not (?:by itself |on its own )?establish\b|\bshould not be confused with\b",
     "hedging disclaimer (WP:AIDISCLAIMER). the honest version is first person and "
     "specific: 'untested at this size. i printed v1.0, not this one.'"),
    ("notability", "med",
     r"\b(?:featured|profiled|covered|mentioned|highlighted) (?:in|by) (?:several|multiple|"
     r"many|numerous|various|leading|prominent|major)\b|\bactive (?:social media|online) "
     r"presence\b|\bindependent coverage\b|\b(?:media|news|hobby|industry) outlets\b|"
     r"\btrade publications\b|\bidentifies (?:him|her|them|it) as\b",
     "canned notability (WP:AIATTR). link the one source that matters, or leave it out."),
    ("challenges", "med",
     r"\b[Dd]espite (?:its|their|these|this|the|his|her) [^.]{0,40}\bchallenges\b|"
     r"\bfaces? (?:several|many|numerous|some|new|significant|a number of) challenges\b|"
     r"\b[Ff]uture (?:outlook|prospects|directions)\b|"
     r"\b[Cc]hallenges and (?:future|opportunities|legacy|limitations)\b|"
     r"\bcontinues? to (?:thrive|evolve|grow)\b",
     "'despite these challenges' formula (WP:FACESCHALLENGES). list the actual limits "
     "with numbers, and stop. no upbeat closer."),
    ("summary", "med",
     r"(?:^|[.!?]\s+)(?:[Oo]verall|[Ii]n summary|[Ii]n conclusion|[Tt]o sum up|"
     r"[Uu]ltimately|[Ii]n short|[Aa]ll in all),",
     "restating conclusion (WP:CONCLUSION). the reader just read it. end on the last "
     "real fact."),
    ("chatbot", "high",
     r"\b[Ii] hope (?:this|that) helps\b|\b[Ll]et me know (?:if|whether)\b|"
     r"\b[Ww]ould you like\b|\b(?:Certainly|Of course|Absolutely|Great question)[!.,]|"
     r"\b[Yy]ou'?re (?:absolutely )?right\b|\b[Hh]ere'?s (?:a|an|the) (?:revised|updated|"
     r"rewritten|polished|more detailed|detailed|breakdown|summary|draft)\b|"
     r"\b[Ff]eel free to\b|\b[Hh]appy to help\b|\bmore detailed breakdown\b",
     "chat aimed at the user left in the text (WP:COLLABCOMM). cut it."),
    ("placeholder", "high",
     r"\[(?:[Ii]nsert|[Yy]our|[Aa]dd|[Dd]escribe|[Ee]nter|[Pp]laceholder|TODO|TBD|"
     r"[Ll]ink|URL|[Dd]ate)\b[^\]]*\](?!\()|\b(?:YYYY-MM-DD|example\.com/your)",
     "unfilled template placeholder (WP:AIPLACEHOLDER)."),
    ("curly", "low", r"[“”‘’]",
     "curly quote or apostrophe (WP:AICURLY). straight quotes, and contractions have no "
     "apostrophe anyway."),
    ("andhead", "low", r"^#{1,6} [^#\n]*\b(?:and|&) (?:recognition|legacy|impact|future|"
     r"challenges|awards|limitations|considerations|benefits|outlook)\b",
     "'X and Y' heading (WP:AISIGNS, 'Awards and recognition'). one heading, one thing, "
     "lowercase, often a question."),
]

# --pro: the professional register (pro/SKILL.md). Same content rules and AI tells,
# but standard capitalization, apostrophes in contractions and no deliberate slips.
# These checks are personal-register rules, so pro mode drops them.
PRO_SKIP = {"apostrophe", "uncontracted", "namecaps"}
PRO_MESSAGES = {
    "titlecase": "Title Case heading: use sentence case. Title Case is a WP:AISIGNS formatting tell.",
    "curly": "curly quote or apostrophe (WP:AICURLY): use straight quotes.",
}
PRO_CHECKS = [
    ("bare", "med",
     r"\b(?:dont|doesnt|didnt|isnt|arent|wasnt|werent|wouldnt|couldnt|shouldnt|hasnt|"
     r"havent|hadnt|youre|theyre|thats|ive|im|youve|theyve|weve)\b",
     "contraction with no apostrophe: personal register. professional copy keeps it: "
     "don't, isn't, you're, that's."),
    ("lowerstart", "low",
     r"(?:^(?:#{1,6} |\s*(?:[-*+]|\d+\.)\s+)?|(?:[!?]|(?<!e\.g)(?<!i\.e)(?<!etc)(?<!vs)\.)\s+)(?!https?://|www\.)[a-z]",
     "sentence or bullet starts lowercase: professional copy uses standard capitalization."),
    ("lowerI", "med", r"(?<![\w.])i(?=\s|'|,)",
     "lowercase 'i' as a pronoun: capitalize it."),
    ("hook", "med",
     r"(?i)\b(?:I'?m|we'?re) (?:thrilled|excited|delighted|proud|humbled|honou?red) to "
     r"(?:announce|share|introduce|launch)|\bhere'?s the thing\b|\blet that sink in\b|"
     r"\bhere'?s what (?:I|we) learned\b|\bwhat do you think\?|\bthoughts\?|"
     r"\bdrop (?:a|your) (?:comment|thoughts)|\bagree\?\s*$|\bgame[- ]chang|"
     r"\b(?:big|huge) news\b|\bstay tuned\b|\bthe secret\?|\bthe result\?|"
     r"\bspoiler:|\bhot take\b|\bunpopular opinion\b",
     "post-template hook or engagement bait: open on what was made or found, end on the "
     "last real fact or the link."),
    ("hashtags", "low", r"(?:#\w+\s*){4,}",
     "a wall of hashtags: zero to three, at the end, in plain words."),
]

LONG_SENTENCE = 30   # words. Chosen register is short sentences and fragments.

# Rhythm. Since mid-2026 the newest models drop em dashes entirely and hold every
# sentence to roughly 8-20 words with only commas and periods (WP:AIWORDS, GPT-6 era;
# WP:AIDASH). "Short sentences, no em dash" is miguelify's own rule, so followed too
# literally it produces exactly that. His typing is bursty: median 11, a fifth of
# sentences 5 words or fewer, the 90th percentile at 25. Flag prose that is too even.
RHYTHM_MIN_SENTENCES = 12
RHYTHM_MIN_CV = 0.40      # stdev / mean of sentence length
RHYTHM_MAX_BAND = 0.75    # share of sentences between 8 and 20 words

# Capitalized forms of the vocabulary in jargon.txt: github, openscad, stl, mtg. The
# corpus types them lowercase, so published prose does too. Checked outside CHECKS
# because the word list is read from a file, not written into a regex here.
NAMECAPS = ("namecaps", "low",
            "capitalized name: the corpus types names and acronyms lowercase, "
            "{jargon_lower} of {jargon_total}. github, openscad, pokemon, stl, mtg.")

# Lines where a tell is being quoted as evidence rather than used.
EXEMPT = re.compile(r"^\s*(>|\|)|zero (em dash|in )|never typed")
INLINE_CODE = re.compile(r"`[^`]*`")
HEADING = re.compile(r"^#{1,6} ")

SELF_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRIVATE = os.path.join(SELF_DIR, "references", "private.md")
PROFILE = os.path.join(SELF_DIR, "references", "profile.json")
JARGON = os.path.join(SELF_DIR, "references", "jargon.txt")
RULEBOOK_FILES = {"SKILL.md", "LICENSE", ".gitignore"}
RULEBOOK_DIRS = {"references", "tools", "examples", "tests", "pro"}
# The tests plant emails, paths and keys on purpose. Listed terms are still a hard
# block there; only the generic review tier steps aside.
GENERIC_SKIP_DIRS = {"tests"}


def jargon_words():
    try:
        with open(JARGON, encoding="utf-8") as fh:
            return [ln.split("#", 1)[0].strip() for ln in fh if ln.split("#", 1)[0].strip()]
    except OSError:
        return []


JARGON_RX = [re.compile(r"\b" + re.escape(w) + r"s?\b", re.I) for w in jargon_words()]

# Numbers quoted in the messages above. The shipped baseline is the fallback when
# no profile has been generated yet; extract_voice_corpus.py overwrites them.
BASELINE = {"messages": 90, "em_dash": 0, "emoji": 0, "british": 0, "bang": 2,
            "jargon_lower": 20, "jargon_total": 22, "apostrophe": 0}


def profile_fields():
    fields = dict(BASELINE)
    try:
        with open(PROFILE, encoding="utf-8") as fh:
            prof = json.load(fh)
        fields["messages"] = prof["messages"]
        for k in ("em_dash", "emoji", "british", "bang", "apostrophe"):
            fields[k] = prof["counts"].get(k, fields[k])
        if prof.get("casing", {}).get("total"):
            fields["jargon_lower"] = prof["casing"]["lowercase"]
            fields["jargon_total"] = prof["casing"]["total"]
    except (OSError, ValueError, KeyError):
        pass
    return fields

# A GitHub noreply address is the public login by construction, never a leak.
NOREPLY = re.compile(r"\S+@users\.noreply\.github\.com")

# Shapes that are a leak in any repo, list or no list. These exit 1 and say "review",
# because a README can legitimately carry an address or an IP; the private.md terms
# are the hard block. The scraper imports the same patterns to redact the corpus.
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
HOMEPATH = re.compile(r"/(?:Users|home)/[A-Za-z0-9._-]+")
IPV4 = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
TOKEN = re.compile(r"\b(?:sk|pk)-[A-Za-z0-9_-]{16,}|\bgh[pousr]_[A-Za-z0-9]{16,}|"
                   r"\bAKIA[A-Z0-9]{16}\b|\bxox[baprs]-[A-Za-z0-9-]+|"
                   r"\beyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{10,}|hooks\.slack\.com/services/\S+")
BEARER = re.compile(r"\b[Bb]earer\s+[A-Za-z0-9._-]{16,}")
PRIVATE_KEY = re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")
CREDENTIAL = re.compile(r"\b(?:password|passwd|api[_-]?key|secret[_-]?key|client[_-]?secret)"
                        r"\s*[:=]\s*\S", re.I)
GENERIC = [("email", EMAIL), ("home path", HOMEPATH), ("ipv4", IPV4), ("token", TOKEN),
           ("bearer", BEARER), ("private key", PRIVATE_KEY), ("credential", CREDENTIAL)]
# Placeholders and documentation addresses are not leaks.
GENERIC_OK = re.compile(r"users\.noreply\.github\.com|example\.(?:com|org|net)$|<[^>]*>")


def sentence_lengths(para_lines):
    """Word count of every sentence in one paragraph."""
    if not para_lines:
        return []
    text = " ".join(INLINE_CODE.sub(" ", t) for _, t in para_lines)
    text = re.sub(r"^\s*(?:[-*+]|\d+\.)\s+", "", text)
    return [len(s.split()) for s in re.split(r"[.!?]+(?:\s|$)", text) if s.split()]


def long_sentences(para_lines):
    """How many sentences in one paragraph run over LONG_SENTENCE words."""
    return sum(1 for n in sentence_lengths(para_lines) if n > LONG_SENTENCE)


def rhythm(lengths):
    """(cv, band share) when the prose is too even to read as typed, else None."""
    if len(lengths) < RHYTHM_MIN_SENTENCES:
        return None
    mean = sum(lengths) / len(lengths)
    sd = (sum((n - mean) ** 2 for n in lengths) / len(lengths)) ** 0.5
    cv = sd / mean if mean else 0
    band = sum(1 for n in lengths if 8 <= n <= 20) / len(lengths)
    if cv < RHYTHM_MIN_CV or band > RHYTHM_MAX_BAND:
        return cv, band
    return None


def active_checks(pro):
    if not pro:
        return CHECKS
    out = [(cid, sev, pat, PRO_MESSAGES.get(cid, msg))
           for cid, sev, pat, msg in CHECKS if cid not in PRO_SKIP]
    return out + PRO_CHECKS


def scan(lines, pro=False):
    """Return {check_id: (severity, message, [line numbers], total hits)}."""
    checks = active_checks(pro)
    found = {}
    in_fence = False
    para = []   # (line number, text) of the paragraph being read
    lengths = []

    def flush():
        lengths.extend(sentence_lengths(para))
        n_long = long_sentences(para)
        if n_long:
            rec = found.setdefault("longsentence", ["low",
                  f"sentence over {LONG_SENTENCE} words: the register is short sentences, "
                  "fragments allowed. Chosen from A/B samples.", [], 0])
            rec[2].append(para[0][0])
            rec[3] += n_long
        para.clear()

    for n, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            flush()
            continue
        if in_fence or EXEMPT.search(line) or not line.strip():
            flush()
            continue
        prose = INLINE_CODE.sub(" ", line)   # a literal keeps its case and its dashes
        is_heading = bool(HEADING.match(line))
        if is_heading:
            flush()               # a heading is not part of any paragraph
        else:
            para.append((n, prose))
        for cid, sev, pat, msg in checks:
            # a code span can open a sentence, so it stands in as a capital here
            target = INLINE_CODE.sub("C", line) if cid == "lowerstart" else prose
            hits = re.findall(pat, target)
            if hits:
                rec = found.setdefault(cid, [sev, msg, [], 0])
                rec[2].append(n)
                rec[3] += len(hits)
        if not is_heading and not pro:
            caps = sum(1 for rx in JARGON_RX for m in rx.finditer(prose)
                       if m.group() != m.group().lower())
            if caps:
                cid, sev, msg = NAMECAPS
                rec = found.setdefault(cid, [sev, msg, [], 0])
                rec[2].append(n)
                rec[3] += caps
    flush()
    even = rhythm(lengths)
    if even:
        cv, band = even
        found["rhythm"] = ["low",
            f"even rhythm: {len(lengths)} sentences, spread {cv:.2f} (want {RHYTHM_MIN_CV}+), "
            f"{band:.0%} of them 8-20 words (want under {RHYTHM_MAX_BAND:.0%}). the newest "
            "models write exactly this. mix in fragments and the odd longer sentence with "
            "a colon or a ' - '.", [1], 1]
    return found


def leak_terms():
    """Backticked strings under '## Leak list' in the untracked private overlay.

    Word-boundaried, so a 3-letter acronym does not match inside an ordinary word.
    Case-sensitive when the term carries any uppercase, since the short all-caps ones
    are the false-positive risk. A '.x' octet is treated as a range, not a literal.
    """
    try:
        with open(PRIVATE, encoding="utf-8") as fh:
            body = fh.read()
    except OSError:
        return []
    m = re.search(r"^## Leak list\s*$(.*?)(?=^## |\Z)", body, re.M | re.S)
    if not m:
        return []
    terms = []
    for raw in sorted(set(re.findall(r"`([^`\n]{3,})`", m.group(1)))):
        if raw.startswith("<") and raw.endswith(">"):
            continue  # an unfilled template placeholder
        pat = re.escape(raw).replace(r"\.x", r"\.\d{1,3}")
        if raw[:1].isalnum():
            pat = r"\b" + pat
        if raw[-1:].isalnum():
            pat = pat + r"\b"
        flags = 0 if any(c.isupper() for c in raw) else re.I
        terms.append((raw, re.compile(pat, flags)))
    return terms


def scan_leaks(lines, terms):
    hits = {}
    for n, line in enumerate(lines, 1):
        line = NOREPLY.sub("", line)
        for raw, rx in terms:
            if rx.search(line):
                hits.setdefault(raw, []).append(n)
    return hits


def scan_generic(lines):
    """{shape: [line numbers]} for anything shaped like a secret or an identity."""
    hits = {}
    for n, line in enumerate(lines, 1):
        for name, rx in GENERIC:
            for m in rx.finditer(line):
                if GENERIC_OK.search(m.group()):
                    continue
                hits.setdefault(name, []).append(n)
                break
    return hits


def report_generic(label, hits):
    print(f"\n{label}  possible leak - review before publishing")
    for name, nums in sorted(hits.items()):
        print(f"  high review    {len(nums):>3}x  looks like a {name}")
        print(f"       {'':<9}      lines {fmt_lines(nums)}")
    return sum(len(v) for v in hits.values())


def private_is_tracked():
    r = subprocess.run(["git", "-C", SELF_DIR, "ls-files", "--error-unmatch",
                        "references/private.md"], capture_output=True)
    return r.returncode == 0


def tracked_files():
    r = subprocess.run(["git", "ls-files", "-z"], capture_output=True, text=True)
    if r.returncode:
        print("--tracked: not inside a git repository", file=sys.stderr)
        return []
    return [p for p in r.stdout.split("\0") if p]


def git_metadata():
    """(label, lines) for every commit on the current branch: identities plus message."""
    fmt = "%H%x00%an%x00%ae%x00%cn%x00%ce%x00%B%x1e"
    r = subprocess.run(["git", "log", f"--format={fmt}"], capture_output=True, text=True)
    if r.returncode:
        print("--git: not inside a git repository", file=sys.stderr)
        return []
    recs = []
    for rec in r.stdout.split("\x1e"):
        rec = rec.strip("\n")
        if not rec:
            continue
        h, an, ae, cn, ce, body = rec.split("\x00", 5)
        lines = [f"author {an} <{ae}>", f"committer {cn} <{ce}>"] + body.splitlines()
        recs.append((f"commit {h[:7]}", lines))
    return recs


def fmt_lines(nums, cap=8):
    shown = ", ".join(str(n) for n in nums[:cap])
    return shown + (f" (+{len(nums) - cap} more)" if len(nums) > cap else "")


def report_leaks(label, lk):
    print(f"\n{label}  LEAK - do not publish")
    for raw, nums in sorted(lk.items()):
        print(f"  high leak      {len(nums):>3}x  private string {raw!r}")
        print(f"       {'':<9}      lines {fmt_lines(nums)}")
    return sum(len(v) for v in lk.values())


def is_binary(path):
    try:
        with open(path, "rb") as fh:
            return b"\0" in fh.read(8192)
    except OSError:
        return False


def main(argv):
    flags = {a for a in argv if a.startswith("--")}
    paths = [a for a in argv if not a.startswith("--")]
    unknown = flags - {"--tracked", "--git", "--pro"}
    pro = "--pro" in flags
    if unknown:
        print(f"unknown flag(s): {' '.join(sorted(unknown))}\n")
        print(__doc__)
        return 2
    if "--tracked" in flags:
        paths += tracked_files()
    if not paths and "--git" not in flags:
        print(__doc__)
        return 2

    if private_is_tracked():
        print("references/private.md is committed in this skill's repo. That file is the")
        print("leak list itself. Remove it from git before doing anything else:")
        print("    git rm --cached references/private.md")
        return 2

    order = {"high": 0, "med": 1, "low": 2}
    grand = 0
    fields = profile_fields()
    terms = leak_terms()
    leaked = 0
    reviews = 0
    for path in paths:
        if is_binary(path):
            print(f"{path}: skipped, binary")
            continue
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                lines = fh.read().splitlines()
        except OSError as exc:
            print(f"{path}: cannot read ({exc})", file=sys.stderr)
            continue

        if terms:
            lk = scan_leaks(lines, terms)
            if lk:
                leaked += report_leaks(path, lk)
        rel0 = os.path.relpath(os.path.abspath(path), SELF_DIR).split(os.sep, 1)[0]
        gn = {} if rel0 in GENERIC_SKIP_DIRS else scan_generic(lines)
        if gn:
            reviews += report_generic(path, gn)

        # The rulebook quotes the tells it bans, so those files exempt themselves.
        # Anything else, README.md included, is public copy wherever it lives.
        rel = os.path.relpath(os.path.abspath(path), SELF_DIR)
        if rel in RULEBOOK_FILES or rel.split(os.sep, 1)[0] in RULEBOOK_DIRS:
            print(f"{path}: skipped, this is the miguelify skill's own rulebook")
            continue

        found = scan(lines, pro=pro)
        total = sum(rec[3] for rec in found.values())
        grand += total
        if not found:
            print(f"{path}: clean")
            continue

        print(f"\n{path}  ({total} hit(s))")
        for cid, (sev, msg, nums, count) in sorted(
                found.items(), key=lambda kv: (order[kv[1][0]], -kv[1][3])):
            print(f"  {sev:<4} {cid:<9} {count:>3}x  {msg.format(**fields)}")
            print(f"       {'':<9}      lines {fmt_lines(nums)}")

    if "--git" in flags:
        commits = git_metadata()
        if not terms:
            print(f"--git: {len(commits)} commit(s), but no leak list to check them against")
        else:
            bad = 0
            for label, lines in commits:
                lk = scan_leaks(lines, terms)
                if lk:
                    leaked += report_leaks(label, lk)
                    bad += 1
                # Generic shapes only on the identity lines: a machine-name email is the
                # real risk there, and a message body quoting one as an example is not.
                gn = scan_generic(lines[:2])
                if gn:
                    reviews += report_generic(label, gn)
            print(f"--git: {len(commits)} commit(s) checked, {bad} with a private string")

    print(f"\n{grand} hit(s) across {len(paths)} file(s).")
    if leaked:
        print(f"{leaked} private-string leak(s). Fix these before anything is pushed.")
        return 2
    if reviews:
        print(f"{reviews} possible leak(s): something shaped like an email, path, IP, token "
              f"or credential. Read each one before pushing.")
    if grand:
        print("Mechanical tells only. Still check by hand: unearned claims, a missing")
        print("trade-off paragraph, a restating conclusion, numbers without units.")
    return 1 if (grand or reviews) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
