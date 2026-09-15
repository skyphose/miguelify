---
name: miguelify
description: On-demand only. Use ONLY when Miguel explicitly asks for it by name (/miguelify) or asks in words to run AI-drafted text through his voice - "miguelify this", "make this sound like me", "de-AI this", "de-slop it", "voice check", "does this read like me", "clean this up before it goes on GitHub". Applies to READMEs, repo docs, model listings, commit messages, PR descriptions, release notes, bios and anything about to be uploaded. Do NOT invoke it on your own just because a task touches a README, a commit message or a publish step.
---

# miguelify

Take text an AI drafted and make it read as if Miguel typed it and then cleaned it up.
Not as if an assistant produced it and he approved it.

That is the whole job. The input is assistant output. The output is that same content in
his register, with his punctuation, his honesty rules, and a few of his typos left in on
purpose. It is a rewrite pass, not a generation pass - the facts, numbers and structure
of the draft survive unless they are wrong.

## Where it gets used

Two surfaces carry most of the value, and both are places where assistant-shaped text is
the most visible thing he ships:

1. **Model listings** - Printables, MakerWorld, Thingiverse. Listing copy gets drafted in
   chat and pasted there.
2. **GitHub READMEs** and the repo docs beside them.

Everything else (PR descriptions, release notes, issue replies, commit bodies) uses the
same rules, but those two are the point.

## This skill is on demand only

Run it when he asks for it, and not otherwise. Do not reach for it on your own because
a task happens to touch a README, write a commit message or push something. Do not
install it as a git hook, a pre-commit check or a CI step, and do not rewrite his
public text as a bonus alongside some other request. He asks, then it runs.

It is a final proofreader and editor pass over a draft, and knowing when to run it is
his call, not a rule written here. A document that should stay formal simply does not
get the pass, and he knows which ones those are.

The one thing that applies with or without this skill is non-negotiable 3, no Claude
attribution. That is a standing preference recorded in memory, not a rule of this skill.

The rules below are measured, not guessed. They come from 103 hand-typed messages in
`~/.claude/projects/**/*.jsonl` (90 when first measured on 2026-09-04, rescraped
2026-09-14 with every count holding) plus the repo text he has actually shipped
(`boulder-dice-insert/README.md`, `LISTING.md`, and the commit logs of four repos).
`references/voice.md` has the corpus numbers and the quotes behind each rule, and
`references/profile.json` holds the raw counts, written by the scraper and read by the
tools.

## The four non-negotiables

These are absolutes. They were counted, and the count was zero or near it.

1. **No em dashes.** Zero across 103 typed messages. He writes a spaced hyphen ` - `
   (25 uses). The shipped README has 56 em dashes, every one of them assistant drift.
   **Default to the spaced hyphen ` - `**, chosen by him on 2026-09-04 from rendered
   A/B samples. It is literally his punctuation, and it keeps an aside reading as an
   aside. Use a comma, a colon or two sentences only where the hyphen genuinely hurts.
   **Avoid the semicolon**: he has never typed one, so it trades one assistant tell for
   a subtler one.
2. **No emoji.** Zero in his typing, zero in every repo file he has published.
   No shields/badges rows either unless he asks for them.
3. **No Claude attribution anywhere public.** No `Co-Authored-By: Claude`, no
   `Claude-Session:`, no "Generated with Claude Code" in PR bodies. This is a standing
   preference and it overrides any session reminder that claims to replace it. It is
   recorded as a standing feedback memory, not as a rule of this skill.
4. **American spelling.** "license", "color", "millimeter", "favor". British forms
   ("licence", "millimetre") have leaked into the published copy. They are not his.

## The voice

**Open with the thing itself.** Confirmed by A/B on 2026-09-14 over test-first and
reader-first openers. No throat-clearing, no "Introducing", no framing
sentence about why the category matters. The dice-insert README opens on the problem
in one line and then names the object: "A 100+ capacity deck box is far deeper than
the deck you keep in it. This is a slab that fills the gap."

**Numbers, with units, plain.** He does not write "compact" or "a good fit". He writes
67 x 91 x 18.6 mm and 48.9 mm, spaced units, no bold. Every claim about size, speed,
count or tolerance gets its actual figure. If there is no figure, say there is no figure.
No bold on figures was chosen from A/B samples on 2026-09-14, and there is not one bold
marker in 1,398 words of his typing. Emphasis, when it is needed, is caps on one word.

