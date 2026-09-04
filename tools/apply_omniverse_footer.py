#!/usr/bin/env python3
"""
OMNIVERSE TECH - FOOTER SIGNATURE INJECTION ENGINE
==================================================
Pod: Frontend Web (Julian Thorne) & CEO Suite (Dr. Alexander Vance)
Directives:
Injects the Omniverse Technologies centered footer mark with:
1. Omniverse Tech logo (scaled ~40px)
2. "Designed by Omniverse Technologies"
3. Telegram direct link badge: https://t.me/OmniverseTech (@OmniverseTech)
"""

import os
import glob
import re

def get_footer_signature_html(option=1):
    if option == 1:
        # Option 1: Modern Cyber Glass Mark (Centered, elegant)
        return """
<!-- OMNIVERSE TECHNOLOGIES FOOTER SIGNATURE -->
<div class="w-full pt-8 pb-4 mt-6 border-t border-white/10 flex flex-col items-center justify-center text-center">
  <a href="https://t.me/OmniverseTech" target="_blank" rel="noopener noreferrer" class="group flex flex-col items-center justify-center gap-2 p-3.5 rounded-2xl bg-white/[0.03] hover:bg-white/[0.08] border border-white/5 hover:border-cyan-500/40 transition-all duration-300 shadow-lg hover:shadow-cyan-500/20">
    <img src="/assets/images/omniverse_tech_logo.png" alt="Omniverse Technologies Logo" class="h-10 w-auto object-contain transition-transform duration-300 group-hover:scale-105 drop-shadow-[0_0_12px_rgba(59,130,246,0.4)]" loading="lazy">
    <span class="text-xs text-slate-400 font-medium tracking-wide">Designed by <span class="font-bold text-white group-hover:text-cyan-400 transition-colors">Omniverse Technologies</span></span>
    <div class="inline-flex items-center gap-1.5 px-3 py-0.5 rounded-full bg-cyan-500/10 border border-cyan-400/30 text-cyan-400 text-[11px] font-mono font-medium group-hover:bg-cyan-500/20 transition-all">
      <svg class="w-3 h-3 fill-current" viewBox="0 0 24 24">
        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.75-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z"/>
      </svg>
      <span>@OmniverseTech</span>
    </div>
  </a>
</div>
<!-- /OMNIVERSE TECHNOLOGIES FOOTER SIGNATURE -->
"""
    elif option == 2:
        # Option 2: Minimalist Monoline
        return """
<!-- OMNIVERSE TECHNOLOGIES FOOTER SIGNATURE -->
<div class="w-full pt-6 mt-4 border-t border-white/10 flex items-center justify-center gap-3 text-center">
  <img src="/assets/images/omniverse_tech_logo.png" alt="Omniverse Technologies" class="h-7 w-auto object-contain" loading="lazy">
  <span class="text-xs text-slate-400 font-medium">Designed by <span class="text-white font-semibold">Omniverse Technologies</span></span>
  <span class="text-slate-600">|</span>
  <a href="https://t.me/OmniverseTech" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1 text-xs text-cyan-400 hover:text-cyan-300 font-mono hover:underline transition">
    <svg class="w-3 h-3 fill-current" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.75-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z"/></svg>
    @OmniverseTech
  </a>
</div>
<!-- /OMNIVERSE TECHNOLOGIES FOOTER SIGNATURE -->
"""
    return ""

def main():
    print("🚀 [OMNIVERSE FOOTER ENGINE] Ready for batch injection upon executive approval.")

if __name__ == "__main__":
    main()
