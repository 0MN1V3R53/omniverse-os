# 🎨 Canvas Engine & Visual FX Specifications

## 1. Core Visual Directives
The game must achieve the visual polish of industry leaders (**Yggdrasil**, **Pragmatic Play**, **Spribe**). It must evoke a dark mythical dragon sanctuary with glowing runes, molten lava tracks, and blazing particle effects.

### A. The Dragon Shooter (Central Avatar)
- **Design**: A golden/obsidian mythical dragon stationed at the center of the track.
- **Interactive Tracking**: Dragon's head, neck, and glowing maw smoothly track the player's mouse/pointer with dynamic angular interpolation (`lerp`).
- **Mouth Cannon**: The dragon holds the currently loaded fireball inside its jaws (with pulsating flame aura) and displays the *Next* ball on its head jewel / horns.
- **Fire Breath Animation**: Upon firing, the dragon undergoes recoil, expels an intense muzzle blast of sparks and smoke rings, and immediately feeds the next orb into position with a satisfying click.

### B. High-Fidelity Marble Track & Kinematics
- **Pathing**: Smooth cubic Bezier spline with custom winding tracks (coiling inwards towards the Dragon's Ancient Maw).
- **Marble Rendering**: Multi-layered radial gradients, specular highlights, internal elemental symbols (Flame, Ice, Poison, Sun, Void), outer glowing halos, and rolling rotational illusion as they move along the path.
- **Gap Snapping & Reverse Magnetism**: When a match occurs, separated train segments evaluate if the exposed end colors match. If yes, the trailing segment accelerates backward with a magnetic spark effect ("SNAP!"), triggering automatic cascading explosions.

### C. Particle & Screen FX Lab
- **Explosion Particles**: Rich burst of 25–40 particle embers per destroyed ball with velocity, gravity, alpha decay, and color-matched fire trails.
- **Screen Shake & Zoom Impulse**: Dynamic micro-screen shake on matches and intense cinematic camera rumble on Bomb explosions or Big Wins.
- **Floating Cash Text**: Vibrant bouncing "+$25.00 (x4 Combo!)" text rendered with glowing drop shadows and floating upward motion.
- **Dragon Pit Danger Indicator**: When marbles enter the last 20% of the track, the ancient dragon skull mouth glows fiery red with flashing alarm warnings and rising heat distortion!
