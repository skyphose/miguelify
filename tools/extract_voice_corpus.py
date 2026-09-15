#!/usr/bin/env python3
"""Rebuild the voice corpus from your own typed messages, and the profile the tools read.

Usage:  extract_voice_corpus.py [OUT] [--force]
        default OUT: ../references/voice_corpus.txt, which .gitignore excludes

Pulls user-authored messages out of ~/.claude/projects/**/*.jsonl and drops the
things that are not typing: tool results, hook and system-reminder noise,
compaction summaries, and the long assistant-written prompts that get replayed
as user turns. Then measures the style counts the rules are built on and writes
them to ../references/profile.json, which voicecheck.py and slipplan.py read.

The corpus is raw chat, so two things guard it. Emails, home paths, token-shaped
strings and every term in ../references/private.md are redacted before anything is
written. And the tool refuses to write into a git working tree unless the target
path is gitignored there, because a transcript dump landing in a project directory
is exactly how it would end up committed. It also refuses to write anything from
fewer than 20 messages, so a machine with no transcripts does not overwrite a real
profile with zeros. --force overrides both checks.

The typo inventory is automatic: a word that is not in the dictionary but is one
adjacent swap, one extra letter or one missing letter away from a word that is,
seen at most twice. Words that repeat are jargon, not slips, and so is anything
in ../references/jargon.txt: add a word there when the inventory flags vocabulary
the system word list does not know. It under-counts (a slip two edits away is
invisible) and cannot see wrong-word errors at all, since those need context. Read
the list it prints before trusting the class weights.

Rerun this after a few months of new sessions to check the rules still hold.
"""
import collections
import datetime
import glob
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from voicecheck import leak_terms, EMAIL, HOMEPATH, TOKEN, BEARER, PRIVATE_KEY  # noqa: E402
from slipplan import load_dict, is_real, JARGON, CONTRACTIONS  # noqa: E402

HOME = os.path.expanduser("~")
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_OUT = os.path.join(SKILL_DIR, "references", "voice_corpus.txt")
PROFILE = os.path.join(SKILL_DIR, "references", "profile.json")
DROP_PREFIX = ("Caveat:", "[Request interrupted", "<", "This session is being continued")
DROP_SUBSTR = ("tool_use_id", "Analysis:\nLet me chronologically")
SHORT = 700  # above this, it is a pasted prompt or a summary, not typing
MIN_MESSAGES = 20  # below this the counts are noise and the profile is left alone

# The secret and identity shapes live in voicecheck.py so the linter and this redactor
# never disagree about what a leak looks like. Credentials get their value blanked.
CREDENTIAL_VALUE = re.compile(r"(\b(?:password|passwd|api[_-]?key|secret[_-]?key|client[_-]?secret)"
                              r"\s*[:=]\s*)\S+", re.I)

LETTERS = "abcdefghijklmnopqrstuvwxyz"
# "double" means any extra letter, not only a doubled one. It is the class slipplan
# generates as a doubled letter, and the name is kept so the two tools agree.
CLASSES = ("swap", "double", "drop")
MAX_REPEATS = 2   # a misspelling that recurs identically is a habit or jargon



def redact(text, terms):
    text = PRIVATE_KEY.sub("[private key]", text)
    text = BEARER.sub("[token]", text)
    text = TOKEN.sub("[token]", text)
    text = CREDENTIAL_VALUE.sub(r"\1[secret]", text)
    text = EMAIL.sub("[email]", text)
    text = HOMEPATH.sub("~", text)
    for _raw, rx in terms:
        text = rx.sub("[private]", text)
    return text


def unsafe_target(out):
    """None if it is fine to write here, else the reason it is not."""
    d = os.path.dirname(os.path.abspath(out)) or "."
    inside = subprocess.run(["git", "-C", d, "rev-parse", "--is-inside-work-tree"],
                            capture_output=True, text=True)
    if inside.returncode != 0:
        return None
    ignored = subprocess.run(["git", "-C", d, "check-ignore", "-q", os.path.abspath(out)],
                             capture_output=True)
    if ignored.returncode == 0:
        return None
    return "inside a git working tree and not gitignored there"


