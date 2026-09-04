"use client";

import React from 'react';

export default function MobileCTABar() {

  return (
    <div className="fixed bottom-0 left-0 w-full z-[100] md:hidden bg-gradient-to-r from-blue-600 to-cyan-500 p-4 flex justify-between items-center shadow-[0_-4px_20px_rgba(0,0,0,0.5)]">
      <div className="text-white font-bold text-sm">Need an Instant Quote?</div>
      <a href="tel:+12244490397" className="bg-white text-blue-900 px-6 py-2 rounded-full font-extrabold animate-pulse hover:bg-gray-100 transition-colors">
        Call Now
      </a>
    </div>
  );
}
