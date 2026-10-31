## `zj` — jumping-attack immunity

Makes the robot immune to jumping attacks on this frame, the usual anti-air trick. A jump attack
that touches it does no damage, causes no hit reaction and is not blocked; it simply passes through.
The attack is not used up: if a later frame of the same move still touches the robot after the
immunity has ended, that frame hits.

- "Jumping" means the move's category in the fighter file, not whether the attacker is in the air.
  In the stock fighters it covers every robot's jump kick and jump punch plus a number of specials.
  A robot that is only jumping, without attacking, is not affected.
- Air grabs count: Jaguar's, Gargoyle's and Flail's grabs from the air cannot catch a `zj` robot, and
  the grabbing move carries on as if it had missed. The same goes for Chronos's air move that turns
  into a follow-up attack on contact.
- Jumping projectile-style copies count too: the shadow copy Shadow sends out with his air move
  passes through a `zj` robot and keeps going.
- Only jumping attacks are ignored. Low, medium and high attacks, throws, projectiles and arena
  hazards still hit; use `zl`, `zm`, `zh`, `zg` or `zp` for those categories, or `zz` for
  everything.
- While it is shown, the opponent also cannot start a throw directly out of a jumping attack (a
  chain that the jump move would have to allow with `jg`). No stock move does this.
- Write it on every frame that should be immune; nothing carries over to the next frame.
- The immunity starts one tick after the frame starts and lasts one tick into the next frame.
- It only works in the robot's own animations (including a move's opponent string, which the victim
  plays). In a projectile's own string or an arena animation it does nothing.
- It is ignored while the robot is frozen by a stasis hit, on the same frame as `uh`, and against an
  opponent who is in the middle of a throw.

Shipped uses: Gargoyle's `P63` special has it on every frame, so the whole move goes under
jump-ins; Shredder's `K252` special has it, together with `zp`, on its first two frames; and Thorn's
`K63` jumping kick has it on one of its hitting frames, so an opposing jump attack cannot hit it back
there.
