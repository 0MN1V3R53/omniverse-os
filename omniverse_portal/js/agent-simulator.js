/* ==========================================================================
   OMNIVERSE TECH — INTERACTIVE MULTI-AGENT THOUGHT & WORKFLOW SIMULATOR
   Demonstrates how 80+ specialized LLM agents collaborate, chat, synchronize
   persistent memory, and execute tasks under hierarchical CEO-to-Pod governance.
   ========================================================================== */

import { soundEngine } from './sound-engine.js';

export const SIMULATION_MISSIONS = {
  audio_macos: {
    id: "audio_macos",
    title: "Engineer an Apple macOS Audio DSP App",
    category: "Division H (Audio DSP) & Division I (macOS Kernel)",
    description: "Client requests a low-latency 192kHz CoreAudio DSP plugin with psychoacoustic bass synthesis and Apple Silicon Metal 3 acceleration.",
    steps: [
      {
        speaker: "Dr. Alexander Vance",
        speaker_id: "exec_ceo_alexander_vance",
        role: "Chief Executive Officer & Chief Architect",
        avatar: "AV",
        color: "#00f0ff",
        action: "Receives Client Directive & Parses Architecture",
        message: "Parsed incoming specification: 192kHz CoreAudio DSP app with psychoacoustic harmonic synthesis and Metal 3 UI. Routing task to Pod 17 Lead Dr. Julian Vance and Pod 16 Lead Dr. Kai Sterling.",
        memory_update: "Global MEMORY_LOG.md: Initialized Milestone - macOS Audio DSP Architecture.",
        review_tier: "Tier 4 Router"
      },
      {
        speaker: "Dr. Julian Vance",
        speaker_id: "audio_systems_lead_dr_julian_vance",
        role: "Audio Systems & DSP Lead (Ph.D. Stanford CCRMA)",
        avatar: "JV",
        color: "#ec4899",
        action: "Mathematical DSP Modeling & Filter Design",
        message: "Designing AudioUnit V3 discrete-time signal pipeline. Implementing missing-fundamental Tartini 2f/3f harmonic synthesis and lookahead peak limiter (-0.2 dBFS brickwall). Assigning low-level CoreAudio C-API bridge to Liam Vance.",
        memory_update: "audio_systems_lead_dr_julian_vance.md: Recorded sample rate 192kHz / 32-bit float headroom invariants.",
        review_tier: "Tier 2 Pod Lead"
      },
      {
        speaker: "Dr. Kai Sterling",
        speaker_id: "macos_kernel_lead_dr_kai_sterling",
        role: "macOS Kernel & Systems Lead (Ph.D. UC Berkeley)",
        avatar: "KS",
        color: "#6366f1",
        action: "Darwin Mach Thread & Metal 3 Integration",
        message: "Configuring Darwin real-time Mach thread policy (THREAD_TIME_CONSTRAINT_POLICY) to guarantee < 1.5ms buffer latency. Bridging AudioUnit buffer to Metal 3 compute shaders for 120Hz retina spectrum visualizer.",
        memory_update: "macos_kernel_lead_dr_kai_sterling.md: Calibrated Mach VM memory governor and lock-free ring buffer.",
        review_tier: "Tier 2 Pod Lead"
      },
      {
        speaker: "Liam Vance",
        speaker_id: "audio_software_dev_liam_vance",
        role: "Audio Software Bridge Engineer (M.S. Stanford)",
        avatar: "LV",
        color: "#06b6d4",
        action: "Writing Atomic C11 / CoreAudio Code",
        message: "Implemented lock-free ring buffers in C11. Bound AudioComponentDescription and verified zero phase distortion across 20Hz - 20kHz sweep test harness.",
        memory_update: "Verified compilation against macOS Monterey CoreAudio SDK with 0 warnings.",
        review_tier: "Tier 1 Specialist"
      },
      {
        speaker: "Michael Chang",
        speaker_id: "security_ciso_michael_chang",
        role: "Chief Information Security Officer (M.S. CMU / CISSP)",
        avatar: "MC",
        color: "#a855f7",
        action: "Hardened Memory & Sandbox Verification",
        message: "Audited Mach shared memory buffers for buffer over-reads and race conditions. Enforced macOS Hardened Runtime with App Sandbox entitlement signatures.",
        memory_update: "CISO Audit Pass: 0 memory leaks, 0 unsigned dylib vulnerabilities.",
        review_tier: "Tier 3 Security Lead"
      },
      {
        speaker: "Dr. Alexander Vance",
        speaker_id: "exec_ceo_alexander_vance",
        role: "Chief Executive Officer & Chief Architect",
        avatar: "AV",
        color: "#00f0ff",
        action: "Final Confluence Merge & Client Release",
        message: "All 4 Tiers verified. CoreAudio DSP and Metal 3 visualizer confirmed 100% compliant with Zero-Drift Mandate. Merging to release branch for client deployment.",
        memory_update: "Global MEMORY_LOG.md: Signed off Milestone - Total macOS Audio DSP Success.",
        review_tier: "Tier 4 CEO Sign-off"
      }
    ]
  },

  seo_network: {
    id: "seo_network",
    title: "Build a 50-State Programmatic SEO Engine",
    category: "Division A: Web & Search Architecture",
    description: "Client needs 2,800+ high-ranking programmatic state corridor routes with zero duplicate content and sub-second Core Web Vitals.",
    steps: [
      {
        speaker: "Dr. Alexander Vance",
        speaker_id: "exec_ceo_alexander_vance",
        role: "Chief Executive Officer & Chief Architect",
        avatar: "AV",
        color: "#00f0ff",
        action: "Directs 50-State SEO Scaling Initiative",
        message: "Mandate received: Deploy 2,806 programmatic routes across all 50 US States with zero duplicate text and real distance calculation. Task routed to Dr. Sarah Lin (SEO Lead) and Julian Thorne (Frontend Lead).",
        memory_update: "Global MEMORY_LOG.md: Initialized Milestone 60 - 50-State Programmatic Deployment.",
        review_tier: "Tier 4 Router"
      },
      {
        speaker: "Dr. Sarah Lin",
        speaker_id: "web_seo_dr_sarah_lin",
        role: "Chief SEO & Search Architecture Lead (Ph.D. CMU)",
        avatar: "SL",
        color: "#f97316",
        action: "Semantic Schema & Geographic Graph Architecture",
        message: "Structuring JSON-LD BreadcrumbList and LocalBusiness schema for all 50 states. Directing Dr. Emily Rivera to generate unique demographic and transport corridor data for each state pair.",
        memory_update: "web_seo_dr_sarah_lin.md: Mapped 3,148 corridor pairs with exact OSRM driving matrix.",
        review_tier: "Tier 2 Pod Lead"
      },
      {
        speaker: "Julian Thorne",
        speaker_id: "web_frontend_julian_thorne",
        role: "Principal Frontend / Next.js Design Lead (M.S. Stanford)",
        avatar: "JT",
        color: "#06b6d4",
        action: "Next.js 15 Static Regeneration & Tailwind UI",
        message: "Engineered dynamic Route Directory components. Pre-rendering 2,806 pages via Next.js SSG with zero CLS layout shifts and optimized webp assets.",
        memory_update: "web_frontend_julian_thorne.md: Verified sub-800ms LCP on all mobile viewports.",
        review_tier: "Tier 1 Specialist"
      },
      {
        speaker: "Sunita Rao",
        speaker_id: "qa_auto_script",
        role: "Automated QA Verification Specialist (M.S. SE UT Austin)",
        avatar: "SR",
        color: "#84cc16",
        action: "Zero-Repeat Text AST Scan Across 2,804 HTMLs",
        message: "Executed scan_repeated_text.py inspecting all 2,804 production HTML files down to 18-character phrases. Verified: EXACTLY 0 FILES WITH REPEATING TEXT (100% Clean).",
        memory_update: "qa_auto_script.md: Verified 2,804 pages 100% free of repeated sentences.",
        review_tier: "Tier 2 QA Lead"
      },
      {
        speaker: "Dr. Alexander Vance",
        speaker_id: "exec_ceo_alexander_vance",
        role: "Chief Executive Officer & Chief Architect",
        avatar: "AV",
        color: "#00f0ff",
        action: "Final Production Deployment Sign-off",
        message: "Confluence confirmed. All 2,806 routes deployed to Hostinger LiteSpeed live server. Tested dual-engine Google rank proofs: #1 Position Verified.",
        memory_update: "Global MEMORY_LOG.md: Signed off Milestone 62 - Zero Repeating Text Achieved.",
        review_tier: "Tier 4 CEO Sign-off"
      }
    ]
  },

  web3_smart_contract: {
    id: "web3_smart_contract",
    title: "Audit & Deploy a Sovereign Web3 Smart Contract",
    category: "Division B: Applied Cryptography & Web3",
    description: "Client requires a non-custodial BIP39 vault, Solana Anchor smart contracts, and Signal-grade Double Ratchet E2EE financial routing.",
    steps: [
      {
        speaker: "Dr. Alexander Vance",
        speaker_id: "exec_ceo_alexander_vance",
        role: "Chief Executive Officer",
        avatar: "AV",
        color: "#00f0ff",
        action: "Cryptographic Architecture Delegation",
        message: "Routing Web3 financial terminal and smart contract requirement to Pod Lead Dr. Leon Nash. Invariant: 0.5% protocol routing fee, BIP39 non-custodial vault, and zero seed phrase leakage.",
        memory_update: "Global MEMORY_LOG.md: Initialized Web3 Sovereign Terminal Architecture.",
        review_tier: "Tier 4 Router"
      },
      {
        speaker: "Dr. Leon Nash",
        speaker_id: "web3_crypto_leon_nash",
        role: "Principal Web3 & Cryptography Lead (Ph.D. MIT Cryptography)",
        avatar: "LN",
        color: "#eab308",
        action: "Double Ratchet Protocol & Rust Anchor Architecture",
        message: "Implementing Libsodium X25519 key exchange with Argon2id passphrase derivation. Authoring Solana Anchor program with strict PDA (Program Derived Address) validation.",
        memory_update: "web3_crypto_leon_nash.md: Enforced memory zeroization for all private key byte arrays.",
        review_tier: "Tier 2 Pod Lead"
      },
      {
        speaker: "Elena Vance",
        speaker_id: "ios_lead_architect",
        role: "Principal iOS Architect (M.S. Stanford)",
        avatar: "EV",
        color: "#e2e8f0",
        action: "Apple Secure Enclave Hardware Binding",
        message: "Binding user wallet key generation to Apple Secure Enclave via CryptoKit. Private keys never leave the hardware security chip.",
        memory_update: "ios_lead_architect.md: Implemented biometric FaceID hardware authentication gate.",
        review_tier: "Tier 1 Specialist"
      },
      {
        speaker: "Michael Chang",
        speaker_id: "security_ciso_michael_chang",
        role: "Chief Information Security Officer (M.S. CMU)",
        avatar: "MC",
        color: "#a855f7",
        action: "Formal Verification & Reentrancy Red-Teaming",
        message: "Ran formal verification solvers (Z3) and fuzzing suites against smart contract bytecode. Verified immune to reentrancy, integer overflow, and flash-loan manipulation.",
        memory_update: "CISO Cryptographic Audit: 100% formal verification proof passed.",
        review_tier: "Tier 3 Security Lead"
      },
      {
        speaker: "Dr. Alexander Vance",
        speaker_id: "exec_ceo_alexander_vance",
        role: "Chief Executive Officer",
        avatar: "AV",
        color: "#00f0ff",
        action: "Mainnet Deployment & Memory Lock",
        message: "Smart contract verified and deployed to Solana Mainnet-Beta. Persistent memory synchronized across all Web3 agent banks.",
        memory_update: "Global MEMORY_LOG.md: Signed off Web3 Cryptographic Terminal Deployment.",
        review_tier: "Tier 4 CEO Sign-off"
      }
    ]
  },

  offensive_cyber: {
    id: "offensive_cyber",
    title: "Reverse Engineer & Patch Binary Vulnerability",
    category: "Omniverse Code: Offensive Vulnerability Research",
    description: "Client requires an offensive binary analysis audit to identify dynamic heap corruption and ROP chain exploitation risks before production release.",
    steps: [
      {
        speaker: "Prof. Lucas Mercer",
        speaker_id: "code_dean_lucas_mercer",
        role: "Dean & Chief Research Officer (DARPA CGC Veteran / Ph.D. MIT)",
        avatar: "LM",
        color: "#ef4444",
        action: "Initializes Binary Disassembly & Symbolic Fuzzing",
        message: "Target binary ingested into Ghidra / IDA Pro headless pipeline. Directing Dr. Vivienne Laurent to analyze glibc ptmalloc heap chunks and Dr. Kaito Tanaka to test ROP chain defenses.",
        memory_update: "code_dean_lucas_mercer.md: Loaded binary AST and symbolic execution targets into Angr.",
        review_tier: "Dean Leadership"
      },
      {
        speaker: "Dr. Vivienne Laurent",
        speaker_id: "code_heap_lead_dr_vivienne_laurent",
        role: "Dynamic Allocator & Heap Lead (Ph.D. Sorbonne)",
        avatar: "VL",
        color: "#f43f5e",
        action: "Heap Feng-Shui & Use-After-Free Audit",
        message: "Discovered an unsafe fastbin consolidation race condition in custom caching module. Formulated exploit proof-of-concept demonstrating potential arbitrary write primitive.",
        memory_update: "code_heap_lead_dr_vivienne_laurent.md: Documented heap chunk metadata corruption vulnerability.",
        review_tier: "Tier 2 Specialist Lead"
      },
      {
        speaker: "Dr. Kaito Tanaka",
        speaker_id: "code_pwn_lead_dr_kaito_tanaka",
        role: "Binary Exploitation & ROP Architect (Ph.D. Tokyo Univ)",
        avatar: "KT",
        color: "#e11d48",
        action: "Mitigation Hardening & Exploit Mitigation Patch",
        message: "Patched memory allocation to use safe linking and jemalloc thread-isolated arenas. Enforced Shadow Stack and CET (Control-flow Enforcement Technology) compliance.",
        memory_update: "code_pwn_lead_dr_kaito_tanaka.md: Validated binary passes all ASLR/NX/Canary strict checks.",
        review_tier: "Tier 2 Specialist Lead"
      },
      {
        speaker: "Prof. Lucas Mercer",
        speaker_id: "code_dean_lucas_mercer",
        role: "Dean & Chief Research Officer",
        avatar: "LM",
        color: "#ef4444",
        action: "Verification Sign-off to CEO Dr. Vance",
        message: "Binary re-fuzzed across 10,000,000 AFL++ mutations with 0 crashes. Hardened binary delivered to CEO Dr. Alexander Vance for final enterprise integration.",
        memory_update: "Global MEMORY_LOG.md: Signed off Omniverse Code Vulnerability Elimination.",
        review_tier: "Dean Sign-off"
      }
    ]
  }
};

