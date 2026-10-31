## `x-N` — move backward N pixels per tick

Moves the object backward by `N` pixels on **every tick** the frame is shown, so `x-5A3` moves it 15
pixels in total. Backward is against the way the object faces: a robot facing right moves left. Repeat
the tag on each frame that should keep moving. `x-` and `x+` set the same value: the last one in a
frame wins, and `x-N` is simply `x+` with the sign flipped.

On a robot:

- On a normal frame the distance is scaled by the pilot's AGILITY, from about 0.67× at 0 to 1× at 10
  and 1.5× at 25. `bh` turns the scaling off, and so do throws: it is off while the opponent is
  holding the robot, and while the robot plays a string forced on it by the opponent's hit, so
  push-backs and throw placements in victim strings are exact.
- The direction follows the robot's facing at that moment, including a turn made on the same frame
  (`ad`, `ac`, `ar`). `e` puts the robot on the opponent and turns it to face the other way from the
  opponent, so in a victim string `ex-N` holds the victim `N` pixels in front of the thrower.
- With `v` on the same frame the robot's speed is set instead: its horizontal speed becomes `N`
  pixels per tick backward and is re-set on every tick of the frame. This is the knock-back:
  `vx-5y-7` on one tick throws a hit robot back and up into an arc. It is AGILITY-scaled unless the
  frame has `bh`, also in victim strings, where the victim's own AGILITY counts. After the frame the
  speed is kept in the air and slows by one pixel a tick on the floor. `h` on the same frame cancels
  it, and `bu` replaces it with a pull toward the middle of the arena.
- With `am` the robot does not move; the value moves the point it walks to.
- The arena walls stop the robot as usual unless the frame has `ab`. A victim pushed past a wall
  during a throw pushes the thrower back instead.
- Nothing happens while the robot is frozen by Chronos' stasis, on the held ticks of a combo hit
  pause, during a wall-bounce reaction, or while the game is paused by a dialog.

The string an arena hazard makes a robot play when it hits uses the same tag: the hazard strings in
ARENA1 and ARENA3 knock the robot back with `vx-5y-6`. The game also adds two `x-20` steps of its
own when a robot is knocked dizzy on the ground.

On a projectile or other spawned object `N` is plain pixels against the direction it was launched
(the robot's facing when it fired), even if the robot turns afterwards; with `v` its horizontal speed
is set to `N` backward. `bh` does nothing there. A projectile that carries `mc` is scaled by its
robot's AGILITY from the tick after the `mc` frame. In a background animation that runs in place,
`x-N` moves its drawn position left by `N` every tick (there is no facing) and the shift stays; inside
an `x=` slide it only lasts that tick.

`x-0` and a bare `x-` do nothing; `x-+5` moves forward 5, and `x-=…` is an `x=` keyframe. A bare `x`
with no sign is a different tag (horizontal scale).

Shipped uses (over 260, values 1–75 and one 435, mostly `x-1` to `x-6`): every robot's block spark
(animation 8) drifts away from the attacker with `x-5A3-x-3B2-x-2C1-x-1D1`; most jump, high, low and
medium attacks knock their victim back with an opponent string such as Shadow 34's `vx-5y-7…`;
throws and scrap moves hold the victim in front, as Electra's throw 42 (`ex-73` … `ex-75`, then
thrown away with `vx-5y-9`) and Flail's scrap moves 33 and 35 (`ex-50`); Shredder's projectile 38
flies out with `x+` and comes back with `x-5` … `x-12`; Electra's move 36 and Gargoyle's move 26 leap
backward with `vx-4y-10` and `vx-1y-2`; Chronos' move 25 vanishes and moves 435 pixels in one tick
with `bhx-435`, past the arena wall, held outside it by `ab` until the move ends.
