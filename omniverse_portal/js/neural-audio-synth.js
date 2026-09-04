/* ==========================================================================
   OMNIVERSE TECH — NEURAL AUDIO DSP & SPATIAL SYNTHESIZER
   Discrete-Time WebAudio Synthesis for Action Potentials & Synaptic Blips
   ========================================================================== */

class NeuralAudioSynthesizer {
  constructor() {
    this.ctx = null;
    this.isMuted = true;
    this.masterGain = null;
    this.droneGain = null;
    this.droneOsc1 = null;
    this.droneOsc2 = null;
    this.lastPulseTime = 0;
  }

  init() {
    if (this.ctx) return;
    try {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      this.ctx = new AudioContext();
      this.masterGain = this.ctx.createGain();
      this.masterGain.gain.setValueAtTime(this.isMuted ? 0 : 0.45, this.ctx.currentTime);
      this.masterGain.connect(this.ctx.destination);
      this.initAmbientDrone();
    } catch (e) {
      console.warn("Web Audio not supported or blocked by autoplay policy", e);
    }
  }

  initAmbientDrone() {
    if (!this.ctx) return;
    // Sub-bass binaural cognitive carrier
    this.droneGain = this.ctx.createGain();
    this.droneGain.gain.setValueAtTime(0.04, this.ctx.currentTime);

    const filter = this.ctx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.setValueAtTime(140, this.ctx.currentTime);

    this.droneOsc1 = this.ctx.createOscillator();
    this.droneOsc1.type = 'sine';
    this.droneOsc1.frequency.setValueAtTime(55, this.ctx.currentTime); // A1 note

    this.droneOsc2 = this.ctx.createOscillator();
    this.droneOsc2.type = 'triangle';
    this.droneOsc2.frequency.setValueAtTime(59, this.ctx.currentTime); // 4Hz Theta beat

    this.droneOsc1.connect(filter);
    this.droneOsc2.connect(filter);
    filter.connect(this.droneGain);
    this.droneGain.connect(this.masterGain);

    this.droneOsc1.start();
    this.droneOsc2.start();
  }

  toggleAudio() {
    if (!this.ctx) {
      this.init();
      this.isMuted = false;
      if (this.ctx && this.ctx.state === 'suspended') {
        this.ctx.resume();
      }
      this.masterGain.gain.setValueAtTime(0.45, this.ctx.currentTime);
      return false; // Not muted
    }

    this.isMuted = !this.isMuted;
    if (this.ctx.state === 'suspended' && !this.isMuted) {
      this.ctx.resume();
    }

    const targetGain = this.isMuted ? 0.0 : 0.45;
    this.masterGain.gain.setTargetAtTime(targetGain, this.ctx.currentTime, 0.05);
    return this.isMuted;
  }

  playSynapseFiring(pitchFactor = 1.0, panX = 0) {
    if (!this.ctx || this.isMuted) return;
    const now = this.ctx.currentTime;
    if (now - this.lastPulseTime < 0.02) return; // Rate limiter for CPU & acoustics
    this.lastPulseTime = now;

    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    const panner = this.ctx.createStereoPanner ? this.ctx.createStereoPanner() : null;

    osc.type = 'sine';
    const baseFreq = (600 + Math.random() * 800) * pitchFactor;
    osc.frequency.setValueAtTime(baseFreq, now);
    osc.frequency.exponentialRampToValueAtTime(baseFreq * 0.4, now + 0.04);

    gain.gain.setValueAtTime(0.08, now);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.04);

    if (panner) {
      panner.pan.setValueAtTime(Math.max(-1, Math.min(1, panX)), now);
      osc.connect(gain);
      gain.connect(panner);
      panner.connect(this.masterGain);
    } else {
      osc.connect(gain);
      gain.connect(this.masterGain);
    }

    osc.start(now);
    osc.stop(now + 0.045);
  }

  playActionPotentialSurge() {
    if (!this.ctx || this.isMuted) return;
    const now = this.ctx.currentTime;

    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    const filter = this.ctx.createBiquadFilter();

    osc.type = 'sawtooth';
    filter.type = 'bandpass';
    filter.Q.setValueAtTime(6, now);

    osc.frequency.setValueAtTime(180, now);
    osc.frequency.exponentialRampToValueAtTime(1200, now + 0.35);

    filter.frequency.setValueAtTime(300, now);
    filter.frequency.exponentialRampToValueAtTime(3200, now + 0.35);

    gain.gain.setValueAtTime(0.001, now);
    gain.gain.linearRampToValueAtTime(0.18, now + 0.08);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.4);

    osc.connect(filter);
    filter.connect(gain);
    gain.connect(this.masterGain);

    osc.start(now);
    osc.stop(now + 0.42);
  }

  playLobeStimulation(baseHz = 330) {
    if (!this.ctx || this.isMuted) return;
    const now = this.ctx.currentTime;

    [1, 1.25, 1.5].forEach((interval, idx) => {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();

      osc.type = 'triangle';
      osc.frequency.setValueAtTime(baseHz * interval, now);
      osc.frequency.exponentialRampToValueAtTime(baseHz * interval * 1.5, now + 0.6);

      gain.gain.setValueAtTime(0.06 / (idx + 1), now);
      gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.65);

      osc.connect(gain);
      gain.connect(this.masterGain);

      osc.start(now + idx * 0.03);
      osc.stop(now + 0.7);
    });
  }

  playProbeSelection() {
    if (!this.ctx || this.isMuted) return;
    const now = this.ctx.currentTime;

    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();

    osc.type = 'sine';
    osc.frequency.setValueAtTime(880, now);
    osc.frequency.exponentialRampToValueAtTime(1760, now + 0.12);

    gain.gain.setValueAtTime(0.15, now);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.22);

    osc.connect(gain);
    gain.connect(this.masterGain);

    osc.start(now);
    osc.stop(now + 0.25);
  }
}

export const neuralAudio = new NeuralAudioSynthesizer();
