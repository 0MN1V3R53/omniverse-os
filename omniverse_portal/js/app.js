/* ==========================================================================
   OMNIVERSE TECH — MASTER APPLICATION CONTROLLER
   Coordinates Data Rendering, Real-Time Search, Filtering, Dossier Modals & Consultations
   ========================================================================== */

import { OMNIVERSE_DATA } from '../src/data/omniverse_dataset.js';
import { soundEngine } from './sound-engine.js';
import { initThreeHero } from './three-hero.js';
import { initFolderExplorer } from './folder-explorer.js';
import { initAgentSimulator } from './agent-simulator.js';

document.addEventListener('DOMContentLoaded', () => {
  // 0. Initialize Anti-Theft Security Guard
  initSecurityGuard();

  // 1. Initialize 3D Hero Canvas
  initThreeHero();

  // 2. Initialize Multi-Agent Workflow Simulator
  initAgentSimulator();

  // 3. Initialize Sound Toggle
  initSoundToggle();

  // 4. Render 11 Capabilities Bento Grid
  renderCapabilities();

  // 5. Render Enterprise Matrix & Employee Directory
  initEnterpriseMatrix();

  // 6. Initialize Client Consultation Configurator
  initConsultationBuilder();

  // 7. Navigation & Smooth Scroll
  initNavigation();
});

/* --------------------------------------------------------------------------
   Anti-Theft & Non-Copyable Security Guard
   -------------------------------------------------------------------------- */
function initSecurityGuard() {
  const isInput = (el) => el && (['INPUT', 'TEXTAREA', 'SELECT'].includes(el.tagName) || el.isContentEditable || el.closest('input, textarea, select, .code-container, pre, code'));

  // Right-click context menu
  document.addEventListener('contextmenu', (e) => {
    if (isInput(e.target)) return;
    e.preventDefault();
  }, true);

  // Dragstart
  document.addEventListener('dragstart', (e) => {
    if (isInput(e.target)) return;
    e.preventDefault();
  }, true);

  // Keyboard shortcut protection
  document.addEventListener('keydown', (e) => {
    const isInteractive = isInput(e.target);
    const isCtrlOrCmd = e.ctrlKey || e.metaKey;

    if (e.key === 'F12' || e.keyCode === 123) {
      e.preventDefault();
      return false;
    }
    if (isCtrlOrCmd && e.shiftKey && ['I', 'i', 'J', 'j', 'C', 'c', 'K', 'k'].includes(e.key)) {
      e.preventDefault();
      return false;
    }
    if (isCtrlOrCmd && ['u', 'U', 's', 'S', 'p', 'P'].includes(e.key)) {
      e.preventDefault();
      return false;
    }
    if (!isInteractive && isCtrlOrCmd && ['a', 'A', 'c', 'C'].includes(e.key)) {
      e.preventDefault();
      return false;
    }
  }, true);
}


/* --------------------------------------------------------------------------
   Sound Toggle Control
   -------------------------------------------------------------------------- */
function initSoundToggle() {
  const soundBtn = document.getElementById('sound-toggle-btn');
  if (!soundBtn) return;

  soundBtn.addEventListener('click', () => {
    const isNowActive = soundEngine.toggle();
    if (isNowActive) {
      soundBtn.classList.add('active');
      soundBtn.querySelector('.sound-status-text').textContent = 'Audio: Active (192kHz)';
    } else {
      soundBtn.classList.remove('active');
      soundBtn.querySelector('.sound-status-text').textContent = 'Audio: Muted';
    }
  });

  // Attach sound feedback to all interactive buttons and links
  document.querySelectorAll('button, .btn, .nav-links a, .filter-pill').forEach(el => {
    el.addEventListener('mouseenter', () => soundEngine.playHover());
    el.addEventListener('click', () => soundEngine.playClick());
  });
}

/* --------------------------------------------------------------------------
   11 Core Technical Capabilities Showcase
   -------------------------------------------------------------------------- */
