## `zz` — invulnerable frame

Nothing can hit the robot while this frame is shown. The opponent's attacks pass through it whatever
kind of attack they are, projectiles and arena hazards miss it, a ground shockwave does nothing, and the
opponent cannot start a throw on it. The robot's own attacks are not affected and still connect.

- The hit is refused before blocking is considered, so the robot does not block either: no chip damage,
  no block reaction.
- It covers everything the other `z` tags cover (`zg`, `zl`, `zm`, `zh`, `zj`, `zp`) and more; it
  replaces any of them written earlier in the same frame.
- It lasts one frame. Write it on every frame that should be protected.
- The protection runs one tick behind the frame: the first tick of a move that opens with `zz` can still
  be hit, and the tick after the last `zz` frame is still protected.
- A throw that has already grabbed the robot still goes through.
- The robot's own `uh` cancels it.
- While the robot is frozen by a stasis hit (`af`), its `z` tags do nothing.
- It only works in a robot's own move strings, including an enemy string the opponent plays as its hit
  reaction. In a projectile's string, any other spawned object's string or an arena animation it does
  nothing.

Shipped uses: Katana's rising attacks (moves 22-24) are invulnerable for nearly all of their rising
frames, and Jaguar's leaping attacks (moves 15-17) for their first two frames. The enemy strings of
Jaguar's move 16, Thorn's move 16 and Shredder's move 38 use it on the first frames of the victim's
reaction, so the following hits of those multi-hit moves cannot land straight away. The game also adds
`zz` itself to the bounce after a hard landing and to the dizzy squash of a knocked-down robot.
