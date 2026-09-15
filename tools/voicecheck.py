#!/usr/bin/env python3
"""Flag mechanical assistant-tells in public-facing text, and private-string leaks.

Usage:  voicecheck.py FILE [FILE...]
        voicecheck.py --tracked        every file git tracks in the current repo
        voicecheck.py --git            author, committer and message of every commit
                                       on the current branch
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
    ("notjust",  "med",  r"[Ii]t'?s not just .{1,40}?,? it'?s|[Mm]ore than just ",
     "'not just X, it's Y' construction."),
    ("whether",  "med",  r"[Ww]hether you'?re (a|an|new|just|looking)",
     "'whether you're X or Y' construction."),
    ("filler",   "med",  r"[Ii]n today'?s .{0,20}world|[Ii]n an era of|[Ii]t'?s worth noting|"
                         r"[Aa]t the end of the day|[Ll]et'?s dive|[Ii]n conclusion",
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
LONG_SENTENCE = 30   # words. Chosen register is short sentences and fragments.

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
RULEBOOK_DIRS = {"references", "tools", "examples", "tests"}
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


def long_sentences(para_lines):
    """Sentences over LONG_SENTENCE words in one paragraph, as (first line, count)."""
    if not para_lines:
        return 0
    text = " ".join(INLINE_CODE.sub(" ", t) for _, t in para_lines)
    return sum(1 for s in re.split(r"[.!?]+\s", text) if len(s.split()) > LONG_SENTENCE)


def scan(lines):
    """Return {check_id: (severity, message, [line numbers], total hits)}."""
    found = {}
    in_fence = False
    para = []   # (line number, text) of the paragraph being read

    def flush():
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
        for cid, sev, pat, msg in CHECKS:
            hits = re.findall(pat, prose)
            if hits:
                rec = found.setdefault(cid, [sev, msg, [], 0])
                rec[2].append(n)
                rec[3] += len(hits)
        if not is_heading:
            caps = sum(1 for rx in JARGON_RX for m in rx.finditer(prose)
                       if m.group() != m.group().lower())
            if caps:
                cid, sev, msg = NAMECAPS
                rec = found.setdefault(cid, [sev, msg, [], 0])
                rec[2].append(n)
                rec[3] += caps
    flush()
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
    unknown = flags - {"--tracked", "--git"}
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

        found = scan(lines)
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