function renderCapabilities() {
  const container = document.getElementById('capabilities-grid-root');
  if (!container) return;

  const caps = OMNIVERSE_DATA.capabilities || [];
  container.innerHTML = '';

  const iconMap = {
    globe: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>`,
    apple: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M12 20.94c1.88 0 3.05-.88 4.22-.88 1.15 0 2.22.88 4.08.88 2.05 0 3.7-1.4 4.7-3.15-2.7-1.57-2.28-5.32.42-6.52-1.32-2.3-3.65-2.65-4.52-2.65-1.92 0-3.32 1.12-4.3 1.12-1.02 0-2.62-1.08-4.22-1.08-2.68 0-5.18 2.05-6.28 4.95-1.12 2.92-.28 7.33 2.1 10.75 1.15 1.62 2.5 3.58 4.8 3.58z"></path><path d="M12 2c.6 1.4-.2 3.1-1.2 4.1-1 1-2.7 1.7-3.8 1.5-.15-1.3.6-2.9 1.5-3.8 1.1-1.1 2.8-1.8 3.5-1.8z"></path></svg>`,
    smartphone: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><rect x="5" y="2" width="14" height="20" rx="2" ry="2"></rect><line x1="12" y1="18" x2="12.01" y2="18"></line></svg>`,
    cpu: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="2"></rect><rect x="9" y="9" width="6" height="6"></rect><line x1="9" y1="1" x2="9" y2="4"></line><line x1="15" y1="1" x2="15" y2="4"></line><line x1="9" y1="20" x2="9" y2="23"></line><line x1="15" y1="20" x2="15" y2="23"></line><line x1="20" y1="9" x2="23" y2="9"></line><line x1="20" y1="14" x2="23" y2="14"></line><line x1="1" y1="9" x2="4" y2="9"></line><line x1="1" y1="14" x2="4" y2="14"></line></svg>`,
    'volume-2': `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path></svg>`,
    key: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="7.5" cy="15.5" r="5.5"></circle><path d="m21 2-9.6 9.6M15.5 7.5l3 3M18.5 4.5l3 3"></path></svg>`,
    layers: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>`,
    terminal: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><polyline points="4 17 10 11 4 5"></polyline><line x1="12" y1="19" x2="20" y2="19"></line></svg>`,
    radar: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle><circle cx="12" cy="12" r="6"></circle><circle cx="12" cy="12" r="2"></circle><line x1="12" y1="12" x2="19" y2="5"></line></svg>`,
    dices: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><rect x="2" y="2" width="20" height="20" rx="4"></rect><circle cx="8" cy="8" r="1.5"></circle><circle cx="16" cy="8" r="1.5"></circle><circle cx="12" cy="12" r="1.5"></circle><circle cx="8" cy="16" r="1.5"></circle><circle cx="16" cy="16" r="1.5"></circle></svg>`,
    brain: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 4.44-2.04zM14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-4.44-2.04z"></path></svg>`
  };

  caps.forEach((cap) => {
    const card = document.createElement('div');
    card.className = 'capability-card';
    card.style.setProperty('--card-accent', cap.accent || '#00f0ff');

    const iconSvg = iconMap[cap.icon] || iconMap.globe;

    const techTagsHtml = (cap.technologies || [])
      .map(t => `<span class="tech-tag">${t}</span>`)
      .join('');

    card.innerHTML = `
      <div>
        <div class="cap-top">
          <div class="cap-icon">${iconSvg}</div>
          <span class="badge" style="border-color: ${cap.accent}; color: ${cap.accent}; font-size: 0.7rem;">Verified Domain</span>
        </div>
        <h3 class="cap-title">${cap.title}</h3>
        <div class="cap-subtitle">${cap.subtitle}</div>
        <p class="cap-tagline">${cap.tagline}</p>
        <div class="cap-lead-badge">
          <span>Lead:</span>
          <strong>${cap.lead}</strong>
        </div>
        <div class="cap-tech-tags">${techTagsHtml}</div>
      </div>
      <div class="cap-action">
        <span>Explore Architecture & Features</span>
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" width="18" height="18">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path>
        </svg>
      </div>
    `;

    card.addEventListener('mouseenter', () => soundEngine.playHover());
    card.addEventListener('click', () => {
      soundEngine.playChime();
      openCapabilityModal(cap);
    });

    container.appendChild(card);
  });
}

