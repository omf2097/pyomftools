## `zp` — projectile immunity

Makes the robot immune to projectiles on this frame. A projectile (fireball, missile, grenade and so on)
that touches it does no damage, causes no hit reaction and is not blocked; it simply passes through and
keeps flying, so it can still hit something else later.

- Only projectiles are ignored. Punches, kicks, throws and arena hazards still hit; use `zl`, `zm`, `zh`,
  `zj` or `zg` for those categories, or `zz` for everything.
- Write it on every frame that should be immune; nothing carries over to the next frame.
- The immunity starts one tick after the frame starts and lasts one tick into the next frame.
- It only works in the robot's own animations. In a projectile's own string it does nothing.
- It is ignored while the robot is frozen by a stasis hit, on the same frame as `uh`, and against an
  opponent who is in the middle of a throw.
- It also works in a move's opponent string: the victim's reaction then ignores further projectiles.

Shipped data uses it on special moves of Jaguar, Thorn, Pyros, Electra, Shredder, Flail and Chronos that
are meant to go through projectiles; Electra's carries it on every frame, Chronos's on the fade-out
frames before the robot vanishes. Nova's missiles and grenade put it in the opponent string, so a robot
hit by one is safe from further projectiles until the last frame of its reaction.
