# miguelify

a claude code skill that takes ai-drafted text and rewrites it so it reads like i wrote
it. its a rewrite pass over assistant output, not a generator. the facts, numbers and
structure of the draft survive. the punctuation, the vocabulary, the register and the
honesty rules become mine.

i built it because my own published repos had quietly picked up a house style i never
chose. the readme for one of my 3d models had 56 em dashes in it. ive typed zero em
dashes across 103 hand-written messages. nobody asked for them. they just arrived, one
draft at a time.

## how it works

four stages. the first and last are tools, the middle two are reading.

1. **scrape.** `tools/extract_voice_corpus.py` pulls my own typed messages out of my
   claude code transcripts, redacts anything private, and measures them. dash and emoji
   counts, spelling, apostrophes, sentence length, how i case names like github and
   openscad, and a typo inventory sorted into the three classes i actually produce. it
   writes the numbers to `references/profile.json` and prints the drift since the last
   run. that file is tracked, so every rule can point at a measurement instead of a
   feeling.
2. **lint.** `tools/voicecheck.py` is a regex pass over the mechanical tells: em dashes,
   emoji, hype words, ai attribution, british spelling, apostrophes in contractions, bold
   figures, long sentences. its messages quote the profile's numbers. it also greps for a
   list of private strings. a file or a commit with one in it doesnt pass.
3. **rewrite.** `SKILL.md`, applied by reading. open on the thing itself, put a number
   with a unit on every claim, hand the reader a test they can run, say who it isnt for.
   `examples/coin-well.md` shows one section of a real readme before and after, and what
   the pass delliberately left alone.
4. **slip.** `tools/slipplan.py` proposes where deliberate typos go, drawing the class
   from the profile's weights and refusing any candidate that lands on a real word.

## what it actually changes

the rules are measured, not guessed. they come from two corpora: 103 messages i typed by
hand, and the repo text ive actually shipped and corrected. `references/voice.md` has the
counts and the quotes behind every rule.

four of them are absolutes, because the measured count was zero:

1. no em dashes. i write a spaced hyphen ` - `. 25 uses in the corpus, 0 em dashes.
2. no emoji. zero in everything ive typed or published.
3. no ai attribution in public repos. no co-authored-by trailer, no generated-with footer.
4. american spelling. "license", "color", "millimeter". the british forms leaked in from
   somewhere and theyre not mine.

three more came out of A/B rounds. i get three variants of a real paragraph, i pick one,
the pick becomes the rule:

- contractions as i type them, with no apostrophe. dont, isnt, youre, lets. the corpus
  has 48 of those and 2 apostrophes.
- plain numbers. 67 x 91 x 18.6 mm, spaced units, no bold. zero bold anywhere in my
  typing.
- short sentences. fragments allowed. my median sentence is 11 words and a fifth of them
  are 5 words or fewer.

past that it enforces the things that are harder to count. open on the thing itself, no
throat-clearing. put real numbers with units on every claim. hand the reader a test they
can run. say who the thing is NOT for before listing what it does well. that last one is
the most dstinctive thing in my published writing and the first thing a draft drops.

it also keeps my words. an ai draft formalizes as it goes: `repository`, `utilize`,
`approximately`, `the README file`. i type repo, use, about, readme, and the corpus backs
that up, make over create is 20 to 0. names go lowercase too, github, openscad, pokemon,
stl, mtg, because thats how i type them, 20 times out of 22. nothing gets expanded,
glossed or capitalized on the way out.

## the typos are on purpose

flawless prose is itself a tell. so the skill places deliberate typos at a rate of one per
200-400 words. the three classes are the ones i actually produce: transposed adjacent
letters, an extra letter, a dropped letter.

one hard rule governs all of it. a slip is allowed only if it costs nothing to read.
`coonsequences` is fine, your eye fixes it before you notice. `form` for `from` isnt,
because a real word gets accepted silently and the sentence has to be read twice. across
1,398 words of my typing the scraper finds 19 typos, one per 74 words. a hand pass finds a
few more it cant see. zero of them are wrong-word errors, so the rule matches how i
actually mistype.

`tools/slipplan.py` picks the positions at random and refuses any candidate that lands on
a real word. placing them by hand produces predicatble, suspiciously cute typos.

