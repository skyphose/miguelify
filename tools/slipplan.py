#!/usr/bin/env python3
"""Plan where deliberate typos go in a public-facing document.

Usage:  slipplan.py FILE [--seed N] [--min 200] [--max 400]

Picks positions at random, one slip every 200-400 words, and proposes candidate
slips built from the three classes measured in the corpus: an adjacent letter swap,
a dropped letter, a doubled letter. The class is drawn per site with the weights in
../references/profile.json, so the mix tracks how the corpus author really mistypes.

It refuses any candidate that is itself a real English word. That is the rule the
whole thing rests on -- a slip landing on a valid word gets accepted by the eye and
silently changes the sentence, while a non-word is autocorrected at no cost. Doing
this by hand produces predictable placements and suspiciously cute typos, which is
why the randomness lives here instead.

Suggestions only. Nothing is written. Pick one per site and edit by hand, and reject
any that collides with a load-bearing technical term. See ../SKILL.md.
"""
import argparse
import json
import os
import random
import re
import sys

DICT = "/usr/share/dict/words"
PROFILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "references", "profile.json")
MIN_LEN = 5          # shorter words swap into real words too easily
PREFER_LEN = 7       # transposition is most transparent from here up
SKIP_LINE = re.compile(r"^\s*(#{1,6}\s|\||>\s*\*\*|\s*[-*]\s*$)")
INLINE_CODE = re.compile(r"`[^`]*`")
URLISH = re.compile(r"https?://|\w+\.(com|org|net|io|md|py|scad|stl)\b|/\w+/")
WORD = re.compile(r"[A-Za-z]+")


JARGON = os.path.join(os.path.dirname(PROFILE), "jargon.txt")


def load_dict():
    """The system word list plus ../references/jargon.txt, one word per line.

    The word list is old and has no "email", "json" or "repo", so without the jargon
    file those read as typos to the scraper and as safe slip targets to this tool.
    """
    try:
        with open(DICT, errors="ignore") as fh:
            words = {w.strip().lower() for w in fh if w.strip()}
    except OSError:
        print(f"warning: {DICT} not found, real-word filter disabled", file=sys.stderr)
        return set()
    try:
        with open(JARGON, encoding="utf-8") as fh:
            for line in fh:
                line = line.split("#", 1)[0].strip().lower()
                if line:
                    words.add(line)
    except OSError:
        pass
    return words


def prose_tokens(lines):
    """Every prose word in reading order, flagged for whether it may carry a slip.

    The spacing interval counts ALL prose words, since that is what the reader reads,
    but a slip may only land on an eligible one. Counting only eligible words made the rate
    silently ~3x too sparse on documents dense with numbers and specs.
    """
    out = []
    in_fence = False
    for n, raw in enumerate(lines, 1):
        if raw.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        protected = bool(SKIP_LINE.match(raw) or URLISH.search(raw))
        line = INLINE_CODE.sub(" ", raw)          # drop inline code spans
        if any(ch.isdigit() for ch in line):
            line = re.sub(r"\S*\d\S*", " ", line)  # drop specs, dimensions, versions
        for m in WORD.finditer(line):
            w = m.group()
            ok = (not protected and len(w) >= MIN_LEN
                  and "_" not in w and w == w.lower())
            out.append((n, w, line.strip(), ok))
    return out


# /usr/share/dict/words is missing most inflected forms, so "scared" is absent even
# though "scare" is there. Checking a few suffixes catches those. Over-rejecting is
# free (another candidate gets picked); under-rejecting is the failure we care about.
SUFFIXES = ("s", "d", "ed", "ing", "er", "est", "ly", "es", "ies")


def is_real(cand, real_words):
    c = cand.lower()
    if c in real_words:
        return True
    for suf in SUFFIXES:
        if not c.endswith(suf):
            continue
        stem = c[: -len(suf)]
        if len(stem) < 3:
            continue
        if stem in real_words or stem + "e" in real_words:
            return True
        if suf == "ies" and stem + "y" in real_words:       # categories -> category
            return True
        if len(stem) >= 4 and stem[-1] == stem[-2] and stem[:-1] in real_words:
            return True                                     # flipped -> flip
    return False


# Drawing the class per site (rather than listing every swap first, which is what an
# unweighted flat list does) is what keeps output from collapsing to swaps only. The
# weights come from the profile the scraper writes, smoothed so a class measured at
# zero still gets an occasional draw. The fallback is the 2026-09-04 hand count.
CLASSES = ("swap", "double", "drop")
FALLBACK_WEIGHTS = (0.52, 0.35, 0.13)


