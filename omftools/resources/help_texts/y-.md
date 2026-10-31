## `y-N` — move up N pixels per tick

Moves the object up by `N` pixels on **every tick** the frame is shown, so `y-4C3` lifts it 12 pixels
in total. Repeat the tag on each frame that should keep moving. `y-` and `y+` set the same value: the
last one in a frame wins, and `y-N` is simply `y+` with the sign flipped. There is no facing flip on
the vertical axis.

On a robot:

- On a normal frame the distance is scaled by the pilot's AGILITY, from about 0.8× at 0 to 1× at 10
  and about 1.3× at 25. `bh` turns the scaling off, and so do throws: it is off while the opponent is
  holding the robot, and while the robot plays a string forced on it by the opponent's hit.
- Gravity keeps pulling while the frame lifts the robot, so a long `y-` frame rises less and less.
  Put `h` on the frame (`hy-2`) for a steady climb of `N` a tick.
- With `v` on the same frame the robot's speed is set instead: its vertical speed becomes `N` pixels
  per tick upward (AGILITY-scaled the same way) and is re-set on every tick of the frame, and gravity
  takes over afterwards. This is the launch: `vx-5y-7` on one tick throws the robot up and back into
  an arc. In scrap, destruction and end-of-round victory animations the speed is `N` times the
  robot's gravity instead, with or without `bh`. A robot standing on the floor is lifted one pixel so
  it leaves the ground. `h` on the same frame cancels the speed.
- `g` puts the robot on the floor first, so `gy-N` holds it `N` pixels above the floor. `e` puts it on
  the opponent first, so `ey-N` places it `N` pixels above the opponent; throws use this in the string
  the victim plays.
- With `am` the robot does not move; the value raises the point it walks to.
- There is no ceiling: large values send the robot off the top of the screen, and it falls back.
- Nothing happens while the robot is frozen by Chronos' stasis, on the held ticks of a combo hit
  pause, during a wall-bounce reaction, or while the game is paused by a dialog.

The string an arena hazard makes a robot play when it hits uses the same tag: the hazard strings in
ARENA1 and ARENA3 knock the robot up with `vx-5y-6`.

On a projectile or other spawned object `N` is plain pixels (applied after any `g` or `e`
placement); with `v` its vertical speed is set to `N` upward. A projectile that carries `mc` is scaled
by its robot's AGILITY from the tick after the `mc` frame. In a background animation that runs in
place, `y-N` raises its drawn position by `N` every tick and the shift stays; inside a `y=` slide it
only lasts that tick.

`y-0` and a bare `y-` do nothing; `y-+5` moves down 5. A bare `y` with no sign is a different tag
(vertical stretch).

Shipped uses (over 540, values 1–482, mostly `y-1` to `y-7`): many jump and high attacks
knock their victim into the air with an opponent string such as Shadow 34's `vx-5y-7…`; Katana's
move 25 leaps with `vx+12y-9`; Pyros' victory 40 rises 4, 6, 8, … pixels a tick with `hy-4`,
`hy-6`, …; Jaguar's victory 28 jumps with `vy-13`; Shadow's move 39 appears 184 pixels above the
floor with `egy-184…bh`; Gargoyle's victory starts 300 pixels up with `gy-300`; scrap and
destruction victim strings such as Jaguar 25 (`ey-47`, `ey-82`) hold the victim over the robot; Nova's
projectiles 25-29 are thrown upward with `vy-8` and similar; the Fire Pit's flame follow-up
(ARENA3 animation 17) rises 10 pixels a tick with `y-10`.
