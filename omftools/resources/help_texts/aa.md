## `aa` — air attack available again

A HAR gets one air attack per jump. Taking off arms an "air attack available" marker, and starting
any move uses it up. Once the first air attack is over and the HAR is falling in its normal jump
animation, it cannot start anything else until it lands. `aa` on any frame of a move re-arms the
marker. One frame is enough: the marker then stays on until the HAR starts its next move.

- **Attack again in the air.** When a move carrying `aa` ends while the HAR is still airborne, the HAR
  can start another jump-category move on the way down.
- **Chaining mid-move.** To cancel into a jump attack *during* the move, the same frame also needs `jj`
  (which allows jump-category follow-ups). `aajj` together is the usual idiom; `aa` alone only helps
  after the move ends.
- **Landing.** A HAR that lands having spent its air attack gives the opponent a moment (5 ticks) in
  which it cannot be thrown. Landing with the marker on, after a plain jump or an `aa` move, gives no
  such moment.
- **Computer opponent.** The AI treats an airborne HAR that has already used its attack, and has no
  marker, as harmless and presses its own attack.
- The marker is also used up when this HAR's attack hits (or is blocked, with `i`) and the HAR is
  switched into the attack's follow-up animation. Getting hit does not use it up.
- On a ground move `aa` has no visible effect: everything above needs the HAR to be in the air, and
  jumping arms the marker anyway.
- On an object spawned by a HAR (a projectile started with `m<N>`), `aa` instead lets the object hit
  once more from that frame on, like `q1` does for a HAR's own move. No shipped projectile uses it.

Shipped uses: Katana's upward-launching kicks (moves 25 and 28) end on a long airborne frame with
`aajj`, so a jump attack can follow; Shredder's flip kick (move 22, one of its alternate strings) puts
`aajj` on each airborne frame; Gargoyle's move 22 ends `aazjC1` so it can attack again after leaving
the ground; Katana's move 35 uses it once. Shredder's move 21 carries it on a ground move, where it
does nothing. No arena or menu file uses it.
