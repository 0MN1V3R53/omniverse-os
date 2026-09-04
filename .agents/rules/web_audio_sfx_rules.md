# 🔊 Web Audio API Procedural SFX Specifications

## 1. Zero External Dependency Mandate
To ensure zero missing assets, zero network latency, and 100% offline reliability, all audio effects and ambient soundtracks MUST be dynamically generated using the native **Web Audio API** (`AudioContext`).

## 2. Synthesizer Sound Palette
- **Dragon Fire Shoot**: Noise buffer passed through a swept bandpass filter (2200Hz down to 200Hz) combined with a sine sub-kick (120Hz -> 40Hz) for physical punch.
- **Marble Clack / Ball Insertion**: High-Q resonant bandpass filter click at 1800Hz with exponential gain decay (0.04s) to simulate crystalline marble collisions.
- **Match Pop & Harmonic Chords**:
  - Combo 1 (Single Match): Pure Sine at 523.25 Hz (C5) + 659.25 Hz (E5) with bell shimmer.
  - Combo 2 (Cascade 2x): Major Triad at G5 (783.99 Hz) + C6 (1046.50 Hz).
  - Combo 3 (Cascade 4x): Seventh Chord with sparkling arpeggiator.
  - Combo 4+ (Mega Cascade): Radiant pentatonic burst with rising pitch envelope!
- **Cash Out / Win Ring**: Rapidly chiming dual triangle wave synthesizer replicating high-end casino coin showers.
- **Bomb Detonation**: Deep white noise explosion passed through lowpass filter with low-frequency oscillator (LFO) sub-bass rumble (35Hz).
- **Lightning Zap**: FM-synthesized sawtooth wave with rapid pitch jitter.
- **Ambient Dragon Lair Music**: Generative subtle drone using filtered sawtooth oscillators with slow LFO pulse and gentle crystal pentatonic chimes in the background.
- **User Audio Controls**: Volume slider, Mute toggle, and dynamic Web Audio unlock on first user click.
