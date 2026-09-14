# Where these rules came from

Derived 2026-09-04 from Miguel's own text. Two corpora, deliberately kept separate,
because they are two different registers.

**Corpus A - what he types.** 111 user messages extracted from
`~/.claude/projects/**/*.jsonl`, filtered to the 103 under 700 characters. The 8 long
ones were assistant-authored prompts and compaction summaries, and were discarded.
Rebuild with `tools/extract_voice_corpus.py`, which also writes `profile.json`, the
counts the tools quote, and prints the drift against the previous profile.

**Corpus B - what he ships.** `boulder-dice-insert/README.md` and `LISTING.md`, plus
`git log` across `boulder-dice-insert` and three repos that are not public. This is text an assistant drafted and he then corrected, cut and approved,
so it shows his editorial judgment rather than his keystrokes.

Rules that hold in **both** corpora are load-bearing. Rules that appear only in B are
suspect, and a few of them turned out to be drift he never asked for.

## Measured counts, Corpus A (103 messages, 1,398 words)

| Feature | 2026-09-04 (90 msgs) | 2026-09-14 (103 msgs) |
|---|---|---|
| Em dash | **0** | **0** |
| Spaced hyphen ` - ` | 21 | 25 |
| Emoji | **0** | **0** |
| "lets" | 35 | 39 |
| "let's" | **0** | **0** |
| "can we ..." | 12 | 14 |
| Question marks | 14 | 16 |
| Exclamation marks | 2 | 2 |
| British spellings | 0 | 0 |
| Messages starting uppercase | 2 / 90 | 2 / 103 |
| Messages ending with a period | 2 / 90 | 2 / 103 |

Ten days and 13 messages later every zero held and no ratio moved by more than a
point. The scraper prints this drift itself on each run, so the check is free.

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

**By hand, 2026-09-04.** Every word in Corpus A checked against `/usr/share/dict/words`,
then proper nouns, URLs, project jargon and dictionary gaps discarded by reading.

**25 real typos in 1,226 hand-typed words, a natural rate of 1 per 49.**

| Class | Count | Examples |
|---|---|---|
| Transposition, adjacent letters swapped | ~12 | `wokr` `htis` `jsut` `nto` `tkaing` `pgorgress` `obisdian` `coupoin` `withg` `ebst` `acutally` |
| Dropped letter | 3 | `histoy` `conver` `eigth` |
| Doubled or extra letter | ~8 | `agressive` `incoludes` `useage` `easyer` `mimicing` `automatally` `detends` |
| **Wrong-word / homophone** | **0** | none |

**Automatically, 2026-09-14.** The scraper now does the inventory itself. A word counts
as a typo if it is not in the dictionary or `jargon.txt`, is not a dropped-apostrophe
contraction, appears at most twice, and is one adjacent swap, one extra letter or one
missing letter away from a real word. On 1,398 words it finds **19 typos, 1 per 74**:
9 swaps, 7 extra letters, 3 dropped. It finds fewer than the hand pass because a
substitution (`easyer`, `detends`) or a two-edit slip (`pgorgress`, `cirriculum`) is
invisible to it, and it cannot judge a wrong-word error at all. The class ratio it
measures, 47/37/16, is within a few points of the hand-derived 52/35/13. The profile
is what `slipplan.py` actually draws from, with add-one smoothing so a class measured
at zero still turns up occasionally.

The zero in the last row is the load-bearing finding. Across 1,226 words he never once
wrote their for there, its for it's, or form for from. Every slip he makes is a motor
error that produces a non-word. That is why the skill permits typos at all: a non-word is
autocorrected by the eye at no cost, while a wrong word silently changes the sentence and
forces a re-read.

He drops apostrophes (`dont`, `its`, `youre`): 48 bare contractions against 2
apostrophes in the corpus. Not a typo, and since the A/B round of 2026-09-14 it is kept
in published text.

**Published rate is deliberately not his natural rate.** 1 per 49 would put ~40 slips in
a 2,000-word README, which reads as a broken document. The skill uses 1 per 200-400, about
six times sparser, chosen by him on 2026-09-04.

## Decisions he made from A/B samples (2026-09-04)

Both chosen after seeing the options rendered on real paragraphs of his own README.

**Em dashes become a spaced hyphen ` - `.** Over splitting into two sentences, and over
comma/semicolon. His reasoning matched the sample text: it keeps an aside feeling like an
aside. The semicolon option was explicitly the weakest, since he has never typed one.

**All three slip classes, mixed** - not transposition only. So `slipplan.py` draws a
class per site weighted to the measured distribution in `profile.json` (9/7/3 as of
2026-09-14, smoothed to about 45/36/18, with the hand count 0.52/0.35/0.13 as the
fallback when no profile exists) rather than listing every transposition first. Before this was fixed the tool always
showed swaps at the top of every site, which would have quietly produced
transposition-only documents.

