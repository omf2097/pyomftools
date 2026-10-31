## `ab` — ignore the walls

`ab` works differently in a fighter's own animation and in the animation of an object the fighter
launches.

**On a fighter**, `ab` lets the robot leave the arena: it is no longer held between the side walls
(x 20 to 300). Everything that normally happens at the wall is skipped along with the clamp: no wall-hit
sparks and no loss of speed when an airborne robot flies into the wall, and no push on the opponent when
the robot is blocking or getting hit in the corner.

- It lasts only while frames carrying `ab` are on screen, so put it on **every** frame that should be
  free of the walls.
- It takes effect one game tick late: a frame with `ab` frees the robot during the tick after the frame is
  shown. Likewise, the first tick after the last `ab` frame snaps the robot back inside the wall in one step.
- A wall-bounce reaction still triggers when the robot reaches the wall; only the snap back to the wall
  line is skipped.
- It does not affect the floor (see `ax`) and is not the same as `aw`, which keeps the robot's speed at the
  wall while the wall still stops it.

**On a launched object** (a projectile or anything else spawned with `m`), a single `ab` frame is enough
and it is permanent. From then on the object is not stopped, removed or bounced at the left and right
screen edges, does not land, bounce or vanish at the floor, and is not removed when it goes above the top
of the screen. The setting stays when the projectile turns into its follow-up animation, and objects it
launches afterwards inherit it.

- Arena (BK) animations never have edge handling to begin with, so `ab` does nothing there.

Shipped data: the impact animations that Jaguar's, Electra's and Chronos's projectiles turn into when
they end start with `ab`, so the impact plays out where the projectile reached the screen edge instead of
being pinned or bounced there. Chronos also uses it on every frame of one jump-category special. Shadow
has it on the single opening frame of one move, where it lasts only one tick.
