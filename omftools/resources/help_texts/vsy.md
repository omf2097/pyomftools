## `vsy` — same as `v` (velocity mode)

`vsy` does exactly what `v` does; the longer name changes nothing. On a frame carrying it, the frame's
`x+N` / `y+N` amounts stop moving the fighter directly and instead **set** its speed: the fighter is
launched forward (relative to the way it faces) and up or down by those amounts, and keeps travelling
after the frame ends, slowed by gravity and friction, until something else changes its speed. The `y` in
the name does not limit the effect to vertical motion.

Details:

- Both speeds are reset to zero first, so a `vsy` frame without an `x` (or without a `y`) stops movement
  along that direction. A fighter standing on the floor is also lifted by 1 pixel on each tick of the
  frame.
- The amounts are scaled by the fighter's agility unless `bh` is on the same frame. In scrap and
  destruction finishers (and in a victory pose once the round is over) the vertical amount is scaled by
  the fighter's falling speed instead.
- The frame is applied again on every tick it is shown, so a long frame holds the speed steady.
- Ignored while the fighter is frozen in stasis and on a frame that also carries `am`. An `h` on the same
  frame stops the fighter anyway. With `bu`, the fighter drifts toward the middle of the arena instead
  of jumping there.
- On a launched object (started with `m`), the frame sets the object's speed to the plain `x` / `y`
  amounts (agility-scaled only for objects marked with `mc`). On an arena background animation the tag
  does nothing.
- **Spelling trap:** after `v` the game only checks whether the next letter is `s`. If it is, three
  letters are used up, whatever the third one is: `vs` followed by any character counts as `vsy`, and
  that character is lost. Writing `v` directly before a sound tag (`vs21`) therefore loses the first digit
  of the sound number. Write plain `v`, and keep it away from a following `s`.
- No animation in the shipped game uses `vsy` (or `vsx`); the resources always write `v`.
