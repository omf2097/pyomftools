## `x+N` — move forward N pixels per tick

Moves the object forward by `N` pixels on **every tick** the frame is shown, so `x+4C5` moves it 20
pixels in total. Forward is the way the object faces: a robot facing left moves left. Repeat the tag on
each frame that should keep moving. `x+` and `x-` set the same value: the last one in a frame wins, and
`x+N` is simply `x-` with the sign flipped.

On a robot:

- On a normal frame the distance is scaled by the pilot's AGILITY, from about 0.67× at 0 to 1× at 10
  and 1.5× at 25. `bh` turns the scaling off, and so do throws: it is off while the opponent is
  holding the robot, and while the robot plays a string forced on it by the opponent's hit, so throw
  placements are exact.
- The direction follows the robot's facing at that moment, including a turn made on the same frame
  (`ad`, `ac`, `ar`). `e` puts the robot on the opponent and turns it to face the other way from the
  opponent, so in a victim string `ex+N` places the victim `N` pixels behind the thrower and `ex-N` in
  front of it; `earx+N` (with `ar` turning it back) places it `N` pixels in front.
- With `v` on the same frame the robot's speed is set instead: its horizontal speed becomes `N`
  pixels per tick forward and is re-set on every tick of the frame. It is AGILITY-scaled unless the
  frame has `bh`, also in throws and in scrap, destruction and victory animations. After the frame
  the speed carries on: it is kept in the air and slows by one pixel a tick on the floor. `h` on the
  same frame cancels it, and `bu` replaces it with a pull toward the middle of the arena.
- `h` without `v` stops the robot's own drift, so `hx+N` is a steady `N` pixels a tick; jump moves
  use this.
- With `am` the robot does not move; the value becomes the horizontal offset of the point it walks to,
  measured the way the opponent faces.
- Nothing happens while the robot is frozen by Chronos' stasis, on the held ticks of a combo hit
  pause, during a wall-bounce reaction, or while the game is paused by a dialog.

On a projectile or other spawned object `N` is plain pixels in the direction it was launched (the
robot's facing when it fired), even if the robot turns afterwards; with `v` its horizontal speed is set
to `N`. `bh` does nothing there, and `h` on the same frame does not cancel the `v` speed. A projectile
that carries `mc` is scaled by its robot's AGILITY from the tick after the `mc` frame. In a background
animation that runs in place, `x+N` moves its drawn position right by `N` every tick (there is no
facing) and the shift stays; inside an `x=` slide it only lasts that tick.

`x+0` and a bare `x+` do nothing. A bare `x` with no sign is a different tag (horizontal scale).

Shipped uses (about 1200, values 1–60, mostly `x+2` to `x+4`; no background file uses it): Jaguar's
jump move 15 drifts forward 1, 2, 5 … pixels a tick with `hx+N`, and the same move's alternative
string does it with `vx+N`; Nova's projectile 35 speeds up two pixels a tick per frame; Chronos'
projectile 38 does the same with `vx+5` … `vx+15`; Jaguar's throw 20 carries the victim from 35 pixels
in front to 32 behind with `egx-35` … `egx+32`; Gargoyle's throw 36 holds the victim in front with
`earhx+35` and throws it with `vx+10`; Electra's victory 38 slides forward with `vx+7`; Shredder's
scrap 34 walks to 20 pixels in front of the opponent with `amex+20`. In Gargoyle's throw 36 the frame
`hx+8-y-3D3` has a stray `-`, which makes the game drop that whole frame.
