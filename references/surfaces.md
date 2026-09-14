# Per-surface rules

## Commit messages

Real examples he has shipped:

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

- Sentence case. Capital first letter, no trailing period.
- Scope or verb first, then a colon, then the specifics. Or just the change if it
  stands alone.
- Numeric deltas as `old -> new` with a plain ASCII arrow, never a Unicode one.
- Semicolons to join two related changes in one commit.
- No conventional-commit prefixes. He has never used `feat:`, `fix:` or `chore:`.
- No emoji, no trailers, no attribution lines.
- Body paragraphs only when the why is not obvious from the subject.

## PR descriptions

- What changed, why, and what was actually verified.
- State what was **not** verified explicitly. This is the same honesty rule as
  everywhere else, and it is the part most likely to get dropped.
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

- **Title**: what it is, plus the single differentiator. "Universal Dice Insert for
  Top-Opening Deck Boxes - with or without a coin well".
- **Summary**: one or two lines, concrete. What it does, how many variants, whether the
  source is parametric.
- **Description** opens on the problem in the reader's own terms, then names the object.
- A blockquote with the hard numbers, so it is skimmable.
- A "will it fit / will it work for me" section that gives the reader a measurement to
  take themselves.
- An explicit trade-off paragraph.
- Tags lowercase, unquoted, generous.
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
- **Anything in the job search.** Resumes, cover letters, application answers, and
  anything else owned by the `job-apply` skill. No exceptions.
