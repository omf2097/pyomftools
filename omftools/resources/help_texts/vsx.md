## `vsx` — same as `v` (velocity mode)

`vsx` does exactly what `v` does; the longer name changes nothing. On a frame carrying it, the frame's
`x+N` / `y+N` amounts stop moving the fighter directly and instead **set** its speed: the fighter is
launched forward (relative to the way it faces) and up or down by those amounts, and keeps travelling
after the frame ends, slowed by gravity and friction, until something else changes its speed. The `x` in
the name does not limit the effect to horizontal motion: the `y` amount on the same frame becomes the
vertical speed as well.

Details:

- Both speeds are reset to zero first, so a `vsx` frame without an `x` (or without a `y`) stops movement
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
- **Spelling trap:** the `x` belongs to the tag and is used up with it. `vsx+20` does not give a forward
  speed of 20: the `+20` left behind is not read as an `x` amount at all; the game takes it as the start of a frame marker instead. Write
  `vx+20` instead. Any letter other than `x` after `vs` gives `vsy`, which behaves the same.
- No animation in the shipped game uses `vsx` (or `vsy`); the resources always write `v`.
