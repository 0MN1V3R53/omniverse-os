/* ==============================================================================
   OMNIVERSE OS - MASTER DESKTOP CONTROLLER & TELEMETRY ENGINE
   ============================================================================== */

const API_BASE = "http://127.0.0.1:8998";
let highestZ = 100;
let dragTarget = null;
let dragOffset = { x: 0, y: 0 };
let commandHistory = [];
let historyIndex = -1;

// Audio Subsystem & WebAudio Synthesizer
let audioCtx = null;
let masterVolume = 0.85;
let isMuted = false;

// Open Windows Tracking for Taskbar
const openWindows = new Map(); // winId -> { title: string, iconClass: string, isMinimized: boolean }

const APP_METADATA = {
  "taskmgr": { title: "Task Manager", icon: "taskmgr-small" },
  "devmgmt": { title: "Device Manager", icon: "devmgmt-small" },
  "bench": { title: "Core Diagnostics", icon: "bench-small" },
  "terminal": { title: "PowerShell", icon: "terminal-small" },
  "explorer": { title: "File Explorer", icon: "explorer-small" },
  "directstorage": { title: "DirectStorage", icon: "directstorage-small" },
  "browser": { title: "Chromium Browser", icon: "browser-small" },
  "settings": { title: "Settings", icon: "settings-small" }
};

document.addEventListener("DOMContentLoaded", () => {
  initClock();
  initCpuGrid();
  initDeviceManagerTree();
  initBackgroundCanvas();
  startTelemetryPolling();
  loadAppCatalog();
  switchSettingsCategory("system");

  // Open Task Manager and Chromium Browser by default
  openWindow("taskmgr");
});

// Sound Effects Synthesizer
function initAudio() {
  if (!audioCtx) {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    audioCtx = new AudioContext();
  }
}

function playSystemSound(freq = 440, type = "sine", duration = 0.08) {
  if (isMuted) return;
  try {
    initAudio();
    if (audioCtx.state === "suspended") audioCtx.resume();

    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = type;
    osc.frequency.setValueAtTime(freq, audioCtx.currentTime);

    gain.gain.setValueAtTime(masterVolume * 0.15, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + duration);

    osc.connect(gain);
    gain.connect(audioCtx.destination);

    osc.start();
    osc.stop(audioCtx.currentTime + duration);
  } catch (e) {}
}

function playWindowClick() {
  playSystemSound(600, "triangle", 0.05);
}

function playSuccessChime() {
  playSystemSound(523.25, "sine", 0.1);
  setTimeout(() => playSystemSound(659.25, "sine", 0.12), 60);
  setTimeout(() => playSystemSound(783.99, "sine", 0.18), 120);
}

// Acrylic Notification Toast System
function showNotification(title, message, icon = "🔔") {
  playSuccessChime();
  const container = document.getElementById("notificationContainer");
  if (!container) return;

  const toast = document.createElement("div");
  toast.className = "notification-toast";
  toast.innerHTML = `
    <div class="toast-icon">${icon}</div>
    <div class="toast-body">
      <div class="toast-title">${title}</div>
      <div class="toast-desc">${message}</div>
    </div>
  `;
  container.appendChild(toast);

  setTimeout(() => {
    toast.classList.add("hide");
    setTimeout(() => toast.remove(), 350);
  }, 4500);
}

// Clock in Taskbar
function initClock() {
  const update = () => {
    const now = new Date();
    const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const dateStr = now.toLocaleDateString([], { month: '2-digit', day: '2-digit', year: 'numeric' });
    const cTime = document.getElementById("clockTime");
    const cDate = document.getElementById("clockDate");
    if (cTime) cTime.textContent = timeStr;
    if (cDate) cDate.textContent = dateStr;
  };
  update();
  setInterval(update, 1000);
}

// 192-Thread CPU Heatmap Grid
function initCpuGrid() {
  const container = document.getElementById("cpuCoresGrid");
  if (!container) return;
  container.innerHTML = "";

  for (let i = 0; i < 192; i++) {
    const cell = document.createElement("div");
    cell.className = "core-cell";
    cell.id = `core-cell-${i}`;
    cell.textContent = i + 1;
    cell.title = `Thread #${i + 1} (CCD ${Math.floor(i / 16)}): 0.0%`;
    container.appendChild(cell);
  }
}

// Device Manager Tree Initialization
function initDeviceManagerTree() {
  const cpuList = document.getElementById("tree-cpu-list");
  if (!cpuList) return;
  cpuList.innerHTML = "";

  for (let i = 0; i < 192; i++) {
    const leaf = document.createElement("div");
    leaf.className = "tree-leaf";
    leaf.innerHTML = `<span class="tree-icon leaf-icon"></span>AMD Ryzen Threadripper PRO 9995WX (Logical Processor ${i + 1} of 192 @ 5.40 GHz)`;
    cpuList.appendChild(leaf);
  }
}

function toggleTreeNode(toggleBtn) {
  const node = toggleBtn.parentElement;
  const children = node.querySelector(".tree-children");
  if (!children) return;

  if (children.style.display === "none" || children.style.display === "") {
    children.style.display = "block";
    toggleBtn.textContent = "▼";
  } else {
    children.style.display = "none";
    toggleBtn.textContent = "▶";
  }
}

