#!/usr/bin/env python3
"""Rebuild the voice corpus from Miguel's own typed messages.

Usage:  extract_voice_corpus.py [OUT] [--force]
        default OUT: ../references/voice_corpus.txt, which .gitignore excludes

Pulls user-authored messages out of ~/.claude/projects/**/*.jsonl and drops the
things that are not his typing: tool results, hook and system-reminder noise,
compaction summaries, and the long assistant-written prompts that get replayed
as user turns. Then prints the style counts the skill's rules are built on.

The corpus is raw chat, so two things guard it. Emails, home paths, token-shaped
strings and every term in ../references/private.md are redacted before anything is
written. And the tool refuses to write into a git working tree unless the target
path is gitignored there, because a transcript dump landing in a project directory
is exactly how it would end up committed. --force overrides that one check.

Rerun this after a few months of new sessions to check the rules still hold.
"""
import glob
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from voicecheck import leak_terms  # noqa: E402

HOME = os.path.expanduser("~")
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_OUT = os.path.join(SKILL_DIR, "references", "voice_corpus.txt")
DROP_PREFIX = ("Caveat:", "[Request interrupted", "<", "This session is being continued")
DROP_SUBSTR = ("tool_use_id", "Analysis:\nLet me chronologically")
SHORT = 700  # above this, it is a pasted prompt or a summary, not typing

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
HOMEPATH = re.compile(r"/(?:Users|home)/[^/\s]+")
TOKEN = re.compile(r"\b(?:sk|pk)-[A-Za-z0-9_-]{16,}|\bgh[pousr]_[A-Za-z0-9]{16,}|"
                   r"\bAKIA[A-Z0-9]{16}\b|\bxox[baprs]-[A-Za-z0-9-]+|"
                   r"\beyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{10,}")


def redact(text, terms):
    text = EMAIL.sub("[email]", text)
    text = HOMEPATH.sub("~", text)
    text = TOKEN.sub("[token]", text)
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


def report(typed):
    blob = "\n".join(typed)
    def n(pat):
        return len(re.findall(pat, blob))
    stats = [
        ("em dash", n(r"[—–]")),
        ("spaced hyphen ' - '", n(r" - ")),
        ("emoji", n(r"[\U0001F300-\U0001FAFF]")),
        ("'lets'", n(r"\blets\b")),
        ("'let's'", n(r"\blet's\b")),
        ("'can we'", n(r"\bcan we\b")),
        ("question marks", n(r"\?")),
        ("exclamation marks", n(r"!")),
        ("British spellings", n(r"\b(licence|colour|favour|centre|metre)\b")),
    ]
    width = max(len(k) for k, _ in stats)
    print(f"\n{len(typed)} hand-typed messages (under {SHORT} chars)\n")
    for key, val in stats:
        print(f"  {key:<{width}}  {val}")
    upper = sum(1 for m in typed if m[:1].isupper())
    period = sum(1 for m in typed if m.rstrip().endswith("."))
    print(f"  {'starts uppercase':<{width}}  {upper}/{len(typed)}")
    print(f"  {'ends with a period':<{width}}  {period}/{len(typed)}")
    print("\nBaseline measured 2026-09-04 over 90 messages: 0 em dashes, 0 emoji,")
    print("0 British spellings, 35 'lets', 0 \"let's\". If those have drifted, the")
    print("rules in ../references/voice.md need rereading.")


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
    with open(out, "w") as fh:
        for ts, text in rows:
            if len(text) < SHORT:
                fh.write(f"=== {ts[:19]}\n{text}\n")
    print(f"wrote {out} ({len(typed)} of {len(rows)} messages kept, redacted)")
    report(typed)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
