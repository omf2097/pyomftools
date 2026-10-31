## `al` — no effect of its own: acts as `at` and cancels earlier `a` tags

`al` has no effect of its own. Writing it on a frame does three things, all to the frame's other `a`-family
tags:

- **It teleports the robot, exactly like `at`.** On every tick the frame is shown the fighter is moved
  sideways to a random spot just inside the left or right wall (by the last stick direction) or 40 pixels
  behind the opponent. Everything on the `at` page applies.
- **It cancels every `a`-family tag written before it on the same frame** (`ar`, `ad`, `ac`, `ai`, `aw`,
  `aa`, `ab`, `af`, `am`, `ao`, `as`, `ae`, `ax`). The same tags written after `al` work normally.
- **It makes some earlier tags on the frame act as `a` tags as well.** Each of these, written before `al`,
  keeps its own effect and also acts as the tag after the arrow: `us` → `ar`, `bn` → `af`, `ag` → `aa`,
  `ur` → `ai`, `ue` → `ac`, `ud` → `aw`, `uh` → `ad`, `uc` → `ab`, `ua` → `ao`, `ug` → `as`, `ul` → `ae`,
  `bo0` or `by` → `am`, `bk` → `ax`. `uz` and `uf` add nothing. Tags written after `al` are not copied.

Details:

- In the animation of a launched object or an arena (BK) file the teleport does nothing; only the
  cancelling and the copied tags that work on objects (`ar`, `aa`, `ab`, `ao`, `as`, `ae`) matter there.
- There is no reason to use `al`: write `at` for the teleport.
- The name suggests a separate effect was planned. The game has one waiting (on a hit, a move's follow-up
  animation would neither hit at once nor take over the opponent's animation), but nothing can switch it
  on, `al` included.

Shipped data: no animation in the game uses `al`.