// Window Management & Taskbar Synchronization
function bringToFront(winId) {
  const win = document.getElementById(`win-${winId}`);
  if (!win) return;
  highestZ += 1;
  win.style.zIndex = highestZ;

  // Update active state in taskbar
  updateTaskbarActive(winId);
}

function openWindow(winId) {
  const win = document.getElementById(`win-${winId}`);
  if (!win) return;
  win.classList.remove("minimized");
  win.style.display = "flex";
  bringToFront(winId);
  playWindowClick();

  // Register in openWindows
  const meta = APP_METADATA[winId] || { title: winId, icon: "taskmgr-small" };
  openWindows.set(winId, { ...meta, isMinimized: false });
  renderTaskbarApps();

  if (winId === "taskmgr") {
    fetchProcesses();
  }
}

function closeWindow(winId) {
  const win = document.getElementById(`win-${winId}`);
  if (!win) return;
  win.style.display = "none";
  playWindowClick();

  openWindows.delete(winId);
  renderTaskbarApps();
}

function minimizeWindow(winId) {
  const win = document.getElementById(`win-${winId}`);
  if (!win) return;
  win.classList.add("minimized");
  playWindowClick();

  if (openWindows.has(winId)) {
    openWindows.get(winId).isMinimized = true;
  }
  renderTaskbarApps();
}

function maximizeWindow(winId) {
  const win = document.getElementById(`win-${winId}`);
  if (!win) return;
  playWindowClick();

  if (win.dataset.maximized === "true") {
    win.style.top = win.dataset.prevTop || "50px";
    win.style.left = win.dataset.prevLeft || "50px";
    win.style.width = win.dataset.prevWidth || "800px";
    win.style.height = win.dataset.prevHeight || "600px";
    win.dataset.maximized = "false";
  } else {
    win.dataset.prevTop = win.style.top;
    win.dataset.prevLeft = win.style.left;
    win.dataset.prevWidth = win.style.width;
    win.dataset.prevHeight = win.style.height;

    win.style.top = "0px";
    win.style.left = "0px";
    win.style.width = "100vw";
    win.style.height = "calc(100vh - 48px)";
    win.dataset.maximized = "true";
  }
  bringToFront(winId);
}

// Render dynamic running apps in taskbar
function renderTaskbarApps() {
  const container = document.getElementById("taskbarRunningApps");
  if (!container) return;
  container.innerHTML = "";

  openWindows.forEach((data, winId) => {
    const btn = document.createElement("button");
    btn.className = `taskbar-app-btn ${data.isMinimized ? "minimized" : "active"}`;
    btn.title = data.title;
    btn.innerHTML = `<span class="icon-img ${data.icon}"></span>`;
    btn.onclick = () => handleTaskbarAppClick(winId);
    container.appendChild(btn);
  });
}

function handleTaskbarAppClick(winId) {
  const win = document.getElementById(`win-${winId}`);
  if (!win) return;

  const data = openWindows.get(winId);
  if (!data) return;

  if (data.isMinimized) {
    win.classList.remove("minimized");
    win.style.display = "flex";
    data.isMinimized = false;
    bringToFront(winId);
  } else {
    // If already top, minimize; otherwise bring to front
    const currentZ = parseInt(win.style.zIndex || "0", 10);
    if (currentZ === highestZ) {
      minimizeWindow(winId);
    } else {
      bringToFront(winId);
    }
  }
  renderTaskbarApps();
}

function updateTaskbarActive(activeWinId) {
  const container = document.getElementById("taskbarRunningApps");
  if (!container) return;
  // Visual highlight is driven by highestZ and openWindows state
}

// Window Dragging
function startDrag(e, winId) {
  const win = document.getElementById(winId);
  if (!win || win.dataset.maximized === "true") return;

  bringToFront(winId.replace("win-", ""));
  dragTarget = win;
  const rect = win.getBoundingClientRect();
  dragOffset.x = e.clientX - rect.left;
  dragOffset.y = e.clientY - rect.top;

  document.addEventListener("mousemove", onDrag);
  document.addEventListener("mouseup", stopDrag);
}

function onDrag(e) {
  if (!dragTarget) return;
  const x = Math.max(0, Math.min(window.innerWidth - 100, e.clientX - dragOffset.x));
  const y = Math.max(0, Math.min(window.innerHeight - 80, e.clientY - dragOffset.y));
  dragTarget.style.left = `${x}px`;
  dragTarget.style.top = `${y}px`;
}

function stopDrag() {
  dragTarget = null;
  document.removeEventListener("mousemove", onDrag);
  document.removeEventListener("mouseup", stopDrag);
}

// Start Menu & Flyouts
function toggleStartMenu() {
  const menu = document.getElementById("startMenu");
  const searchFlyout = document.getElementById("searchFlyout");
  const volumeFlyout = document.getElementById("volumeFlyout");
  if (searchFlyout) searchFlyout.classList.remove("open");
  if (volumeFlyout) volumeFlyout.classList.remove("open");
  if (menu) menu.classList.toggle("open");
}

function toggleSearchFlyout() {
  const searchFlyout = document.getElementById("searchFlyout");
  const menu = document.getElementById("startMenu");
  const volumeFlyout = document.getElementById("volumeFlyout");
  if (menu) menu.classList.remove("open");
  if (volumeFlyout) volumeFlyout.classList.remove("open");

  if (searchFlyout) {
    searchFlyout.classList.toggle("open");
    if (searchFlyout.classList.contains("open")) {
      const inp = document.getElementById("spotlightInput");
      if (inp) { inp.value = ""; inp.focus(); }
      handleSpotlightSearch("");
    }
  }
}

