/* ==========================================================================
   OMNIVERSE TECH — INTERACTIVE REPOSITORY CODE & FOLDER EXPLORER
   Enables Real-Time Folder Tree Traversal, Search & Manifest Code Viewing
   ========================================================================== */

import { OMNIVERSE_DATA } from '../src/data/omniverse_dataset.js';
import { EMBEDDED_FILES } from '../src/data/embedded_files.js';
import { soundEngine } from './sound-engine.js';

export function initFolderExplorer() {
  const treeContainer = document.getElementById('explorer-tree-root');
  const fileTitle = document.getElementById('active-file-title');
  const filePathEl = document.getElementById('active-file-path');
  const fileSizeEl = document.getElementById('active-file-size');
  const codeContentEl = document.getElementById('active-code-content');
  const copyBtn = document.getElementById('explorer-copy-btn');
  const searchInput = document.getElementById('explorer-search-input');

  if (!treeContainer || !codeContentEl) return;

  const repositories = OMNIVERSE_DATA.repository_explorer || [];

  function renderTree(filterQuery = '') {
    treeContainer.innerHTML = '';
    const q = filterQuery.toLowerCase().trim();

    repositories.forEach((repo) => {
      const repoEl = document.createElement('div');
      repoEl.className = 'repo-group';

      const header = document.createElement('div');
      header.className = 'tree-node repo-header';
      header.innerHTML = `
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" width="16" height="16">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"></path>
        </svg>
        <span style="font-weight: 700; color: #ffffff;">${repo.name}</span>
      `;
      repoEl.appendChild(header);

      const childrenContainer = document.createElement('div');
      childrenContainer.style.paddingLeft = '1rem';

      (repo.children || []).forEach((child) => {
        const matches = !q || child.name.toLowerCase().includes(q) || (child.desc && child.desc.toLowerCase().includes(q));
        if (!matches) return;

        const node = document.createElement('div');
        node.className = 'tree-node';
        node.dataset.filename = child.name;

        const isDir = child.type === 'directory';
        const iconSvg = isDir
          ? `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24" width="16" height="16"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"></path></svg>`
          : `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24" width="16" height="16"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>`;

        node.innerHTML = `
          ${iconSvg}
          <span>${child.name}</span>
        `;

        node.addEventListener('mouseenter', () => soundEngine.playHover());
        node.addEventListener('click', () => {
          soundEngine.playClick();
          document.querySelectorAll('.tree-node').forEach(n => n.classList.remove('active'));
          node.classList.add('active');
          loadFile(child.name, repo.path + '/' + child.path, child.desc);
        });

        childrenContainer.appendChild(node);
      });

      repoEl.appendChild(childrenContainer);
      treeContainer.appendChild(repoEl);
    });
  }

  function loadFile(filename, fullPath, desc) {
    if (fileTitle) fileTitle.textContent = filename;
    if (filePathEl) filePathEl.textContent = fullPath;

    const embedded = EMBEDDED_FILES[filename];

    if (embedded) {
      if (fileSizeEl) fileSizeEl.textContent = (embedded.size / 1024).toFixed(1) + ' KB';
      
      // Render code with numbered lines
      const lines = embedded.content.split('\n');
      const formatted = lines.map((line, idx) => {
        const lineNum = String(idx + 1).padStart(4, ' ');
        const escaped = line
          .replace(/&/g, '&amp;')
          .replace(/</g, '&lt;')
          .replace(/>/g, '&gt;');
        return `<span style="color: #475569; user-select: none;">${lineNum} | </span>${escaped}`;
      }).join('\n');

      codeContentEl.innerHTML = formatted;
    } else {
      if (fileSizeEl) fileSizeEl.textContent = 'Directory / Manifest';
      codeContentEl.innerHTML = `// [OMNIVERSE REPOSITORY DIRECTORY]\n// Path: ${fullPath}\n// Purpose: ${desc || 'Core Workspace Architecture Module'}\n\n// To explore active files, select any of the key manifest files in the left sidebar:\n// - omniverse.md (Master Operating Manifest)\n// - omniverse_code.md (Offensive Cybersecurity & Exploitation Manifest)\n// - mythos_agent.md (Frontier AI Agentic Architecture)\n// - 07_omniverse_enterprise_hierarchy.md\n// - audio_systems_lead_dr_julian_vance.md`;
    }
  }

  // Copy Action
  if (copyBtn) {
    copyBtn.addEventListener('click', () => {
      soundEngine.playClick();
      const textToCopy = codeContentEl.textContent;
      navigator.clipboard.writeText(textToCopy).then(() => {
        copyBtn.innerHTML = `
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" width="14" height="14">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
          </svg> Copied!
        `;
        setTimeout(() => {
          copyBtn.innerHTML = `
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" width="14" height="14">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"></path>
            </svg> Copy Code
          `;
        }, 2000);
      });
    });
  }

  // Live Search
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      renderTree(e.target.value);
    });
  }

  // Initial Render
  renderTree();
  // Default load omniverse.md
  loadFile('omniverse.md', '/Users/silversurfer/Documents/Aegis shield of the gods/omniverse.md', 'Master Enterprise Operating Manifest');
}
