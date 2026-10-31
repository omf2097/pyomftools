## `x<N>` — horizontal sprite scale (no visible effect)

Meant to draw this frame's sprite at `N` percent of its width, the way `y` scales its height. In the
game it changes nothing you can see: sprites are always drawn at full width, whatever the number.

- `x50y50` looks exactly like `y50`, and `x50` on its own leaves the sprite unchanged. To make a
  sprite narrower, draw a narrower sprite.
- The default is 100. A value other than 100 only makes the game use a slower drawing routine for
  a plain sprite; the picture is the same.
- Only the lowest 8 bits of the number count (`x356` is `x100`), and an `x` with no number is 0.
- A sign after the letter makes a different tag: `x-N` and `x+N` move the object, `x=N` sets a
  position keyframe. Watch for typos: an `x` followed by another letter is this tag, not a move.
- Nothing carries over between frames, and it never affects position, movement, where attacks hit
  or the robot's shadow.

Shipped uses: every arena's six announcement banners pair it with `y`
(`x10y10A1-x20y20A1-…-x90y90A1`); the banners grow and shrink in height only. Two fighter strings
carry a stray `x` with no number (Shadow move 52, Nova move 50), which does nothing.
