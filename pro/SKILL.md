---
name: miguelify-pro
description: On-demand only. The professional register of miguelify. Use ONLY when Miguel asks for it by name (/miguelify-pro, "miguelify pro") or asks in words for a professional pass on AI-drafted text - "make this professional", "professional miguelify", "clean this up for linkedin", "polish this post without making it sound like ai". Same research and AI-tell rules as miguelify, but standard capitalization, apostrophes and no deliberate typos. For posts, announcements, project write-ups, listings, READMEs and bios that should read as written by a careful person. Do NOT invoke on your own, and do not use it when he asks for plain miguelify.
---

# miguelify-pro

Take text an AI drafted and make it read as if Miguel wrote it carefully, for an
audience he wants to take him seriously. Not as if an assistant produced it, and not as
if he typed it fast in a chat window.

Plain miguelify keeps his keyboard habits on purpose: lowercase names, `dont`, a few
typos. This skill drops that layer and keeps everything underneath it. The part of his
voice that survives is the part that was never about keystrokes: specific facts, plain
words, honest limits, and an opening that gets to the point.

It is a rewrite pass, not a generation pass. Facts, numbers and structure in the draft
survive unless they are wrong.

## When it runs

On demand only. He asks, then it runs. Do not apply it to a post, README or commit on
your own, and do not swap it in when he asks for plain miguelify. If it is not clear
which register he wants, ask in one line: "personal or professional?"

## Where the rules come from

Nothing here is new taste. Every rule is one of these:

- **Kept from miguelify.** Measured from 108 messages he typed by hand (1,446 words) and
  the repo text he has shipped, then settled across four A/B rounds on 2026-09-14 where
  he picked between rendered variants. `~/.claude/skills/miguelify/references/voice.md`
  has the counts and the picks.
- **From Wikipedia's AI cleanup project.** [WP:AISIGNS](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing),
  read in full on 2026-11-09. `~/.claude/skills/miguelify/references/ai-tells.md` maps
  every pattern to its fix.
- **Changed for this register.** Only the four keyboard habits in "What changes" below.
  Each one was a deliberate personal-register choice, not a finding about what makes
  text read as human, so dropping it costs nothing.

## The first pass is content

WP:AISIGNS makes the point that matters most: the tells are symptoms. A model drifts
toward the most likely sentence, so a specific fact gets swapped for a generic,
important-sounding one, and the text gets vaguer and louder at once. Polishing the words
while leaving the vagueness just hides it, and professional copy is where that happens
most, because "professional" pulls a draft toward corporate filler.

So before touching a word, go sentence by sentence and ask: would this still be true of
someone else's project? If yes, put the specific fact back (the number, the
measurement, what was or was not tested, what it cost, how long it took) or cut the
sentence. Never invent a figure to fill a gap. If there is no number, say so or say
nothing.

Professional does not mean impressive. It means a reader who does not know him can
trust every sentence.

## What stays exactly as in miguelify

**No em dashes.** Zero in his typing. Use the spaced hyphen ` - ` for an aside, his
A/B pick on 2026-09-04, or a colon, or two sentences. No en dash in ranges either:
`29.8-51.6 mm`. Avoid the semicolon. He has never typed one, and swapping one tell for
a subtler one is not a fix.

**No emoji.** Zero in his typing and in everything he has published. No badge rows.

**No Claude attribution anywhere public.** No co-author trailer, no generated-with
footer. A standing preference, recorded in memory, that applies with or without this
skill.

**American spelling.** license, color, millimeter, organize.

**Open with the thing itself.** No throat-clearing, no "Introducing", no framing
sentence about why the field matters. A/B confirmed 2026-09-14. A post about a model
opens on the problem and the object: "A 100+ card deck box is far deeper than the deck
you keep in it. I made a slab that fills the gap."

**Numbers with units, plain.** 67 x 91 x 18.6 mm, spaced units, no bold. A/B confirmed.
Every claim about size, speed, count, time or cost gets its figure.

**Hand the reader a test they can run.** "Measure the inside of your box and compare."
Better than any assurance that it works.

**Say what it costs and who it is not for.** The most distinctive thing in his
published writing and the first thing a draft drops. The cost as a number, then the
exclusion, no lead-in: "The slab takes 18.6 mm of the 67.5 mm interior, about a quarter.
If you fill your deck box to the brim, this isn't for you." A/B pick, 2026-09-14. Never
ship copy that only lists upsides.

