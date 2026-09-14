#!/usr/bin/env python3
"""Rebuild the voice corpus from Miguel's own typed messages.

Usage:  extract_voice_corpus.py [OUT]      (default: ./voice_corpus.txt)

Pulls user-authored messages out of ~/.claude/projects/**/*.jsonl and drops the
things that are not his typing: tool results, hook and system-reminder noise,
compaction summaries, and the long assistant-written prompts that get replayed
as user turns. Then prints the style counts the skill's rules are built on.

Rerun this after a few months of new sessions to check the rules still hold.
"""
import glob
import json
import os
import re
import sys

HOME = os.path.expanduser("~")
DROP_PREFIX = ("Caveat:", "[Request interrupted", "<", "This session is being continued")
DROP_SUBSTR = ("tool_use_id", "Analysis:\nLet me chronologically")
SHORT = 700  # above this, it is a pasted prompt or a summary, not typing


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


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "voice_corpus.txt"
    rows = collect()
    typed = [t for _, t in rows if len(t) < SHORT]
    with open(out, "w") as fh:
        for ts, text in rows:
            if len(text) < SHORT:
                fh.write(f"=== {ts[:19]}\n{text}\n")
    print(f"wrote {out} ({len(typed)} of {len(rows)} messages kept)")
    report(typed)


if __name__ == "__main__":
    main()
