## `ar` — turn around

`ar` turns the robot around: facing right becomes facing left and the other way round. Nothing is checked
first, neither the controls nor where the opponent is.

- The turn is repeated on every game tick the frame is on screen. Put `ar` on a one-tick frame (`arA1`) to
  turn once. On a two-tick frame the robot turns and turns back; on a three-tick frame it ends up turned,
  with the sprite flipping every tick in between. While a robot is frozen by Chronos's stasis on an `ar`
  frame, it flips on every tick of the freeze.
- The frame is already drawn facing the new way, and movement on the same frame (`x+`, `x-`, `v` speeds)
  goes in the new forward direction.
- The `ox` draw offset and any object launched with `m` on the same frame still use the facing from before
  the turn.
- `ar` comes after `ad`, `ac` and `e` and before `am`: `am` sets the facing toward its target and wins.
  With `e`, which faces the robot away from where the opponent faces, `ar` turns it back, so `ear` means
  "stand on the opponent, facing the same way". Because `e` resets the facing every tick, `ear` works on
  frames of any length.
- The facing stays after the frame, until the robot's normal turning takes over. That can happen on the
  very next tick: if the player is holding the stick forward, back or diagonally down, and the opponent is
  now behind the robot, it turns back toward the opponent (not while throwing). Otherwise it turns back
  when it is on the ground in its standing, crouching, blocking or getting-up animation, or starts a new
  move on the ground.
- In the animation of a launched object, `ar` turns the object the same way (sprite and movement), every
  tick the frame shows. A launched object's animation starts at its second tick, so `ar` on a one-tick
  first frame never happens. Background animations in arena (BK) files ignore it.

Shipped data: Chronos and Katana each have a leaping kick that opens with `arA1`, turning away from the
opponent so the jump that follows goes the other way. One of Flail's throws turns Flail round on its last
tick. The opponent strings of Jaguar's, Thorn's and Gargoyle's throws turn the thrown robot round on a
one-tick frame near the end, and another Gargoyle throw uses `ear` to hold the victim in front of it facing the same
way. Shadow's shadow figure uses `ex-49ar` to appear 49 pixels behind the opponent's back.