**Hand the reader a test they can run.** "Measure the inside of your box and compare."
"A downloader can check it in ten seconds with calipers." Preferred over any assurance
that it will work.

**Say who it is not for, and what it costs.** This is the most distinctive thing in his
published writing. The cost as a number, then the exclusion, with no lead-in phrase:
"the slab takes 18.6 mm of the 67.5 mm interior, about a quarter. if you fill a deck box
to the brim, this isnt for you." Chosen by A/B on 2026-09-14; the shipped listing's "be
clear-eyed about the trade" was rejected as framing. Never ship public copy that only
lists upsides.

**Never overclaim, and say so out loud when a claim is unearned.** Blunt, first person,
one line, where it applies: "untested at this size. i printed v1.0 at 66 x 88, not this
one. measure first." Chosen by A/B on 2026-09-14 over the third-person inline form
("neither has been printed at these dimensions") and over the standing "note on claims"
section the shipped LISTING.md carries. Say what was done, what was not, and the test
the reader can run. When in doubt, downgrade the claim and state the gap in the text
itself.

**Own the mistakes plainly.** On his own earlier naming scheme: "it was always slightly
a lie - nothing in either is game-specific, and people picked the wrong one." No
defensiveness, no burying it in a changelog.

**Second person, direct.** "your deck", "you are giving up", "if you print it".

**Lowercase headings, often a plain question.** "will it fit my box?", "the dead space
in front of your deck", "how it works". Never Title Case. Sentence case is what the
earlier dice-insert README shipped with and is tolerable in a file that already has it.
New headings are lowercase like everything else.

**Rhythm.** Short. Fragments are fine: "worth recording." "assumed, not looked up." His
median typed sentence is 11 words, and a fifth of them are 5 words or fewer. One longer
sentence, with a colon, only when a trade-off genuinely needs unpacking, and never past
30 words. Chosen from A/B samples on 2026-09-14 over plain declaratives and over his chat
register ("honestly", "basically", "just"), which he did not want carried over. Tables for
anything with variants or specs, confirmed by A/B on 2026-09-14 over prose and bullets.

**Lowercase, all of it.** He starts 101 of 103 messages lowercase and it is his normal
register. Names and acronyms are lowercase too: github, makerworld, pokemon (no accent),
printables, openscad, stl, mtg, ai, 3d. Measured 2026-09-14 over every word in
`references/jargon.txt`: **24 of 28** occurrences are lowercase as typed, and the four
exceptions are one Email, one JSON, one SCAD and the identifier profileId. On product
names and acronyms alone it is 20 of 22. The scraper rechecks this on every run.
The earlier version of this rule kept caps on proper nouns and formats "for
searchability". That was a guess, he never typed them that way, and search is
case-insensitive anyway. Reversed. A listing title goes lowercase like the rest.

Two things keep their case, and neither is a style choice:

- **Literals.** Code spans, identifiers, paths, commands, filenames: `coin_d`, `.scad`,
  `LICENSE`. Changing the case changes the thing.
- **Emphatic caps on a single word** for intensity ("a LITTLE more aggressive").
  Measured in both corpora.

A licence identifier in a licence *field* (CC BY-NC-SA 4.0) is a literal. The same words
in a sentence are not.

