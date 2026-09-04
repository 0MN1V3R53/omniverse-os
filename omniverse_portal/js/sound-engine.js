/* ==========================================================================
   OMNIVERSE TECH — WEBAUDIO DSP SOUND & SYNTHESIZER ENGINE
   Homage to Dr. Julian Vance (Stanford CCRMA Audio Systems & DSP Lead)
   ========================================================================== */

class OmniverseSoundEngine {
  constructor() {
    this.audioCtx = null;
    this.isEnabled = false;
    this.masterGain = null;
    this.initialized = false;
  }

  init() {
    if (this.initialized) return;
    try {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      this.audioCtx = new AudioContext();
      this.masterGain = this.audioCtx.createGain();
      this.masterGain.gain.setValueAtTime(0.15, this.audioCtx.currentTime);
      this.masterGain.connect(this.audioCtx.destination);
      this.initialized = true;
      this.isEnabled = true;
    } catch (e) {
      console.warn("WebAudio not supported or blocked:", e);
    }
  }

  toggle() {
    if (!this.initialized) {
      this.init();
      return true;
    }
    this.isEnabled = !this.isEnabled;
    if (this.audioCtx && this.audioCtx.state === 'suspended' && this.isEnabled) {
      this.audioCtx.resume();
    }
    if (this.isEnabled) {
      this.playChime();
    }
    return this.isEnabled;
  }

  playClick() {
    if (!this.isEnabled || !this.audioCtx) return;
    try {
      const now = this.audioCtx.currentTime;
      const osc = this.audioCtx.createOscillator();
      const gain = this.audioCtx.createGain();

      osc.type = 'sine';
      osc.frequency.setValueAtTime(1200, now);
      osc.frequency.exponentialRampToValueAtTime(300, now + 0.04);

      gain.gain.setValueAtTime(0.2, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.04);

      osc.connect(gain);
      gain.connect(this.masterGain);

      osc.start(now);
      osc.stop(now + 0.045);
    } catch (e) {}
  }

  playHover() {
    if (!this.isEnabled || !this.audioCtx) return;
    try {
      const now = this.audioCtx.currentTime;
      const osc = this.audioCtx.createOscillator();
      const gain = this.audioCtx.createGain();

      osc.type = 'triangle';
      osc.frequency.setValueAtTime(440, now);
      osc.frequency.linearRampToValueAtTime(580, now + 0.03);

      gain.gain.setValueAtTime(0.04, now);
      gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.03);

      osc.connect(gain);
      gain.connect(this.masterGain);

      osc.start(now);
      osc.stop(now + 0.035);
    } catch (e) {}
  }

  playChime() {
    if (!this.isEnabled || !this.audioCtx) return;
    try {
      const now = this.audioCtx.currentTime;
      const freqs = [523.25, 659.25, 783.99, 1046.50]; // C Major Chord (C5, E5, G5, C6)

      freqs.forEach((freq, idx) => {
        const osc = this.audioCtx.createOscillator();
        const gain = this.audioCtx.createGain();
        const startTime = now + idx * 0.05;

        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, startTime);

        gain.gain.setValueAtTime(0.12, startTime);
        gain.gain.exponentialRampToValueAtTime(0.0001, startTime + 0.35);

        osc.connect(gain);
        gain.connect(this.masterGain);

        osc.start(startTime);
        osc.stop(startTime + 0.36);
      });
    } catch (e) {}
  }

  playShockwave() {
    if (!this.isEnabled || !this.audioCtx) return;
    try {
      const now = this.audioCtx.currentTime;
      const osc = this.audioCtx.createOscillator();
      const gain = this.audioCtx.createGain();

      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(160, now);
      osc.frequency.exponentialRampToValueAtTime(40, now + 0.25);

      gain.gain.setValueAtTime(0.25, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.25);

      osc.connect(gain);
      gain.connect(this.masterGain);

      osc.start(now);
      osc.stop(now + 0.26);
    } catch (e) {}
  }
}

export const soundEngine = new OmniverseSoundEngine();
