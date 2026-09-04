/**
 * OMNIVERSE AETHER CREATION ENGINE — CLIENT CONTROLLER & AUDIO ENGINE
 * Port: 9999 | Localhost Studio Interface
 */

document.addEventListener('DOMContentLoaded', () => {
  // Global State
  const state = {
    voiceEnabled: true,
    agents: [],
    contexts: [],
    currentBriefing: '',
    audioCtx: null
  };

  // 1. Web Audio Synthesizer (432Hz / 110Hz Quantum Chimes)
  function initAudio() {
    if (!state.audioCtx) {
      state.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
  }

  function playCyberChime(freq = 432, duration = 0.35, type = 'sine') {
    try {
      initAudio();
      if (state.audioCtx.state === 'suspended') {
        state.audioCtx.resume();
      }
      const osc = state.audioCtx.createOscillator();
      const gain = state.audioCtx.createGain();
      
      osc.type = type;
      osc.frequency.setValueAtTime(freq, state.audioCtx.currentTime);
      
      // Smooth ADSR envelope
      gain.gain.setValueAtTime(0.01, state.audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.2, state.audioCtx.currentTime + 0.05);
      gain.gain.exponentialRampToValueAtTime(0.001, state.audioCtx.currentTime + duration);
      
      osc.connect(gain);
      gain.connect(state.audioCtx.destination);
      
      osc.start();
      osc.stop(state.audioCtx.currentTime + duration);
    } catch (e) {
      console.warn('[Audio] Synth fallback', e);
    }
  }

  function playEngageFanfare() {
    playCyberChime(110, 0.4, 'sawtooth');
    setTimeout(() => playCyberChime(220, 0.3, 'sine'), 100);
    setTimeout(() => playCyberChime(432, 0.5, 'triangle'), 200);
    setTimeout(() => playCyberChime(864, 0.6, 'sine'), 350);
  }

  // 2. Speech Synthesis Engine (Clinical & Authoritative AI Voice)
  function speakBriefing(text) {
    if (!state.voiceEnabled || !('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel(); // Stop any pending speech
    
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.05;
    utterance.pitch = 0.95;
    
    // Select best English voice
    const voices = window.speechSynthesis.getVoices();
    const preferredVoice = voices.find(v => v.lang.includes('en') && (v.name.includes('Google') || v.name.includes('Natural') || v.name.includes('Samantha') || v.name.includes('Daniel')));
    if (preferredVoice) {
      utterance.voice = preferredVoice;
    }
    
    window.speechSynthesis.speak(utterance);
  }

  // DOM Elements
  const voiceToggleBtn = document.getElementById('voiceToggleBtn');
  const voiceStatusText = document.getElementById('voiceStatusText');
  const sfxPingBtn = document.getElementById('sfxPingBtn');
  const engageEngineBtn = document.getElementById('engageEngineBtn');
  const directiveInput = document.getElementById('directiveInput');
  const creationModeSelect = document.getElementById('creationModeSelect');
  const podSelect = document.getElementById('podSelect');
  const outputCode = document.getElementById('outputCode');
  const outputTitle = document.getElementById('outputTitle');
  const prmBadge = document.getElementById('prmBadge');
  const voiceBriefingText = document.getElementById('voiceBriefingText');
  const speakOutputBtn = document.getElementById('speakOutputBtn');
  const copyOutputBtn = document.getElementById('copyOutputBtn');
  const downloadOutputBtn = document.getElementById('downloadOutputBtn');
  const agentSearchInput = document.getElementById('agentSearchInput');
  const agentsGrid = document.getElementById('agentsGrid');
  const contextSearchInput = document.getElementById('contextSearchInput');
  const contextsGrid = document.getElementById('contextsGrid');
  const runDreamSimBtn = document.getElementById('runDreamSimBtn');
  const dreamscapeCanvas = document.getElementById('dreamscapeCanvas');
  const dreamTelemetryList = document.getElementById('dreamTelemetryList');

  // Navigation Tab Switching
  document.querySelectorAll('.nav-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
      
      tab.classList.add('active');
      const target = tab.getAttribute('data-tab');
      document.getElementById(target).classList.add('active');
      playCyberChime(330, 0.15, 'sine');

      if (target === 'dreamscape-studio') {
        initDreamscapeCanvas();
      }
    });
  });

  // Voice Toggle Handler
  voiceToggleBtn.addEventListener('click', () => {
    state.voiceEnabled = !state.voiceEnabled;
    voiceStatusText.innerText = state.voiceEnabled ? 'VOICE: ON' : 'VOICE: OFF';
    voiceToggleBtn.style.borderColor = state.voiceEnabled ? 'var(--accent-cyan)' : 'var(--accent-red)';
    playCyberChime(state.voiceEnabled ? 528 : 220, 0.2);
  });

  // Manual SFX Ping
  sfxPingBtn.addEventListener('click', () => {
    playCyberChime(432, 0.4, 'sine');
  });

  // 3. Autonomous Creation Engine Dispatch
  engageEngineBtn.addEventListener('click', async () => {
    const prompt = directiveInput.value.trim() || 'Synthesize high-concurrency verified service architecture.';
    const mode = creationModeSelect.value;
    const pod = podSelect.value;

    engageEngineBtn.disabled = true;
    engageEngineBtn.innerHTML = '<span>⏳ COMPILING CONTEXT SANDWICH & PRM...</span>';
    playEngageFanfare();

    try {
      const res = await fetch('/api/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt, mode, pod })
      });
      const data = await res.json();

      if (data.success) {
        outputTitle.innerText = `📦 ${data.title}`;
        outputCode.innerText = data.output_code;
        prmBadge.innerText = `PRM: ${data.prm_score.toFixed(2)} (PASSED)`;
        prmBadge.style.color = 'var(--accent-green)';
        
        state.currentBriefing = data.voice_briefing;
        voiceBriefingText.innerText = data.voice_briefing;
        
        speakBriefing(data.voice_briefing);
        playCyberChime(880, 0.4, 'sine');
      }
    } catch (err) {
      outputCode.innerText = `// Error executing creation engine: ${err.message}`;
    } finally {
      engageEngineBtn.disabled = false;
      engageEngineBtn.innerHTML = '<span>⚡ ENGAGE OMNIVERSE CREATION ENGINE</span>';
    }
  });

  // Speak Output Manually
  speakOutputBtn.addEventListener('click', () => {
    if (state.currentBriefing) {
      speakBriefing(state.currentBriefing);
    }
  });

  // Copy Output
  copyOutputBtn.addEventListener('click', () => {
    navigator.clipboard.writeText(outputCode.innerText);
    copyOutputBtn.innerText = '✅ COPIED';
    setTimeout(() => copyOutputBtn.innerText = '📋 COPY', 2000);
    playCyberChime(660, 0.2);
  });

  // Export Deliverable File
  downloadOutputBtn.addEventListener('click', () => {
    const blob = new Blob([outputCode.innerText], { type: 'text/plain;charset=utf-8' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `omniverse_deliverable_${Date.now()}.txt`;
    a.click();
    playCyberChime(550, 0.2);
  });

  // 4. Fetch & Render 144 Agents Directory
  async function fetchAgents() {
    try {
      const res = await fetch('/api/agents');
      const data = await res.json();
      state.agents = data.agents || [];
      renderAgents(state.agents);
    } catch (e) {
      console.warn('Failed to load agents', e);
    }
  }

  function renderAgents(agentsList) {
    agentsGrid.innerHTML = '';
    agentsList.forEach(a => {
      const card = document.createElement('div');
      card.className = 'agent-card';
      card.innerHTML = `
        <h4>${a.name}</h4>
        <div class="agent-role">${a.role}</div>
        <div class="agent-meta">
          <span>${a.level}</span>
          <span style="color:var(--accent-purple);font-weight:700;">${a.mbti}</span>
        </div>
      `;
      card.addEventListener('click', () => {
        directiveInput.value = `Pairing with ${a.name} (${a.role}): Please execute task according to ${a.mbti} temperament and PRM standards.`;
        document.querySelector('[data-tab="creation-forge"]').click();
        playCyberChime(440, 0.2);
      });
      agentsGrid.appendChild(card);
    });
  }

  agentSearchInput.addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase();
    const filtered = state.agents.filter(a => 
      a.name.toLowerCase().includes(query) || 
      a.role.toLowerCase().includes(query) ||
      a.mbti.toLowerCase().includes(query) ||
      a.department.toLowerCase().includes(query)
    );
    renderAgents(filtered);
  });

  // 5. Fetch & Render 23 Context Blueprints
  async function fetchContexts() {
    try {
      const res = await fetch('/api/contexts');
      const data = await res.json();
      state.contexts = data.contexts || [];
      renderContexts(state.contexts);
    } catch (e) {
      console.warn('Failed to load contexts', e);
    }
  }

  function renderContexts(contextsList) {
    contextsGrid.innerHTML = '';
    contextsList.forEach(c => {
      const card = document.createElement('div');
      card.className = 'context-card';
      card.innerHTML = `
        <h4>${c.title}</h4>
        <div class="agent-role">${c.filename}</div>
        <div class="agent-meta">
          <span>${(c.size_bytes / 1024).toFixed(1)} KB</span>
          <span style="color:var(--accent-green);font-weight:700;">WORM PREFIX</span>
        </div>
      `;
      card.addEventListener('click', () => {
        directiveInput.value = `Binding context blueprint: ${c.filename}\nDirective: Synthesize architectural module implementing all specifications in ${c.title}.`;
        document.querySelector('[data-tab="creation-forge"]').click();
        playCyberChime(550, 0.2);
      });
      contextsGrid.appendChild(card);
    });
  }

  contextSearchInput.addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase();
    const filtered = state.contexts.filter(c => 
      c.title.toLowerCase().includes(query) || 
      c.filename.toLowerCase().includes(query)
    );
    renderContexts(filtered);
  });

  // 6. RSSM Dreamscape Latent Canvas Engine
  function initDreamscapeCanvas() {
    const ctx = dreamscapeCanvas.getContext('2d');
    const width = dreamscapeCanvas.parentElement.clientWidth;
    const height = 340;
    dreamscapeCanvas.width = width;
    dreamscapeCanvas.height = height;

    let frame = 0;
    function animate() {
      ctx.fillStyle = '#030508';
      ctx.fillRect(0, 0, width, height);

      // Draw Grid
      ctx.strokeStyle = 'rgba(0, 240, 255, 0.08)';
      ctx.lineWidth = 1;
      for (let x = 0; x < width; x += 40) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, height);
        ctx.stroke();
      }
      for (let y = 0; y < height; y += 40) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(width, y);
        ctx.stroke();
      }

      // Draw Latent Quantum Waves
      const t = frame * 0.03;
      ctx.strokeStyle = '#00f0ff';
      ctx.lineWidth = 2;
      ctx.beginPath();
      for (let x = 0; x < width; x += 5) {
        const y = height / 2 + Math.sin(x * 0.015 + t) * 45 + Math.sin(x * 0.03 - t * 0.5) * 20;
        if (x === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.stroke();

      // Second harmonic wave (Purple 110Hz resonance)
      ctx.strokeStyle = '#a855f7';
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      for (let x = 0; x < width; x += 5) {
        const y = height / 2 + Math.cos(x * 0.02 - t) * 35 + Math.sin(x * 0.008 + t) * 25;
        if (x === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.stroke();

      frame++;
      requestAnimationFrame(animate);
    }
    animate();
  }

  // Run Dreamscape Simulation
  runDreamSimBtn.addEventListener('click', async () => {
    runDreamSimBtn.innerText = '⏳ COMPUTING RSSM ROLLOUT...';
    playCyberChime(110, 0.5, 'sawtooth');

    try {
      const res = await fetch('/api/dreamscape/simulate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ steps: 16 })
      });
      const data = await res.json();
      
      dreamTelemetryList.innerHTML = '';
      data.trajectory.forEach(node => {
        const card = document.createElement('div');
        card.className = 'telemetry-card';
        card.innerHTML = `
          <div style="color:var(--accent-cyan);font-weight:700;">STEP T+${node.step}</div>
          <div>Energy: ${node.latent_energy}</div>
          <div style="color:var(--accent-green);">PRM: ${node.prm}</div>
        `;
        dreamTelemetryList.appendChild(card);
      });
      
      speakBriefing(`Dreamscape simulation complete. 16 latent steps calculated with global minima convergence.`);
      playCyberChime(880, 0.4);
    } catch (e) {
      console.warn('Dream sim error', e);
    } finally {
      runDreamSimBtn.innerText = '🚀 RUN 32-STEP TRAJECTORY ROLLOUT';
    }
  });

  // Initialize Data
  fetchAgents();
  fetchContexts();
});