def collect():
    rows = []
    for path in glob.glob(os.path.join(HOME, ".claude/projects/**/*.jsonl"), recursive=True):
        with open(path, errors="ignore") as fh:
            for line in fh:
                try:
                    d = json.loads(line)
                except ValueError:
                    continue
                if d.get("type") != "user" or d.get("isMeta"):
                    continue
                content = (d.get("message") or {}).get("content")
                if isinstance(content, list):
                    text = " ".join(p.get("text", "") for p in content
                                    if isinstance(p, dict) and p.get("type") == "text")
                elif isinstance(content, str):
                    text = content
                else:
                    continue
                text = re.sub(r"<system-reminder>.*?</system-reminder>", "",
                              text, flags=re.S).strip()
                if not text or text.startswith(DROP_PREFIX):
                    continue
                if any(s in text for s in DROP_SUBSTR):
                    continue
                rows.append((d.get("timestamp", ""), text))
    rows.sort()
    return rows


def measure(typed):
    blob = "\n".join(typed)

    def n(pat):
        return len(re.findall(pat, blob))

    return {
        "em_dash": n(r"[—–]"),
        "spaced_hyphen": n(r" - "),
        "emoji": n(r"[\U0001F300-\U0001FAFF]"),
        "lets": n(r"\blets\b"),
        "let_s": n(r"\blet's\b"),
        "can_we": n(r"\bcan we\b"),
        "question": n(r"\?"),
        "bang": n(r"!"),
        "british": n(r"\b(licence|colour|favour|centre|metre)\b"),
        "apostrophe": n(r"[A-Za-z]'[A-Za-z]"),
        "bare_contractions": len([w for w in re.findall(r"[a-z]+", blob.lower())
                                  if w in CONTRACTIONS and w not in ("its", "were")]),   # those two are ambiguous
        "starts_upper": sum(1 for m in typed if m[:1].isupper()),
        "ends_period": sum(1 for m in typed if m.rstrip().endswith(".")),
    }


def classify_typo(w, real):
    """(class, correction) if w is one edit from a real word, else None."""
    for i in range(len(w) - 1):
        s = w[:i] + w[i + 1] + w[i] + w[i + 2:]
        if s != w and is_real(s, real):
            return "swap", s
    for i in range(len(w)):
        s = w[:i] + w[i + 1:]
        if len(s) >= 3 and is_real(s, real):
            return "double", s
    for i in range(len(w) + 1):
        for ch in LETTERS:
            s = w[:i] + ch + w[i:]
            if is_real(s, real):
                return "drop", s
    return None


def typo_inventory(typed, real):
    """(total words, {typo: (class, correction)})."""
    words = re.findall(r"[a-z]+", " ".join(typed).lower())
    found = {}
    for w, n in collections.Counter(words).items():
        if len(w) < 4 or n > MAX_REPEATS or w in CONTRACTIONS or is_real(w, real):
            continue
        r = classify_typo(w, real)
        if r:
            found[w] = r
    return len(words), found


def jargon_words():
    try:
        with open(JARGON, encoding="utf-8") as fh:
            return [ln.split("#", 1)[0].strip() for ln in fh if ln.split("#", 1)[0].strip()]
    except OSError:
        return []


def casing(typed, words):
    """How the corpus author cases the vocabulary in jargon.txt, exact forms as typed.

    This is what backs the lowercase-names rule: product names and acronyms are
    lowercase in the corpus, so they stay lowercase in published prose.
    """
    blob = "\n".join(typed)
    forms = {}
    for w in words:
        c = collections.Counter(m.group() for m in
                                re.finditer(r"\b" + re.escape(w) + r"s?\b", blob, re.I))
        if c:
            forms[w] = dict(c.most_common())
    lower = sum(n for f in forms.values() for k, n in f.items() if k == k.lower())
    total = sum(n for f in forms.values() for n in f.values())
    return {"lowercase": lower, "total": total, "forms": forms}