function toggleVolumeFlyout() {
  const volumeFlyout = document.getElementById("volumeFlyout");
  const menu = document.getElementById("startMenu");
  const searchFlyout = document.getElementById("searchFlyout");
  if (menu) menu.classList.remove("open");
  if (searchFlyout) searchFlyout.classList.remove("open");
  if (volumeFlyout) volumeFlyout.classList.toggle("open");
}

document.addEventListener("click", (e) => {
  const menu = document.getElementById("startMenu");
  const startBtn = document.querySelector(".start-btn");
  if (menu && startBtn && !menu.contains(e.target) && !startBtn.contains(e.target) && menu.classList.contains("open")) {
    menu.classList.remove("open");
  }

  const searchFlyout = document.getElementById("searchFlyout");
  const searchBtn = document.querySelector(".search-btn");
  if (searchFlyout && searchBtn && !searchFlyout.contains(e.target) && !searchBtn.contains(e.target) && searchFlyout.classList.contains("open")) {
    searchFlyout.classList.remove("open");
  }

  const volumeFlyout = document.getElementById("volumeFlyout");
  const trayVolIcon = document.querySelector(".tray-icon:nth-child(2)");
  if (volumeFlyout && trayVolIcon && !volumeFlyout.contains(e.target) && !trayVolIcon.contains(e.target) && volumeFlyout.classList.contains("open")) {
    volumeFlyout.classList.remove("open");
  }
});

// Spotlight Live Search
const SEARCH_DATABASE = [
  { name: "Task Manager", type: "System App", target: "taskmgr", icon: "📊", desc: "Monitor 192 cores, 512GB DDR5, NVMe RAID, and RTX 5090" },
  { name: "Device Manager", type: "Hardware", target: "devmgmt", icon: "⚙️", desc: "Inspect AMD WRX90 platform, 128 PCIe 5.0 lanes" },
  { name: "Core Diagnostics & Benchmarks", type: "Benchmarking", target: "bench", icon: "⚡", desc: "Run AVX-512 GEMM, STREAM memory, NVMe 58 GB/s tests" },
  { name: "Chromium Web Browser", type: "Web & Store", target: "browser", icon: "🌐", desc: "Browse open web and download software into Omniverse OS" },
  { name: "PowerShell 7.5", type: "Terminal", target: "terminal", icon: ">_", desc: "Execute kernel directives and hardware diagnostics" },
  { name: "File Explorer", type: "Filesystem", target: "explorer", icon: "📁", desc: "Explore 16TB NVMe DirectStorage array" },
  { name: "DirectStorage 1.2 Monitor", type: "Storage", target: "directstorage", icon: "🚀", desc: "BypassIO PCIe 5.0 DMA GPU streaming status" },
  { name: "System Settings", type: "Settings", target: "settings", icon: "⚙️", desc: "Unified Windows & macOS display, sound, network, and security" },
  { name: "Audio Codecs & Volume", type: "Hardware", target: "settings", icon: "🔊", desc: "Realtek ALC4080 + ESS SABRE 384kHz 32-bit Float DAC" },
  { name: "NVIDIA RTX 5090 Blackwell", type: "GPU", target: "devmgmt", icon: "🎮", desc: "21,760 CUDA cores, 680 Tensor Cores, 32GB GDDR7" }
];

function handleSpotlightSearch(query) {
  const resultsBox = document.getElementById("spotlightResults");
  if (!resultsBox) return;
  resultsBox.innerHTML = "";

  const q = query.trim().toLowerCase();
  const matched = q === "" ? SEARCH_DATABASE.slice(0, 6) : SEARCH_DATABASE.filter(item => 
    item.name.toLowerCase().includes(q) || item.desc.toLowerCase().includes(q) || item.type.toLowerCase().includes(q)
  );

  matched.forEach(item => {
    const el = document.createElement("div");
    el.className = "search-result-item";
    el.innerHTML = `
      <span style="font-size: 20px;">${item.icon}</span>
      <div class="search-res-info">
        <span class="search-res-name">${item.name}</span>
        <span class="search-res-sub">${item.type} — ${item.desc}</span>
      </div>
    `;
    el.onclick = () => {
      openWindow(item.target);
      const sf = document.getElementById("searchFlyout");
      if (sf) sf.classList.remove("open");
    };
    resultsBox.appendChild(el);
  });
}

function openSearchWithQuery(q) {
  toggleSearchFlyout();
  const inp = document.getElementById("spotlightInput");
  if (inp) {
    inp.value = q;
    handleSpotlightSearch(q);
  }
}

// Audio Control
function handleVolumeSlider(val) {
  masterVolume = parseInt(val, 10) / 100.0;
  const label = document.getElementById("volPercentLabel");
  if (label) label.textContent = `${val}%`;

  fetch(`${API_BASE}/api/audio/configure`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ volume: parseInt(val, 10), mute: isMuted })
  }).catch(() => {});
}

function toggleAudioMute() {
  isMuted = !isMuted;
  const icon = document.getElementById("muteIconBtn");
  if (icon) icon.textContent = isMuted ? "🔇" : "🔊";
}