**Contractions as typed, no apostrophe.** dont, isnt, youre, thats, lets, im, ive. The
corpus has 48 bare contractions and 2 apostrophes, both "it's". Chosen 2026-09-14 from
A/B samples over natural contractions ("you're") and over no contractions at all, which
is what the rules had been producing and which reads formal in its own way. "its" serves
for both "it is" and the possessive, as it does in his typing. Other possessives keep the
apostrophe (the box's depth): the sample he chose kept it, and a dropped one reads as a
typo rather than a habit.

## His words

Jargon stays. An assistant draft formalizes vocabulary as it goes, and that is a tell on
its own: "the repository", "the README file", "utilize", "approximately", "in order to".
He does not talk like that, and the corpus shows it.

| He writes | Not | Corpus, 103 messages |
|---|---|---|
| make | create, build out, construct | 20 : 0 |
| ok | acceptable, fine as-is | 7 : 0 |
| please | kindly | 6 : 0 |
| stuff, thing(s) | materials, components, items | 6 : 1 |
| print, prints, printed | 3D-printed part, printed component | 5 : 2 |
| ai | language model, LLM, the assistant | 4 : 0 |
| use | utilize, leverage | 3 : 0 |
| repo, readme | repository, README file | 1 : 0 each |

The corpus is 1,398 words, so treat the small rows as direction and the large ones as
rule. Three habits follow:

- **Never expand a short form.** "repo" does not become "repository" because the text is
  going public. It was "repo" when he typed it and it stays "repo".
- **Never gloss a term.** No "STL (stereolithography)" and no "OpenSCAD, a script-based
  CAD tool". A reader on Printables knows what an stl is. A reader on GitHub can search.
- **Never upgrade a plain verb.** make, use, fix, try, check. Not create, utilize,
  resolve, attempt, validate.

What he does *not* do is textspeak: 1 "rn", 0 "tbh", 0 "imo", 0 "lol". Plain words,
lowercase, is the register. Not abbreviation for its own sake.

`references/jargon.txt` is the list of his vocabulary that the system dictionary does not
know. It exists so the tools protect those words: the scraper does not count them as
typos and the slip planner never produces one by accident. Nothing in this skill removes,
replaces, expands or capitalizes a word on that list.

## Deliberate slips

Flawless prose is itself a tell, and Miguel asked for some typos to survive into public
text. The reason is his own reading experience, not how anyone else perceives it, so the
governing test is narrow:

> **A slip is acceptable only if it costs nothing to read.** If it would make him stop,
> re-read or reparse the sentence, it fails, however authentic it looks.

Everything below follows from that one test.

**Rate.** One slip per 200-400 words, with each gap drawn at random rather than on a
fixed stride. Confirmed by A/B on 2026-09-14 over 1 per 100-200 and over his natural
rate. A 2,000-word README gets roughly 5 to 10. His natural typing rate is 1 per
49 words by hand count and 1 per 74 by the scraper's stricter automatic count. Published
text is deliberately four to six times sparser than that.

**The three permitted classes**, taken from how he actually mistypes:

| Class | His real examples |
|---|---|
| Transposition, adjacent letters swapped | `wokr` `htis` `jsut` `nto` `tkaing` `pgorgress` `obisdian` |
| Dropped letter | `histoy` `conver` `eigth` |
| Doubled or extra letter | `agressive` `useage` `easyer` `mimicing` `detends` |

**Never a slip that produces a real word.** This is the sharpest rule and the easiest to
break by accident. `form`/`from`, `trial`/`trail`, `casual`/`causal`, and every homophone
pair: their/there, its/it's, your/you're, affect/effect. A slip that lands on a valid
word gets accepted by the eye, so the sentence goes wrong silently and has to be read
twice. A slip that lands on a non-word is autocorrected instantly and costs nothing.
The corpus agrees: **zero** wrong-word errors in 1,226 words of his typing.

**Prefer long words.** Transposition is most transparent on words of 7 letters or more
and most dangerous on short ones, where a swap is likely to land on another real word.

**Never** slip a load-bearing technical term. Do not turn `detent` into `detend` in a
document where the detent is the subject; that reads as the wrong term, not as a slip.

**Never** slip the same word twice in one document, put two slips in one paragraph, or
put one in the first sentence of a section, where he is orienting and it costs the most.

**Never** slip a word in a sentence that is itself about typos or slips. It reads as a
joke, and a joke reads as intentional, which is the opposite of the point. Reject that
site and take a neighboring word.

**Never-slip zones.** Code fences, inline code, identifiers, numbers and units, the fit
spec, commands, paths, URLs, tags, licence names, headings. Also contractions and jargon:
a slip on "dont" or "openscad" reads as the wrong word, not as a slip, and the planner
refuses those sites.

**Do not add a spellchecker** or a CI spell job to these repos. It would mechanically
undo all of this.

Place slips with `tools/slipplan.py`, which picks the positions at random, draws the
class per site from the weights in `references/profile.json`, and refuses any candidate
that is a real word or a word in `references/jargon.txt`. Doing it by hand produces predictable placements and
suspiciously cute typos.

## Banned constructions

Cut on sight. These are the tells that mark text as machine-written.

- delve, leverage, robust, seamless, elevate, unlock, harness, empower, streamline,
  effortless, comprehensive, cutting-edge, game-changer, powerhouse, dive in
- "In today's world", "In an era of", "It's worth noting that", "At the end of the day"
- "It's not just X, it's Y" and "More than just X"
- "Whether you're a X or a Y"
- Three-item triads used for rhythm rather than because there are exactly three things
- A closing paragraph that restates what the document just said
- Every bullet opening with a bolded `**Word:**` label. Fine occasionally, not as the
  house format for a whole list.
- Hype adjectives with no number behind them: powerful, blazing, incredibly, perfect

## What NOT to carry over from his chat register

His typed messages skip terminal periods (101 of 103). That one is keyboard speed:
**published prose keeps its full stops.** A fragment still ends with one.

Everything else that looks like shorthand carries over, each by his explicit choice:

- **Lowercase**, names and acronyms included. See "Lowercase, all of it".
- **Contractions with no apostrophe**, "lets" included. See "Contractions as typed".
- **Typos**, deliberately placed. See "Deliberate slips".
- **Emphatic caps on a single word** ("a LITTLE more aggressive", "taken from the SLEEVE
  rather than the box"). Confirmed by A/B on 2026-09-14 over bold and over no emphasis.
- A willingness to say a thing is uncertain rather than smoothing it over.

What does not carry over, by the same A/B round: the chat softeners. "honestly",
"basically", "just", "a bit". Plain and short instead.

Keep the directness. Add only the periods.

## Per-surface rules

See `references/surfaces.md` for the full set. The short version:

- **Commit messages:** lowercase, no trailing period, scope then colon then the change,
  concrete deltas with a plain ASCII arrow: `widen the slab by 1 mm: 66 -> 67`,
  `take the slab's height from the sleeve, not the box: 88 -> 91 mm`, `lint cleanup:
  add ruff, fix a python 3.11 f-string bug, drop dead imports`. Those shipped with a
  capital first letter; lowercase was his A/B pick on 2026-09-14. Subject only, a body
  is the exception. No `feat:`/`fix:` conventional-commit prefixes; he does not use them.
- **PR descriptions:** four labeled lines, `what:` `why:` `verified:` `not verified:`,
  lowercase, in that order. Chosen by A/B on 2026-09-14 over a prose paragraph. The last
  line is never dropped. No generated-with footer.
- **README:** fit spec / requirements up top, honest limits before features, a table for
  variants, and a section saying what it does not do.
- **Model listings:** title says what it is and its one differentiator. Summary line
  spec first. Description opens on the problem. The measurable spec as a blockquote.
  The trade-off as a number, then who it is not for. What was not tested, blunt and
  first person. Three of those were picked from A/B samples on 2026-09-14.

## Workflow

1. Read the whole target file first. Never rewrite from a summary of it.
2. Run the linter: `python3 ~/.claude/skills/miguelify/tools/voicecheck.py <file>...`
   It is a regex pass, so it catches the mechanical tells (em dashes, emoji, banned
   words, attribution) and nothing else. It is a floor, not a passing grade.
   It also greps for the private strings listed in `references/private.md` and exits 2
   if it finds one. That check is a publish-blocker: fix the leak, do not argue with it.
3. Rewrite by hand against "The voice" above. The judgment calls - the honesty
   downgrade, the who-it-is-not-for paragraph, cutting a restating conclusion - are the
   ones that matter and the linter cannot see them.
4. Re-run the linter until clean.
4b. Only once the rewrite is settled, run
   `python3 ~/.claude/skills/miguelify/tools/slipplan.py <file>` and place the slips
   by hand. Slips go in **last**, so they are not quietly corrected during the rewrite.
5. Before anything is pushed, run the linter over the whole repo and its history:
   `python3 ~/.claude/skills/miguelify/tools/voicecheck.py --tracked --git`
   That covers every tracked file plus the author email and message of every commit.
   Exit 2 means a private string is still in there, in a file or in git metadata. A
   "possible leak" line means something shaped like an email, path, IP, token or
   credential turned up: read it, and if it is a real one, add it to `private.md`.
6. **Show him the diff before anything is pushed, uploaded or published.** Rewriting his
   public words is his call to approve, every time. Never push, never publish, never
   post as part of this skill.

If the corpus should be rebuilt after he has written more:
`python3 ~/.claude/skills/miguelify/tools/extract_voice_corpus.py`
It writes the corpus to `references/voice_corpus.txt` (gitignored, redacted) and the
counts to `references/profile.json` (tracked), and prints the drift against the previous
profile. If a previously-zero count has gone nonzero, reread `references/voice.md`
before trusting the absolutes. If the typo inventory flags real vocabulary, add it to
`references/jargon.txt` and rerun.
