## `b` — no effect on its own

`b` is the first letter of many tags (`ba` to `bp`, `br` to `bu`, `bw` to `bz`, `b1`, `b2`). Written on its
own, with no recognised letter after it, it does nothing: the game skips the `b` and reads the rest of the
string exactly as if the `b` had been deleted. The frame looks and lasts the same.

Details:

- "No recognised letter" means an uppercase frame letter, a `-`, a digit other than `1` or `2`, the end
  of the string, or one of the two lowercase letters that start no `b` tag, `q` and `v`.
- Whatever follows keeps its own meaning. `bA2` is frame `A2`; `bq1` is the tag `q1` and `bv` is the tag
  `v`, the `b` does not swallow them.
- A digit or `-` straight after the `b` is still a trap, because it would be one without the `b` too:
  `b3A2-` reads as `3A2-`, a broken frame that makes frame `A2` disappear. The same goes for `b0` and
  `b4` to `b9`.
- `bp` followed by anything other than `b`, `d`, `f`, `n`, `o`, `p` or `s` is skipped the same way: both
  letters are ignored and reading carries on at the next character, so `bpB2` is just frame `B2`.
- There is never a reason to write a bare `b`. The shipped game has it only as leftover filler in front
  of frame letters: Shredder's close-range move 28 (`bA2-bpB2-bC2-bpD2-bE2-bD2-bC2-bB2-bA2`, which plays as
  `A2-B2-C2-D2-E2-D2-C2-B2-A2`) and the opponent's part of Pyros' close-range move 26 (`…bC4-bL5-M300`).
  Thorn's scrap finisher has two bare `bp` in the opponent's part. No arena or menu animation uses it.