function openCapabilityModal(cap) {
  const modalOverlay = document.getElementById('employee-dossier-modal');
  const modalBody = document.getElementById('modal-dossier-body');
  if (!modalOverlay || !modalBody) return;

  const featuresListHtml = (cap.features || [])
    .map(f => `<li style="margin-bottom: 0.75rem; color: #cbd5e1; font-size: 0.92rem;"><span style="color: ${cap.accent}; font-weight: bold; margin-right: 0.5rem;">▶</span>${f}</li>`)
    .join('');

  const techPills = (cap.technologies || [])
    .map(t => `<span class="tech-tag" style="border-color: ${cap.accent}; color: #ffffff;">${t}</span>`)
    .join('');

  modalBody.innerHTML = `
    <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
      <div style="width: 52px; height: 52px; border-radius: 12px; background: rgba(255,255,255,0.05); border: 1px solid ${cap.accent}; display: flex; align-items: center; justify-content: center; color: ${cap.accent};">
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" width="28" height="28">
          <circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 14 14"></polyline>
        </svg>
      </div>
      <div>
        <h2 style="font-size: 1.6rem; color: #ffffff; margin-bottom: 0.2rem;">${cap.title}</h2>
        <div style="font-family: var(--font-mono); font-size: 0.8rem; color: ${cap.accent};">${cap.subtitle}</div>
      </div>
    </div>

    <div style="background: rgba(11, 16, 27, 0.8); border: 1px solid var(--border-subtle); border-radius: 12px; padding: 1.25rem; margin-bottom: 1.5rem;">
      <div style="font-size: 0.8rem; font-family: var(--font-mono); color: #64748b; margin-bottom: 0.35rem;">FACULTY & POD LEADERSHIP</div>
      <div style="font-size: 1.05rem; font-weight: 700; color: #ffffff;">${cap.lead}</div>
    </div>

    <div style="margin-bottom: 1.5rem;">
      <h4 style="font-size: 1rem; color: #ffffff; margin-bottom: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; font-family: var(--font-mono);">Architectural Specifications & Invariants</h4>
      <ul style="list-style: none; padding: 0;">
        ${featuresListHtml}
      </ul>
    </div>

    <div style="margin-bottom: 1.5rem;">
      <h4 style="font-size: 1rem; color: #ffffff; margin-bottom: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; font-family: var(--font-mono);">Technology Stack & Tooling</h4>
      <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
        ${techPills}
      </div>
    </div>

    <div style="background: rgba(0, 240, 255, 0.05); border: 1px solid rgba(0, 240, 255, 0.2); border-radius: 12px; padding: 1.25rem;">
      <div style="font-size: 0.8rem; font-family: var(--font-mono); color: var(--neon-cyan); margin-bottom: 0.35rem;">CLIENT ROI & STRATEGIC ADVANTAGE</div>
      <p style="color: #e2e8f0; font-size: 0.95rem; line-height: 1.6;">${cap.client_benefit}</p>
    </div>
  `;

  modalOverlay.classList.add('active');
}

/* --------------------------------------------------------------------------
   Omniverse Enterprise Matrix & Employee Directory
   -------------------------------------------------------------------------- */
let activeDivisionFilter = 'all';
let employeeSearchQuery = '';

function initEnterpriseMatrix() {
  const searchInput = document.getElementById('matrix-search-input');
  const filterPills = document.querySelectorAll('.filter-pill');
  const modalOverlay = document.getElementById('employee-dossier-modal');
  const modalCloseBtn = document.getElementById('modal-close-btn');

  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      employeeSearchQuery = e.target.value;
      renderEmployeeCards();
    });
  }

  filterPills.forEach(pill => {
    pill.addEventListener('click', () => {
      filterPills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      activeDivisionFilter = pill.dataset.division || 'all';
      renderEmployeeCards();
    });
  });

  if (modalCloseBtn && modalOverlay) {
    modalCloseBtn.addEventListener('click', () => {
      modalOverlay.classList.remove('active');
      soundEngine.playClick();
    });

    modalOverlay.addEventListener('click', (e) => {
      if (e.target === modalOverlay) {
        modalOverlay.classList.remove('active');
      }
    });
  }

  renderEmployeeCards();
}

