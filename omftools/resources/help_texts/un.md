## `un` — no corner push-back for this attack

When a fighter is pinned against an arena wall while blocking or taking damage, the game normally pushes
the *other* fighter back by the overlap, so nobody can be trapped in the corner. Blocked: the attacker
moves back by the full overlap. Hit, both grounded: half the overlap plus a little. Hit with one fighter
airborne (and the knock-down "rehit" option on): the attacker gets a recoil speed instead.

`un` on the attacking frame switches that push off. Use it on attacks whose hit box is not the attacker's
body, above all projectiles: without it, a fireball blocked in the corner would shove its thrower
backwards across the arena.

- Only the most recently shown frame of the attacking animation counts, so put `un` on **every** frame
  that can make contact. A frame without it turns the push back on.
- For a projectile it is the projectile's current frame that is checked, not the thrower's.
- It does not affect the cornered fighter's own wall clamp, the wall-hit sparks, or the separate push
  used during throws.
- No effect inside arena (BK) animations.
