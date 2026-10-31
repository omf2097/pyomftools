## `ae` — launched object ends without its follow-up animation

`ae` is for the animation of an object a fighter launches with `m` (a projectile, a flash, a trail). A
fighter's move can name a follow-up animation, and an object playing that move normally switches to the
follow-up when its own animation runs out (Jaguar's projectile, for example, switches to a second
animation when its flight ends). If any frame of the launched object's animation carries `ae`, the follow-up is skipped: when the
animation runs out, the object simply disappears.

- One `ae` frame is enough, and it can be any frame of the animation, the last one included. The
  setting stays with the object for the rest of its life.
- If the launched move has no follow-up (most of them), `ae` makes no difference: the object
  disappears at the end of its animation either way.
- It only changes what happens when the animation runs out. An object removed some other way (its `d`
  timer running out, leaving the screen or reaching the floor, an `mp100` / `mp101` clean-up, or an `m`
  delete) is handled as usual.
- It does not freeze the object on its last frame or keep it on screen.
- It does nothing in a fighter's own move, in an arena (BK) background animation, or in an object
  launched from a BK file's animations.

Shipped data: no animation uses `ae`. Launched objects that have a follow-up, where `ae` would make a
difference, exist for Jaguar, Shadow, Electra, Katana, Chronos and Nova.