function renderEmployeeCards() {
  const container = document.getElementById('employees-grid-root');
  const countEl = document.getElementById('matrix-rendered-count');
  if (!container) return;

  const employees = OMNIVERSE_DATA.employees || [];
  const q = employeeSearchQuery.toLowerCase().trim();

  const filtered = employees.filter(emp => {
    // Division filter
    let matchesDiv = true;
    if (activeDivisionFilter !== 'all') {
      const divLower = (emp.division || '').toLowerCase();
      const podLower = (emp.pod_name || '').toLowerCase();
      matchesDiv = divLower.includes(activeDivisionFilter.toLowerCase()) || podLower.includes(activeDivisionFilter.toLowerCase());
    }

    // Search query filter
    let matchesSearch = true;
    if (q) {
      const searchStr = `${emp.name} ${emp.role} ${emp.credentials} ${emp.alma_mater} ${emp.pod_name} ${emp.division} ${emp.id}`.toLowerCase();
      matchesSearch = searchStr.includes(q);
    }

    return matchesDiv && matchesSearch;
  });

  if (countEl) {
    countEl.innerHTML = `Displaying <strong>${filtered.length}</strong> of <strong>${employees.length}</strong> Registered Enterprise Specialists`;
  }

  container.innerHTML = '';

  if (filtered.length === 0) {
    container.innerHTML = `
      <div style="grid-column: 1 / -1; text-align: center; padding: 4rem 1rem; color: #64748b;">
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" width="48" height="48" style="margin: 0 auto 1rem auto; display: block; opacity: 0.5;">
          <circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
        <p style="font-size: 1.1rem; color: #94a3b8;">No registered specialists found matching "${employeeSearchQuery}".</p>
        <p style="font-size: 0.85rem; margin-top: 0.5rem;">Try searching for "Ph.D.", "MIT", "Stanford", "Kernel", "Audio", or "Exploitation".</p>
      </div>
    `;
    return;
  }

  filtered.forEach(emp => {
    const card = document.createElement('div');
    card.className = 'employee-card';

    // Initials for avatar
    const initials = (emp.name || 'Omniverse')
      .split(' ')
      .filter(w => !w.startsWith('Dr.') && !w.startsWith('Prof.'))
      .map(w => w[0])
      .slice(0, 2)
      .join('') || 'OV';

    card.innerHTML = `
      <div>
        <div class="emp-header">
          <div class="emp-avatar">${initials}</div>
          <div class="emp-info">
            <h4>${emp.name}</h4>
            <div class="emp-role">${emp.role}</div>
            <div class="emp-id-tag">ID: ${emp.id}</div>
          </div>
        </div>
        <div class="emp-details">
          <div class="emp-credentials-badge">${emp.credentials}</div>
          <div class="emp-pod-line">
            <span>Pod:</span>
            <strong>${emp.pod_name}</strong>
          </div>
          <div class="emp-pod-line" style="margin-top: 0.25rem;">
            <span>Alma Mater:</span>
            <strong>${emp.alma_mater}</strong>
          </div>
        </div>
      </div>
      <div class="emp-footer">
        <span>Channel: ${emp.channel}</span>
        <span style="color: var(--neon-cyan); display: flex; align-items: center; gap: 0.25rem;">
          View Dossier ➔
        </span>
      </div>
    `;

    card.addEventListener('mouseenter', () => soundEngine.playHover());
    card.addEventListener('click', () => {
      soundEngine.playClick();
      openEmployeeModal(emp);
    });

    container.appendChild(card);
  });
}