**Say what was not done, first person, one line.** "Untested at this size. I printed
v1.0 at 66 x 88 mm, not this one." A/B pick over the third-person form and over a
standing disclaimer section. This is the opposite of an AI hedge: a model writes "fit
should be treated as approximate", he writes what he did and did not do.

**Own mistakes plainly.** "The game-specific names were always slightly misleading.
Nothing in either layout is game-specific, and people picked the wrong one." No
defensiveness, no burying it.

**Plain words.** His counts, 108 messages: make over create 20 to 0, use over utilize,
ok over acceptable. In this register:

| Write | Not |
|---|---|
| make, build | create, construct, craft |
| use | utilize, leverage |
| about | approximately |
| before, after | prior to, subsequently |
| to | in order to |
| repo, README | repository, README file |
| tried, fixed, checked | attempted, resolved, validated |
| print, printed part | 3D-printed component |

Never gloss a term the audience knows ("STL (stereolithography)"). Never expand a short
form because the text is going public.

**Rhythm is bursty, not even.** His median sentence is 11 words, a fifth are 5 or
fewer, the 90th percentile is 25. Mix short sentences with the occasional longer one
that carries a colon. Nothing over 30 words. The newest models (late 2026) write every
sentence at 8-20 words with only commas and periods, and that is now its own tell. The
linter's `rhythm` check flags it.

**Tables for anything with variants or specs.** A/B confirmed over prose and bullets.

## What changes

Four things, and only these. Each was a choice for his personal register.

| miguelify | miguelify-pro | Why it was a choice, not a finding |
|---|---|---|
| everything lowercase, names included: github, openscad | Standard capitalization. Sentences, the pronoun I, and names as their owners style them: GitHub, OpenSCAD, Printables, MakerWorld, STL, AI, 3D | Lowercase matched how he types, 25 of 29. It was never a readability rule |
| dont, isnt, youre | don't, isn't, you're | Contracting at all stays: the uncontracted form reads stiff. Only the apostrophe comes back |
| one deliberate typo per 200-400 words | None. Spell-check the result | WP:AISIGNS lists perfect grammar as an unreliable AI sign, so a clean text gives nothing away |
| emphatic caps on one word: "the SLEEVE" | No caps emphasis and no bold in prose. Let the sentence carry it, or italics once | Caps read as shouting outside his own spaces |

Headings: sentence case ("Will it fit my box?"), never Title Case, which is itself a
WP:AISIGNS formatting tell. A plain question still makes a good heading.

Full stops on every sentence. That was already true of published miguelify text.

Still out, as in his A/B round: the chat softeners "honestly", "basically", "just",
"a bit". Professional is not the same as warm.

## AI tells

Everything in miguelify's list applies: `~/.claude/skills/miguelify/references/ai-tells.md`.
The short version, with linter ids:

- Significance nobody asked for: "stands as a testament", "plays a pivotal role",
  "marks a shift". (`legacy`)
- A fact followed by ", highlighting / underscoring / ensuring ...". End at the fact.
  (`ingtail`)
- "serves as", "boasts", "features a" for is and has. (`copula`)
- "not just X, it's Y", "no X, no Y, just Z". (`negpar`) "Y rather than X" as a habit.
  (`ratherthan`)
- "many users report", "experts agree", "widely regarded". Who, how many, where.
  (`vague`)
- AI vocabulary: delve, pivotal, crucial, vibrant, showcase, foster, enhance,
  landscape, robust, seamless, leverage, quietly, multifaceted. Several in one text is
  the strongest tell there is. (`aivocab`, `hype`)
- "it's important to note", "should be treated as", "based on available
  information". (`disclaim`)
- "Overall,", "In summary," and a last paragraph that restates the first. (`summary`)
- Triads for rhythm, one thing called four names, a rigid intro-features-benefits-
  conclusion outline. (by hand)

### Post tells

Posts (LinkedIn, Bluesky, X, forum and blog announcements) have their own template, and
"professional" pulls a draft straight into it. These are flagged by `hook` and
`hashtags` in `--pro` mode, or caught by hand:

