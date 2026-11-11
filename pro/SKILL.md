---
name: miguelify-pro
description: On-demand only. The professional register of miguelify: semi-casual and fully correct. Use ONLY when Miguel asks for it by name (/miguelify-pro, "miguelify pro") or asks in words for a professional pass on AI-drafted text - "make this professional", "professional miguelify", "clean this up for linkedin", "polish this post without making it sound like ai". Fully correct English (spelling, capitalization, punctuation, grammar) with miguelify's research-backed rules against AI-sounding text. For posts, captions, slides, announcements, project write-ups, listings, READMEs and bios. Do NOT invoke on your own, and do not use it when he asks for plain miguelify.
---

# miguelify-pro

Take text an AI drafted and make it correct in every mechanical way (spelling,
capitalization, punctuation, grammar) while making sure it does not read as if an AI
wrote it.

Those are two separate jobs, and the research behind miguelify says why they do not
conflict. Wikipedia's AI cleanup project lists perfect grammar as an unreliable sign of
AI writing: careful people write correct English too. What gives a draft away is
content and shape: generic claims in place of specific facts, inflated significance,
stock phrases, the same sentence length over and over. So this skill gets the
mechanics fully right and does all of its anti-AI work in the content, the word
choice and the structure.

Plain miguelify keeps his keyboard habits on purpose: lowercase, `dont`, the spaced
hyphen, a few typos. None of that belongs here. What carries over is the part of his
voice that was never about keystrokes: specific facts, plain words, honest limits, and
an opening that gets to the point.

It is a rewrite pass, not a generation pass. Facts, numbers and structure in the draft
survive unless they are wrong.

## Tone: semi-casual, still professional

The target is a person who knows the subject talking to people they respect: relaxed,
direct, warm, and correct. Think of a good club or project post, not a press release
and not a group chat. A/B round 5 (2026-11-11) put the dial toward casual: given a
reserved, a semi-casual and a casual version of the same caption, he picked casual.

His picks, which are the reference samples for this register:

> Got a resume that hasn't been touched since freshman year? Bring it to room 1300 on
> Tuesday, Nov 18, 6–8 pm. We'll tear it apart (nicely), and you'll walk out with a
> better one. There's pizza, too!
>
> Sign up through the link in bio. See you there!

> Fair warning: this size is untested. Mine was 66 × 88 mm. Measure first and you'll
> be fine.

What that looks like:

- **First and second person.** "I made", "we're hosting", "you'll need". Never "the
  organization is pleased to" or "attendees will".
- **Contractions everywhere a person would use them.** "We're", "you'll", "it's",
  "don't". A post with none reads like a form letter.
- **Everyday words.** "a lot of", "pretty much", "okay", "grab", "stop by", "come
  hang out" are all fine. "Utilize", "facilitate", "opportunity to engage" are not.
- **One short parenthetical per post.** "(nicely)", "(bring your own if you have a
  favorite)". A/B round 5 picked this over no asides and over a deadpan joke line, so
  the personality lives in one bracketed aside, not in a punchline.
- **An opening question is fine when it describes the reader's real situation**, and
  the next sentence gives the what, where and when: "Got a resume that hasn't been
  touched since freshman year? Bring it to room 1300 on Tuesday, Nov 18, 6–8 pm." A/B
  round 5 pick. A teaser question with no answer ("The secret?") is still a hook.
- **End with the action, then a short send-off.** "Sign up through the link in bio.
  See you there!" A/B round 5 pick over the bare action and over adding an urgency
  line. The send-off is a real sign-off, never a question fishing for comments.
- **Exclamation marks: up to two per post**, each where a person would say it with
  energy: a real perk ("There's pizza, too!") or the send-off. Never on the facts.
- **Limits get a light label.** "Fair warning:" then the fact in the first person,
  the number, and the test: "Mine was 66 × 88 mm. Measure first and you'll be fine."
  A/B round 5 pick over a plain statement and over "Quick caveat". The reassurance at
  the end is only allowed when it follows a real test the reader can run.

What it is not:

