# miguelify

a claude code skill that takes ai-drafted text and rewrites it so it reads like i wrote
it. it is a rewrite pass over assistant output, not a generator. the facts, numbers and
structure of the draft survive. the punctuation, the register and the honesty rules
become mine.

i built it because my own published repos had quietly acquired a house style i never
chose. the readme for one of my 3d models had **56 em dashes** in it. i have typed
**zero** em dashes across 90 hand-written messages. nobody asked for them, they just
arrived, one draft at a time.

## what it actually changes

the rules are measured, not guessed. they come from two corpora: 90 messages i typed by
hand, and the repo text i have actually shipped and corrected. `references/voice.md` has
the counts and the quotes behind every rule.

four of them are absolutes, because the measured count was zero:

1. no em dashes. i write a spaced hyphen ` - `. 21 uses in the corpus, 0 em dashes.
2. no emoji. zero in everything i have typed or published.
3. no ai attribution in public repos. no co-authored-by trailer, no generated-with footer.
4. american spelling. "license", "color", "millimeter". the british forms leaked in from
   somewhere and they are not mine.

past that it enforces the things that are harder to count: open on the thing itself with
no throat-clearing, put real numbers with units on every claim, hand the reader a test
they can run, and say who the thing is **not** for before listing what it does well. that
last one is the most disstinctive thing in my published writing and the first thing a
draft drops.

## the typos are on purpose

flawless prose is itself a tell. so the skill places deliberate typos at a rate of **one
per 200-400 words**, drawn from the three classes i actually produce: transposed adjacent
letters, a dropped letter, a doubled letter.

there is one hard rule governing all of it. a slip is allowed only if it costs nothing to
read. `coonsequences` is fine, your eye fixes it before you notice. `form` for `from` is
not, because a real word gets accepted silently and the sentence has to be read twice.
across 1,226 words of my typing there are 25 typos and **zero** wrong-word errors, so the
rule matches how i actually mistype.

`tools/slipplan.py` picks the positions at random and refuses any candidate that lands on
a real word. placing them by hand produces predictable, suspiciously cute typos.

slips never go in headings, code, commands, numbers, units, tags or commit subject lines.
they never go anywhere near a job application.

## install

```
git clone <this repo> ~/.claude/skills/miguelify
```

that is the whole install. claude code picks up skills from `~/.claude/skills/`. python 3
is the only dependency and the tools use the standard library.

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
| `tools/slipplan.py FILE` | proposes typo positions and candidates, refusing any that make a real word |
| `tools/extract_voice_corpus.py` | rebuilds the corpus from your own claude code transcripts and prints the style counts |

the linter is a floor, not a passing grade. it catches what can be counted. the judgment
calls, donwgrading an unearned claim or cutting a conclusion that just restates the
document, still need a careful read.

## what it is not

this encodes **my** voice, measured from **my** writing. run it on your text and you will
get a document that sounds like me, which is probably not what you want.

if you want your own version, the machinery is the reusable part and the rules are not.
run `tools/extract_voice_corpus.py` against your own transcripts, read the counts it
prints, and rewrite `SKILL.md` and `references/voice.md` to match what you find. the em
dash count, the typo rate, the lowercase habit - all of those are measurements of one
person, and yours will come out different.

it is also not a detector and not an attempt to defeat one. it is a style pass i run on
my own drafts before they go public, for my own reading experience.

## private overlay

`references/private.md` is gitignored. it holds the strings that must never appear in a
public repo: home paths, internal hostnames, vpn ranges, affiliations, job-search files.
`voicecheck.py` reads it and greps every file for those strings, exiting 2 if it finds
one. if the file is absent the rest of the linter still works and the leak check just has
nothing to look for.

there is a template at the top of that file in my own cehckout. if you fork this, write
your own.

## license

mit. see `LICENSE`.
