# before and after: a listing full of wikipedia's ai tells

a model listing description for the dice insert, drafted the way a 2025-26 model drafts
one. the "before" was written for this example to plant one of each pattern from
[signs of ai writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). the
facts in the "after" are the real ones from the dice-insert readme and listing.

this file quotes the tells on purpose, so `voicecheck.py` skips it.

## before

```
# Coin Tray And Dice Insert

This insert serves as a compact home for your dice, marking a pivotal shift in how
players organize their decks.

The tray features two variants and boasts a 38 mm coin well, highlighting the attention
to detail that went into the design.

It's not a gimmick, but a genuine upgrade. Rather than replacing your deck box, it works
alongside it.

Additionally, the design has been featured in several hobby outlets and maintains an
active social media presence.

Many users report that it fits most boxes. Experts argue that a snug fit is crucial.

While specific details about tolerances are not widely documented, the fit should be
treated as approximate rather than guaranteed.

Despite its strengths, the insert faces several challenges. Despite these challenges, it
continues to thrive as a valuable tool for players.

- **Durability:** Strong, sturdy, and reliable.
- **Fit:** Snug, secure, and stable.

Overall, this insert is a testament to thoughtful, practical design that quietly makes
game night better.

I hope this helps! Let me know if you'd like a more detailed breakdown.
```

voicecheck: 18 checks fire, 35 hits. the linter before this pass found 7.

## content pass first

before touching a word, every sentence got the same question: would this still be true
of some other insert? if yes, either the real fact goes back or the sentence goes.

| sentence | true of any insert? | outcome |
|---|---|---|
| "compact home for your dice, marking a pivotal shift" | yes | replaced with the dimensions |
| "two variants ... 38 mm coin well, highlighting the attention to detail" | half | kept the facts, cut the analysis |
| "not a gimmick, but a genuine upgrade" | yes | cut. nobody said it was a gimmick |
| "rather than replacing your deck box" | yes | replaced with where it actually sits |
| "featured in several hobby outlets", "active social media presence" | yes, and unsourced | cut. there is no coverage to cite |
| "many users report it fits most boxes" | yes, and unsourced | replaced with the measurement a reader can take |
| "not widely documented ... should be treated as approximate" | yes | replaced with what was and wasnt printed |
| "faces several challenges ... continues to thrive" | yes | replaced with the actual cost, as a number |
| the bold-label bullets | yes | cut. "strong, sturdy, and reliable" has no figure |
| "Overall, ... a testament to" and "I hope this helps" | yes | cut |

about half the draft had nothing under it. that is normal, and it is the point of doing
this pass before the wording pass: rewording those sentences would have produced
plausible-sounding sentences that still say nothing.

## after

```
## dice insert for top-opening deck boxes - with or without a coin well

a 100+ capacity deck box is far deeper than the deck you keep in it. this is a slab that fills
the gap and holds your dice.

> 67 x 91 x 18.6 mm. two variants: coin well or not. the well is 38.8 mm and takes
> every official pokemon coin up to 38 mm. openscad source included.

## will it fit my box?

measure the inside of your box and compare it to 67 x 91 mm.

the slab takes 18.6 mm of the 67.5 mm interior, about a quarter. if you fill a deck box
to the brim, this isnt for you.

untested at this size. i printed v1.0 at 66 x 88, not this one. measure first.
```

## what changed, by pattern

| pattern | before | after |
|---|---|---|
| copula avoidance | serves as, features, boasts | is, two variants:, takes |
| legacy | marking a pivotal shift | gone |
| trailing -ing | highlighting the attention to detail | gone |
| negative parallelism | not a gimmick, but; rather than replacing | gone |
| notability | featured in several hobby outlets | gone, nothing to cite |
| vague attribution | many users report, experts argue | a measurement the reader takes |
| disclaimer | should be treated as approximate rather than guaranteed | untested at this size. i printed v1.0 at 66 x 88 |
| challenges formula | faces several challenges ... continues to thrive | the slab takes 18.6 mm of the 67.5 mm interior |
| rule of three | strong, sturdy, and reliable | gone |
| summary | Overall, ... a testament to | gone. it ends on the last real fact |
| chat leftover | I hope this helps | gone |
| title case, curly quotes | Coin Tray And Dice Insert | lowercase, straight |

## what did not change

- **the 38 mm coin well and the two variants.** those were the only facts in the draft
  and they survive.
- **the rhythm stays uneven on purpose.** sentence lengths in the after run from 2 to 15
  words, with a colon and a spaced hyphen. trimming every sentence to the same middle
  length would have traded the old tells for the 2026 one.
- **no slips.** about 110 words, under the 200-400 threshold, so the planner places none.
