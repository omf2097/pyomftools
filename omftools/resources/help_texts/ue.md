## `ue` — ground shockwave hit

Replaces the normal hit test for this frame. Instead of checking whether the attack's sprite touches the
opponent, the game asks two things about the opponent: are they standing on the ground, and are they out
of hit-stun? If both hold, the hit connects at any distance, and it cannot be blocked. If the opponent is
airborne or still reeling, nothing happens this frame.

- The opponent must still be hittable in the usual sense (not in the damage or stand-up animation).
- Jumping is the only defence, which is what the tag is for: a ground slam that shakes the whole arena.
- The frame's own collision data is not used at all, and `n` has no effect on a `ue` frame.
- A hit landed this way records no impact point.
- Put it on each frame that should hit; the shipped ground slam uses three consecutive frames.