export function initAgentSimulator() {
  const missionSelect = document.getElementById('simulator-mission-select');
  const chatContainer = document.getElementById('simulator-chat-container');
  const stepCountEl = document.getElementById('simulator-step-count');
  const progressBar = document.getElementById('simulator-progress-bar');
  const nextBtn = document.getElementById('sim-next-btn');
  const playBtn = document.getElementById('sim-play-btn');
  const resetBtn = document.getElementById('sim-reset-btn');
  const missionDescEl = document.getElementById('sim-mission-desc');
  const activeMemoryLogEl = document.getElementById('sim-active-memory-log');

  if (!missionSelect || !chatContainer) return;

  let currentMission = SIMULATION_MISSIONS.audio_macos;
  let currentStepIdx = 0;
  let isAutoPlaying = false;
  let autoPlayTimer = null;

  function loadMission(missionKey) {
    currentMission = SIMULATION_MISSIONS[missionKey] || SIMULATION_MISSIONS.audio_macos;
    currentStepIdx = 0;
    stopAutoPlay();
    if (missionDescEl) {
      missionDescEl.textContent = currentMission.description;
    }
    renderSteps();
  }

  function renderSteps() {
    chatContainer.innerHTML = '';
    const steps = currentMission.steps;
    const progress = (currentStepIdx / steps.length) * 100;

    if (progressBar) progressBar.style.width = `${progress}%`;
    if (stepCountEl) stepCountEl.textContent = `Step ${currentStepIdx} of ${steps.length}`;

    if (currentStepIdx === 0) {
      chatContainer.innerHTML = `
        <div style="text-align: center; padding: 3rem 1rem; color: #64748b;">
          <div style="font-size: 2.5rem; margin-bottom: 1rem;">🤖 ➔ 🧠 ➔ ⚡</div>
          <h4 style="color: #ffffff; font-size: 1.2rem; margin-bottom: 0.5rem;">Multi-Agent Simulation Ready</h4>
          <p style="font-size: 0.92rem; max-width: 480px; margin: 0 auto;">Click <strong>"Step Forward"</strong> or <strong>"Auto-Play"</strong> to watch how CEO Dr. Alexander Vance routes tasks, delegates to Pod Leads, synchronizes persistent memory, and merges flawless code.</p>
        </div>
      `;
      if (activeMemoryLogEl) {
        activeMemoryLogEl.innerHTML = `<span style="color: #64748b;">Waiting for simulation step...</span>`;
      }
      return;
    }

    let latestMemory = "";

    for (let i = 0; i < currentStepIdx; i++) {
      const step = steps[i];
      latestMemory = step.memory_update;

      const bubble = document.createElement('div');
      bubble.className = 'sim-chat-bubble';
      bubble.style.cssText = `
        display: flex;
        gap: 1rem;
        margin-bottom: 1.25rem;
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-left: 4px solid ${step.color};
        border-radius: 12px;
        padding: 1.25rem;
        animation: fadeSlideUp 0.35s ease-out;
        backdrop-filter: blur(12px);
      `;

      bubble.innerHTML = `
        <div style="width: 44px; height: 44px; border-radius: 10px; background: rgba(255,255,255,0.06); border: 1px solid ${step.color}; display: flex; align-items: center; justify-content: center; font-weight: 800; color: ${step.color}; font-size: 1.1rem; flex-shrink: 0;">
          ${step.avatar}
        </div>
        <div style="flex: 1;">
          <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 0.35rem;">
            <div>
              <strong style="color: #ffffff; font-size: 1.05rem;">${step.speaker}</strong>
              <span style="font-size: 0.78rem; color: #94a3b8; margin-left: 0.5rem;">(${step.role})</span>
            </div>
            <span class="badge" style="border-color: ${step.color}; color: ${step.color}; font-size: 0.68rem;">${step.review_tier}</span>
          </div>
          <div style="font-size: 0.8rem; font-family: var(--font-mono); color: ${step.color}; margin-bottom: 0.5rem;">
            ⚡ Action: ${step.action}
          </div>
          <p style="color: #cbd5e1; font-size: 0.92rem; line-height: 1.6; margin-bottom: 0.65rem;">
            "${step.message}"
          </p>
          <div style="font-size: 0.75rem; font-family: var(--font-mono); color: #10b981; background: rgba(16, 185, 129, 0.08); padding: 0.35rem 0.65rem; border-radius: 4px; border: 1px solid rgba(16, 185, 129, 0.2);">
            💾 Memory Synchronized: ${step.memory_update}
          </div>
        </div>
      `;

      chatContainer.appendChild(bubble);
    }

    if (activeMemoryLogEl) {
      activeMemoryLogEl.innerHTML = `<span style="color: #10b981;">[LIVE STATE SYNC]</span> ${latestMemory}`;
    }

    // Scroll to bottom of chat
    chatContainer.scrollTop = chatContainer.scrollHeight;

    // Check if finished
    if (currentStepIdx === steps.length) {
      const banner = document.createElement('div');
      banner.style.cssText = `
        background: linear-gradient(135deg, rgba(0, 240, 255, 0.15), rgba(16, 185, 129, 0.15));
        border: 1px solid var(--neon-cyan);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        margin-top: 1.5rem;
        animation: fadeSlideUp 0.4s ease-out;
      `;
      banner.innerHTML = `
        <div style="font-size: 1.5rem; margin-bottom: 0.4rem;">🎉</div>
        <h4 style="color: #ffffff; font-size: 1.2rem; margin-bottom: 0.3rem;">Mission Successfully Completed &amp; Verified</h4>
        <p style="color: #94a3b8; font-size: 0.9rem;">4-Tier Code Review Passed &bull; 0 Hallucinations &bull; 0 Mock Data &bull; Persistent Memory Written to Disk</p>
      `;
      chatContainer.appendChild(banner);
      stopAutoPlay();
    }
  }

  function stepForward() {
    if (currentStepIdx < currentMission.steps.length) {
      currentStepIdx++;
      soundEngine.playClick();
      renderSteps();
    } else {
      stopAutoPlay();
    }
  }

  function startAutoPlay() {
    isAutoPlaying = true;
    if (playBtn) playBtn.innerHTML = `<span>Pause</span>`;
    soundEngine.playChime();

    if (currentStepIdx >= currentMission.steps.length) {
      currentStepIdx = 0;
    }

    autoPlayTimer = setInterval(() => {
      if (currentStepIdx < currentMission.steps.length) {
        stepForward();
      } else {
        stopAutoPlay();
      }
    }, 2200);
  }

  function stopAutoPlay() {
    isAutoPlaying = false;
    if (autoPlayTimer) clearInterval(autoPlayTimer);
    if (playBtn) playBtn.innerHTML = `<span>Auto-Play Flow</span>`;
  }

  function resetSimulation() {
    stopAutoPlay();
    currentStepIdx = 0;
    soundEngine.playClick();
    renderSteps();
  }

  // Event Listeners
  missionSelect.addEventListener('change', (e) => {
    soundEngine.playClick();
    loadMission(e.target.value);
  });

  if (nextBtn) nextBtn.addEventListener('click', stepForward);
  if (playBtn) {
    playBtn.addEventListener('click', () => {
      if (isAutoPlaying) {
        stopAutoPlay();
      } else {
        startAutoPlay();
      }
    });
  }
  if (resetBtn) resetBtn.addEventListener('click', resetSimulation);

  // Initialize with default mission
  loadMission('audio_macos');
}
