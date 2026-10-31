## `zh` — high-attack immunity

Makes the robot immune to high attacks on this frame. A high attack that touches it does no damage,
causes no hit reaction and is not blocked; it simply passes through. The attack is not used up: if a
later frame of the same move still touches the robot after the immunity has ended, that frame hits.

- "High" means the move's category in the fighter file, not where the blow lands on the sprite. In
  the stock fighters it covers most robots' standing punch and their `P4` / `K4` moves, plus a number
  of specials. A robot that is only standing, walking or crouching is not affected.
- Moves that do no damage themselves count: Chronos's ground `K41`, which turns into a flying attack
  when it touches the opponent, cannot touch a `zh` robot and plays out as a miss.
- Shadow's high shadow copies count too: the copies sent out by his `P41` and `P252` specials pass
  through a `zh` robot and keep going. The `P252` copy turns into a medium attack when it connects;
  `zh` stops it before that happens, `zm` only stops the second stage.
- Only high attacks are ignored. Low, medium and jumping attacks, throws, projectiles and arena
  hazards still hit; use `zl`, `zm`, `zj` or `zp` for those categories (`zg` does not stop throws), or `zz` for
  everything.
- While it is shown, the opponent also cannot start a throw directly out of a high attack (a chain
  that the high move would have to allow with `jg`). No stock move does this.
- Write it on every frame that should be immune; nothing carries over to the next frame.
- The immunity starts one tick after the frame starts and lasts one tick into the next frame.
- It only works in the robot's own animations (including a move's opponent string, which the victim
  plays). In a projectile's own string or an arena animation it does nothing.
- It is ignored while the robot is frozen by a stasis hit, on the same frame as `uh`, and against an
  opponent who is in the middle of a throw.

Shipped uses: none. No stock fighter or arena file uses `zh`.
