/* ==============================================================================
   OMNIVERSE OS - DESKTOP CONTROLLER & TELEMETRY ENGINE
   ============================================================================== */

const API_BASE = "http://127.0.0.1:8998";
let highestZ = 100;
let dragTarget = null;
let dragOffset = { x: 0, y: 0 };
let commandHistory = [];
let historyIndex = -1;

// Initialize Desktop
document.addEventListener("DOMContentLoaded", () => {
  initClock();
  initCpuGrid();
  initDeviceManagerTree();
  initBackgroundCanvas();
  startTelemetryPolling();

  // Open Task Manager by default
  openWindow("taskmgr");
});

// Clock in Taskbar
function initClock() {
  const update = () => {
    const now = new Date();
    const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const dateStr = now.toLocaleDateString([], { month: '2-digit', day: '2-digit', year: 'numeric' });
    document.getElementById("clockTime").textContent = timeStr;
    document.getElementById("clockDate").textContent = dateStr;
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

// Window Management
function bringToFront(winId) {
  const win = document.getElementById(`win-${winId}`);
  if (!win) return;
  highestZ += 1;
  win.style.zIndex = highestZ;
}

function openWindow(winId) {
  const win = document.getElementById(`win-${winId}`);
  if (!win) return;
  win.classList.remove("minimized");
  win.style.display = "flex";
  bringToFront(winId);

  // If opening task manager, refresh metrics
  if (winId === "taskmgr") {
    fetchProcesses();
  }
}

function closeWindow(winId) {
  const win = document.getElementById(`win-${winId}`);
  if (!win) return;
  win.style.display = "none";
}

function minimizeWindow(winId) {
  const win = document.getElementById(`win-${winId}`);
  if (!win) return;
  win.classList.add("minimized");
}

function maximizeWindow(winId) {
  const win = document.getElementById(`win-${winId}`);
  if (!win) return;
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

// Start Menu
function toggleStartMenu() {
  const menu = document.getElementById("startMenu");
  if (!menu) return;
  menu.classList.toggle("open");
}

document.addEventListener("click", (e) => {
  const menu = document.getElementById("startMenu");
  const startBtn = document.querySelector(".start-btn");
  if (!menu || !startBtn) return;
  if (!menu.contains(e.target) && !startBtn.contains(e.target) && menu.classList.contains("open")) {
    menu.classList.remove("open");
  }
});

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
    } catch (err) {
      // Backend starting up
    }
  };
  poll();
  setInterval(poll, 1000);
}

function updateTelemetryUI(data) {
  if (!data) return;

  // CPU
  const cpu = data.processor;
  const cpuPct = cpu.aggregate_utilization_pct;
  document.getElementById("sb-cpu-pct").textContent = `${cpuPct}%`;
  document.getElementById("cpu-stat-util").textContent = `${cpuPct}%`;
  document.getElementById("active-util-label").textContent = `Overall: ${cpuPct}%`;
  document.getElementById("cpu-stat-speed").textContent = `${cpu.active_clock_ghz.toFixed(2)} GHz`;
  document.getElementById("cpu-stat-procs").textContent = cpu.processes_count;
  document.getElementById("cpu-stat-threads").textContent = cpu.threads_total;
  document.getElementById("cpu-stat-uptime").textContent = data.uptime_formatted;

  // 192 Cores Heatmap
  if (cpu.threads_utilization && cpu.threads_utilization.length === 192) {
    for (let i = 0; i < 192; i++) {
      const cell = document.getElementById(`core-cell-${i}`);
      if (!cell) continue;
      const u = cpu.threads_utilization[i];
      cell.title = `Thread #${i + 1} (CCD ${Math.floor(i / 16)}): ${u}%`;

      // Color Interpolation
      if (u < 15) {
        cell.style.backgroundColor = `rgba(14, 165, 233, ${0.15 + (u / 15) * 0.25})`;
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
  document.getElementById("sb-mem-pct").textContent = `${mem.used_gb} GB`;
  document.getElementById("mem-stat-used").textContent = `${mem.used_gb} GB`;
  document.getElementById("mem-stat-avail").textContent = `${mem.available_gb} GB`;

  // Disk
  const disk = data.storage;
  document.getElementById("sb-disk-val").textContent = `${disk.active_time_pct}%`;
  document.getElementById("disk-stat-act").textContent = `${disk.active_time_pct}%`;
  document.getElementById("disk-stat-read").textContent = `${disk.read_speed_mb_s} MB/s`;
  document.getElementById("disk-stat-write").textContent = `${disk.write_speed_mb_s} MB/s`;

  // GPU
  const gpu = data.graphics;
  document.getElementById("sb-gpu-val").textContent = `${gpu.gpu_utilization_pct}%`;
  document.getElementById("gpu-stat-util").textContent = `${gpu.gpu_utilization_pct}%`;
  document.getElementById("gpu-stat-vram").textContent = `${gpu.vram_used_gb} / ${gpu.vram_total_gb} GB`;
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

    const data = await res.json();
    logEl.textContent += `[+] Benchmark Execution Successful!\n`;
    logEl.textContent += JSON.stringify(data, null, 2);

    // Update Card UI numbers if present
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

    // Scroll to bottom
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
  for (let i = 0; i < 40; i++) {
    particles.push({
      x: Math.random() * w,
      y: Math.random() * h,
      vx: (Math.random() - 0.5) * 0.4,
      vy: (Math.random() - 0.5) * 0.4,
      radius: Math.random() * 2 + 1,
      alpha: Math.random() * 0.4 + 0.1
    });
  }

  function render() {
    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = "rgba(0, 242, 254, 0.25)";

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
