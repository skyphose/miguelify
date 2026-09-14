# before and after: the coin well

one section of the README for [boulder-dice-insert](https://github.com/skyphose/boulder-dice-insert),
a 3D-printed deck box insert. the "before" is what shipped. the "after" is the same
section after miguelify. it is a worked example, not a template: the point is what
changed and, just as much, what did not.

this file quotes the tells on purpose, so `voicecheck.py` skips it.

## before, as shipped

```
**This was wrong for a long time and is worth recording.** The well was built around
`coin_d = 26.0`, a figure assumed rather than looked up. Official Pokémon coins actually run
**29.8–51.6 mm**. The common modern flip coin is the 34 mm "large"; the bigger authorised
collectible is 38 mm; 25 mm compact ones and 51 mm jumbos sit at the extremes. A 26.8 mm well
took only the smallest of them, so for most people the coin simply would not go in.

It is now built for **`coin_d = 38.0`** — a ⌀38.8 mm well, which swallows every size below it:
```

## after

```
**this was wrong for a long time and is worth recording.** the well was built around
`coin_d = 26.0`, a figure assumed rather than looked up. official Pokémon coins actually run
**29.8-51.6 mm**. the common modern flip coin is the 34 mm "large", the bigger authorized
collectible is 38 mm, and 25 mm compact ones and 51 mm jumbos sit at the extremes. a 26.8 mm
well took only the smallest of them, so for most people the coin simply would not go in.

it is now built for **`coin_d = 38.0`** - a ⌀38.8 mm well, which swallows every size below it:
```

## what changed

five edits, all mechanical:

| before | after | rule |
|---|---|---|
| `29.8–51.6 mm` (en dash) | `29.8-51.6 mm` | no em or en dashes, 0 in the corpus |
| `— a ⌀38.8 mm well` (em dash) | `- a ⌀38.8 mm well` | the aside keeps its shape, with the spaced hyphen that is actually typed |
| `"large"; the bigger ... 38 mm; 25 mm compact` | `"large", the bigger ... 38 mm, and 25 mm compact` | no semicolons, 0 in the corpus |
| `authorised` | `authorized` | american spelling |
| `The well`, `Official`, `It is now` | `the well`, `official`, `it is now` | lowercase running prose |

## what did not change

- **the hard numbers and their bold.** 29.8-51.6 mm, 34 mm, 38 mm, ⌀38.8 mm. the
  skill never touches a figure.
- **owning the mistake.** "this was wrong for a long time and is worth recording"
  survives word for word. that sentence is the most miguel thing in the section and
  a rewrite that softened it would have failed.
- **Pokémon** keeps its capital and its accent. proper nouns are not lowercased.
- **the code spans.** `coin_d = 26.0` and `coin_d = 38.0` are identifiers.
- **no slips.** the section is 118 words. at one per 200-400 the planner places
  nothing here, which is the expected result for most individual sections.

that last row is what makes the output read as occasional rather than sloppy. the
whole README this came from got 3 slips across 1,070 eligible words.
