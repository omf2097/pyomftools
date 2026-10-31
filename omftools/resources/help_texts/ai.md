## `ai` — hit launches the opponent into the air

A hit that lands while the attacker's frame carries `ai` launches the opponent. Instead of its
normal hit reaction, the opponent plays a fixed knock-down animation (`A1-s01l50B2-C2-L5-M400`,
which replaces the move's own opponent string), is thrown upward at 9 pixels per tick and backward
at 5 pixels per tick (both scaled by the opponent's own agility), and falls back down under
normal gravity. The long last frame `M` covers the fall.

- It only works on an opponent standing or crouching on the ground. If the opponent is already in
  the air when the hit lands (jumping, or knocked up earlier), the ordinary air knock-back is used
  instead, with its own animation and speeds.
- Throws and projectiles never launch, nor do blocked hits, nor hits from a move whose hitting
  frame carries `af` (the freeze replaces the whole hit reaction).
- The hit test sees the attacker's frame one tick late. A hit on the first tick of an `ai` frame
  only launches if the frame before it carries `ai` as well, and a hit on the first tick after
  the last `ai` frame still launches. Put `ai` on every hitting frame and on the frame just before
  the first one.
- A launched fighter cannot be hit again in the air unless the REHIT option is on. With REHIT on,
  air hits on it do more damage and stun, each move can hit it only once per launch, and the
  juggle ends when it first bounces off the floor. An `ai` on such a follow-up hit does not launch
  again, because the opponent is already in the air.
- The tag marks the fighter, not the move: while the fighter's frame carries `ai`, any other hit
  its opponent takes that is not a throw or a projectile also launches, such as a non-projectile
  object the fighter spawned or an arena hazard. In the shipped data this only happens by
  coincidence of timing.
- It has no effect in arena (BK) animations, nor in the animation of an object a fighter spawns.

Shipped data: 177 uses on ten moves, all on the attacks themselves. Nova's moves 32 and 33,
Chronos' moves 26 and 33, Jaguar's move 16, Thorn's move 16, Pyros' move 17 and Katana's moves 22,
23 and 24 (the last one started in the air) carry `ai` on their hitting frames, usually starting
one frame before the first hit, e.g. Nova 33 `A1-aiB3-aicpC4-njmB3-njmA2`.
