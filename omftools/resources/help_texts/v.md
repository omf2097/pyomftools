## `v` — velocity mode: x/y set the speed

Puts the frame in velocity mode. The frame's `x+N` / `x-N` and `y+N` / `y-N` amounts no longer move the
object; they **set** its speed, in pixels per tick. Both speeds are reset to zero first, so `v` replaces
the speed instead of adding to it, and a `v` frame without a `y` (or without an `x`) stops movement
along that direction. The frame is applied again on every tick it is shown, so while it lasts the
object moves at exactly that speed and gravity does not build up; when the frame ends the speed stays
and the normal physics take over. `vx+5y-7` launches the object forward at 5 and up at 7 pixels a
tick, and it keeps flying after the frame.

On a robot:

- Forward is the way the robot faces at that moment, including a turn on the same frame (`ad`, `ac`,
  `ar`, `e`). Both amounts are scaled by the pilot's AGILITY (about 0.67× at 0, 1× at 10, 1.5× at 25)
  unless the frame has `bh`. Unlike plain `x+` / `y+`, throws and victim strings keep the scaling, so
  `vx-5y-7` in an opponent string launches the victim by the victim's own AGILITY.
- In scrap and destruction moves, and in a victory pose once the round is over, the vertical amount is
  multiplied by the robot's falling speed instead, so `vy-10` there is a hop of about 20 ticks for every
  robot.
- A robot standing on the floor is lifted one pixel when the frame starts. With no downward `y` it
  hovers there for the whole frame, so the floor does not slow a `vx+N` slide while the frame lasts; when
  the frame ends it drops back and the landing stops the slide. With a downward `y` the robot touches
  the floor again within a tick or two and every landing stops it, so `vx+7y+1` on the floor hardly
  moves it.
- In the air the speed carries on after the frame until the robot lands.
- Nothing happens while the robot is frozen by Chronos' stasis or on a frame that also has `am`.
- `h` on the same frame cancels the speed again.
- With `bu` the horizontal speed becomes a drift toward the middle of the arena instead (without `v`,
  `bu` snaps the robot to the middle). The victory and destruction hops `vy-10bu…` use this to land
  the robot near the centre.

On a projectile or other launched object the speeds are the plain `x` / `y` amounts, `x` in the
direction it was launched (scaled by its robot's AGILITY only when its string has `mc`). `bh` does
nothing there, and `h` on the same frame does **not** cancel the speed. A background animation that
runs in place ignores `v`; its `x` / `y` just move it.

`v` takes no number. Writing `v` directly before `s` makes the game read `vsx` / `vsy` and lose the next
character, so put another tag between them.

Shipped uses (about 350): most jump, high, low and medium attacks knock the victim away with an opponent
string like Shadow's jump 34 `vx-5y-7…`, and the Danger Room and Fire Pit hazards do the same to the
robot they hit (`vx-5y-6…`); Katana's high 25 leaps with `vx+12y-9`; Chronos' projectile 38 speeds up
with `vx+5`, `vx+7`, `vx+9` …; Thorn's and Electra's victory poses hop to the centre with `vy-10bu`;
Electra's victory 38 starts with `vx+7y+1`; one alternative string of Shadow's move 26 uses a bare `v`
to stop the robot.
