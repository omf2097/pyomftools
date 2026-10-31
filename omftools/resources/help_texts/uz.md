## `uz` — launched object ends whenever its owner's attacks reach the opponent

`uz` marks a launched object (a projectile or other object a robot creates with `m`). Put it on a frame of
the object's own animation. Once a `uz` frame has been shown the object stays marked for the rest of its
life, and from then on, every time something of its owner's touches the opponent and the game checks that
hit, every marked object of that owner's is ended. That happens on:

- the owner's own attacks touching the opponent, whether blocked or not, and every tick of a throw the
  owner is performing;
- any of the owner's objects hitting the opponent, the marked object itself included;
- an arena hazard hitting the opponent.

"Ended" works the same way as when an object hits a wall:

- If the object's move has a follow-up animation, the object switches to it at once. It stays marked, so the
  next such hit ends the follow-up as well.
- If it has no follow-up, the object is only removed when its animation has already run out. In practice it
  keeps flying, and only loses the flip it was launched with.

Details:

- `uz` is the counterpart of `ud`, which ends the object when its owner is hit. An object can carry both.
- Nothing happens when the hit is turned away before it is checked: the attack's hit was already used up,
  the opponent was blocking after an `ur` move had used its hit, a hazard hit during the end-of-round
  countdown, or the opponent is immune to the object's kind of attack through a `z` tag.
- In a robot's own move animation `uz` does nothing. Objects started by an arena (BK) animation have no
  owner, so it does nothing there either.

Shipped data: used twice, in Shadow's animation 50 (a close-range throw stage). That animation can only be
reached from Shadow's animation 40, which nothing in the game starts, and it plays as a robot animation,
where `uz` has no effect. No arena file uses `uz`.
