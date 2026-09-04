# ⚖️ iGaming Compliance, Provable Fairness & UX Rules

## 1. Regulatory Alignment (GLI-19 & MGA / UKGC Standards)
The game interface and state engine must incorporate the standard compliance and player-protection systems seen in tier-1 licensed casinos (Mr Green, Casumo):

### A. Provably Fair Verification System
- **Server Seed**: Cryptographically secure seed generated prior to round start.
- **Client Seed**: Player-customizable or timestamped entropy seed.
- **Nonce / Round ID**: Incremental integer tracking every shot and round.
- **Verification Modal**: Accessible directly from the UI header/footer, displaying the SHA-256 hash before the round and revealing the unhashed seed after the round for independent mathematical verification.

### B. Betting Engine & Game State Machine
- **Bet Controls**:
  - Quick Bet Selectors: $0.10, $0.50, $1.00, $2.00, $5.00, $10.00, $25.00, $100.00.
  - Min / Max / 2x / 0.5x quick modifier buttons.
  - Auto-Play Controls: Select 10, 25, 50, 100 auto rounds, with "Stop on Bonus" and "Stop on Single Win > $X".
  - Auto Cash-Out Selector: Pre-set multiplier target (e.g. 2.00x, 5.00x, 10.00x) that triggers instantaneous payout.
- **Dual Play Modes**:
  1. **Dragon Crash Multiplier (Aviator-Hybrid Mode)**: Place stake per round, multiplier surges as you clear marbles and string combos, cash out whenever you choose before the chain reaches the dragon maw!
  2. **Arcade Paytable Mode**: Classic pay-per-shot or round scoring with fixed paytable multipliers per color match and special orb bonuses.

### C. Responsible Gaming & Transparency UI
- **Live Session Clock**: Displays elapsed session duration in the top bar.
- **Balance & Profit/Loss Telemetry**: Real-time tracking of current balance, total wagered, total won, and net session profit.
- **Paytable & Help Drawer**: Fully transparent interactive modal detailing exact payout multipliers, special orb mechanics, RTP percentage (96.65%), and rule explanations.
- **Session History Log**: Real-time table displaying recent rounds, bet amounts, multipliers achieved, and cashout status.