// Chromium Browser Operations
function switchBrowserTab(tab) {
  const webTab = document.getElementById("btab-web");
  const appsTab = document.getElementById("btab-apps");
  const webPane = document.getElementById("browser-pane-web");
  const appsPane = document.getElementById("browser-pane-apps");

  if (tab === "web") {
    webTab.classList.add("active");
    appsTab.classList.remove("active");
    webPane.style.display = "block";
    appsPane.style.display = "none";
  } else {
    webTab.classList.remove("active");
    appsTab.classList.add("active");
    webPane.style.display = "none";
    appsPane.style.display = "block";
    loadAppCatalog();
  }
}

function handleBrowserKey(e) {
  if (e.key === "Enter") {
    navigateBrowser();
  }
}

function navigateBrowser() {
  const inp = document.getElementById("browserUrlInput");
  const iframe = document.getElementById("browserIframe");
  if (!inp || !iframe) return;

  let url = inp.value.trim();
  if (!url) return;

  if (!url.startsWith("http://") && !url.startsWith("https://")) {
    if (url.includes(".") && !url.includes(" ")) {
      url = "https://" + url;
    } else {
      url = `https://duckduckgo.com/?q=${encodeURIComponent(url)}`;
    }
  }

  inp.value = url;
  iframe.src = url;
}

function browserGoBack() {
  const iframe = document.getElementById("browserIframe");
  if (iframe) iframe.contentWindow?.history.back();
}

function browserGoForward() {
  const iframe = document.getElementById("browserIframe");
  if (iframe) iframe.contentWindow?.history.forward();
}

function browserReload() {
  const iframe = document.getElementById("browserIframe");
  if (iframe) iframe.src = iframe.src;
}

// Software Center / App Catalog
async function loadAppCatalog() {
  const grid = document.getElementById("appCatalogGrid");
  if (!grid) return;

  try {
    const res = await fetch(`${API_BASE}/api/apps/catalog`);
    if (!res.ok) return;
    const data = await res.json();
    grid.innerHTML = "";

    data.catalog.forEach(app => {
      const card = document.createElement("div");
      card.className = "app-catalog-card";
      card.innerHTML = `
        <div>
          <div class="app-card-title">${app.name}</div>
          <div class="app-card-meta">${app.category} • v${app.version} (${app.size_mb} MB)</div>
          <p class="app-card-desc" style="margin-top:8px;">${app.description}</p>
        </div>
        <button class="btn-primary" style="padding:6px 14px; font-size:12px;" onclick="installSoftware('${app.id}', '${app.name}', this)">
          ${app.installed ? "✓ Installed" : "📥 Install to NVMe"}
        </button>
      `;
      grid.appendChild(card);
    });
  } catch (err) {}
}

async function installSoftware(id, name, btnEl) {
  btnEl.textContent = "⏳ Installing...";
  btnEl.disabled = true;

  try {
    const res = await fetch(`${API_BASE}/api/apps/install`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id, name })
    });

    if (res.ok) {
      playSuccessChime();
      btnEl.textContent = "✓ Installed";
      btnEl.style.background = "var(--accent-green)";

      // Append notification to desktop
      showNotification('Omniverse App Center', `Successfully installed '${name}' to C:\\Program Files\\Omniverse\\${id}\\! Ready for execution across all 192 cores.`, '📥');
      fetchProcesses();
    }
  } catch (err) {
    btnEl.textContent = "Install to NVMe";
    btnEl.disabled = false;
  }
}

