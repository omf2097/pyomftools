## `ur` — hold a blocking opponent in place

When an attack is blocked, the defender goes into a block animation whose length comes from the attack's
block-stun value, and the attack is spent (it may not connect again). On every later frame that carries
`ur`, if the attack is still touching a defender who is in that block animation, the defender's block
animation is rewound to its first frame. The block stun therefore lasts as long as `ur` frames keep
touching the blocker, instead of the fixed length.

- Nothing else happens on those frames: no new block, no extra chip damage, no push-back.
- The frame has to actually touch the opponent; the normal hit test triggers it. `ur` on a frame with
  `n` does nothing.
- Only a blocked attack sets this up. A landed hit puts the opponent in the damage animation, where `ur`
  is ignored.
- Typical use: long sweeps and charges that stay active for many frames.
