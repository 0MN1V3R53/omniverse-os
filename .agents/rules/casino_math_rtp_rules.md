# 📊 Casino Math & RTP Specifications

## 1. Mathematical Objective & Framework
The mathematical engine must strictly follow real-money casino standards (GLI-19 certification level) ensuring an exact certified Return-To-Player (RTP) and transparent paytables.

### Target RTP
- **Target RTP**: **96.65%** (Base Game: 72.40%, Cascading Multipliers: 15.25%, Dragon Hoard Bonus Features: 9.00%).
- **House Edge**: **3.35%**.
- **Hit Frequency**: ~38.5% on marble matches, ~12.2% on multi-cascade combos.

## 2. Multiplier Ladder & Crash Mechanics (Aviator / Zuma Fusion)
- **Base Match Multipliers (3-of-a-kind)**:
  - 🔴 Ruby Fire Orb: 1.5x base multiplier
  - 🔵 Sapphire Frost Orb: 1.8x base multiplier
  - 🟢 Emerald Poison Orb: 2.2x base multiplier
  - 🟡 Topaz Sun Orb: 3.0x base multiplier
  - 🟣 Amethyst Void Orb: 5.0x base multiplier
- **Cascading Chain Reaction Combos**:
  - Combo 1 (Initial Match): 1.0x
  - Combo 2 (First Cascade / Gap Closure): 2.0x
  - Combo 3 (Second Cascade): 4.0x
  - Combo 4 (Third Cascade): 8.0x
  - Combo 5+ (Super Cascade): 16x -> 32x -> 64x
- **Aviator-Style Cash Out Mechanic**:
  - In Multiplier Rush mode, clearing balls charges the **Dragon Multiplier Gauge** (1.00x -> 50.00x+).
  - The player can hit **CASH OUT** at any millisecond before the chain reaches the Skull / Dragon Maw.
  - If the player clears 100% of the marble chain, an instant **+50x Dragon Slayer Jackpot Bonus** is unlocked!

## 3. Special Feature Orbs (Provably Distributed)
1. **Bomb Orb (🌋)**: Explodes a 120px radius on the track, clearing 6–10 balls and awarding an instant 3x explosion prize.
2. **Wild Rainbow Orb (🌈)**: Dynamically substitutes for any color to trigger immediate matching and gap closure.
3. **Lightning Chain Orb (⚡)**: Discharges electric arcs that disintegrate ALL balls of a matching color currently on the board.
4. **Frost Time Freeze Orb (❄️)**: Halts chain progression for 5.0 seconds and rewinds the train by 10%.
5. **Dragon Hoard Bonus Orb (👑)**: Triggers the 3-Chest Mini-Game or Free Fire Spins with guaranteed high-tier multipliers.