function openEmployeeModal(emp) {
  const modalOverlay = document.getElementById('employee-dossier-modal');
  const modalBody = document.getElementById('modal-dossier-body');
  if (!modalOverlay || !modalBody) return;

  const initials = (emp.name || 'OV')
    .split(' ')
    .filter(w => !w.startsWith('Dr.') && !w.startsWith('Prof.'))
    .map(w => w[0])
    .slice(0, 2)
    .join('') || 'OV';

  modalBody.innerHTML = `
    <div style="display: flex; align-items: center; gap: 1.25rem; margin-bottom: 2rem;">
      <div style="width: 64px; height: 64px; border-radius: 14px; background: linear-gradient(135deg, rgba(0,240,255,0.3), rgba(168,85,247,0.3)); border: 1px solid var(--neon-cyan); display: flex; align-items: center; justify-content: center; font-size: 1.5rem; font-weight: 800; color: #ffffff;">
        ${initials}
      </div>
      <div>
        <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.2rem;">
          <h2 style="font-size: 1.7rem; color: #ffffff; margin: 0;">${emp.name}</h2>
          <span class="pulse-dot" title="Active in Matrix"></span>
        </div>
        <div style="font-size: 0.95rem; color: var(--neon-cyan); font-weight: 600;">${emp.role}</div>
        <div style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--neon-violet); margin-top: 0.2rem;">Agent ID: ${emp.id}</div>
      </div>
    </div>

    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 1.75rem;">
      <div style="background: rgba(11, 16, 27, 0.8); border: 1px solid var(--border-subtle); border-radius: 8px; padding: 0.85rem 1rem;">
        <div style="font-size: 0.72rem; font-family: var(--font-mono); color: #64748b;">CREDENTIALS & DEGREES</div>
        <div style="font-size: 0.92rem; font-weight: 600; color: var(--neon-emerald); margin-top: 0.2rem;">${emp.credentials}</div>
      </div>
      <div style="background: rgba(11, 16, 27, 0.8); border: 1px solid var(--border-subtle); border-radius: 8px; padding: 0.85rem 1rem;">
        <div style="font-size: 0.72rem; font-family: var(--font-mono); color: #64748b;">ALMA MATER</div>
        <div style="font-size: 0.92rem; font-weight: 600; color: #ffffff; margin-top: 0.2rem;">${emp.alma_mater}</div>
      </div>
      <div style="background: rgba(11, 16, 27, 0.8); border: 1px solid var(--border-subtle); border-radius: 8px; padding: 0.85rem 1rem;">
        <div style="font-size: 0.72rem; font-family: var(--font-mono); color: #64748b;">REPORTING HIERARCHY</div>
        <div style="font-size: 0.92rem; font-weight: 600; color: #ffffff; margin-top: 0.2rem;">${emp.reports_to}</div>
      </div>
      <div style="background: rgba(11, 16, 27, 0.8); border: 1px solid var(--border-subtle); border-radius: 8px; padding: 0.85rem 1rem;">
        <div style="font-size: 0.72rem; font-family: var(--font-mono); color: #64748b;">SLACK DIRECT ROUTE</div>
        <div style="font-size: 0.92rem; font-weight: 600; color: var(--neon-cyan); margin-top: 0.2rem;">${emp.channel}</div>
      </div>
    </div>

    <div style="margin-bottom: 1.75rem;">
      <h4 style="font-size: 0.9rem; color: #94a3b8; margin-bottom: 0.6rem; text-transform: uppercase; letter-spacing: 0.08em; font-family: var(--font-mono);">Active Memory Bank Directives & Invariants</h4>
      <div style="background: #060910; border: 1px solid var(--border-subtle); border-radius: 10px; padding: 1.25rem; font-family: var(--font-mono); font-size: 0.82rem; line-height: 1.6; color: #cbd5e1; max-height: 240px; overflow-y: auto; white-space: pre-wrap;">
${emp.memory_preview}
      </div>
    </div>

    <div style="display: flex; align-items: center; justify-content: space-between; padding-top: 1rem; border-top: 1px solid var(--border-subtle);">
      <span class="badge badge-emerald" style="font-size: 0.72rem;">100% Zero-Drift Certified</span>
      <span style="font-family: var(--font-mono); font-size: 0.75rem; color: #64748b;">Omniverse Enterprise Matrix Core</span>
    </div>
  `;

  modalOverlay.classList.add('active');
}