// Settings Categories
function switchSettingsCategory(cat) {
  document.querySelectorAll(".settings-nav-item").forEach(item => item.classList.remove("active"));
  const items = Array.from(document.querySelectorAll(".settings-nav-item"));
  const activeItem = items.find(i => i.getAttribute("onclick")?.includes(cat));
  if (activeItem) activeItem.classList.add("active");

  const content = document.getElementById("settingsContent");
  if (!content) return;

  if (cat === "system") {
    content.innerHTML = `
      <div class="settings-section-title">System & Display Specifications</div>
      <div class="settings-section-sub">Omniverse OS Workstation Edition (Build 2026.9995 - 64-bit Sovereign Substrate)</div>

      <div class="settings-card">
        <div class="settings-card-info">
          <h4>Display Resolution & Refresh Rate</h4>
          <p>3840 x 2160 UHD (4K) @ 240 Hz • High Dynamic Range (HDR10+)</p>
        </div>
        <select style="background:#131b2e; color:#fff; border:1px solid var(--border-acrylic); padding:6px 12px; border-radius:6px;">
          <option>3840 x 2160 @ 240 Hz (Recommended)</option>
          <option>2560 x 1440 @ 360 Hz</option>
          <option>1920 x 1080 @ 500 Hz</option>
        </select>
      </div>

      <div class="settings-card">
        <div class="settings-card-info">
          <h4>Processor Microarchitecture</h4>
          <p>AMD Ryzen Threadripper PRO 9995WX (96 Cores / 192 Threads @ 5.40 GHz Boost)</p>
        </div>
        <button class="btn-card" onclick="openWindow('taskmgr')">Open Task Manager</button>
      </div>

      <div class="settings-card">
        <div class="settings-card-info">
          <h4>Physical System Memory</h4>
          <p>512 GB Octa-Channel DDR5-6400 ECC Registered RDIMM (409.6 GB/s)</p>
        </div>
        <span style="color:var(--accent-green); font-weight:600; font-size:12px;">SEC-DED Protected</span>
      </div>

      <div class="settings-card">
        <div class="settings-card-info">
          <h4>DirectStorage NVMe Storage</h4>
          <p>16.0 TB High-Speed Scratch Array (4x 4TB Crucial T705 RAID 0 @ 58 GB/s)</p>
        </div>
        <span style="color:var(--accent-cyan); font-weight:600; font-size:12px;">BypassIO Active</span>
      </div>
    `;
  } else if (cat === "hardware") {
    content.innerHTML = `
      <div class="settings-section-title">Zen 5 CPU & WRX90 Platform Topology</div>
      <div class="settings-section-sub">Hardware Abstraction Layer & Core Thread Grouping</div>

      <div class="settings-card">
        <div class="settings-card-info">
          <h4>Unified 256-Bit Affinity Dispatcher</h4>
          <p>Overrides legacy Windows 64-core Processor Groups. All 192 threads execute simultaneously.</p>
        </div>
        <label class="toggle-switch">
          <input type="checkbox" checked disabled>
          <span class="toggle-slider"></span>
        </label>
      </div>

      <div class="settings-card">
        <div class="settings-card-info">
          <h4>Dual 512-bit AVX-512 FMA Pipelines</h4>
          <p>Hardware vector execution on Zen 5 cores sustaining 29.62 TFLOPS GEMM throughput.</p>
        </div>
        <span style="color:var(--accent-green); font-weight:600; font-size:12px;">HARDWARE_ENABLED</span>
      </div>

      <div class="settings-card">
        <div class="settings-card-info">
          <h4>ASUS WRX90 SAGE Motherboard 128 PCIe 5.0 Lanes</h4>
          <p>Full x16 bandwidth across all 7 physical expansion slots (504.06 GB/s aggregate bus).</p>
        </div>
        <button class="btn-card" onclick="openWindow('devmgmt')">Audit PCIe Bus</button>
      </div>
    `;
  } else if (cat === "graphics") {
    content.innerHTML = `
      <div class="settings-section-title">NVIDIA GeForce RTX 5090 Blackwell</div>
      <div class="settings-section-sub">WDDM 3.3 GPU Driver & AI Acceleration Engine</div>

      <div class="settings-card">
        <div class="settings-card-info">
          <h4>Hardware Accelerated GPU Scheduling (HAGS)</h4>
          <p>Direct BAR memory mapping reducing frame and compute dispatch latency to sub-microsecond levels.</p>
        </div>
        <label class="toggle-switch">
          <input type="checkbox" checked>
          <span class="toggle-slider"></span>
        </label>
      </div>

      <div class="settings-card">
        <div class="settings-card-info">
          <h4>5th-Generation Blackwell Tensor Cores</h4>
          <p>680 Tensor Cores delivering 3,320 TFLOPS FP8/FP4 AI transformer acceleration.</p>
        </div>
        <button class="btn-card" onclick="openWindow('bench')">Run Tensor Benchmark</button>
      </div>

      <div class="settings-card">
        <div class="settings-card-info">
          <h4>32 GB GDDR7 Video Memory</h4>
          <p>512-bit Memory Bus @ 28 Gbps (1,792 GB/s Peak Bandwidth)</p>
        </div>
        <span style="color:var(--accent-cyan); font-weight:600; font-size:12px;">Optimal Speed</span>
      </div>
    `;
  } else if (cat === "sound") {
    content.innerHTML = `
      <div class="settings-section-title">High-Definition Audio & Hardware Codecs</div>
      <div class="settings-section-sub">Realtek ALC4080 + ESS SABRE 9018Q2C DAC Architecture</div>

      <div class="settings-card">
        <div class="settings-card-info">
          <h4>Master DAC Sample Rate & Bit Depth</h4>
          <p>32-bit Floating Point @ 384,000 Hz (Audiophile Reference Grade Studio DAC)</p>
        </div>
        <span style="color:var(--accent-green); font-weight:600; font-size:12px;">384 kHz / 32-bit Float</span>
      </div>

      <div class="settings-card">
        <div class="settings-card-info">
          <h4>Hardware Lossless Codec Stack</h4>
          <p>PCM 32-bit (0.4ms), FLAC 24-bit 192kHz (0.8ms), Opus 1.4 Low-Latency, AAC-LC, Dolby Atmos Spatial</p>
        </div>
        <span style="color:var(--accent-cyan); font-weight:600; font-size:12px;">All Codecs Online</span>
      </div>

      <div class="settings-card">
        <div class="settings-card-info">
          <h4>System Sound Effects & Synthesizer</h4>
          <p>Play acoustic audio feedback on window events, clicks, and core diagnostic triggers.</p>
        </div>
        <label class="toggle-switch">
          <input type="checkbox" checked onchange="isMuted = !this.checked">
          <span class="toggle-slider"></span>
        </label>
      </div>
    `;
  } else if (cat === "network") {
    content.innerHTML = `
      <div class="settings-section-title">Network & Connectivity</div>
      <div class="settings-section-sub">Intel X710-AT2 Dual 10GbE + Wi-Fi 7 Substrate Adapter</div>

      <div class="settings-card">
        <div class="settings-card-info">
          <h4>Ethernet 1 (Intel X710-AT2 10GbE)</h4>
          <p>Link Speed: 10,000 / 10,000 Mbps • Full Duplex • Hardware Packet Filtering</p>
        </div>
        <span style="color:var(--accent-green); font-weight:600; font-size:12px;">CONNECTED</span>
      </div>

      <div class="settings-card">
        <div class="settings-card-info">
          <h4>IPv4 / IPv6 Substrate Routing</h4>
          <p>Low-latency P2P encrypted socket bridge to AetherCore 999 cluster</p>
        </div>
        <span style="color:var(--accent-cyan); font-weight:600; font-size:12px;">Sub-millisecond</span>
      </div>
    `;
  } else if (cat === "personalization") {
    content.innerHTML = `
      <div class="settings-section-title">Personalization & Omniverse Aesthetics</div>
      <div class="settings-section-sub">Select Desktop Wallpaper, Acrylic Themes, and Accent Colors</div>

      <div class="settings-card">
        <div class="settings-card-info">
          <h4>Active Wallpaper</h4>
          <p>Omniverse Hub 7 — Celestial Quantum Matrix (8K Cyberpunk Celestial Vista)</p>
        </div>
        <button class="btn-card" onclick="showNotification('Personalization Engine', 'Omniverse Hub 7 8K celestial wallpaper is active across all workspaces.', '🎨')">Set Active</button>
      </div>

      <div class="settings-card">
        <div class="settings-card-info">
          <h4>Acrylic Glassmorphism Blur</h4>
          <p>36px Gaussian Backdrop Filter with Dynamic Saturation Boost</p>
        </div>
        <label class="toggle-switch">
          <input type="checkbox" checked disabled>
          <span class="toggle-slider"></span>
        </label>
      </div>
    `;
  } else if (cat === "update") {
    content.innerHTML = `
      <div class="settings-section-title">Omniverse OS Update & Kernel Integrity</div>
      <div class="settings-section-sub">Sovereign Substrate Build Synchronization</div>

      <div class="settings-card">
        <div class="settings-card-info">
          <h4>Kernel Version 12.0.2026.9995</h4>
          <p>You are up to date. Last verified: ${new Date().toLocaleTimeString()} (Zero-Drift Invariant)</p>
        </div>
        <button class="btn-primary" onclick="showNotification('Omniverse Update', 'Omniverse OS is running the latest 2026 sovereign kernel build (12.0.2026.9995).', '🔄')">Check for Updates</button>
      </div>
    `;
  }
}

