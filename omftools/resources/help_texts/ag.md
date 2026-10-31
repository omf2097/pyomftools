## `ag` — jump attack can be blocked holding either way

Normally a standing fighter blocks an opponent's jump attack only by holding the stick back, away
from the way it faces. While the attacker's current frame carries `ag`, holding the stick forward,
toward the attacker, blocks the attack too.

This is meant for moves that cross over the opponent or drop onto it from above. When the attacker
passes overhead the defender turns round, so "back" changes sides in the middle of the move, and a
player who reverses the stick at the wrong moment ends up holding the wrong way. With `ag`, either
horizontal direction works.

- It only matters while the fighter whose frame carries `ag` is doing a move of the jump category.
  On any other kind of move the frame does nothing.
- Only plain forward is added. Down-forward and up-forward still do not block, and a crouching
  fighter cannot block a jump attack at all: the defender must be standing (idle, walking, or
  already in its standing block).
- Holding back works as usual, from either side of the attacker.
- Put `ag` on every frame that should be blockable this way. The block test sees the attacker's
  frame one tick late, so the window starts and ends one tick after the tagged frames.
- It does not change damage, hit boxes or anything about the attacker; it only changes which stick
  direction counts as blocking for the opponent.
- It has no effect in arena (BK) animations, nor in a move that is launched as a separate object
  (a projectile or a shadow image).

Shipped data: Katana's airborne follow-up move 26 (after moves 25, 27 and 28) and move 35, Chronos'
move 25 (after moves 24 and 29) and Jaguar's move 39 carry `ag` on most of their frames. Shadow's
shadow-image moves 34, 37 and 39 also carry it, but they are launched as separate objects, so there
it does nothing.
