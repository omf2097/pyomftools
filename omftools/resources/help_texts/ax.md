## `ax` — ignore the floor

`ax` takes the arena floor (y 190) away from the robot whose animation carries it. A robot that is
falling keeps falling: gravity goes on pulling it down past the floor line and out of the bottom of the
screen, and it never lands. Everything a landing normally does is skipped with it: the robot is not put
back on the floor, its speed is not stopped, there is no landing dust, sound or ground shake, and the
move **does not end**. Touching the floor normally ends the running move (the robot goes back to
standing, or follows a `cl` or `cg` instruction); under `ax` the animation simply carries on.

While `ax` is on, the robot also does not count as standing on the ground, even at floor level: it can
only start jump moves, the opponent cannot throw it, and hits treat it as airborne.

- It lasts only while frames carrying `ax` are on screen, so put it on **every** frame that should be
  floorless.
- It takes effect one game tick late: the frame frees the robot from the floor during the tick after the
  frame is shown.
- On the first tick after a frame without `ax`, a robot below the floor is put back on it. If it is still
  falling (1 pixel per tick or faster), that is a full landing and the move ends; if its vertical speed is
  zero (for example because `h` zeroed it), it is just lifted to the floor and the animation continues.
- It does not make a robot sink. A robot standing on the floor stays there; `ax` only stops the floor from
  catching a robot that is already moving down (after a `v` jump, under gravity, or moved by `y+`).
- Sliding still slows down below the floor exactly as it does on the ground.
- During a throw, a `y+` on the held robot's frame that would take it below the floor normally lifts the
  thrower instead; with `ax` the held robot goes below the floor and the thrower stays where it is.
- It has no effect on launched objects or in arena (BK) animations.

Shipped data: only the robots' own round-end finishing moves use it, always together with `be`. Jaguar,
Thorn, Electra and Shadow share one: the robot leaps, falls through the floor from the top of the arc and
out of the bottom of the screen, then loops blank frames so it never returns. Katana, Shredder and Flail
leap and dive through the floor the same way. Pyros and Gargoyle lift themselves far above the screen and
come down 20 pixels per tick on `ax` frames, so reaching the floor line does not end the move.