- Not slang or textspeak: no "lol", "ngl", "lowkey", "vibes", "y'all" unless it is
  his audience's own word and he asks for it.
- Not the chat softeners his A/B round cut even from personal copy: "honestly",
  "basically", "just" as filler, "a bit".
- Not sloppy. Semi-casual changes the word choice and the warmth, never the spelling,
  capitals or punctuation.
- Not hype. Casual drafts drift toward "super excited!!" and "amazing", which is the
  AI announcement template in a T-shirt.

When the audience is formal (a cover letter, a grant, a message to faculty or an
employer), dial the casual words down and keep everything else. He will say if a piece
needs to be fully formal.

## When it runs

On demand only. He asks, then it runs. Do not apply it to a post, README or commit on
your own, and do not swap it in when he asks for plain miguelify. If it is not clear
which register he wants, ask in one line: "Personal or professional?"

## Where the rules come from

Paths in this file are relative to this skill's folder.

- **Content rules from miguelify.** Measured from 108 messages he typed by hand and the
  repo text he has shipped, then settled across four A/B rounds on 2026-09-14 where he
  picked between rendered variants. `references/voice.md` has the counts and the picks.
- **AI tells from Wikipedia's AI cleanup project.**
  [WP:AISIGNS](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), read in
  full on 2026-11-09. `references/ai-tells.md` maps every pattern to its fix.
- **Mechanics from standard written American English.** His personal-register habits
  were his choices for his own spaces. In this register, correct wins every time.

## The first pass is content

WP:AISIGNS makes the point that matters most: the tells are symptoms. A model drifts
toward the most likely sentence, so a specific fact gets swapped for a generic,
important-sounding one, and the text gets vaguer and louder at once. Polishing the words
while leaving the vagueness just hides it, and professional copy is where that happens
most, because "professional" pulls a draft toward corporate filler.

So before touching a word, go sentence by sentence and ask: would this still be true of
someone else's project or event? If yes, put the specific fact back (the number, the
date, the measurement, what was or was not tested, what it cost, how long it took) or
cut the sentence. Never invent a figure to fill a gap. If there is no number, say so or
say nothing.

Professional does not mean impressive. It means a reader who does not know him can
trust every sentence.

## Correct, all of it

Every one of these is non-negotiable. The result should pass a careful copy editor.

**Spelling.** No typos, ever. American spelling: license, color, millimeter, organize,
capitalization. Proofread every word before showing the result, and run the linter's
`spelling` check as a second pair of eyes (it uses an old word list, so read its hits
rather than trusting them).

