# CONTEXT 12: GAMING, CASINO & INTERACTIVE 3D ARCHITECTURE

## 1. Provably Fair Cryptographic RNG Specification
Every game round MUST be verifiable by the player using standard HMAC-SHA256 provably fair cryptography:

$$\text{Hash} = \text{HMAC-SHA256}(\text{key} = \text{ServerSeed}, \text{msg} = \text{ClientSeed} + ":" + \text{Nonce} + ":" + \text{RoundId})$$

- **Server Seed**: Cryptographically secure 256-bit entropy generated via CSPRNG. Revealed to player only after the seed is rotated.
- **Server Seed Hash**: $\text{SHA-256}(\text{ServerSeed})$ published to the client *before* bets are placed.
- **Client Seed**: Player-controlled entropy (customizable string).
- **Nonce**: Incremental integer counter per bet under the active seed pair.
- **RNG Extraction**: Convert leading 8 hex characters (32 bits) of the HMAC hash to a float in range $[0, 1)$:
  $$\text{RandomFloat} = \frac{\text{HexToUInt32}(\text{Hash}[0..7])}{2^{32}}$$

---

## 2. Slot Engine Matrix & Mathematical Model
- **Grid Representation**: Matrix $R \times C$ (e.g. $5 \times 3$, $6 \times 4$, or dynamic Megaways $6 \times [2..7]$).
- **Reel Strip Arrays**: Weighted integer symbol ID arrays per reel column.
- **Payline Evaluation**:
  - Left-to-right matching against predefined line coordinate vectors.
  - Multiway (Ways to Win): $N_1 \times N_2 \times \dots \times N_k$ matching adjacent symbol occurrences.
  - Cluster Pays: Breadth-First Search (BFS) flood-fill finding connected symbol clusters ($S \ge 5$).
- **Theoretical RTP (Return to Player) Invariant**:
  $$\text{RTP} = \frac{\sum (\text{Payout}_i \times P_i)}{\text{Total Bet}} \times 100\% \quad (\text{Target: } 96.0\% - 97.5\%)$$
- **Precision Mandate**: All financial transactions and balance tracking must use integer cents / micro-units (e.g., `BigInt` or fixed-point integer math) to prevent IEEE-754 floating-point drift.

---

## 3. High-Performance 2D/3D Game Frontend Pipeline
- **Rendering Engines**: Pixi.js (for high-speed 2D canvas slot reels & particle fx) and Three.js / React Three Fiber (for 3D casino tables, dice, roulette wheels).
- **Frame Budget**: Enforce $\le 16.6\text{ms}$ per frame (steady 60 FPS target, zero garbage collection stutter).
- **Texture Atlas / Sprite Sheets**: Pack all symbol assets, win animations, and UI icons into unified WebP/AVIF sprite sheets via TexturePacker.
- **Audio & Visual Synch**: Decouple logic ticks from rendering ticks. Use Web Audio API for low-latency spin, stop, anticipation, and big-win audio cues.

---

## 4. Real-Time Multiplayer State Machine (WebSockets)
- **Live Games**: Blackjack, Roulette, Crash / Multiplier curves, Baccarat.
- **Server-Authoritative State Engine**:
  - `BETTING_OPEN` (timer countdown, client bet submissions)
  - `BETTING_CLOSED` (lock bets, compute provably fair outcome)
  - `ROUND_ACTIVE` (card dealing, wheel spin, or multiplier growth tick)
  - `ROUND_SETTLED` (atomic payout settlement, leaderboard broadcast)
- **State Serialization**: Protocol Buffers (Protobuf) or compact binary WebSockets for ultra-low latency sub-50ms round updates.
