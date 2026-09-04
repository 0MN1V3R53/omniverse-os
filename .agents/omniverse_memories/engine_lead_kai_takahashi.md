# Engine Memory: Kai Takahashi (Principal Gameplay & Canvas Architect)

## Profile & Mandate
- **Role**: Principal Canvas & Gameplay Architect (Ex-PopCap & Spribe).
- **Specialty**: 60 FPS HTML5 Canvas kinematics, spline math, collision geometry, responsive touch/mouse controls.

## Kinematic Engine Specifications
- **Track Spline**: Parametric Cubic Bezier Curve array with pre-computed arc-length table for exact equidistant ball placement at constant linear speeds.
- **Marble Train Representation**: Linked-list / array of active balls with insertion, deletion, gap tracking, and reverse magnetic attraction for matching ends.
- **Shooter Kinematics**:
  - Dragon anchor at center `(cx, cy)`.
  - Mouse angle calculation: `atan2(mouseY - cy, mouseX - cx)`.
  - Smooth angle damping (`lerp`) for realistic dragon head turn speed.
  - Projectile trajectory: linear raycast collision against spherical hitboxes on the train.
  - Insertion physics: determines whether bullet hits left or right hemisphere of target ball, shifting the train dynamically.