// Task Manager Tabs
function switchTaskmgrTab(tabKey) {
  document.querySelectorAll(".nav-tab").forEach(t => t.classList.remove("active"));
  document.querySelectorAll(".tab-pane").forEach(p => p.classList.remove("active"));

  if (tabKey === "perf") {
    document.querySelector(".nav-tab:nth-child(1)").classList.add("active");
    document.getElementById("taskmgr-tab-perf").classList.add("active");
  } else if (tabKey === "procs") {
    document.querySelector(".nav-tab:nth-child(2)").classList.add("active");
    document.getElementById("taskmgr-tab-procs").classList.add("active");
    fetchProcesses();
  } else if (tabKey === "numa") {
    document.querySelector(".nav-tab:nth-child(3)").classList.add("active");
    document.getElementById("taskmgr-tab-numa").classList.add("active");
    fetchNuma();
  }
}

// Performance Metric Selection
function selectPerfMetric(metric) {
  document.querySelectorAll(".perf-card").forEach(c => c.classList.remove("active"));
  document.querySelectorAll(".perf-metric-view").forEach(v => v.style.display = "none");

  const titleEl = document.getElementById("perf-title-text");
  const subEl = document.getElementById("perf-sub-text");

  if (metric === "cpu") {
    document.querySelectorAll(".perf-card")[0].classList.add("active");
    document.getElementById("perf-view-cpu").style.display = "block";
    titleEl.textContent = "AMD Ryzen Threadripper PRO 9995WX 96-Core Processor";
    subEl.textContent = "192 Logical Processors | 12 CCDs | 384MB L3 Cache";
  } else if (metric === "memory") {
    document.querySelectorAll(".perf-card")[1].classList.add("active");
    document.getElementById("perf-view-memory").style.display = "block";
    titleEl.textContent = "512 GB DDR5-6400 ECC Registered RDIMM";
    subEl.textContent = "8 Discrete 64-bit Channels (409.6 GB/s Peak) | SEC-DED Active";
  } else if (metric === "disk") {
    document.querySelectorAll(".perf-card")[2].classList.add("active");
    document.getElementById("perf-view-disk").style.display = "block";
    titleEl.textContent = "16.0 TB PCIe 5.0 NVMe RAID 0 (4x Crucial T705)";
    subEl.textContent = "Phison PS5026-E26 | 55,680 MB/s Sequential Read | 6.2M IOPS";
  } else if (metric === "gpu") {
    document.querySelectorAll(".perf-card")[3].classList.add("active");
    document.getElementById("perf-view-gpu").style.display = "block";
    titleEl.textContent = "NVIDIA GeForce RTX 5090 (Blackwell GB202-300)";
    subEl.textContent = "21,760 CUDA Cores | 680 Tensor Cores | 32 GB GDDR7 (1,792 GB/s)";
  }
}

