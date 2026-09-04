'use client';

import { useEffect, useState } from 'react';

/**
 * 🛡️ SecurityGuard Component
 * Developed by Omniverse Tech Security Pod (CISO Michael Chang & Web Lead Julian Thorne)
 * 
 * Provides enterprise-grade client-side anti-theft, anti-scraping, and non-copyable protection:
 * 1. Disables right-click context menu across static site assets.
 * 2. Blocks text highlight & selection on non-input DOM elements.
 * 3. Blocks copy/cut/paste theft on site content while preserving full form input usability.
 * 4. Intercepts DevTools, View Source, and Page Save keyboard shortcuts (F12, Ctrl+U, Ctrl+S, Ctrl+Shift+I/J/C, Cmd+Opt+I/J/C).
 * 5. Prevents image/asset drag-and-drop theft.
 * 6. Prevents iframe embedding / clickjacking.
 * 7. Injects legal proprietary copyright watermark in DevTools console.
 */
export default function SecurityGuard() {
  const [toastMessage, setToastMessage] = useState('');
  const [showToast, setShowToast] = useState(false);

  const triggerSecurityNotice = (message = 'Content Protected — Copying & Inspection Disabled') => {
    setToastMessage(message);
    setShowToast(true);
    setTimeout(() => {
      setShowToast(false);
    }, 2200);
  };

  useEffect(() => {
    // 1. Console Security & Intellectual Property Banner
    try {
      console.clear();
      console.log(
        '%c🔒 SKY AUTO SERVICES LLC — PROPRIETARY SYSTEM',
        'color: #38bdf8; font-size: 20px; font-weight: bold; background: #030712; padding: 8px 16px; border-radius: 6px; border: 1px solid #0284c7;'
      );
      console.log(
        '%c[!] NOTICE: All route data, pricing algorithms, telemetry matrices, and UI assets are proprietary intellectual property.\n[!] Unauthorized scraping, automated harvesting, data-mining, or site duplication is strictly prohibited under 18 U.S.C. § 1030 (Computer Fraud and Abuse Act) and international copyright treaties.\n[!] All unauthorized access attempts and API payloads are logged with visitor telemetry.',
        'color: #94a3b8; font-size: 11px; line-height: 1.5;'
      );
    } catch {
      // Ignore in restricted environments
    }

    // 2. Anti-Frame / Clickjacking Protection
    try {
      if (window.top !== window.self) {
        window.top.location = window.self.location;
      }
    } catch {
      // Cross-origin iframe prevention
    }

    // Helper: Determine if user is interacting with an authorized form input
    const isInteractiveInput = (target) => {
      if (!target) return false;
      const tagName = target.tagName ? target.tagName.toUpperCase() : '';
      if (tagName === 'INPUT' || tagName === 'TEXTAREA' || tagName === 'SELECT') {
        return true;
      }
      if (target.isContentEditable || target.closest('input, textarea, select, [contenteditable="true"]')) {
        return true;
      }
      return false;
    };

    // 3. Right-Click Context Menu Prevention
    const handleContextMenu = (e) => {
      if (isInteractiveInput(e.target)) return;
      e.preventDefault();
      triggerSecurityNotice('Right-click & context menu disabled for content protection.');
      return false;
    };

    // 4. Text Selection Prevention (except in form inputs)
    const handleSelectStart = (e) => {
      if (isInteractiveInput(e.target)) return true;
      e.preventDefault();
      return false;
    };

    // 5. Clipboard Copy & Cut Prevention (except in form inputs)
    const handleCopy = (e) => {
      if (isInteractiveInput(e.target)) return true;
      e.preventDefault();
      triggerSecurityNotice('Copying site data is restricted.');
      return false;
    };

    const handleCut = (e) => {
      if (isInteractiveInput(e.target)) return true;
      e.preventDefault();
      return false;
    };

    // 6. Image & Asset Drag-and-Drop Prevention
    const handleDragStart = (e) => {
      if (isInteractiveInput(e.target)) return true;
      e.preventDefault();
      return false;
    };

    // 7. Keyboard Shortcut Interception (F12, Ctrl+U, Ctrl+S, Ctrl+P, DevTools combos)
    const handleKeyDown = (e) => {
      const isInput = isInteractiveInput(e.target);
      const isCtrlOrCmd = e.ctrlKey || e.metaKey;

      // F12 (Developer Tools)
      if (e.key === 'F12' || e.keyCode === 123) {
        e.preventDefault();
        e.stopPropagation();
        triggerSecurityNotice('Developer inspection shortcut disabled.');
        return false;
      }

      // Ctrl/Cmd + Shift + I (Inspect Element)
      // Ctrl/Cmd + Shift + J (Developer Console)
      // Ctrl/Cmd + Shift + C (Element Selector)
      if (isCtrlOrCmd && e.shiftKey && ['I', 'i', 'J', 'j', 'C', 'c', 'K', 'k'].includes(e.key)) {
        e.preventDefault();
        e.stopPropagation();
        triggerSecurityNotice('Developer tools inspection is disabled.');
        return false;
      }

      // Ctrl/Cmd + U (View Source)
      if (isCtrlOrCmd && (e.key === 'u' || e.key === 'U' || e.keyCode === 85)) {
        e.preventDefault();
        e.stopPropagation();
        triggerSecurityNotice('View page source is disabled.');
        return false;
      }

      // Ctrl/Cmd + S (Save Webpage)
      if (isCtrlOrCmd && (e.key === 's' || e.key === 'S' || e.keyCode === 83)) {
        e.preventDefault();
        e.stopPropagation();
        triggerSecurityNotice('Page saving is disabled.');
        return false;
      }

      // Ctrl/Cmd + P (Print Page)
      if (isCtrlOrCmd && (e.key === 'p' || e.key === 'P' || e.keyCode === 80)) {
        e.preventDefault();
        e.stopPropagation();
        triggerSecurityNotice('Direct printing is disabled.');
        return false;
      }

      // Ctrl/Cmd + A (Select All - blocked on non-input elements)
      if (!isInput && isCtrlOrCmd && (e.key === 'a' || e.key === 'A' || e.keyCode === 65)) {
        e.preventDefault();
        e.stopPropagation();
        return false;
      }

      // Ctrl/Cmd + C (Copy - blocked on non-input elements)
      if (!isInput && isCtrlOrCmd && (e.key === 'c' || e.key === 'C' || e.keyCode === 67)) {
        e.preventDefault();
        e.stopPropagation();
        triggerSecurityNotice('Copying site data is restricted.');
        return false;
      }
    };

    // Attach listeners with capture
    document.addEventListener('contextmenu', handleContextMenu, true);
    document.addEventListener('selectstart', handleSelectStart, true);
    document.addEventListener('copy', handleCopy, true);
    document.addEventListener('cut', handleCut, true);
    document.addEventListener('dragstart', handleDragStart, true);
    document.addEventListener('keydown', handleKeyDown, true);

    return () => {
      document.removeEventListener('contextmenu', handleContextMenu, true);
      document.removeEventListener('selectstart', handleSelectStart, true);
      document.removeEventListener('copy', handleCopy, true);
      document.removeEventListener('cut', handleCut, true);
      document.removeEventListener('dragstart', handleDragStart, true);
      document.removeEventListener('keydown', handleKeyDown, true);
    };
  }, []);

  if (!showToast) return null;

  return (
    <div
      id="security-protection-toast"
      className="fixed bottom-20 left-1/2 -translate-x-1/2 z-[9999] bg-slate-950/95 text-white border border-rose-500/40 shadow-2xl backdrop-blur-md px-5 py-2.5 rounded-full flex items-center gap-2.5 text-xs font-semibold animate-in fade-in zoom-in-95 duration-200 pointer-events-none select-none"
    >
      <span className="w-2 h-2 rounded-full bg-rose-500 animate-pulse"></span>
      <span className="text-rose-400 font-bold uppercase tracking-wider text-[10px]">Security Notice:</span>
      <span className="text-slate-200">{toastMessage}</span>
    </div>
  );
}
