## `ao` — launched object bounces off the screen sides and comes to rest on the floor

`ao` is for the animation of an object a fighter launches with `m`: thrown debris or a piece that should
fall, bounce about and then lie on the floor. One `ao` frame marks the object, and the mark stays with it
after that frame has passed. A marked object:

- **bounces off the screen sides.** At the left or right edge of the screen it is put back at the edge,
  its horizontal speed is reversed and a clank plays, louder the faster it was moving. Without `ao` it
  is held at the edge instead (or switches to its follow-up animation, if its move has one). The
  bounce repeats at every edge for as long as the mark lasts.
- **comes to rest on the floor.** When it reaches the floor slowly enough to settle (slower than about
  4 pixels per tick, or with no gravity), it is put on the floor, its gravity and speed are zeroed and
  the mark is used up. Then, if its move has a follow-up animation, the object switches to it and lies
  still where it landed; if not, its animation jumps to **tick 25** and carries on from there. So put
  the airborne frames before tick 25 (loop them with `d`) and the landed frames from tick 25 on.

A hard landing is not changed by `ao`: an object falling fast under gravity bounces back up at half
speed with a clank, with or without `ao`, until it is slow enough to settle. Without `ao`, an object
that settles is held on the floor line and keeps its speed; if its move has a follow-up it switches to
it, still moving.

- The floor part needs the object's floor handling to be on: every object a fighter launches with `m`
  has it, objects from arena (BK) files only with `mc`. The side bounce works only for objects launched
  by fighters. An `ab` frame turns both off for good, and then `ao` has nothing to do.
- An object playing an arena (BK) animation is only held on the floor line; it keeps its speed and the
  mark is never used up.
- An object launched by the marked object does not inherit the mark.
- `ao` does nothing in a fighter's own move animation.
- The game gives the same treatment to the scrap that flies off a robot when it is hit or when an
  `m12` frame plays: the pieces bounce off the sides, and when they settle their animation jumps to
  tick 25, where the spinning loop ends and the lying frame begins.

Shipped data: Nova's moves 25, 27 and 29, the three pieces Nova throws in move 47 (the defeat a
computer-controlled Nova plays when it loses the match). Each carries `ao` on its first frame
(`aovx+5y-8bwA2-…-d2J3`), spins until it settles, then switches to its follow-up (26, 28, 30, a single
long still frame) and lies on the floor. No arena (BK) file uses `ao`.
