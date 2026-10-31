## `ad` — turn around if the player holds back

`ad` lets the player turn the fighter around during a move. On every game tick the frame is on screen,
if the player is holding back (back, down-back or up-back, away from the way the robot faces), the robot
turns to face the other way. With any other direction, or nothing held, the frame does nothing. Where the
opponent is makes no difference.

- The game only re-reads the stick when the player's controls change (a direction or a button pressed or
  released). After `ad` has turned the robot, a stick that is still held the same way keeps counting as
  "back", even though it now points the way the robot faces.
- So on a frame that lasts one tick, holding back turns the robot once. On a frame that lasts several
  ticks, or on several `ad` frames in a row, holding back turns the robot on every tick: it flips back and
  forth and ends up facing the original way after an even number of ticks. The turn only sticks if the
  controls change during the frame, for example by pressing back during the frame rather than before it.
  Use one-tick `ad` frames.
- The frame is already drawn facing the new way, and movement on the same frame (`x+`, `x-`, and `v`
  speeds) goes in the new forward direction.
- The `ox` draw offset and any object launched with `m` on the same frame still use the facing the robot
  had before the turn.
- The facing stays after the frame ends, until the robot's normal turning takes over again: back on the
  ground in its standing, crouching, blocking or getting-up animation, at the start of a new move made on
  the ground, or when walking with the opponent behind it.
- On a frame that also has `ac` or `am`, those set the facing instead.
- It only affects fighters. In the animation of a launched object or in an arena (BK) file it does nothing.

Shipped data: only Katana uses it. The bounce after Katana's in-air down + kick connects has `ad` on a
one-tick frame, so holding back through the bounce turns Katana around. The rebound after another of
Katana's jumping kicks connects has it on a two-tick frame, so a steadily held back turns Katana and
turns it straight back again.
