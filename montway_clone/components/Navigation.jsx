"use client";
import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
export default function Navigation() {
  const [scrolled, setScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const pathname = usePathname();
  const isHomePage = pathname === '/';

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <>
      <nav className={`fixed top-0 left-0 w-full z-50 transition-all duration-300 ease-in-out ${scrolled ? 'bg-white/95 backdrop-blur-md shadow-md py-4' : 'bg-transparent py-4 lg:py-6'} ${mobileMenuOpen ? 'opacity-0 pointer-events-none invisible' : 'opacity-100 visible'}`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center">
            {/* ===== BRANDED LOGO (Official Shield Logo) ===== */}
            <div className="flex-shrink-0">
              <Link href="/" className="flex items-center gap-3 group" aria-label="Sky Auto Services – Home">
                <img
                  src="/assets/images/logo.png"
                  alt="Sky Auto Services Official Shield Logo"
                  className="w-16 h-16 object-contain drop-shadow-md group-hover:scale-105 transition-transform duration-300"
                />
                <span className="flex flex-col leading-none">
                  <span className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400 tracking-tight group-hover:from-blue-300 group-hover:to-emerald-300 transition-all">
                    SKY <span className="font-extrabold">SERVICES</span>
                  </span>
                  <span className="hidden sm:block text-[11px] uppercase tracking-[0.25em] text-gray-500 mt-0.5">Nationwide Logistics</span>
                  <span className="hidden sm:block text-[9px] font-semibold tracking-wider text-emerald-400/90 mt-1">USDOT: 4504932 | MC: 1782670</span>
                  <span className="hidden sm:block text-[8px] uppercase tracking-wider text-emerald-400/70 mt-0.5">Licensed & Bonded Broker</span>
                </span>
              </Link>
            </div>

            {/* ===== Desktop Navigation ===== */}
            <div className="hidden md:flex space-x-8 items-center">
              <Link href="/services" className="text-slate-700 hover:text-blue-600 transition-colors font-medium">Services</Link>
              <Link href="/usa-auto-transport-news" className="text-slate-700 hover:text-blue-600 transition-colors font-medium">News</Link>
              <Link href="/about" className="text-slate-700 hover:text-blue-600 transition-colors font-medium">About</Link>
              <Link href="/contact" className="text-slate-700 hover:text-blue-600 transition-colors font-medium">Contact</Link>
              <div className="flex items-center gap-4 bg-white/5 border border-white/10 px-5 py-2 rounded-full text-xs font-medium text-slate-700">
                <a href="tel:+12244490397" className="hover:text-slate-900 transition-colors flex items-center gap-1.5">
                  <svg className="w-3.5 h-3.5 text-cyan-400" fill="currentColor" viewBox="0 0 24 24"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.4 0 .8-.3 1l-2.2 2.2z"/></svg>
                  Service: (224) 449-0397
                </a>
                <span className="text-slate-900/20">|</span>
                <a href="tel:+12243101830" className="hover:text-slate-900 transition-colors flex items-center gap-1.5">
                  <svg className="w-3.5 h-3.5 text-emerald-400" fill="currentColor" viewBox="0 0 24 24"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.4 0 .8-.3 1l-2.2 2.2z"/></svg>
                  Dispatch: (224) 310-1830
                </a>
              </div>
              <Link href="/#quote-calculator" className="bg-gradient-to-r from-blue-500 to-indigo-600 text-slate-900 px-6 py-2.5 rounded-full font-semibold hover:shadow-[0_0_15px_rgba(59,130,246,0.5)] transition-all hover:-translate-y-0.5">
                Get a Quote
              </Link>
            </div>

            {/* ===== Mobile Hamburger Menu (Only) ===== */}
            <div className="flex md:hidden items-center">
              <button
                className="w-10 h-10 rounded-full bg-white/5 border border-white/10 flex items-center justify-center text-slate-800 border-slate-200 bg-slate-50 hover:bg-slate-100 transition-colors"
                onClick={() => setMobileMenuOpen(true)}
                aria-label="Open Navigation Menu"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
            </div>
          </div>

          {/* ===== Mobile Action Buttons (Underneath Logo) ===== */}
          <div className="flex md:hidden items-center justify-center gap-3 mt-4 w-full">
            <a
              href="tel:+12244490397"
              className="flex-1 h-10 rounded-full bg-cyan-500/15 border border-cyan-400/50 flex items-center justify-center text-cyan-400 text-sm font-semibold gap-2 hover:bg-cyan-500/25 transition-colors"
              aria-label="Call Service"
            >
              <svg className="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.4 0 .8-.3 1l-2.2 2.2z"/></svg>
              Service
            </a>
            <a
              href="tel:+12243101830"
              className="flex-1 h-10 rounded-full bg-emerald-500/15 border border-emerald-400/50 flex items-center justify-center text-emerald-400 text-sm font-semibold gap-2 hover:bg-emerald-500/25 transition-colors"
              aria-label="Call Dispatch"
            >
              <svg className="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.4 0 .8-.3 1l-2.2 2.2z"/></svg>
              Dispatch
            </a>
          </div>
        </div>
      </nav>

      {/* ===== Spacer to prevent mobile overlap on internal pages ===== */}
      {!isHomePage && <div className="h-32 md:h-0 w-full invisible pointer-events-none" aria-hidden="true" />}

      {/* ===== Sliding Mobile Drawer Overlay ===== */}
      {mobileMenuOpen && (
        <div className="fixed inset-0 z-[100] bg-white/95 backdrop-blur-2xl shadow-xl flex flex-col justify-between p-6 animate-in fade-in slide-in-from-top-4 duration-300 overflow-y-auto">
          <div className="flex items-center justify-between pb-6 border-b border-slate-200">
            <Link href="/" onClick={() => setMobileMenuOpen(false)} className="flex items-center gap-3">
              <img src="/assets/images/logo.png" alt="Sky Auto Services Official Shield Logo" className="w-10 h-10 object-contain" />
              <span className="text-lg font-bold text-slate-900">SKY <span className="text-emerald-500">SERVICES</span></span>
            </Link>
            <button
              onClick={() => setMobileMenuOpen(false)}
              className="w-10 h-10 rounded-full bg-slate-100 text-slate-900 flex items-center justify-center text-lg hover:bg-slate-200 transition-colors"
              aria-label="Close menu"
            >
              ✕
            </button>
          </div>

          <div className="space-y-6 my-auto py-8">
            <Link href="/services" onClick={() => setMobileMenuOpen(false)} className="block text-2xl font-semibold text-slate-900 hover:text-emerald-500 transition-colors">Services</Link>
            <Link href="/usa-auto-transport-news" onClick={() => setMobileMenuOpen(false)} className="block text-2xl font-semibold text-slate-900 hover:text-emerald-500 transition-colors">News</Link>
            <Link href="/about" onClick={() => setMobileMenuOpen(false)} className="block text-2xl font-semibold text-slate-900 hover:text-emerald-500 transition-colors">About</Link>
            <Link href="/contact" onClick={() => setMobileMenuOpen(false)} className="block text-2xl font-semibold text-slate-900 hover:text-emerald-500 transition-colors">Contact</Link>
          </div>

          <div className="space-y-4 pt-6 border-t border-slate-200">
            <a href="tel:+12244490397" className="w-full flex items-center justify-center gap-3 py-3.5 rounded-full bg-cyan-50 border border-cyan-200 text-cyan-800 font-bold text-center">
              <svg className="w-5 h-5 text-cyan-600 fill-current" viewBox="0 0 24 24"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.4 0 .8-.3 1l-2.2 2.2z"/></svg>
              Service: (224) 449-0397
            </a>
            <a href="tel:+12243101830" className="w-full flex items-center justify-center gap-3 py-3.5 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-800 font-bold text-center">
              <svg className="w-5 h-5 text-emerald-600 fill-current" viewBox="0 0 24 24"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.4 0 .8-.3 1l-2.2 2.2z"/></svg>
              Dispatch: (224) 310-1830
            </a>
            <Link href="/#quote-calculator" onClick={() => setMobileMenuOpen(false)} className="block w-full py-4 rounded-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-bold text-center shadow-lg hover:opacity-95 transition-opacity">
              Get Instant Quote
            </Link>
            <div className="text-center text-xs text-gray-500 uppercase tracking-widest pt-2">
              FMCSA MC-1782670 • 24/7 Dispatch
            </div>
          </div>
        </div>
      )}
    </>
  );
}