/* --------------------------------------------------------------------------
   Interactive Client Consultation Terminal
   -------------------------------------------------------------------------- */
function initConsultationBuilder() {
  const checkboxes = document.querySelectorAll('.spec-checkbox');
  const countDisplay = document.getElementById('allocated-specialists-count');
  const podsListContainer = document.getElementById('allocated-pods-list');
  const submitBtn = document.getElementById('submit-consultation-btn');
  const confirmationBanner = document.getElementById('consultation-confirmation');

  if (!checkboxes.length) return;

  const podMap = {
    web: { name: 'Division A (Web & Next.js)', lead: 'Julian Thorne', specialists: 6 },
    ios: { name: 'Division B (Native iOS & Apple Crypto)', lead: 'Elena Vance', specialists: 4 },
    android: { name: 'Division B (Android & NDK C++)', lead: 'Viktor Drago', specialists: 6 },
    macos: { name: 'Division I (macOS Systems & Kernel)', lead: 'Dr. Kai Sterling', specialists: 5 },
    kernel: { name: 'Division 04 (Kernel & Ring 0)', lead: 'Samantha Reed', specialists: 5 },
    audio: { name: 'Division H (Audio DSP Systems)', lead: 'Dr. Julian Vance', specialists: 7 },
    web3: { name: 'Division B (Applied Cryptography & Web3)', lead: 'Dr. Leon Nash', specialists: 6 },
    sap: { name: 'Division F (Enterprise SAP S/4HANA & WMS)', lead: 'Dr. Hans Schmidt', specialists: 4 },
    cyber: { name: 'Omniverse Code (Offensive Cyber & Exploit Synthesis)', lead: 'Prof. Lucas Mercer', specialists: 6 },
    osint: { name: 'Division G (Sovereign OSINT & Reconnaissance)', lead: 'Dr. Morgan Cross', specialists: 6 },
    casino: { name: 'Division E (Casino Gaming & Provably Fair Math)', lead: 'Viktor Kane', specialists: 4 },
    ai: { name: 'Division D (Frontier AI Agentics & PRM Reasoning)', lead: 'Dr. Aris Thorne', specialists: 6 }
  };

  function updateAllocation() {
    let totalSpecialists = 4; // Base Executive & Review Pod
    const activePods = [
      { name: 'Executive Suite & 4-Tier Code Review', lead: 'Dr. Alexander Vance (CEO)', specialists: 4 }
    ];

    checkboxes.forEach(cb => {
      if (cb.checked && podMap[cb.value]) {
        const p = podMap[cb.value];
        activePods.push(p);
        totalSpecialists += p.specialists;
      }
    });

    if (countDisplay) {
      countDisplay.textContent = totalSpecialists;
    }

    if (podsListContainer) {
      podsListContainer.innerHTML = activePods.map(p => `
        <div class="allocated-pod-pill">
          <strong>${p.name}</strong> • Lead: ${p.lead} (+${p.specialists} Specialists)
        </div>
      `).join('');
    }
  }

  checkboxes.forEach(cb => {
    cb.addEventListener('change', () => {
      soundEngine.playClick();
      updateAllocation();
    });
  });

  if (submitBtn) {
    submitBtn.addEventListener('click', (e) => {
      e.preventDefault();
      soundEngine.playChime();
      if (confirmationBanner) {
        confirmationBanner.style.display = 'block';
        confirmationBanner.scrollIntoView({ behavior: 'smooth' });
      }
    });
  }

  updateAllocation();
}

/* --------------------------------------------------------------------------
   Navigation & Smooth Scroll
   -------------------------------------------------------------------------- */
function initNavigation() {
  const links = document.querySelectorAll('.nav-links a');

  links.forEach(link => {
    link.addEventListener('click', (e) => {
      const targetId = link.getAttribute('href');
      if (targetId && targetId.startsWith('#')) {
        e.preventDefault();
        const targetEl = document.querySelector(targetId);
        if (targetEl) {
          targetEl.scrollIntoView({ behavior: 'smooth' });
        }
      }
    });
  });
}
