## `zg` — close-range immunity (does not stop throws)

Meant to make the robot immune to the close-range category, the category every throw belongs to. In
practice it does not protect against throws: a `zg` robot is thrown exactly like any other. The game
checks the immunity against the animation the *attacker* is playing at the moment of contact, and a
throw is never in its close-range animation at a moment that is checked.

- A ground throw is started from standing, walking or crouching, so the start-up check looks at the
  basic category, not the close-range one. Only `zz` keeps the opponent from starting a throw.
- An air grab or a grabbing special (Jaguar's air `P2`, Gargoyle's air `K2`, Flail's `K6565`, Thorn's
  `P656`) touches the opponent as a jumping or medium move and only then turns into its throw. `zj`
  or `zm` is what stops the grab.
- Once the throw is running, its hold on the victim ignores every immunity, and the throw's damage is
  dealt when the hold ends without any hit test.

What `zg` would stop, in a custom fighter:

- a close-range animation that still has hit frames after its throw hold has ended, when such a frame
  touches the robot;
- a throw started from inside another throw animation (allowed with `jg` or `jn` on the first throw's
  frame);
- a projectile or other spawned object whose animation is in the close-range category.

None of these happens with the stock fighters, so `zg` changes nothing there. Use `zz` on a frame
that must not be thrown.

- Write it on every frame that should be immune; nothing carries over to the next frame.
- It only works in the robot's own animations. In a projectile's own string or an arena animation it
  does nothing.
- It is ignored while the robot is frozen by a stasis hit and on the same frame as `uh`.

Shipped uses: none. No stock fighter or arena file uses `zg`.
