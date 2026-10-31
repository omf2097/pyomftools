## `af` — hit freezes the opponent in stasis

When a hit from a frame carrying `af` lands, the opponent is not damaged: it is frozen in place
instead. It takes no damage and no stun, does not play its hit animation, is not knocked back, and the
hit does not count towards a combo. The frozen fighter stays on the frame and at the position it was
in, in mid-air if it was airborne, cannot move, attack or block, and is drawn with a translucent dark
tint. The attacker is still paid the move's points.

- The freeze lasts as many game ticks as the move's damage value, scaled by the attacker's `k` damage
  percentage (100 % by default). A move with damage 70 freezes for 70 ticks.
- A move with damage 0 never freezes anything.
- The freeze ends early when the frozen fighter is hit again. An ordinary hit or a throw releases it
  and does its full damage (the frozen fighter cannot block, which is what makes the freeze useful).
  A second `af` hit releases it without freezing it again, and also clears the stun it had built up.
- The hit itself works as usual up to the point of landing: an opponent that blocks it blocks it, and
  an opponent immune to the move's kind of attack (`zp` for a projectile) lets it pass.
- On any hit that lands, `af` also stops the opponent from being turned round to face the attacker
  when it was hit from behind: it keeps the way it was facing.
- `af` is checked on the frame that lands the hit, so put it on every frame that can hit. On a
  fighter's own move the game reads the frame from one tick earlier, so cover the frame before the hit
  frame too (or simply tag every frame of the move). For a launched projectile the hit frame itself
  counts.
- It has no effect in arena (BK) animations.

Shipped data: Chronos' stasis activator. His two stasis projectiles (moves 38 and 39, launched by
moves 18 and 23) carry `af` on every frame and have damage 70, so a hit freezes the opponent for 70
ticks. Shadow's scrap-move shadow images (moves 62 and 63) also carry `af` on their first frames, but
they do no damage and never hit anything, so there it has no effect.
