## `aw` — rebound off the side walls into the move's follow-up

`aw` makes the side walls count like a hit for the move's follow-up. Every move can name a follow-up
animation, the one it switches to when it connects with the opponent (the move's "next animation"). While
the frame carries `aw`, a fighter that runs into the left or right wall switches to that same follow-up:
the arena's wall-impact animation plays, the follow-up starts from its first frame, and the robot is put
back on the wall line. A rolling or flying attack therefore bounces off the wall the way it bounces off the
opponent. It works on the ground and in the air, whichever way the robot faces.

The switch needs all of these on the game tick after the frame is shown:

- **The robot has moved past the wall.** The wall normally stops a fighter exactly on its edge, so the
  move itself has to push further: `x+` / `x-` steps on the frame, or sideways speed from `v`.
- **The move has a follow-up.** Without one, `aw` has nothing to switch to.
- **The opponent is still standing.** Once the finishing blow has landed, the wall no longer triggers
  anything.

Details:

- The follow-up keeps the speed the robot had; the switch does not stop or reverse it. Give the follow-up
  its own `v` to send the robot away. If it does not carry `aw` and keeps pushing into the wall before its
  `v` frame, the wall simply holds it there.
- In the air, `aw` also stops the wall from killing sideways speed. Without it a jumping fighter that hits
  a wall stops dead and drops. With it the robot is still held inside the wall and the impact still plays,
  but the speed is kept, so the next tick it presses on again and the follow-up starts. When no follow-up
  can start (none named, or the opponent is finished), the robot slides down the wall instead.
- It is not a pass-through: the walls still keep the robot in the arena. Use `ab` to cross a wall. With
  `ab` on the frame the robot also stays where the switch found it instead of being put back on the line.
- Keeping the speed in the air does not apply while the robot is in its hit reaction.
- It lasts only for the frame it is on. Repeat it on every frame of the move that should rebound.
- `al` copies the frame's `u…` tags into the `a…` group, so `ud` followed by `al` also turns on `aw`.
- It only affects fighters. In the animation of a launched object or in an arena (BK) file it does nothing.

Shipped data: Electra, Katana and Chronos use it, 121 times in all.

- Electra's rolling attacks (moves 34, 35 and 37) carry `aw` on every rolling frame
  (`…x+11iawugzpubD1-…`). Their follow-up is a back-flip away, so the roll rebounds off a wall just as it
  does off the opponent.
- Katana's jumping moves 25, 27 and 28 carry it on the airborne frames (`…awF1000`). A wall starts move 26,
  a flying kick back the other way; when that kick connects it chains to 27, which rebounds off the next
  wall into 26 again.
- Chronos's jumps (moves 24 and 29) carry it on the airborne frames; a wall starts move 25, in which he fades
  out, reappears and attacks.
