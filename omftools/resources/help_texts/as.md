## `as` — object wanders on a fixed looping path over the arena

`as` makes an arena object fly a smooth, looping path on its own. Every tick a frame with `as` is
showing, the object is placed on that path and its speed is set to zero, so its spawn position, speed
and gravity make no difference while `as` lasts.

- The path is two swings side to side and two up and down, added together. It is centred on screen
  point (160, 60) and reaches x 30-290 and y 0-120: nearly the full width of the screen and its upper
  part. Each swing repeats every 70-220 ticks and they do not line up, so the path does not visibly
  repeat. The object moves at most about 5-10 pixels per tick.
- The path follows the match's clock, which keeps running from round to round, so the orbs do not
  start over when a new round begins.
- Every object gets its own random number when it is spawned. It picks one of eight paces (the slowest
  is about half as fast as the fastest) and shifts the object along and across its path, so several
  objects launched together wander independently.
- The position given when the object is spawned (`mx` / `my`) is not used: the object is on its path
  from its first frame.

Put `as` on every frame. A frame without it leaves the object where it last was, at rest, and its own
movement (gravity, `cx` / `cy` drift) takes over from there. `x+` / `y+` on an `as` frame have no
effect. Two animations that both carry `as` can follow each other on the same object without a jump,
because the object keeps its random number.

`as` does nothing in a fighter's own move animation. It works on an object a fighter launches with `m`
too, though no fighter uses it.

Shipped data: the fire orbs of the Fire Pit arena. The arena's random background event (animation 0)
launches two orbs (`m15`). Animation 15 is the orb: it dissolves in, wanders and dissolves out, with
`as` on all eleven frames (`mn20mp12bf10asA2-bf60asA2-…-asA250-…-bf10asA2`). When a fighter's hit
registers on an orb, the orb switches to animation 16, a sound and a dissolve-out that also carries
`as` on every frame so the orb keeps to its path, and a damaging flame (animation 17) appears where
the orb was. No fighter file uses `as`.
