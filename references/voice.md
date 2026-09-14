# Where these rules came from

Derived 2026-09-04 from Miguel's own text. Two corpora, deliberately kept separate,
because they are two different registers.

**Corpus A - what he types.** 101 user messages extracted from
`~/.claude/projects/**/*.jsonl`, filtered to the 90 under 700 characters. The 11 long
ones were assistant-authored prompts and compaction summaries, and were discarded.
Rebuild with `tools/extract_voice_corpus.py`.

**Corpus B - what he ships.** `boulder-dice-insert/README.md` and `LISTING.md`, plus
`git log` across `boulder-dice-insert` and three repos that are not public. This is text an assistant drafted and he then corrected, cut and approved,
so it shows his editorial judgment rather than his keystrokes.

Rules that hold in **both** corpora are load-bearing. Rules that appear only in B are
suspect, and a few of them turned out to be drift he never asked for.

## Measured counts, Corpus A (90 messages)

| Feature | Count |
|---|---|
| Em dash | **0** |
| Spaced hyphen ` - ` | 21 |
| Emoji | **0** |
| "lets" | 35 |
| "let's" | **0** |
| "can we ..." | 12 |
| Question marks | 14 |
| Exclamation marks | 2 |
| British spellings | 0 |
| Messages starting uppercase | 2 / 90 |
| Messages ending with a period | 2 / 90 |

## The drift finding

Corpus A has **zero** em dashes. `boulder-dice-insert/README.md` has **54**. He never
typed one and never asked for one. Same story with "licence" and "millimetre", which are
British forms absent from everything he has typed.

This is the core reason the skill exists: his public repos have gradually acquired a
house style he did not choose. Stripping em dashes and restoring American spelling is
the single highest-signal edit available on any file of his.

Emoji are the one clean case: zero in A, zero in B. Nothing to fix, just do not start.

## Rules confirmed in both corpora

**Concrete over qualitative.** In A he corrects with numbers and physical comparisons:
"scallops are wayyyy to sharp they should be like an eigth of an arc", "can we try
making it wider by 1mm". In B this shows up as bolded figures with units throughout.

**Research over guessing.** A is full of "please research", "lets research if there are
existing similar things", "research how / if we should install the beacon". He does not
want a confident answer built on nothing, and his published copy inherits that: it tells
readers which numbers are reported rather than verified.

**Iterative, reversible framing.** "can we try" (12 uses), "lets try adding a little bit
more depth", and clean reversals: "honestly, lest revert it . i just tested the draft
and i dont like it." Public text should carry the same posture - versioned, willing to
say v1 was wrong, not pretending the current state is final.

**Emphatic caps for intensity.** A: "detends need to be a LITTLE more aggressive".
B: "taken from the SLEEVE rather than the box". One word, rarely, and it survives into
published text.

**Honesty about what has not been done.** The strongest signature in B, and it traces
straight back to A's insistence on testing things physically. LISTING.md carries a
standing note explaining that it does *not* claim the insert was tested across a range
of boxes, because it was not. README states "Neither has been printed at these
dimensions." He also names his own past errors: of the old game-themed variants, "it was
always slightly a lie".

## Typo inventory

Extracted by checking every word in Corpus A against `/usr/share/dict/words`, then
discarding proper nouns, URLs, project jargon and dictionary gaps by hand.

**25 real typos in 1,226 hand-typed words, a natural rate of 1 per 49.**

| Class | Count | Examples |
|---|---|---|
| Transposition, adjacent letters swapped | ~12 | `wokr` `htis` `jsut` `nto` `tkaing` `pgorgress` `obisdian` `coupoin` `withg` `ebst` `acutally` |
| Dropped letter | 3 | `histoy` `conver` `eigth` |
| Doubled or extra letter | ~8 | `agressive` `incoludes` `useage` `easyer` `mimicing` `automatally` `detends` |
| **Wrong-word / homophone** | **0** | none |

The zero in the last row is the load-bearing finding. Across 1,226 words he never once
wrote their for there, its for it's, or form for from. Every slip he makes is a motor
error that produces a non-word. That is why the skill permits typos at all: a non-word is
autocorrected by the eye at no cost, while a wrong word silently changes the sentence and
forces a re-read.

He does drop apostrophes (`dont`, `its`, `youre`), but that is chat shorthand rather than
a typo, and it is stripped from published text along with the lowercase openings.

**Published rate is deliberately not his natural rate.** 1 per 49 would put ~40 slips in
a 2,000-word README, which reads as a broken document. The skill uses 1 per 200-400, about
six times sparser, chosen by him on 2026-09-04.

## Decisions he made from A/B samples (2026-09-04)

Both chosen after seeing the options rendered on real paragraphs of his own README.

**Em dashes become a spaced hyphen ` - `.** Over splitting into two sentences, and over
comma/semicolon. His reasoning matched the sample text: it keeps an aside feeling like an
aside. The semicolon option was explicitly the weakest, since he has never typed one.

**All three slip classes, mixed** - not transposition only. So `slipplan.py` draws a
class per site weighted to his real distribution (swap 0.52, double 0.35, drop 0.13)
rather than listing every transposition first. Before this was fixed the tool always
showed swaps at the top of every site, which would have quietly produced
transposition-only documents.

## Chat-only, do not publish

Lowercase openings, absent terminal periods, "lets", and fast typos ("wokr",
"cirriculum", "acutally", "htis"). These are keyboard speed, not style. He fixes them
when text goes public, and so should you.

The `*` correction convention ("* text histoy", "*back to the non-reversible version")
is chat-only too, but it is worth reading as intent: he corrects tersely and expects the
correction applied without discussion.

## A note on this file

The reference files under `references/` are internal documentation, not public copy, so
the linter's findings on them are expected where they quote drift as evidence.
