## `y<N>` — vertical sprite scale

Draws this frame's sprite at `N` percent of its height. `y50` is half as tall, `y100` (or no `y` at
all) is the normal height. Works in robot animations, projectiles and other spawned objects, and arena and other
background animations.

- Only the height changes. The width stays full: `x` does not widen or narrow anything, so `x50y50`
  looks the same as `y50`.
- The sprite shrinks or grows toward its anchor point, the point its sprite offset is measured from.
  For a robot that is its feet, so a squashed robot sinks toward the floor rather than toward its
  middle.
- Rows are placed, not resampled: each row of the picture is drawn once at its scaled height. Below
  100, rows land on top of each other and the lower row wins. Above 100 they spread apart with empty
  lines between them, so `y200` looks like the sprite drawn on every other line.
- `y0`, or a `y` with no number, flattens the sprite into a one-pixel strip on its anchor line.
- Only the lowest 8 bits of the number count, so values run 0-255 and wrap after that: `y256` is
  the same as `y0`, `y300` the same as `y44`.
- A sign after the letter makes a different tag: `y-N` and `y+N` move the object, `y=N` sets a
  position keyframe.
- Write it on every frame that should be scaled. Nothing carries over: the next frame without `y`
  is drawn at full height, even in the middle of a run of scaled frames.
- It does not change the robot's shadow, its position, its movement or where its attacks hit. The
  character-select screen always draws its animations at full size.

Shipped uses: none in the fighter files. Every arena uses it for its six announcement banners, which
grow from 10 % to 90 % of their height one tick at a time (`x10y10A1-x20y20A1-…-x90y90A1`), jump to
full height for the frame that plays its sound, then shrink back the same way.
