## `us` — mark the opponent as scrapped (or destroyed) in a finishing move

`us` belongs in a robot's own scrap or destruction move. Every tick a frame carrying it is shown, the
opponent's pilot is marked:

- in a **scrap** move: *scrapped*;
- in a **destruction** move: *scrapped* and *destroyed*.

The mark does not depend on the move connecting; showing the frame is enough. It lasts until the next round
starts. In any other kind of move, in a launched object's animation and in an arena (BK) animation, `us`
does nothing.

What the marks do for the rest of the round:

- **Scrap first, then destroy.** At the end of the round a destruction move can only be started once the
  opponent is marked scrapped, unless it is the direct `jn` follow-up of the move being played. Put `us`
  on the scrap move before the frames that allow the destruction input (`jf2`).
- **No second scrap.** Against a scrapped opponent a scrap move can only be started as the `jn` follow-up of
  the scrap being played. Against a destroyed opponent no scrap or destruction move can be started at all.
  From the victory pose (move 48) nothing but a `jn` follow-up can be started once the opponent is
  scrapped.
- **The victim stays in your hands.** A scrapped robot is no longer let go early from the reaction your `ua`
  frames put it in, and when it lands below zero health it does not collapse into its defeat animation.
- **Fire Pit finishers.** The special follow-up moves that need a destroyed opponent (one each for every robot but Nova, only in
  the Fire Pit under its one-player conditions) become possible once the destruction's `us` has been shown.
  Shipped destructions put `us` on or before the frame that offers the follow-up, for example Thorn's
  `uabewusjn38N40`.
- **Score and tournament.** Player 1 scrapping or destroying a computer player 2 earns the round-end scrap
  bonus (twice as much for a destruction). In a tournament, the marks left after the fight decide whether
  challengers that require a scrap or a destruction become available, and destroying a secret challenger
  lets you take its robot enhancement if it is higher than yours.

Details:

- Written before `al` on the same frame, `us` also turns the robot round, as `ar` would.
- On the opponent's reaction string (the string your move makes the opponent play) `us` does nothing,
  because that string plays as the opponent's damage animation.

Shipped data: every robot puts `us` in at least one scrap move and one destruction move (for example
Jaguar's scrap marks at `bewusD20` and only then allows the destruction input at `uabejf2wF30`). Two Fire
Pit follow-ups (Shadow and Electra) and two reaction strings (Thorn's `usw30X1`, which is `us` followed by
`w30`, and Pyros') also carry it, where it has no effect. No arena file uses `us`.
