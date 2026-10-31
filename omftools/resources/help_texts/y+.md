## `y+N` — move down N pixels per tick

Moves the object down by `N` pixels on **every tick** the frame is shown, so `y+5C3` moves it 15
pixels in total. Repeat the tag on each frame that should keep moving. `y+` and `y-` set the same value:
the last one in a frame wins, and `y+N` is simply `y-` with the sign flipped. There is no facing flip
on the vertical axis.

On a robot:

- On a normal frame the distance is scaled by the pilot's AGILITY, from about 0.8× at 0 to 1× at 10
  and about 1.3× at 25. `bh` turns the scaling off, and so do throws: it is off while the opponent is
  holding the robot, and while the robot plays a string forced on it by the opponent's hit.
- With `v` on the same frame the robot's speed is set instead: its vertical speed becomes `N` pixels
  per tick (AGILITY-scaled the same way) and is re-set on every tick of the frame, so the robot moves
  at that speed while the frame lasts and gravity takes over afterwards. In scrap, destruction and
  end-of-round victory animations the speed is `N` times the robot's gravity instead, with or without
  `bh`. A robot standing on the floor is also lifted one pixel. `h` on the same frame cancels the
  speed.
- `g` puts the robot on the floor first, so `gy+N` places it `N` pixels below the floor. `e` puts it
  on the opponent first, so `ey+N` places it `N` pixels below the opponent; throws use this in the
  string the victim plays.
- With `am` the robot does not move; the value becomes the height of the point it walks to.
- If a victim held in a throw is pushed below the floor, it is put back just above the floor and the
  thrower is raised by the difference instead (unless the frame has `ax`). A victim string `ey+40`
  lifts the thrower rather than burying the victim.
- Nothing happens while the robot is frozen by Chronos' stasis, on the held ticks of a combo hit
  pause, during a wall-bounce reaction, or while the game is paused by a dialog.

On a projectile or other spawned object `N` is plain pixels (applied after any `g` or `e`
placement); with `v` its vertical speed is set to `N`. A projectile that carries `mc` is scaled by its
robot's AGILITY from the tick after the `mc` frame. In a background animation that runs in place,
`y+N` lowers its drawn position by `N` every tick and the shift stays; inside a `y=` slide it only
lasts that tick.

`y+0` and a bare `y+` do nothing. A bare `y` with no sign is a different tag (vertical stretch).

Shipped uses (about 220, values 1–40, mostly `y+1` and `y+2`): Nova's jump move 34 pushes its fall
down 1, 2, 3, 4 and then 5 pixels a tick; Gargoyle's victory drops in from 300 pixels up with
`y+20` frames; Thorn's jump move 39 uses `vx+8y+6`; throw victim strings such as Gargoyle 36
(`earhx+35y+40…`) and Jaguar 22 (`ey+1x+58…`) place the victim under the thrower; Nova's projectile 36
falls in an arc with `y+1` … `y+4`; Shadow's shadow image (34) slides down 5 pixels a tick; the Fire
Pit's flame follow-up (ARENA3 animation 17) starts below the floor with `gey+20`.
