## `q<N>` — multi-hit counter

Every move may connect once. After it lands or is blocked, its hit boxes are ignored for the rest of
the move. `q<N>` declares "this frame belongs to hit number N of the move" (N is 1–15): it allows one
more hit to connect on this frame and on the following frames that carry the same `q<N>`. Once that hit
connects or is blocked, those frames are inert until a frame with a higher number opens the next hit.

- Chain the stages in order for a multi-hit move: `…q2cpF2-…q3cpB2-…q4cp…`.
- A stage does not need to connect to be used up. If the `q2` hit missed, `q3` still allows only one hit.
- `q1` is special: it re-opens the hit on *every* frame it appears on.
- All projectiles of the same move share one hit counter. Each new projectile starts with one hit, but
  the first one to connect uses it up for the others still in flight. Put `q1` on the projectile's frames
  so every copy can still hit.
- A projectile that touches the opponent turns into its successor animation, so `q1` does not make one
  projectile hit several times. Without a successor it keeps flying and can hit again on a `q1` frame.
- Each new stage also lets the hit-pause effect (`cp`) fire again.
- Repeat the tag on every frame it should apply to; it is read per frame.
- Values above 15 wrap around (only the low 4 bits are kept).

Related: `n` removes the hit boxes for a frame; `q` controls how many times the remaining boxes may
connect over the whole move.
