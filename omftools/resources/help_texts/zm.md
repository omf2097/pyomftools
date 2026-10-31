## `zm` — medium-attack immunity

Makes the robot immune to medium attacks on this frame. A medium move that touches it does no damage,
causes no hit reaction and is not blocked; it simply passes through. The attack is not used up: if a
later frame of the same move still touches the robot after the immunity has ended, that frame hits.

- "Medium" means the move's category in the fighter file, not the height at which the blow lands on the
  sprite.
- Only medium moves are ignored. Low, high and jumping attacks, throws, projectiles and arena hazards
  still hit; use `zl`, `zh`, `zj`, `zg` or `zp` for those categories, or `zz` for everything.
- While it is shown, the opponent also cannot start a throw directly out of a medium attack (a chain
  that the medium move would have to allow with `jg`). Throws from standing, walking or crouching are
  not affected.
- Write it on every frame that should be immune; nothing carries over to the next frame.
- The immunity starts one tick after the frame starts and lasts one tick into the next frame.
- It only works in the robot's own animations (including a move's opponent string, which the victim
  plays). In a projectile's own string or an arena animation it does nothing.
- It is ignored while the robot is frozen by a stasis hit, on the same frame as `uh`, and against an
  opponent who is in the middle of a throw.

No shipped animation uses it.
