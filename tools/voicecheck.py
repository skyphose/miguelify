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

Exit: 0 clean, 1 voice findings, 2 leak or a committed private.md.
"""
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
     "em/en dash: he types a spaced hyphen ' - '. Zero em dashes in 90 typed messages."),
    ("emoji",    "high", r"[\U0001F300-\U0001FAFF\U00002600-\U000027BF️]",
     "emoji: zero in everything he has written or shipped."),
    ("claude",   "high", r"Co-Authored-By:\s*Claude|Claude-Session:|Generated with \[?Claude",
     "Claude attribution: never on his public repos. Standing preference."),
    ("british",  "med",  r"\b(licence|colour|favour|centre|metre|millimetre|organis\w+|analyse)\b",
     "British spelling: he writes American forms."),
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
     "Title Case heading: he uses sentence case."),
    ("arrow",    "low",  r"→",
     "Unicode arrow: his commits and docs use ASCII '->'."),
    ("bang",     "low",  r"!(?!\[|=|\]|\))",
     "exclamation mark: 2 in 90 messages. Almost always cut."),
    ("labelbul", "low",  r"^\s*[-*] \*\*[A-Z][^*]{1,30}:\*\*",
     "bolded-label bullet: fine occasionally, not as the house format."),
]

# Lines where a tell is being quoted as evidence rather than used.
EXEMPT = re.compile(r"^\s*(>|\|)|zero (em dash|in )|never typed")

SELF_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRIVATE = os.path.join(SELF_DIR, "references", "private.md")

# A GitHub noreply address is the public login by construction, never a leak.
NOREPLY = re.compile(r"\S+@users\.noreply\.github\.com")


def scan(lines):
    """Return {check_id: (severity, message, [line numbers], total hits)}."""
    found = {}
    in_fence = False
    for n, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or EXEMPT.search(line):
            continue
        for cid, sev, pat, msg in CHECKS:
            hits = re.findall(pat, line)
            if hits:
                rec = found.setdefault(cid, [sev, msg, [], 0])
                rec[2].append(n)
                rec[3] += len(hits)
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
    terms = leak_terms()
    leaked = 0
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

        # The rulebook quotes the tells it bans, so it exempts itself. README.md is
        # ordinary public copy that happens to live here, so it does not.
        ap = os.path.abspath(path)
        rel = os.path.relpath(ap, SELF_DIR)
        if ap.startswith(SELF_DIR) and not rel.startswith("..") \
                and os.path.basename(ap) != "README.md":
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
            print(f"  {sev:<4} {cid:<9} {count:>3}x  {msg}")
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
            print(f"--git: {len(commits)} commit(s) checked, {bad} with a private string")

    print(f"\n{grand} hit(s) across {len(paths)} file(s).")
    if leaked:
        print(f"{leaked} private-string leak(s). Fix these before anything is pushed.")
        return 2
    if grand:
        print("Mechanical tells only. Still check by hand: unearned claims, a missing")
        print("trade-off paragraph, a restating conclusion, numbers without units.")
    return 1 if grand else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