**Capitalization.** Sentences start with a capital. The pronoun I is capitalized.
Names are styled the way their owners style them: GitHub, OpenSCAD, Printables,
MakerWorld, Instagram, LinkedIn, STL, AI, 3D. Headings in sentence case ("Will
it fit my box?"), never Title Case, which is itself a WP:AISIGNS formatting tell.

**Complete sentences in prose.** Every sentence in running text has a subject and a
verb. Fragments are fine only in titles, slide bullets, table cells and spec lines.
"Untested at this size." becomes "I haven't tested it at this size."

**Punctuation.**
- No em dashes. They are the most recognized AI tell there is. Use a comma, a colon,
  parentheses or two sentences. No spaced hyphen ` - ` either: that is a keyboard
  habit, not punctuation.
- Number ranges take an en dash with no spaces (6–8 pm, 29.8–51.6 mm), or "to" in
  running prose (from 29.8 to 51.6 mm). The linter accepts an en dash only between
  two numbers.
- Semicolons are correct but rare in natural writing, and a string of them reads as
  machine-made. Prefer two sentences.
- Apostrophes in every contraction and possessive: don't, it's, the box's. Use
  contractions where a person would say them. Writing out every "do not" reads stiff.
- Straight quotes, not curly ones. Full stops on every sentence.
- Exclamation marks: at most two per post (see "Tone"). Most drafts have more on the
  facts themselves; cut those.

**Numbers.** Figures with units: 67 × 91 × 18.6 mm (a multiplication sign or a plain
x, consistently), 38 mm, 6–8 pm. Dates and times in a consistent house form, such as
"Tue, Nov 18, 6–8 pm". No bold on figures.

**Emphasis.** None in prose: no bold, no caps on a word. Let the sentence carry it.
Italics once in a long piece, at most.

**No emoji, no badge rows,** unless he asks for them on a specific post.

**No Claude attribution anywhere public.** No co-author trailer, no generated-with
footer. A standing preference that applies with or without this skill.

## Not sounding like AI

These are the rules that keep correct text from reading as generated. All of them come
from his A/B picks or from WP:AISIGNS.

**Open with the thing itself, or the reader's situation.** No throat-clearing, no
"Introducing", no framing sentence about why the field matters. A post opens on the
problem and the object, on the event and its date, or on a one-line question about
the reader's real situation followed straight away by the what and when.

**Numbers in place of adjectives.** He never writes "compact" or "a great fit" when
there is a figure. Every claim about size, speed, count, time or cost gets its number.

**Hand the reader a test they can run.** "Measure the inside of your box and compare."
Better than any assurance that it works.

**Say what it costs and who it is not for.** The most distinctive thing in his
published writing and the first thing a draft drops. The cost as a number, then the
exclusion, with no lead-in: "The slab takes 18.6 mm of the 67.5 mm interior, about a
quarter. If you fill your deck box to the brim, this isn't for you." A/B pick,
2026-09-14. Never ship copy that only lists upsides.

**Say what was not done, in the first person.** "Fair warning: this size is
untested. Mine was 66 × 88 mm. Measure first and you'll be fine." This is the opposite
of an AI hedge: a model writes "fit should be treated as approximate", he says what he
did and did not do, and hands over the test.

**Own mistakes plainly.** "The game-specific names were misleading. Nothing in either
layout is game-specific, and people picked the wrong one." No defensiveness.

**Plain words.** His counts, 108 messages: make over create 20 to 0, use over utilize.

| Write | Not |
|---|---|
| make, build | create, construct, craft |
| use | utilize, leverage |
| about | approximately |
| before, after | prior to, subsequently |
| to | in order to |
| tried, fixed, checked | attempted, resolved, validated |
| help | empower, enable |
| printed part | 3D-printed component |

Plain words are where the semi-casual tone comes from (see "Tone" above). Never gloss
a term the audience knows ("STL (stereolithography)").

**Vary sentence length.** His median sentence is 11 words, a fifth are 5 words or
fewer, and the 90th percentile is 25. Mix short complete sentences with the occasional
longer one that carries a colon. Nothing over 30 words. The newest models (late 2026)
write every sentence at 8 to 20 words with only commas and periods, and that is now its
own tell. The linter's `rhythm` check flags it.

**One name per thing.** If it is the slab in the first paragraph, it is the slab in the
last. No rotating synonyms (the insert, the tray, the accessory, the solution).

**Tables for anything with variants or specs.** A/B confirmed over prose and bullets.

## AI tells

The full list is `references/ai-tells.md`. The short version, with linter ids:

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

Posts (LinkedIn, Instagram, Bluesky, X, forum and blog announcements) have their own
template, and "professional" pulls a draft straight into it. These are flagged by
`hook` and `hashtags` in `--pro` mode, or caught by hand:

- **The announcement opener.** "I'm thrilled to share", "Excited to announce", "Big
  news". Open on what was made, found or scheduled, with a number or a date.
- **The one-line hook and the line-break ladder.** A teaser sentence, a blank line, a
  reveal: "The result? 40% faster." Write it as one sentence.
- **Engagement bait at the end.** "Thoughts?", "What do you think?", "Agree?", "Drop
  a comment". End on the last real fact or the link.
- **The lessons listicle.** "5 things I learned building X", each lesson a platitude.
  If there is one real lesson, state it with what happened.
- **"Here's the thing", "Let that sink in", "Unpopular opinion".** Cut.
- **A wall of hashtags.** Zero to three, at the end, in CamelCase so screen readers
  can say them: #3DPrinting, #CareerFair.
- **Gratitude padding.** Thanking people is fine when they did something. Say what
  they did.

## Per-surface rules

**Posts.** What it is and the one number or date that matters, in the first sentence.
Then what it does, then what it costs or what did not work, then the link. Usually
under 150 words. Stop after the link. No call to action unless there is a real one
("Issues and pull requests are welcome" is real for a repo, "Follow for more" is not).

**Instagram and Facebook captions.** Same order as a post, shorter. The first line is
all most people see before "more", so it carries the what and the when: "Resume review
night is Tuesday, Nov 18, 6–8 pm, in room 1300." Date, time and place as plain figures,
never "this week" or "soon". Links do not work in Instagram captions, so "Link in bio"
is a real call to action there and the only one. Hashtags zero to three, at the end.
When a set of scheduled captions is reviewed together, check they do not all open the
same way: a series that starts every post with "Join us" is its own tell.

**Slide text.** One claim per slide, with its number. Titles in sentence case with no
full stop. Bullets may be fragments but stay parallel in form. No three-word triads, no
"Key takeaways" slide that repeats the deck.

**Model listings.** As `references/surfaces.md`, with full standard mechanics. Title
says what it is plus the one differentiator, in sentence case: "Universal dice insert
for top-opening deck boxes, with or without a coin well". Summary is spec first. The
hard numbers in a blockquote. The trade-off as a number, then who it is not for. What
was not tested, in one first-person sentence. Tags in the tag field stay lowercase:
they are search terms, not prose.

**READMEs.** Name, version, one sentence on what it is. The spec or requirement before
anything else. How it works. A table for variants. Limits and who it is not for, above
the fold, not at the bottom.

**PR descriptions.** Four labeled lines, in full sentences: `What:` `Why:`
`Verified:` `Not verified:`. The last one is never dropped.

**Commit messages.** His shipped shape with a capital first letter: "Widen the slab by
1 mm: 66 -> 67". Imperative, no period, no conventional-commit prefix, subject only.

**Bios and about sections.** What he makes and where, with one concrete example. No
adjectives about himself ("passionate", "driven", "innovative").

## Workflow

1. Read the whole draft. Never rewrite from a summary of it.
2. Lint it: `python3 tools/voicecheck.py --pro <file>`, with the path taken from this
   skill's own folder. For pasted text, write it to a scratch file first. It catches
   the mechanical tells and nothing else. Where `references/private.md` exists (his
   machine only, never uploaded) it also greps for those private strings: exit 2 is a
   publish-blocker. Without it, anything shaped like an email, home path, IP or token
   is still flagged for review.
3. Content pass, sentence by sentence, as above. Check every claim against what was
   actually done.
4. Rewrite against "Correct, all of it" and "Not sounding like AI". The judgment calls
   are the ones that matter: the cost-and-who-it-isn't-for sentence, the first-person
   untested sentence, cutting a restating close, one name per thing.
5. Proofread the result as a copy editor would: spelling, capitals, apostrophes,
   complete sentences, consistent dates and numbers. Re-lint until clean, and read
   every `spelling` hit. No slip pass: nothing in this skill adds typos.
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

> A 100-card deck box is far deeper than the deck you keep in it. I made a
> 67 × 91 × 18.6 mm slab that fills the gap and holds your dice, with an optional well
> for a coin up to 38 mm.
>
> The cost: it takes about a quarter of the box's depth. If you fill your box to the
> brim, this isn't for you. Measure the inside of your box before you print.
>
> Fair warning: this exact size is untested. Mine was 66 × 88 mm. Measure first and
> you'll be fine, and the OpenSCAD source is there if your box needs different numbers.
>
> [link] #3DPrinting #MTG

What changed: the announcement opener and the closing bait are gone. "Robust",
"versatile", "seamlessly", "showcases" and "game-changing" became three numbers. "Many
users" had nobody behind it, so it went. The em dash and the "not just X" line went with
the claim they carried. The trade-off and the untested sentence were added, because a
draft that lists only upsides is the first thing to fix. Every sentence is complete,
capitalized and spelled correctly.
