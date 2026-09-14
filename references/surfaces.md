# Per-surface rules

## Commit messages

Real examples he has shipped, capitalized as they were at the time. New subjects are
lowercase, by A/B on 2026-09-14, and otherwise keep exactly this shape:

```
Widen the slab by 1 mm: 66 -> 67
Take the slab's height from the sleeve, not the box: 88 -> 91 mm
Two variants on the slide version too: coin and no coin
Lint cleanup: add ruff, fix a Python 3.11 f-string bug, drop dead imports
Add the v1.0 print photos, with an index that says what they are
Remove per-page sys.path boilerplate; add tests/conftest.py
Parametric TCG deck-box insert: source, release bundle and docs
```

The pattern:

- Lowercase first letter, like everything else. No trailing period. "widen the slab by
  1 mm: 66 -> 67". Chosen by A/B on 2026-09-14 over the capitalized form he had shipped
  and over folding the reason into the subject.
- Scope or verb first, then a colon, then the specifics. Or just the change if it
  stands alone.
- Numeric deltas as `old -> new` with a plain ASCII arrow, never a Unicode one.
- Semicolons to join two related changes in one commit.
- No conventional-commit prefixes. He has never used `feat:`, `fix:` or `chore:`.
- No emoji, no trailers, no attribution lines.
- Subject only. A body is the exception, for when the why is genuinely not in the
  subject, and even then it is short prose, not bullets. Confirmed by A/B on 2026-09-14:
  offered a prose body and a bullet body for the sleeve-height commit, he took neither.

## PR descriptions

Four labeled lines, in this order, lowercase:

```
what: slab 67 x 91 mm, two variants (coin, no coin) replacing three game layouts.
why: the game names were a lie. nothing in either layout is game-specific.
verified: both export from openscad, a 38 mm coin fits the well in cad.
not verified: nothing printed at these dimensions.
```

- Chosen by A/B on 2026-09-14 over one prose paragraph carrying the same four parts and
  over a one-liner with only the caveat.
- The "not verified" line is never dropped. It is the same honesty rule as everywhere
  else, and it is the part a draft loses first.
- A line can run to two or three sentences. It cannot become a paragraph with a heading.
- No "Generated with Claude Code" footer, no session link.

## README

Order that matches his shipped README:

1. Project name, version, one sentence on what it is and where it lives.
2. A version note if there is a previous release, saying plainly what changed and
   whether the old one still works.
3. The spec or requirement a reader needs to know before they invest anything. For a
   physical model that is the fit spec. For software it is the runtime, dependencies
   and the one command that runs it.
4. How it works.
5. A table for variants, options or configuration.
6. Limits, trade-offs and who it is not for. Do not bury this at the bottom as a
   footnote. His README puts the "measure before you print" warning above the fold.

## Model listings (Printables / MakerWorld / Thingiverse)

- **Title**: what it is, plus the single differentiator, lowercase like everything else:
  "universal dice insert for top-opening deck boxes - with or without a coin well".
  Search on every model site is case-insensitive, so caps buy nothing there. Confirmed
  by A/B on 2026-09-14 over object-plus-a-number and over problem-first.
- **Summary**: spec first. The dimensions, then the variants, then what is included:
  "67 x 91 x 18.6 mm dice tray for top-opening deck boxes. two variants, coin well or
  not. openscad source included." Chosen by A/B on 2026-09-14 over a concrete one-liner
  and over problem-then-object. A reader who cannot fit it should find out in the first
  five words.
- **Description** opens on the problem in the reader's own terms, then names the object.
- A blockquote with the hard numbers, so it is skimmable.
- A "will it fit / will it work for me" section that gives the reader a measurement to
  take themselves.
- The trade-off as a number, then who it is not for, with no lead-in phrase: "the slab
  takes 18.6 mm of the 67.5 mm interior, about a quarter. if you fill a deck box to the
  brim, this isnt for you." Chosen by A/B on 2026-09-14. "be clear-eyed about the
  trade", which the shipped listing opens with, was rejected.
- What was not done, blunt and first person, one line where it applies: "untested at
  this size. i printed v1.0 at 66 x 88, not this one. measure first." Chosen by A/B on
  2026-09-14 over an inline third-person sentence and over a standing "note on claims"
  section. The note-on-claims form in the shipped LISTING.md is the older approach.
- Tags lowercase, unquoted, generous. Use his words: "deck box", "dice", "mtg", "tcg",
  not "trading card game accessory".
- Licence field: CC BY-NC-SA 4.0 has been his default on models. Confirm, do not assume.

## GitHub profile, bios, issue and PR replies

- Same voice, shorter. Plain, specific, no self-promotion adjectives.
- In replies, answer the question first, then context. Do not open with thanks-for-
  raising-this filler.
- If he does not know, the reply says he does not know.

## Anything about to be uploaded

Before publish, check the four non-negotiables in SKILL.md plus:

- No absolute home-directory paths (`/Users/<username>`, `/home/<username>`) in shipped
  files. Use `~`, `$HOME` or a repo-relative path.
- No email address unless he put it there deliberately.
- No internal hostnames, VPN or Tailscale IPs (`100.x.x.x`), LAN IPs or device addresses
  in public repos. The specific names to grep for are in `references/private.md`, which is
  untracked.
- No school or employer student, staff or program data in anything public. Named in
  `references/private.md`.

## Where slips go

The deliberate-typo rule in `SKILL.md` applies per surface. One slip per 200-400 words,
and only in running prose.

**Allowed**

- README body prose
- Model listing descriptions (the prose, not the spec blockquote)
- Issue and PR reply prose
- Release note prose
- Commit message bodies

**Never**

- Commit subject lines. They are read as a list, out of context, where a slip is noise.
- The fit spec, any number, any unit
- Tags and keywords. A misspelled tag costs search traffic.
- Identifiers, parameter names, commands, paths, URLs, licence names
- Headings
