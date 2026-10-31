## `am` — walk to a destination

`am` makes the fighter walk to a point instead of moving the usual way. The frame works out a destination
from the other tags on it, turns the robot toward it, and the robot then walks there at its own walking
speed. The frame stays on screen (its time does not run down) until the robot arrives; on the tick it
arrives, the animation moves on to the next frame.

The destination is built from the other tags on the same frame:

- `g` puts the destination on the floor.
- `e` makes it the opponent's position, on the floor. The frame is re-read on every tick of the walk, so
  the robot follows an opponent that moves.
- `cf` makes it the far side of the arena from the opponent: 300 minus the `x+` amount when the opponent is
  in the left half, 20 plus the `x+` amount when it is in the right half.
- `x+N` / `x-N` (when `cf` has not used it) moves the destination N pixels in front of the opponent, toward
  the side the opponent faces. `y+N` / `y-N` moves it down / up by N pixels.
- With none of these there is no destination and no walk: the robot just turns to face left.

How the walk behaves:

- On this frame `x+`, `x-`, `y+`, `y-`, `v` and the `e` jump onto the opponent do not move the robot; they
  only shape the destination.
- The robot only steps while it is on the ground. In the air it rises and falls as usual and waits.
- It arrives when it is within 8 pixels of the destination both across and up/down, or as soon as it gets
  closer than 20 pixels to either side of the arena; it is then placed exactly on the destination. A
  destination that is not on the floor (no `g` or `e`) cannot be reached by walking, so the robot walks
  until it nears the side of the arena and is then placed there.
- On arrival, with `e` the robot turns to face against the opponent, and with `cf` it turns to face the
  nearer side of the arena.
- An overlay animation started with `bm` on the same frame is switched off on arrival. `bm10` (the robot's
  walking animation) therefore shows the walk cycle for exactly as long as the walk lasts.
- While it walks the robot does not turn itself toward the opponent.
- If the opponent is held by a grip (`ua`) after the round is over, it waits on its frame while the robot
  walks.
- It only affects fighters. In the animation of a launched object or in an arena (BK) file it does nothing.

Shipped data: the first frame of every scrap finisher except Gargoyle's starts with `bm10am`. Most add `e`
and an `x+` distance (`x+60` for Nova and Flail, `x+40` for Pyros, Katana and Chronos, `x+20` for Electra
and Shredder), so the robot walks up to stand that far in front of the opponent before the grab. Jaguar
and Thorn use no distance and stop on the opponent's own spot; Thorn walks a second time later in the move.
Shadow uses `cf` with `x+52` and `g` instead of `e`, walking away from the opponent to the far side of the
arena and ending with its back to it.