## A/B round 1 (2026-09-14)

Four questions, three variants each, built from real sentences in the dice-insert README
and listing. Option A was always the current rule. He picked:

| Question | Pick | What backs it |
|---|---|---|
| Contractions | **C**, as typed with no apostrophe: youre, isnt, dont | 48 bare contractions, 2 apostrophes (both "it's") |
| Asides | **A**, spaced hyphen, unchanged | 25 uses, still reads right in lowercase |
| Register | **C**, terse, fragments allowed, over plain declaratives (A) and chat softeners (B) | median sentence 11.5 words, mean 13.2, 90th pct 25, max 40; 21 of 106 are 5 words or fewer |
| Numbers | **B**, plain with spaced units, over bold (A) and "67x91x18.6mm" (C) | 0 bold markers in 1,398 typed words |

Rejected on purpose: natural contractions with apostrophes, parentheses and sentence
splits for asides, the chat register ("honestly", "basically"), and the chat number form
with no space before the unit.

What changed because of it: `voicecheck.py` gained apostrophe, uncontracted, boldnum and
longsentence checks; `slipplan.py` refuses a contraction or a non-dictionary word as a
slip site; the scraper counts apostrophes and bare contractions into `profile.json`;
`examples/coin-well.md` now shows the picked variants.

## A/B round 2 (2026-09-14)

Four more questions on the same footing. Every pick was the current rule, which turns
four judgment calls into his choices:

| Question | Pick | Rejected |
|---|---|---|
| Emphasis | **A**, caps on one word ("the SLEEVE") | bold; no emphasis, rephrase instead |
| Structure for variants and specs | **C**, a table | prose; bullets |
| Slip density | **A**, 1 per 200-400 | 1 per 100-200; his natural 1 per 50 |
| Section openers | **A**, the thing itself, spec first | the test first; the reader's situation first |

Nothing in the tools changed. SKILL.md marks those four rules as A/B-confirmed.

## Chat-only, do not publish

Absent terminal periods (101 of 103). That is keyboard speed, and full stops come back
when text goes public. The chat softeners ("honestly", "basically", "just") stay in chat
too, by the A/B round below.

Everything else that looks like keyboard speed carries over, by his explicit decision:
lowercase (2026-09-04, "no caps normally", extended to names and acronyms 2026-09-14),
typos (1 per 200-400 words, SKILL.md), and contractions with no apostrophe, "lets"
included (A/B round 1, 2026-09-14).

The `*` correction convention ("* text histoy", "*back to the non-reversible version")
is chat-only too, but it is worth reading as intent: he corrects tersely and expects the
correction applied without discussion.

## Lexicon and casing (measured 2026-09-14)

Vocabulary, his short form against the formal one an assistant draft reaches for:

| Short | Count | Formal | Count |
|---|---|---|---|
| make | 20 | create | 0 |
| ok / okay | 7 | acceptable | 0 |
| please | 6 | kindly | 0 |
| print / prints / printed | 5 | 3d print / 3d-printed | 2 |
| ai | 4 | language model, LLM | 0 |
| stuff | 3 | materials | 1 |
| thing / things | 3 | components, items | 0 |
| use | 3 | utilize | 0 |
| repo | 1 | repository | 0 |
| readme | 1 | README file | 0 |

Casing of names and acronyms, exact forms as typed:

| Word | Forms |
|---|---|
| pokemon | pokemon 5, no accent |
| ai | ai 4 |
| github | github 3 |
| makerworld | makerworld 3 |
| printables | printables 2 |
| 3d | 3d 2 |
| openscad | openscad 1 |
| stl | stl 1 |
| mtg | mtg 1 |
| claude | claude 1 |
| scad | SCAD 1 |
| json | JSON 1 |

**20 of 22 lowercase** on product names and acronyms, **24 of 28** across every word in
`jargon.txt` (the profile's figure, which the linter quotes). The SKILL.md rule that kept
caps on proper nouns and formats was
a judgment call from 2026-09-04, made for searchability, and it was wrong on both
counts: he does not type them that way and search does not care. Reversed 2026-09-14.
The scraper now records this per word in `profile.json` under `casing`, for every word
in `jargon.txt`, so the rule can be rechecked as the corpus grows.

Textspeak is nearly absent: "rn" 1, "ok" 7, and nothing from the rest of the usual set
(tbh, imo, idk, lol, btw, kinda, gonna). Plain lowercase words is the register, not
abbreviation.

## A note on this file

The reference files under `references/` are internal documentation, not public copy, so
the linter's findings on them are expected where they quote drift as evidence.
