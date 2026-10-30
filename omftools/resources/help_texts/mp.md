## `mp<N>` — spawn priority

Priority of the object spawned by this frame. The arena has 199 spawn slots; while one is free the
priority does nothing. When all are taken, the new object steals a slot: first the highest slot with a
lower priority, else the oldest slot with a priority not above its own, else it does not spawn.

- The stored priority is N modulo 16 (0–15). `mp0` or no tag means 10. A higher value both wins slots
  more easily and is harder to evict; it is also the sprite's draw-queue priority.
- The comparison uses the full byte but the store keeps only 0–15: `mp20` evicts anything but is then
  stored as 4, the easiest thing to evict. `mp15` is the strongest stable value; `mp16` stores as 0.
- `mp100`: before spawning, remove every object playing the same animation (used to replace a looping
  element in place). `mp101`: same, but only objects at the same position.
- `mp-1` in a **BK** string is not a spawn: it fills the arena's palette-remap range `[mx, my)` with the
  `m` value. In a fighter string `mp-1` is just a very high priority.
- `mp` does not set any of the object's behaviour flags (tracking, mirroring, screen-edge bounce,
  blending); those come from how it was spawned.
