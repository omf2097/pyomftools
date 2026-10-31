## `at` — teleport sideways, to a screen edge or behind the opponent

`at` moves the fighter horizontally in one jump. On every game tick the frame is on screen, the robot's
position across the arena is replaced by one of three places, picked from the direction the player's stick
reads:

- **Left** on screen (whichever way the robot faces): a random spot in the 30 pixels just inside the left
  wall.
- **Right** on screen: a random spot in the 30 pixels just inside the right wall.
- **Anything else** (nothing held, up, down, or any diagonal): 40 pixels behind the opponent, on the side
  their back is turned to.

Details:

- Only the position across the arena changes. Height, speed and facing stay as they were, so after
  landing behind the opponent the robot still has its back to them until it turns round in the usual way
  (for example at the start of its next move).
- The game only re-reads the stick when the player's controls change (a direction or a button pressed or
  released), so what counts is the last direction pressed or released before the frame.
- The computer player picks the place from the last input it fed in. For Chronos's teleport that is
  punch with no direction, so the computer normally reappears behind its opponent.
- The edge spots are always inside the walls. The spot behind the opponent can be outside them when the
  opponent stands near a wall with its back to it; the wall then pushes the robot back in on the next tick.
- The place is picked again on every tick the frame lasts: on a longer frame the edge spot jumps about
  inside its 30-pixel band and the spot behind the opponent follows them. Use a one-tick frame.
- `x+` / `x-` movement on the same frame is overwritten. `bu` on the same frame wins over `at` when no
  `v` movement is running and puts the robot in the middle of the arena. An `am` walk on the same frame
  starts from the new place.
- `al` also triggers this teleport.
- It only affects fighters. In the animation of a launched object or in an arena (BK) file it does nothing.

Shipped data: only Chronos uses it, in his teleport (down, then punch). The robot dissolves out over seven
one-tick frames, `at` sits on a one-tick blank frame, and the robot dissolves back in at the new place:
`…bf60zpA1-atZ1-bf30…`. Holding left or right during the move sends Chronos to that edge; otherwise he
reappears behind the opponent.