// Live Telemetry Polling
function startTelemetryPolling() {
  const poll = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/system/telemetry`);
      if (res.ok) {
        const data = await res.json();
        updateTelemetryUI(data);
      }
    } catch (err) {}
  };
  poll();
  setInterval(poll, 1000);
}

function updateTelemetryUI(data) {
  if (!data) return;

  // CPU
  const cpu = data.processor;
  const cpuPct = cpu.aggregate_utilization_pct;
  const sCpu = document.getElementById("sb-cpu-pct");
  const cStat = document.getElementById("cpu-stat-util");
  const aUtil = document.getElementById("active-util-label");
  const cSpeed = document.getElementById("cpu-stat-speed");
  const cProcs = document.getElementById("cpu-stat-procs");
  const cThreads = document.getElementById("cpu-stat-threads");
  const cUptime = document.getElementById("cpu-stat-uptime");

  if (sCpu) sCpu.textContent = `${cpuPct}%`;
  if (cStat) cStat.textContent = `${cpuPct}%`;
  if (aUtil) aUtil.textContent = `Overall: ${cpuPct}%`;
  if (cSpeed) cSpeed.textContent = `${cpu.active_clock_ghz.toFixed(2)} GHz`;
  if (cProcs) cProcs.textContent = cpu.processes_count;
  if (cThreads) cThreads.textContent = cpu.threads_total;
  if (cUptime) cUptime.textContent = data.uptime_formatted;

  // 192 Cores Heatmap
  if (cpu.threads_utilization && cpu.threads_utilization.length === 192) {
    for (let i = 0; i < 192; i++) {
      const cell = document.getElementById(`core-cell-${i}`);
      if (!cell) continue;
      const u = cpu.threads_utilization[i];
      cell.title = `Thread #${i + 1} (CCD ${Math.floor(i / 16)}): ${u}%`;

      if (u < 15) {
        cell.style.backgroundColor = `rgba(14, 165, 233, ${0.2 + (u / 15) * 0.25})`;
      } else if (u < 50) {
        cell.style.backgroundColor = `rgba(99, 102, 241, ${0.4 + (u / 50) * 0.3})`;
      } else if (u < 80) {
        cell.style.backgroundColor = `rgba(245, 158, 11, ${0.6 + (u / 80) * 0.2})`;
      } else {
        cell.style.backgroundColor = `rgba(239, 68, 68, ${0.8 + (u / 100) * 0.2})`;
      }
    }
  }

  // Memory
  const mem = data.memory;
  const sMem = document.getElementById("sb-mem-pct");
  const mUsed = document.getElementById("mem-stat-used");
  const mAvail = document.getElementById("mem-stat-avail");
  if (sMem) sMem.textContent = `${mem.used_gb} GB`;
  if (mUsed) mUsed.textContent = `${mem.used_gb} GB`;
  if (mAvail) mAvail.textContent = `${mem.available_gb} GB`;

  // Disk
  const disk = data.storage;
  const sDisk = document.getElementById("sb-disk-val");
  const dAct = document.getElementById("disk-stat-act");
  const dRead = document.getElementById("disk-stat-read");
  const dWrite = document.getElementById("disk-stat-write");
  if (sDisk) sDisk.textContent = `${disk.active_time_pct}%`;
  if (dAct) dAct.textContent = `${disk.active_time_pct}%`;
  if (dRead) dRead.textContent = `${disk.read_speed_mb_s} MB/s`;
  if (dWrite) dWrite.textContent = `${disk.write_speed_mb_s} MB/s`;

  // GPU
  const gpu = data.graphics;
  const sGpu = document.getElementById("sb-gpu-val");
  const gUtil = document.getElementById("gpu-stat-util");
  const gVram = document.getElementById("gpu-stat-vram");
  if (sGpu) sGpu.textContent = `${gpu.gpu_utilization_pct}%`;
  if (gUtil) gUtil.textContent = `${gpu.gpu_utilization_pct}%`;
  if (gVram) gVram.textContent = `${gpu.vram_used_gb} / ${gpu.vram_total_gb} GB`;
}

