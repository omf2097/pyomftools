## `x=N` — horizontal position keyframe

Marks a horizontal position for the object at the start of this frame and slides it in a straight
line to the value of the next `x=` in the same string, arriving exactly when that later keyframe's
frame starts. The look-ahead runs across frame markers and adds up their durations, so the next
keyframe can be many frames away. The last `x=` in a string simply puts the object at `N` and leaves
it there. Repeating a value (`x=160 … x=160`) holds the object still between the two keyframes.

What `N` means depends on where the string is used:

- In a background or arena animation that runs in place, `N` is the screen column the sprite is
  drawn at.
- In an object spawned by another background animation (with `m`), `N` is an offset from the point
  it was spawned at. If the object is turned around (with `ar` or `e`, or because the object that
  spawned it was turned), the offset turns with it: `x=-30` then moves it 30 pixels the other way.
  Objects it spawns in turn are placed from its spawn point, without the offset.
- In a robot's moves or projectiles it has no visible effect.

Things to know:

- `x=0` does not start a slide. Followed by another `x=` it does nothing at all, and the object stays
  where it was. Use `x=1` to slide to or from the left edge.
- The first frame of a new slide is drawn one tick late: on its first tick the object is still at its
  previous position. A keyframe that ends a running slide has no such delay.
- Two copies of the same background animation on screen at once share one position and fight over
  it. Use separate animation numbers for objects that can overlap.
- In an animation that runs in place, `x-N` and `x+N` on a frame inside a slide only nudge the object
  for that tick; outside a slide the nudges add up.
- Two `x=` in one frame: the later one wins.
- Values are signed, so positions off the left edge work: `x=-250`.
- `x-=N` is read as `x=N`; put the sign after the `=`.
- An animation that loops without resetting its timer drifts on later passes; jump back with `d` as
  the shipped looping strings do.

Shipped uses: only in background files. The credits headers hold at the centre (`x=160`) and slide
off to the left (`x=1`) or right (`x=320`); the intro sends an object across the screen from `x=-250`
to `x=250`; an ending scene eases an object from `x=240` to the left edge with ever longer steps;
the versus screen walks a figure back and forth between its stops, flipping it with `r`; one
tournament-win screen slides the player's robot animation from `x=170` to `x=0`, another slides two
objects from `x=-140` and `x=140` to `x=0` over 20 seconds. In one arena two falling objects
fan out to the left and right (`x=-4` … `x=-110` and `x=4` … `x=110`) as they climb back out.
