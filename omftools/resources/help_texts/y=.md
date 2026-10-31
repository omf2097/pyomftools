## `y=N` — vertical position keyframe

Marks a vertical position for the object at the start of this frame and slides it in a straight line
to the value of the next `y=` in the same string, arriving exactly when that later keyframe's frame
starts. The look-ahead runs across frame markers and adds up their durations, so the next keyframe
can be many frames away. The last `y=` in a string simply puts the object at `N` and leaves it there.

What `N` means depends on where the string is used:

- In a background or arena animation that runs in place, `N` is the screen row the sprite is drawn
  at.
- In an object spawned by another background animation (with `m`), `N` is an offset from the point
  it was spawned at. Objects it spawns in turn are placed from that point, without the offset.
- In a robot's moves or projectiles it has no visible effect.

Things to know:

- `y=0` does not start a slide. Followed by another `y=` it does nothing at all, and the object stays
  where it was. Use `y=1` to slide in from the top edge.
- The first frame of a new slide is drawn one tick late: on its first tick the object is still at its
  previous height. A keyframe that ends a running slide has no such delay.
- Two copies of the same background animation on screen at once share one position and fight over
  it. Use separate animation numbers for objects that can overlap.
- In an animation that runs in place, `y-N` and `y+N` on a frame inside a slide only nudge the object
  for that tick; outside a slide the nudges add up.
- Two `y=` in one frame: the later one wins.
- Values are signed, so negative rows (above the screen) work: `y=-10`.
- `y-=N` is read as `y=N`; put the sign after the `=`.

Shipped uses: only in background files. The credits roll slides each line in from the top
(`y=1` to `y=100`) or up from the bottom (`y=200` to `y=100`) over 140 ticks, then holds it at 100.
One arena's hazard objects step through `y=1`, `y=5`, `y=10` … `y=62` and back to `y=-10`,
sinking from the top edge with growing speed and climbing back out.