- **The announcement opener.** "I'm thrilled to share", "Excited to announce", "Big
  news". Open on what was made or found, with a number.
- **The one-line hook and the line-break ladder.** A teaser sentence, a blank line, a
  reveal: "The result? 40% faster." Write it as one sentence.
- **Engagement bait at the end.** "Thoughts?", "What do you think?", "Agree?", "Drop
  a comment". End on the last real fact or the link.
- **The lessons listicle.** "5 things I learned building X", each lesson a platitude.
  If there is one real lesson, state it with what happened.
- **"Here's the thing", "Let that sink in", "Unpopular opinion".** Cut.
- **A wall of hashtags.** Zero to three, at the end, in plain words.
- **Gratitude padding.** Thanking a list of people is fine when they did something; say
  what they did.

## Per-surface rules

**Posts.** What it is and the one number that matters, in the first sentence. Then what
it does, then what it costs or what did not work, then the link. Usually under 150
words. Stop after the link. No call to action unless there is a real one ("Issues and
pull requests welcome" is real for a repo, "Follow for more" is not).

**Model listings.** As miguelify's `surfaces.md`, with standard caps. Title says what it
is plus the one differentiator, in sentence case: "Universal dice insert for
top-opening deck boxes - with or without a coin well". Summary is spec first. The hard
numbers in a blockquote. The trade-off as a number, then who it is not for. What was not
tested, in one first-person line. Tags stay lowercase: they are search terms.

**READMEs.** Name, version, one sentence on what it is. The spec or requirement before
anything else. How it works. A table for variants. Limits and who it is not for, above
the fold, not at the bottom.

**PR descriptions.** The same four labeled lines, capitalized: `What:` `Why:`
`Verified:` `Not verified:`. The last one is never dropped.

**Commit messages.** His shipped shape with a capital first letter, which is how they
originally shipped: "Widen the slab by 1 mm: 66 -> 67". ASCII arrow, no period, no
conventional-commit prefix, subject only.

**Bios and about sections.** What he makes and where, with one concrete example. No
adjectives about himself ("passionate", "driven", "innovative").

## Workflow

1. Read the whole draft. Never rewrite from a summary of it.
2. Lint it: `python3 ~/.claude/skills/miguelify/tools/voicecheck.py --pro <file>`.
   For pasted text, write it to a scratch file first. It catches the mechanical tells
   and nothing else. It also greps for the private strings in
   `~/.claude/skills/miguelify/references/private.md`; exit 2 is a publish-blocker.
3. Content pass, sentence by sentence, as above. Check every claim against what was
   actually done.
4. Rewrite against "What stays" and "What changes". The judgment calls are the ones
   that matter: the cost-and-who-it-isn't-for line, the first-person untested line,
   cutting a restating close, one name per thing.
5. Re-lint until clean. No slip pass. `slipplan.py` is not part of this skill.
6. Show him the result, or the diff for a file, before anything is posted, pushed or
   published. Never post as part of this skill.

## Before and after

A post drafted for a model release.

Before:

> I'm thrilled to share my latest project! 🎲 After weeks of iteration, I've created a
> robust, versatile dice insert that seamlessly fits into most deck boxes — not just a
> tray, but a complete organization solution for TCG players. It features a coin well
> and showcases the power of parametric design. Many users have found it game-changing!
> Check it out and let me know your thoughts! #3DPrinting #TCG #MTG #Pokemon #Maker

After:

> A 100+ card deck box is far deeper than the deck you keep in it. I made a 67 x 91 x
> 18.6 mm slab that fills the gap and holds your dice, with an optional well for a
> coin up to 38 mm.
>
> The cost: it takes about a quarter of the box's depth. If you fill your box to the
> brim, this isn't for you. Measure the inside before you print.
>
> Untested at this exact size. I printed v1.0 at 66 x 88 mm. OpenSCAD source is
> included if yours needs different numbers.
>
> [link] #3dprinting #mtg

What changed: the announcement opener and the closing bait are gone. "Robust",
"versatile", "seamlessly", "showcases" and "game-changing" became three numbers. "Many
users" had nobody behind it, so it went. The em dash and the "not just X" line went with
the claim they carried. The trade-off and the untested line were added, because a
draft that lists only upsides is the first thing to fix. Capitals and apostrophes stay.
