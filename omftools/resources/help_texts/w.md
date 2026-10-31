## `w` — draw this frame behind

`w` sends the frame to the back of the draw order. Sprites are drawn in layers, higher layers in front of
lower ones, and `w` replaces the sprite's usual layer with a low fixed one. What that means depends on
whose animation carries it:

- **A fighter** is drawn behind the other fighter and behind the objects fighters launch (unless those
  carry `mn15` or lower), but still in front of most of the arena background. It wins over a bare `u` on
  the same frame. It lasts only for the frame it is on, so repeat it on every frame that should stay
  behind.
- **A launched object** (anything started with `m`, from a fighter or from an arena file) moves to the
  lowest object layer, the same as `mn1`: behind both fighters and every other object. This one sticks:
  the object stays at the back after the frame has passed, until a later frame carries `mn`. An `mn` on
  the same frame as `w` wins.
- **An arena background animation** (one the arena plays by itself, such as the wall-impact animations)
  is drawn at the very back for that frame instead of at its usual place.

Details:

- A fighter is also sent behind automatically, without any tag, while it is in its hit reaction or
  blocking, so the attacker is always drawn over the robot it hits. This is switched off while the
  opponent is still holding the fighter in a throw, and while the opponent is playing a scrap or
  destruction finisher. Those moves therefore use `w` by hand to choose, frame by frame, which robot is in
  front: in the attacker's own animation to put the attacker behind, or in the animation it hands its
  victim to put the victim behind.
- On a blank (`Z`) frame, the fighter also stays behind for the next frame that is shown.
- While the game is paused or a dialog is open, a fighter's `w` is ignored; the automatic drop while hit
  still applies, and objects and arena animations keep obeying `w`.
- `w` takes no number. Digits written right after it start an empty frame that swallows the rest of that
  frame's tags.
- `w` changes only drawing order. It does not move the sprite, change its size or affect hits.

Shipped data: over 500 uses, almost all in finishing moves, throws and victory poses, plus the Desert and
Power Plant arenas.

- Jaguar's scrap (move 25) carries `w` on every frame (`bm10amebewA1-bebxwA3-…`), so Jaguar is drawn
  behind the robot it is tearing apart.
- Katana's throw (move 33) puts Katana behind the thrown robot on every frame (`wA12-wB2-wC2-…`).
- Flail's throw (move 20) puts `w` in the animation the thrown robot plays, on the frames where it swings
  behind Flail (`ex-35C8-ewx-20C7-ewC6-…`).
- Electra's victory pose (move 48) and an effect her move 57 launches (move 58) both use it; the effect
  stays behind both fighters.
- In the Desert arena, the planes that fly over and the bombs they drop carry `w` on every frame to stay
  behind the fighters, and the wall-impact animations (20 and 21) of the Desert and Power Plant arenas
  use it to stay at the very back.
