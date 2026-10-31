## `ac` — turn to face the middle of the arena

`ac` turns the fighter toward the middle of the arena. A robot standing in the left half of the screen
(x below 160) turns to face right; a robot in the right half (x 160 or more) turns to face left. Where the
opponent is makes no difference.

- The turn happens on every game tick the frame is on screen, and the frame is already drawn facing the
  new way.
- Movement on the same frame (`x+`, `x-`, and `v` speeds) goes in the new forward direction, so
  `acx+30` moves the robot 30 pixels toward the middle.
- The `ox` draw offset and any object launched with `m` on the same frame still use the facing the robot
  had before the turn. Put them on the next frame if they should follow the new facing.
- The facing stays after the frame ends. The robot keeps facing the middle until its normal turning
  takes over again: back on the ground in its standing, crouching, blocking or getting-up animation, at the
  start of a new move made on the ground, or when the player holds a direction while the opponent is behind
  the robot.
- On a frame that also has `ad`, `ac` wins; on a frame that also has `am`, the `am` walk sets the facing
  toward its target instead.
- It only affects fighters. In the animation of a launched object or in an arena (BK) file it does nothing.

Shipped data: Thorn's air kick (kick with down-forward while jumping) opens with `acx+30`, turning
toward the middle and moving 30 pixels that way before the dive. Flail's two scrap moves turn toward the
middle on their second frame before walking forward with the opponent in tow. Shredder and Flail each have
a leap off the top of the screen that turns toward the middle on its take-off frame.