def class_weights():
    try:
        with open(PROFILE, encoding="utf-8") as fh:
            cl = json.load(fh)["typos"]["classes"]
        counts = [cl.get(c, 0) for c in CLASSES]
        total = sum(counts)
        if total:
            return tuple((n + 1) / (total + len(CLASSES)) for n in counts)
    except (OSError, ValueError, KeyError, TypeError):
        pass
    return FALLBACK_WEIGHTS


CLASS_WEIGHTS = class_weights()


def candidates(word, real_words):
    """Slips built the three measured ways, bucketed by class.

    Returns ({class: [candidates]}, rejected_count). Real words are dropped here so
    the readability rule cannot be skipped downstream.
    """
    buckets = {c: [] for c in CLASSES}
    seen, rejected = set(), 0

    def add(cand, how):
        nonlocal rejected
        if cand == word or cand in seen:
            return
        seen.add(cand)
        if real_words and is_real(cand, real_words):
            rejected += 1
            return
        buckets[how].append(cand)

    for i in range(1, len(word) - 1):             # keep first and last letter stable
        add(word[:i] + word[i + 1] + word[i] + word[i + 2:], "swap")
    for i in range(1, len(word) - 1):
        add(word[:i] + word[i + 1:], "drop")
    for i in range(1, len(word) - 1):
        add(word[:i] + word[i] + word[i:], "double")
    return buckets, rejected


def pick_class(buckets, rng):
    """Draw a class by the measured distribution, falling back if that class is empty."""
    available = [c for c in CLASSES if buckets[c]]
    if not available:
        return None
    weights = [CLASS_WEIGHTS[CLASSES.index(c)] for c in available]
    return rng.choices(available, weights=weights, k=1)[0]


def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("file")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--min", type=int, default=200)
    ap.add_argument("--max", type=int, default=400)
    args = ap.parse_args()

    rng = random.Random(args.seed)
    with open(args.file, encoding="utf-8", errors="replace") as fh:
        lines = fh.read().splitlines()

    real_words = load_dict()
    toks = prose_tokens(lines)
    n_eligible = sum(1 for t in toks if t[3])
    if not n_eligible:
        print("no eligible prose found")
        return 0

    plan, rejected_total, used_words, used_lines = [], 0, set(), set()
    cursor = rng.randint(args.min, args.max)
    while cursor < len(toks):
        # walk forward from the target for a word that works, preferring long ones
        window = [t for t in toks[cursor:cursor + 120] if t[3]]
        window.sort(key=lambda t: (t[1] in used_words, t[0] in used_lines,
                                   -(len(t[1]) >= PREFER_LEN), -len(t[1])))
        for line_no, word, sentence, _ in window:
            if word in used_words or line_no in used_lines:
                continue
            buckets, rej = candidates(word, real_words)
            rejected_total += rej
            chosen = pick_class(buckets, rng)
            if chosen:
                # preferred class first, then one fallback from each other class for
                # when the top pick collides with a load-bearing technical term
                offers = [(c, chosen) for c in buckets[chosen][:2]]
                offers += [(buckets[c][0], c) for c in CLASSES
                           if c != chosen and buckets[c]]
                plan.append((cursor, line_no, word, sentence, offers, chosen))
                used_words.add(word)
                used_lines.add(line_no)
                break
        cursor += rng.randint(args.min, args.max)

    print(f"\n{args.file}")
    print(f"{len(toks)} prose words ({n_eligible} eligible), "
          f"{len(plan)} slip(s) planned "
          f"at 1 per {args.min}-{args.max}"
          + (f", seed {args.seed}" if args.seed is not None else ""))

    prev, mix = 0, {c: 0 for c in CLASSES}
    for offset, line_no, word, sentence, offers, chosen in plan:
        gap = offset - prev
        prev = offset
        mix[chosen] += 1
        ctx = sentence if len(sentence) <= 88 else sentence[:85] + "..."
        print(f"\n  word {offset:>5}  (+{gap})  line {line_no}   class: {chosen}")
        print(f"    {word}  ->  " + "   ".join(f"{c} [{h}]" for c, h in offers[:4]))
        print(f"    context: {ctx}")

    if plan:
        shown = ", ".join(f"{c} {mix[c]}" for c in CLASSES)
        target = "/".join(str(round(w * 100)) for w in CLASS_WEIGHTS)
        print(f"\nclass mix: {shown}   (target roughly {target})")
    print(f"{rejected_total} candidate(s) rejected for being real words.")
    print("Suggestions only, nothing written. Pick one per site, reject any that")
    print("collides with a technical term, then edit by hand.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main())
