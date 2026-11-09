# AI tells, from Wikipedia's field guide

Source: [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
(WP:AISIGNS), maintained by WikiProject AI Cleanup. Read in full on 2026-11-09. Everything
below is paraphrased and mapped onto the surfaces this skill works on: READMEs, model
listings, commits, PRs and bios. The page is about encyclopedia articles, so the
Wikipedia-only signs (broken DOIs, AfC notes, edit summaries) are left out.

## Read this before the list

The page makes three points that change how this skill should work.

**The signs are symptoms.** The page says outright that fixing only the surface markers
can just make detection harder while the real problem stays. That problem is what
language models do by default: they drift toward the most statistically likely
sentence, so a specific, unusual fact gets swapped for a generic, important-sounding
one. The page's example is "inventor of the first train-coupling device" turning into
"a revolutionary titan of industry". The text gets vaguer and louder at once.

For this skill that means **the first pass is content, not wording**. Find every
sentence that would still be true of some other project, and either put the specific
fact back (the number, the measurement, the thing that was or wasnt tested) or cut it.
Most of the patterns below disappear once that is done, because they are what a model
writes when it has no specific fact to hand.

**Some things people assume are tells are not.** The page lists these as ineffective
indicators: perfect grammar, a mix of casual and technical register, "bland" or
"fancy" prose in general, transition words on their own, and unsourced claims. So the
deliberate slips in SKILL.md are his preference, not camouflage, and they do nothing to
fix text that is still generic. His mixed register (lowercase, technical figures, blunt
asides) is explicitly called a normal human pattern.

**The tells change by model generation.** "delve" peaked in 2023 and was mostly gone by
2025. The newest models (mid-2026 on) have been tuned to drop em dashes completely, and
that created a new tell: prose with only commas and periods and every sentence held to
roughly 8-20 words. See "the 2026 trap" below, because miguelify's own rules point
straight at it.

## Content patterns

| Pattern (WP shortcut) | What it looks like | What to write instead | Linter |
|---|---|---|---|
| Puffed-up significance (AILEGACY) | "stands as a testament", "plays a pivotal role", "marks a shift", "reflects broader trends", "an enduring legacy" | Cut it. If something real is under it, say what the thing does, with a number. A dice tray does not have a legacy. | `legacy` |
| Trailing analysis (SUPERFICIAL) | a fact, then ", highlighting / underscoring / reflecting / ensuring / fostering ..." | End the sentence at the fact. If the why matters, it gets its own sentence with its own evidence. | `ingtail` |
| Canned notability (AIATTR) | "featured in several outlets", "independent coverage", "maintains an active social media presence" | Link the one source that matters, by name, or leave it out. | `notability` |
| Leaning on sources to identify (AIIDENTIFY) | "his website identifies him as", "the listing describes it as" | State the fact. Cite if needed. | `notability` (partly) |
| Vague connection (AICONNECT) | "associated with", "in connection with" | The actual relationship: made, uses, runs, forked from. | `connect` |
| Vague attribution (AIWEASEL) | "many users report", "experts argue", "widely regarded" | Who, how many, where, in the shape of "3 people in the comments said it was loose in an ultimate guard box". Or cut. | `vague` |
| Challenges formula (FACESCHALLENGES) | "Despite its strengths, it faces several challenges ... Despite these challenges, it continues to thrive" | The limits, as numbers, then stop. No upbeat closer. His version: the cost as a number, then who it isnt for. | `challenges` |
| "X and Y" sections (AISIGNS, Awards and recognition) | "## Challenges and Future Directions", "## Features and Benefits" | One heading, one thing, lowercase, often a question: "will it fit my box?" | `andhead`, `titlecase` |

## Language patterns

| Pattern | What it looks like | What to write instead | Linter |
|---|---|---|---|
| AI vocabulary (AIWORDS) | see the era list below | The plain word, or the figure. Density is the tell: one is chance, five is a signature. | `aivocab`, `hype` |
| Avoiding "is" and "has" (AINOCOPULA) | "serves as", "stands as", "functions as", "boasts", "features a", "offers two" | "is", "has". A study the page cites found "is" and "are" fell by over 10% in academic writing in 2023 alone. | `copula` |
| Not X, but Y (AIPARALLEL) | "not just a tray, its a system", "not only ... but also", "no X, no Y, just Z" | Say what it is. Nobody claimed it was X. | `negpar` |
| Y rather than X (AIPARALLEL) | "it sits beside the deck rather than replacing it" | Fine once, for a real choice between two options. The newest models lean on it as a habit. | `ratherthan` |
| Rule of three (RO3) | "strong, sturdy, and reliable", three-phrase lists that pad an analysis | Only when there are exactly three things. Otherwise one, with a number. | by hand |
| Elegant variation (AIELEVAR) | the same thing called "the insert", then "the tray", then "the accessory", then "the solution" | Pick the word and keep it. "repo stays repo" is the same rule. | by hand |
| Stiff synonyms | authored, relocated, utilized, attempted | wrote, moved, used, tried. Wikipedia lists the plain verbs as a sign of human writing. | `formal` |

## Disclaimers and chat leftovers

| Pattern | What it looks like | What to write instead | Linter |
|---|---|---|---|
| Didactic disclaimers (DIDACTIC, 2023-24) | "it's important to note", "it's crucial to remember" | Cut. If the note is real, say it as a plain instruction: "measure first." | `disclaim` |
| Source-availability hedges (AIDISCLAIMER, 2024-25) | "not widely documented", "based on available information" | Say what you checked and what you did not. | `disclaim` |
| Corrective framing (AIDISCLAIMER, mid-2026 on) | "should be treated as approximate rather than guaranteed", "this does not by itself establish", "should not be confused with" | His honesty rule, which is the opposite in shape: first person, specific, blunt. "untested at this size. i printed v1.0 at 66 x 88, not this one. measure first." | `disclaim`, `ratherthan` |
| Restating conclusion (CONCLUSION) | "Overall,", "In summary,", "Ultimately," and a last paragraph that repeats the first | End on the last real fact. | `summary` |
| Talking to the user (COLLABCOMM) | "I hope this helps", "Let me know if", "Here's a revised version", "Certainly!" | Cut. This is a pasting accident. | `chatbot` |
| Placeholders (AIPLACEHOLDER) | "[insert print settings]", "YYYY-MM-DD" | Fill it or cut it. | `placeholder` |

## Formatting

Wikipedia lists these as style signs. Most are already miguelify rules.

- Title Case headings instead of sentence case. Here: lowercase. `titlecase`
- Bold scattered through prose, and lists where every item starts with a bold label
  ("**Durability:** ..."). `boldnum`, `labelbul`
- Emoji at the start of headings or bullets. `emoji`
- Curly quotes and apostrophes. Straight quotes, and contractions have no apostrophe
  anyway. `curly`
- Em dashes, especially spaced ones used for punch. `emdash`

## AI vocabulary by era

From the page's breakdown. These co-occur: where there is one there are usually more.
The page also warns to take each word literally (a synonym is not a tell) and in context
("landscape" in a photo caption is fine).

| Era | Words |
|---|---|
| 2023 to mid-2024 | additionally, boasts, bolstered, crucial, delve, emphasizing, enduring, garner, intricate, interplay, key, landscape, meticulously, pivotal, underscore, tapestry, testament, valuable, vibrant |
| mid-2024 to mid-2025 | align with, bolstered, crucial, emphasizing, enhance, enduring, fostering, highlighting, pivotal, showcasing, underscore, vibrant |
| mid-2025 to mid-2026 | emphasizing, enhance, highlighting, showcasing, plus the notability phrases above |
| mid-2026 on | challenge, clearer, dependable, echoed, foster, leverage, matters, multifaceted, practical, prioritize, quietly, steady, universally |
| Promotional, 2023-25 | nestled, in the heart of, groundbreaking, renowned, diverse array, commitment to, exemplifies, profound, rich, natural beauty |

The linter matches the distinctive ones. "key", "practical", "clearer", "steady",
"matters" and "challenge" are too common in ordinary writing to flag on sight, so check
them by density when reading.

## The 2026 trap

Three miguelify rules, followed literally, produce the newest AI signature:

1. no em dashes
2. avoid the semicolon
3. short sentences, never past 30 words

The page notes that models from late 2026 have been tuned so hard away from em dashes
that they barely use any punctuation but commas and periods, and that they hold
sentences to a narrow 8-20 word band. Text that is all mid-length sentences with commas
and periods now reads as a model.

His typing does not look like that. Median sentence 11 words, but a fifth are 5 words or
fewer and the 90th percentile is 25. He uses the spaced hyphen (26 times in the corpus) and
question marks (17), and every shipped commit subject hangs its specifics off a colon. So the rules stay, with two clarifications that are
now in SKILL.md:

- **Vary the length.** Fragments next to the occasional longer sentence. Not every
  sentence trimmed to the same size. The linter's `rhythm` check flags prose where the
  spread of sentence lengths is low or most sentences sit in the 8-20 band.
- **Use the punctuation he types.** The spaced hyphen for an aside, a colon before a
  number or a trade-off, a plain question as a heading or an opener. Avoiding the em
  dash is not the same as avoiding asides.

## What the page says humans do more

Over 25 years of articles, Wikipedia's editors found these more common in human writing
than in AI text. They line up with his voice, which is the point.

- Plain "there is" / "it has" sentences.
- Plain verbs: wrote, moved, used, tried, died.
- Definite and superlative statements where they are true: "the only", "the first", "one
  of the few". Models smooth these into "a notable". If it is the only slab design that
  takes a 38 mm coin, say so, and say how you know.
- Qualifiers and intensifiers: very, perhaps, tends to. (His A/B round cut the chat
  softeners, "honestly", "basically", "just". That stands. Emphatic caps on one word are
  his intensifier.)

## What the linter cannot see

Regex catches words. It cannot catch:

- a sentence that would be true of any project (the root problem)
- elegant variation across a document
- a rigid outline: intro, features, benefits, challenges, conclusion
- a rule of three that pads
- invented or misdescribed sources
- a disclaimer that hides a gap instead of naming it

Those are the reading pass in SKILL.md, and they matter more than anything the linter
reports.