def load_previous():
    try:
        with open(PROFILE, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


def report(typed, counts, total_words, found, previous):
    labels = [
        ("em_dash", "em dash"), ("spaced_hyphen", "spaced hyphen ' - '"),
        ("emoji", "emoji"), ("lets", "'lets'"), ("let_s", "'let's'"),
        ("can_we", "'can we'"), ("question", "question marks"),
        ("bang", "exclamation marks"), ("british", "British spellings"),
        ("apostrophe", "apostrophes inside words"),
        ("bare_contractions", "contractions with no apostrophe"),
    ]
    width = max(len(lbl) for _, lbl in labels) + 2
    print(f"\n{len(typed)} hand-typed messages (under {SHORT} chars), {total_words} words\n")
    for key, lbl in labels:
        print(f"  {lbl:<{width}}  {counts[key]}")
    print(f"  {'starts uppercase':<{width}}  {counts['starts_upper']}/{len(typed)}")
    print(f"  {'ends with a period':<{width}}  {counts['ends_period']}/{len(typed)}")

    by_class = {c: sorted(w for w, (k, _) in found.items() if k == c) for c in CLASSES}
    rate = round(total_words / len(found)) if found else None
    print(f"\n{len(found)} typos found, 1 per {rate} words" if found else "\nno typos found")
    for c in CLASSES:
        print(f"  {c:<8} {len(by_class[c]):>3}   " + " ".join(by_class[c][:12]))
    print("\n  full inventory (word -> what it probably was):")
    for w in sorted(found):
        k, fix = found[w]
        print(f"    {w:<16} -> {fix:<16} [{k}]")

    cs = casing(typed, jargon_words())
    if cs["total"]:
        odd = [f"{k} {n}" for f in cs["forms"].values() for k, n in f.items() if k != k.lower()]
        print(f"\ncasing of jargon.txt words: {cs['lowercase']} of {cs['total']} lowercase"
              + (f"   (not: {', '.join(odd)})" if odd else ""))

    if previous:
        keys = ("em_dash", "emoji", "british", "lets", "let_s")
        drift = [(k, previous["counts"].get(k), counts[k]) for k in keys
                 if previous["counts"].get(k) != counts[k]]
        print(f"\nDrift since profile of {previous.get('generated')} "
              f"({previous.get('messages')} messages):")
        if not drift:
            print("  none on the load-bearing counts.")
        for k, old, new in drift:
            print(f"  {k}: {old} -> {new}")
        zeros = [k for k in ("em_dash", "emoji", "british", "let_s") if counts[k]]
        if zeros:
            print(f"  A previously-zero count is now nonzero: {', '.join(zeros)}.")
            print("  Reread ../references/voice.md before trusting the absolutes.")


def main(argv):
    force = "--force" in argv
    args = [a for a in argv if a != "--force"]
    out = args[0] if args else DEFAULT_OUT

    why = unsafe_target(out)
    if why and not force:
        print(f"refusing to write {out}: {why}.", file=sys.stderr)
        print("The corpus is raw chat. Write it somewhere gitignored, or pass --force.",
              file=sys.stderr)
        return 2

    terms = leak_terms()
    if not terms:
        print("note: no references/private.md leak list, so only emails, home paths and",
              file=sys.stderr)
        print("token-shaped strings are redacted. Hostnames and names will pass through.",
              file=sys.stderr)

    rows = [(ts, redact(t, terms)) for ts, t in collect()]
    typed = [t for _, t in rows if len(t) < SHORT]
    if len(typed) < MIN_MESSAGES and not force:
        print(f"only {len(typed)} typed message(s) under ~/.claude/projects. That is not a "
              f"corpus, and the counts would be noise.", file=sys.stderr)
        print(f"Nothing written, previous profile kept. --force overrides. The numbers start "
              f"to mean something around {MIN_MESSAGES} messages.", file=sys.stderr)
        return 1
    with open(out, "w") as fh:
        for ts, text in rows:
            if len(text) < SHORT:
                fh.write(f"=== {ts[:19]}\n{text}\n")
    print(f"wrote {out} ({len(typed)} of {len(rows)} messages kept, redacted)")

    counts = measure(typed)
    total_words, found = typo_inventory(typed, load_dict())
    previous = load_previous()
    report(typed, counts, total_words, found, previous)

    by_class = {c: sorted(w for w, (k, _) in found.items() if k == c) for c in CLASSES}
    profile = {
        "generated": datetime.date.today().isoformat(),
        "source": "user turns under 700 characters in ~/.claude/projects/**/*.jsonl",
        "messages": len(typed),
        "words": total_words,
        "counts": counts,
        "casing": casing(typed, jargon_words()),
        "typos": {
            "found": len(found),
            "words_per_typo": round(total_words / len(found)) if found else None,
            "classes": {c: len(by_class[c]) for c in CLASSES},
            "examples": {c: by_class[c][:8] for c in CLASSES},
            "note": "automatic, one edit from a dictionary word, seen at most twice; "
                    "cannot detect wrong-word errors",
        },
    }
    with open(PROFILE, "w", encoding="utf-8") as fh:
        json.dump(profile, fh, indent=2)
        fh.write("\n")
    print(f"\nwrote {PROFILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