slips never go in headings, code, commands, numbers, units, tags or commit subject lines.
when to run the pass at all is my call. some things should stay formal, and they just
dont get it.

## install

```
git clone https://github.com/skyphose/miguelify ~/.claude/skills/miguelify
```

thats the whole install. claude code picks up skills from `~/.claude/skills/`. python 3
is the only dependency. the tools use the standard library plus `/usr/share/dict/words`.

## use

its on demand only. it doesnt run on its own because a task happened to touch a readme,
and it shouldnt be wired into a git hook or a ci step. ask for it:

```
/miguelify README.md
```

or just say "miguelify this" or "make this sound like me" with the text in front of it.

the tools can also be run directly:

| tool | what it does |
|---|---|
| `tools/voicecheck.py FILE...` | regex linter. flags em dashes, emoji, hype words, attribution, british spelling, apostrophes, bold figures, long sentences. exit 1 on findings, exit 2 on a private-string leak |
| `tools/voicecheck.py --tracked --git` | the pre-push check. every file git tracks, plus the author, committer and message of every commit on the branch |
| `tools/slipplan.py FILE` | proposes typo positions and candidates, refusing any that make a real word |
| `tools/extract_voice_corpus.py` | rebuilds the corpus from your own claude code transcripts, writes `references/profile.json`, prints the typo inventory and the drift since last time |

the linter is a floor, not a passing grade. it catches what can be counted. the judgment
calls, downgrading an unearned claim or cutting a conclusion that just restates the
document, still need a careful read.

## what it isnt

this encodes MY voice, measured from my writing. run it on your text and youll get a
document that sounds like me, which is probably not what you want.

its also not a detector and not an attempt to defeat one. its a final proofreading pass
i run on my own drafts before they go public, for my own reading experience.

## make it yours

the machinery is the reusable part and the rules arent. in order:

1. clone it and run `python3 tools/extract_voice_corpus.py`. it reads your own claude
   code tarnscripts and overwrites `references/profile.json` with your counts.
2. read the typo inventory it prints. anything thats your vocabulary rather than a slip
   goes in `references/jargon.txt`, one word per line. that file is your words and the
   tools protect it: nothing on it gets counted as a typo, corrected, expanded or produced
   as a slip. rerun until the inventory is only real slips. on my corpus that took two
   passes and 25 words.
3. copy `references/private.example.md` to `references/private.md` and fill in the
   strings that must never leave your machine.
4. rewrite `SKILL.md` and `references/voice.md` against your numbers. if your em dash
   count is 40, the em dash rule isnt yours. the tools dont care which rules you keep,
   they only supply the counts.
5. rename it. its your voice now.

## status

a project im working on, not a finished thing. as of 2026-09-14:

- **works.** the scrape with drift check, the linter with leak checking of files and git
  metadata, the slip planner with profile-driven class weights. four A/B rounds to
  settle the rules the counts cant: 16 questions, 8 rule changes, 8 confirmations. two
  of my own documents have been through the full pass: a model listing and this readme.
- **rough.** the typo inventory misses substitutions and two-edit slips, so it counts
  about a third fewer than a hand pass. the rewrite step has no tool behind it. its the
  skill's rules applied by reading, and im not convinced it should be automated.
- **next.** run the dice-insert readme and listing through the current rules. the
  readme has 72 findings waiting and the listing was written before rounds 1 and 3. add
  a second corpus source, the commit messages i typed myself. write tests for the tools.

## private overlay

`references/private.md` is gitignored. it holds the strings that must never appear in a
public repo: home paths, internal hostnames, vpn ranges, afifliations, private project
names. `voicecheck.py` reads it and greps every file for those strings, exiting 2 if it
finds one. with `--git` it also reads the author email and message of every commit on the
branch. thats where the first real leak in this repo turned up: a commit authored as
`user@hostname.local` from a machine with no git email configured. if the file is absent
the rest of the linter still works and the leak check has nothing to look for. if the
file is ever committed the linter refuses to run at all.

`references/private.example.md` is the tracked template. copy it and fill in your own.
unfilled placeholders are ignored, so a fresh clone doesnt flag anything.

## license

mit. see `LICENSE`.
