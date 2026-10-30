## `mn<N>` — render layer of the spawned object

Sets the layer, 0–63, of every object spawned by the same frame (`m<N>` and friends). Higher layers
draw later and so appear in front. The fighters draw at 30 (player 1) and 31 (player 2), five higher
while staggered, at 60 under `u` and at 17 under `w`.

- No `mn` (or `mn0`) leaves the spawn on layer 27, just behind both fighters. `mn` ≤ 27 is behind both,
  `mn` ≥ 30 in front of both.
- The layer is a soft floor: if that slot is taken the object moves up to the next free one, so several
  objects on one layer draw in spawn order.
- Only the low 6 bits are kept: `mn64` is layer 0, `mn-1` is layer 63.
- `w` in the spawned object's *own* string forces it to layer 1 on each frame it appears.
- Works from a fighter string or from a spawned object's string. A BK scene animation that spawns with
  `m<N>` ignores `mn`; the new object's layer is N itself.
