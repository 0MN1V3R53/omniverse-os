# CONTEXT 06: CYBERPUNK DESIGN SYSTEM & MULTI-THEME TOKENS

## 1. Theme Engine Architecture (`ThemeEngine.kt`)
The UI is built on Jetpack Compose with dynamic runtime theme swapping across 4 primary modes:
1. **`CYBERPUNK_NEON`**: High-contrast electric cyan (`#00FFE0`), neon magenta (`#FF007A`), deep void black (`#0A0A12`), and solar amber (`#FFB800`).
2. **`DARK_MOON`**: Obsidian black (`#050508`), midnight blue (`#0D1117`), luminescent silver (`#E6EDF3`), and icy blue (`#58A6FF`).
3. **`CYBER_SUNRISE`**: Deep twilight purple (`#1A0B2E`), radiant gold (`#FFAA00`), vibrant sunset orange (`#FF4500`), and neon rose (`#FF0055`).
4. **`CLASSIC_DARK`**: Matte dark grey (`#121212`), elevated slate (`#1E1E1E`), clean white typography (`#FFFFFF`), and muted accent blue (`#2196F3`).

## 2. Visual Style Guidelines
- **Glassmorphism**: Translucent panels with background blur (`Modifier.blur()`), subtle 1dp glowing borders, and rounded corners (16dp to 24dp).
- **Micro-Animations**: Smooth scale and alpha transitions during message send, swipe gestures, and crypto tipping modals.
- **Typography**: Clean, monospace and futuristic sans-serif scales for wallet addresses, transaction hashes, and chat bubbles.
