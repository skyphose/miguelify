# miguelify

a claude code skill that takes ai-drafted text and rewrites it so it reads like i wrote
it. it is a rewrite pass over assistant output, not a generator. the facts, numbers and
structure of the draft survive. the punctuation, the vocabulary, the register and the
honesty rules become mine.

i built it because my own published repos had quietly acquired a house style i never
chose. the readme for one of my 3d models had **56 em dashes** in it. i have typed
**zero** em dashes across 103 hand-written messages. nobody asked for them, they just
arrived, one draft at a time.

## how it works

four stages. the first and last are tools, the middle two are reading.

1. **scrape.** `tools/extract_voice_corpus.py` pulls my own typed messages out of my
   claude code transcripts, redacts anything private, and measures them: dash and emoji
   counts, spelling, how sentences start and end, how i case names like github and
   openscad, and a typo inventory sorted into the three classes i actually produce. it writes the numbers to `references/profile.json`
   and prints the drift since the last run. that file is tracked, so every rule can
   point at a measurement instead of a feeling.
2. **lint.** `tools/voicecheck.py` is a regex pass over the mechanical tells: em dashes,
   emoji, hype words, ai attribution, british spelling, title case headings. its messages
   quote the profile's numbers. it also greps for a list of private strings and will not
   pass a file, or a commit, that contains one.
3. **rewrite.** `SKILL.md`, applied by reading. open on the thing itself, put a number
   with a unit on every claim, hand the reader a test they can run, say who it is not
   for. `examples/coin-well.md` shows one section of a real readme before and after, and
   what the pass delliberately left alone.
4. **slip.** `tools/slipplan.py` proposes where deliberate typos go, drawing the class
   from the profile's weights and refusing any candidate that lands on a real word.

## what it actually changes

the rules are measured, not guessed. they come from two corpora: 103 messages i typed
by hand, and the repo text i have actually shipped and corrected. `references/voice.md`
has the counts and the quotes behind every rule.

four of them are absolutes, because the measured count was zero:

1. no em dashes. i write a spaced hyphen ` - `. 25 uses in the corpus, 0 em dashes.
2. no emoji. zero in everything i have typed or published.
3. no ai attribution in public repos. no co-authored-by trailer, no generated-with footer.
4. american spelling. "license", "color", "millimeter". the british forms leaked in from
   somewhere and they are not mine.

past that it enforces the things that are harder to count: open on the thing itself with
no throat-clearing, put real numbers with units on every claim, hand the reader a test
they can run, and say who the thing is **not** for before listing what it does well. that
last one is the most distinctive thing in my published writing and the first thing a
draft drops.

it also keeps my words. an ai draft formalizes as it goes: `repository`, `utilize`,
`approximately`, `the README file`. i type repo, use, about, readme, and the corpus
backs that up, make over create is 20 to 0. names go lowercase too, github, openscad,
pokemon, stl, mtg, because that is how i type them, 20 times out of 22. nothing gets
expanded, glossed or capitalized on the way out.

## the typos are on purpose

flawless prose is itself a tell. so the skill places deliberate typos at a rate of **one
per 200-400 words**, drawn from the three classes i actually produce: transposed adjacent
letters, an extra letter, a dropped letter.

there is one hard rule governing all of it. a slip is allowed only if it costs nothing to
read. `coonsequences` is fine, your eye fixes it before you notice. `form` for `from` is
not, because a real word gets accepted silently and the sentence has to be read twice.
across 1,398 words of my typing the scraper finds 19 typos, one per 74 words, and a hand
pass finds a few more it cannot see. **zero** of them are wrong-word errors, so the rule
matches how i actually mistype.

`tools/slipplan.py` picks the positions at random and refuses any candidate that lands on
a real word. placing them by hand produces predicatble, suspiciously cute typos.

slips never go in headings, code, commands, numbers, units, tags or commit subject lines.
they never go anywhere near a job application.

## install

```
git clone https://github.com/skyphose/miguelify ~/.claude/skills/miguelify
```

that is the whole install. claude code picks up skills from `~/.claude/skills/`. python 3
is the only dependency and the tools use the standard library plus `/usr/share/dict/words`.

## use

it is on demand only. it does not run on its own because a task happened to touch a
readme, and it should not be wired into a git hook or a ci step. ask for it:

```
/miguelify README.md
```

or just say "miguelify this" or "make this sound like me" with the text in front of it.

the tools can also be run directly:

| tool | what it does |
|---|---|
| `tools/voicecheck.py FILE...` | regex linter. flags em dashes, emoji, hype words, attribution, british spelling. exit 1 on findings, exit 2 on a private-string leak |
| `tools/voicecheck.py --tracked --git` | the pre-push check. every file git tracks, plus the author, committer and message of every commit on the branch |
| `tools/slipplan.py FILE` | proposes typo positions and candidates, refusing any that make a real word |
| `tools/extract_voice_corpus.py` | rebuilds the corpus from your own claude code transcripts, writes `references/profile.json`, prints the typo inventory and the drift since last time |

the linter is a floor, not a passing grade. it catches what can be counted. the judgment
calls, downgrading an unearned claim or cutting a conclusion that just restates the
document, still need a careful read.

## what it is not

this encodes **my** voice, measured from **my** writing. run it on your text and you will
get a document that sounds like me, which is probably not what you want.

it is also not a detector and not an attempt to defeat one. it is a style pass i run on
my own drafts before they go public, for my own reading experience.

## make it yours

the machinery is the reusable part and the rules are not. in order:

1. clone it and run `python3 tools/extract_voice_corpus.py`. it reads your own claude
   code tarnscripts and overwrites `references/profile.json` with your counts.
2. read the typo inventory it prints. anything that is your vocabulary rather than a slip
   goes in `references/jargon.txt`, one word per line. that file is your words and the
   tools protect it: nothing on it is counted as a typo, corrected, expanded or produced
   as a slip. rerun until the inventory is only real slips. on my corpus that took two
   passes and 25 words.
3. copy `references/private.example.md` to `references/private.md` and fill in the
   strings that must never leave your machine.
4. rewrite `SKILL.md` and `references/voice.md` against your numbers. if your em dash
   count is 40, the em dash rule is not yours. the tools do not care which rules you
   keep, they only supply the counts.
5. rename it. it is your voice now.

## status

a project i am working on, not a finished thing. as of 2026-09-14:

- **works.** the scrape with drift check, the linter with leak checking of files and git
  metadata, the slip planner with profile-driven class weights. two of my own documents
  have been through the full pass: a model listing and this readme.
- **rough.** the typo inventory misses substitutions and two-edit slips, so it counts
  about a third fewer than a hand pass. the rewrite step has no tool behind it. it is
  the skill's rules applied by reading, and i am not convinced it should be automated.
- **next.** run it over the dice-insert readme, which has 72 findings waiting. add a
  second corpus source, the commit messages i typed myself. write tests for the tools.

## private overlay

`references/private.md` is gitignored. it holds the strings that must never appear in a
public repo: home paths, internal hostnames, vpn ranges, afifliations, job-search files.
`voicecheck.py` reads it and greps every file for those strings, exiting 2 if it finds
one. with `--git` it also reads the author email and message of every commit on the
branch, because that is where the first real leak in this repo turned up: a commit
authored as `user@hostname.local` from a machine with no git email configured. if the
file is absent the rest of the linter still works and the leak check has nothing to look
for. if the file is ever committed the linter refuses to run at all.

`references/private.example.md` is the tracked template. copy it and fill in your own.
unfilled placeholders are ignored, so a fresh clone does not flag anything.

## license

mit. see `LICENSE`.