// Fetch Processes Table
async function fetchProcesses() {
  try {
    const res = await fetch(`${API_BASE}/api/processes`);
    if (!res.ok) return;
    const data = await res.json();
    const tbody = document.getElementById("procsTableBody");
    if (!tbody) return;

    tbody.innerHTML = "";
    data.processes.forEach(p => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td><strong>${p.name}</strong></td>
        <td>${p.pid}</td>
        <td><span style="color:var(--accent-green)">${p.status}</span></td>
        <td>${p.cpu_pct}%</td>
        <td>${p.memory_mb.toFixed(1)} MB</td>
        <td>${p.disk_mb_s > 0 ? p.disk_mb_s.toFixed(1) + " MB/s" : "0 MB/s"}</td>
        <td>${p.gpu_pct > 0 ? p.gpu_pct.toFixed(1) + "%" : "0%"}</td>
        <td>${p.threads}</td>
      `;
      tbody.appendChild(row);
    });
  } catch (err) {}
}

// Fetch NUMA Nodes
async function fetchNuma() {
  try {
    const res = await fetch(`${API_BASE}/api/memory/vmm`);
    if (!res.ok) return;
    const data = await res.json();
    const grid = document.getElementById("numaGrid");
    if (!grid) return;

    grid.innerHTML = "";
    data.numa_nodes.forEach(n => {
      const card = document.createElement("div");
      card.className = "bench-card";
      card.innerHTML = `
        <div class="bench-card-header">
          <span class="badge badge-ram">NUMA Node ${n.node_id}</span>
          <h3>128 GB Interleaved Arena</h3>
        </div>
        <div class="bench-metric-row">
          <span>Assigned CCDs:</span>
          <strong>CCDs ${n.associated_ccds.join(", ")} (24C / 48T)</strong>
        </div>
        <div class="bench-metric-row">
          <span>Allocated Memory:</span>
          <strong>${n.used_ram_gb} GB / ${n.total_ram_gb} GB</strong>
        </div>
        <div class="bench-metric-row">
          <span>Bus Saturation:</span>
          <strong>${n.bandwidth_saturation_pct}% (102.4 GB/s)</strong>
        </div>
      `;
      grid.appendChild(card);
    });
  } catch (err) {}
}

// Benchmark Execution
async function triggerBenchmark(testType) {
  playSystemSound(700, "square", 0.08);
  const logEl = document.getElementById("benchConsoleLog");
  logEl.textContent = `[*] Dispatching ${testType.toUpperCase()} test to Omniverse HAL Substrate...\n`;

  try {
    const res = await fetch(`${API_BASE}/api/benchmark/run`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ test: testType })
    });

    if (!res.ok) {
      logEl.textContent += `[-] Benchmark dispatch failed: HTTP ${res.status}\n`;
      return;
    }

    playSuccessChime();
    const data = await res.json();
    logEl.textContent += `[+] Benchmark Execution Successful!\n`;
    logEl.textContent += JSON.stringify(data, null, 2);

    if (data.cpu_avx512_result) {
      document.getElementById("bm-cpu-tflops").textContent = `${data.cpu_avx512_result.effective_throughput_tflops} TFLOPS`;
    }
    if (data.octa_channel_ram_result) {
      document.getElementById("bm-ram-bw").textContent = `${data.octa_channel_ram_result.average_bandwidth_gb_s} GB/s`;
    }
    if (data.nvme_raid0_storage_result) {
      document.getElementById("bm-disk-write").textContent = `${data.nvme_raid0_storage_result.write_speed_mb_s} MB/s`;
    }
    if (data.rtx5090_blackwell_result) {
      document.getElementById("bm-gpu-speed").textContent = `${data.rtx5090_blackwell_result.simulated_throughput_tokens_per_sec} tokens/s`;
    }
  } catch (err) {
    logEl.textContent += `[-] Error communicating with kernel daemon: ${err}\n`;
  }
}

// Terminal Execution
async function handleTermKey(e) {
  const input = document.getElementById("termInput");
  const output = document.getElementById("termOutput");

  if (e.key === "Enter") {
    const cmd = input.value.trim();
    if (!cmd) return;

    playSystemSound(400, "triangle", 0.03);
    commandHistory.push(cmd);
    historyIndex = commandHistory.length;

    output.textContent += `\nPS C:\\Omniverse> ${cmd}\n`;
    input.value = "";

    if (cmd.toLowerCase() === "cls" || cmd.toLowerCase() === "clear") {
      output.textContent = "Omniverse OS PowerShell 7.5\n";
      return;
    }

    try {
      const res = await fetch(`${API_BASE}/api/terminal/execute`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ command: cmd })
      });

      if (res.ok) {
        const data = await res.json();
        if (data.is_json) {
          output.textContent += JSON.stringify(data.output, null, 2) + "\n";
        } else {
          output.textContent += data.output + "\n";
        }
      } else {
        output.textContent += `[-] Command failed: HTTP ${res.status}\n`;
      }
    } catch (err) {
      output.textContent += `[-] Error: ${err}\n`;
    }

    const body = document.querySelector(".terminal-body");
    if (body) body.scrollTop = body.scrollHeight;
  } else if (e.key === "ArrowUp") {
    if (historyIndex > 0) {
      historyIndex--;
      input.value = commandHistory[historyIndex];
    }
  } else if (e.key === "ArrowDown") {
    if (historyIndex < commandHistory.length - 1) {
      historyIndex++;
      input.value = commandHistory[historyIndex];
    } else {
      historyIndex = commandHistory.length;
      input.value = "";
    }
  }
}

// Background Substrate Particle Animation
function initBackgroundCanvas() {
  const canvas = document.getElementById("bgCanvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");

  let w = (canvas.width = window.innerWidth);
  let h = (canvas.height = window.innerHeight);

  window.addEventListener("resize", () => {
    w = canvas.width = window.innerWidth;
    h = canvas.height = window.innerHeight;
  });

  const particles = [];
  for (let i = 0; i < 35; i++) {
    particles.push({
      x: Math.random() * w,
      y: Math.random() * h,
      vx: (Math.random() - 0.5) * 0.35,
      vy: (Math.random() - 0.5) * 0.35,
      radius: Math.random() * 2 + 1,
      alpha: Math.random() * 0.3 + 0.1
    });
  }

  function render() {
    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = "rgba(0, 242, 254, 0.22)";

    for (let p of particles) {
      p.x += p.vx;
      p.y += p.vy;

      if (p.x < 0) p.x = w;
      if (p.x > w) p.x = 0;
      if (p.y < 0) p.y = h;
      if (p.y > h) p.y = 0;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
      ctx.fill();
    }
    requestAnimationFrame(render);
  }
  render();
}
