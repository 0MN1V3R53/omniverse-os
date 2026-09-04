"use client";

import React, { useEffect, useState, useRef } from 'react';

export default function ExitIntentModal() {
  const [isVisible, setIsVisible] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [assignedQuoteId, setAssignedQuoteId] = useState('');
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    email: '',
    origin: '',
    destination: ''
  });
  const [smsConsent, setSmsConsent] = useState(false);

  const canvasRef = useRef(null);
  const animationFrameId = useRef(null);

  // Trigger on Exit-Intent (Desktop) and Scroll/Time Delay (Mobile)
  useEffect(() => {
    if (typeof window === 'undefined') return;

    const hasShown = sessionStorage.getItem('sky_vip_dispatch_modal_shown');
    if (hasShown) return;

    // Desktop Mouseleave
    const handleMouseLeave = (e) => {
      if (e.clientY <= 10 && !sessionStorage.getItem('sky_vip_dispatch_modal_shown')) {
        setIsVisible(true);
        sessionStorage.setItem('sky_vip_dispatch_modal_shown', 'true');
      }
    };

    // Mobile fallback: after 45s of active browsing
    const timer = setTimeout(() => {
      if (!sessionStorage.getItem('sky_vip_dispatch_modal_shown')) {
        setIsVisible(true);
        sessionStorage.setItem('sky_vip_dispatch_modal_shown', 'true');
      }
    }, 45000);

    document.addEventListener('mouseleave', handleMouseLeave);

    return () => {
      document.removeEventListener('mouseleave', handleMouseLeave);
      clearTimeout(timer);
    };
  }, []);

  // Fireworks Animation Engine on Canvas
  useEffect(() => {
    if (!isVisible) {
      if (animationFrameId.current) cancelAnimationFrame(animationFrameId.current);
      return;
    }

    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    const handleResize = () => {
      if (!canvas) return;
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    };
    window.addEventListener('resize', handleResize);

    const colors = [
      '#38bdf8', // sky blue
      '#10b981', // emerald
      '#f59e0b', // amber / gold
      '#ec4899', // pink
      '#818cf8', // indigo
      '#06b6d4', // cyan
      '#fbbf24'  // warm gold
    ];

    let fireworks = [];
    let particles = [];

    class Firework {
      constructor(targetX, targetY) {
        this.x = Math.random() * width * 0.8 + width * 0.1;
        this.y = height;
        this.targetX = targetX || Math.random() * width * 0.8 + width * 0.1;
        this.targetY = targetY || Math.random() * (height * 0.45) + height * 0.1;
        this.speed = Math.random() * 3 + 4.5;
        this.angle = Math.atan2(this.targetY - this.y, this.targetX - this.x);
        this.velocity = {
          x: Math.cos(this.angle) * this.speed,
          y: Math.sin(this.angle) * this.speed
        };
        this.trail = [];
        this.trailLength = 4;
        this.color = colors[Math.floor(Math.random() * colors.length)];
        this.exploded = false;
      }

      update() {
        this.trail.push({ x: this.x, y: this.y });
        if (this.trail.length > this.trailLength) this.trail.shift();

        this.x += this.velocity.x;
        this.y += this.velocity.y;

        const distance = Math.hypot(this.targetX - this.x, this.targetY - this.y);
        if (distance < 12 || this.y <= this.targetY) {
          this.exploded = true;
          this.explode();
        }
      }

      draw() {
        ctx.beginPath();
        for (let i = 0; i < this.trail.length; i++) {
          const point = this.trail[i];
          ctx.lineTo(point.x, point.y);
        }
        ctx.strokeStyle = this.color;
        ctx.lineWidth = 2.5;
        ctx.shadowBlur = 10;
        ctx.shadowColor = this.color;
        ctx.stroke();
      }

      explode() {
        const particleCount = 45;
        for (let i = 0; i < particleCount; i++) {
          particles.push(new Particle(this.x, this.y, this.color));
        }
      }
    }

    class Particle {
      constructor(x, y, color) {
        this.x = x;
        this.y = y;
        this.color = color;
        const angle = Math.random() * Math.PI * 2;
        const speed = Math.random() * 4.5 + 1;
        this.velocity = {
          x: Math.cos(angle) * speed,
          y: Math.sin(angle) * speed
        };
        this.alpha = 1;
        this.friction = 0.96;
        this.gravity = 0.06;
        this.decay = Math.random() * 0.015 + 0.012;
      }

      update() {
        this.velocity.x *= this.friction;
        this.velocity.y *= this.friction;
        this.velocity.y += this.gravity;
        this.x += this.velocity.x;
        this.y += this.velocity.y;
        this.alpha -= this.decay;
      }

      draw() {
        ctx.save();
        ctx.globalAlpha = Math.max(this.alpha, 0);
        ctx.beginPath();
        ctx.arc(this.x, this.y, 2, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.shadowBlur = 8;
        ctx.shadowColor = this.color;
        ctx.fill();
        ctx.restore();
      }
    }

    let frameCount = 0;

    const loop = () => {
      ctx.globalCompositeOperation = 'destination-out';
      ctx.fillStyle = 'rgba(0, 0, 0, 0.25)';
      ctx.fillRect(0, 0, width, height);
      ctx.globalCompositeOperation = 'lighter';

      frameCount++;
      if (frameCount % 32 === 0 || fireworks.length === 0) {
        fireworks.push(new Firework());
      }

      for (let i = fireworks.length - 1; i >= 0; i--) {
        fireworks[i].update();
        fireworks[i].draw();
        if (fireworks[i].exploded) {
          fireworks.splice(i, 1);
        }
      }

      for (let i = particles.length - 1; i >= 0; i--) {
        particles[i].update();
        particles[i].draw();
        if (particles[i].alpha <= 0) {
          particles.splice(i, 1);
        }
      }

      animationFrameId.current = requestAnimationFrame(loop);
    };

    loop();

    return () => {
      window.removeEventListener('resize', handleResize);
      if (animationFrameId.current) cancelAnimationFrame(animationFrameId.current);
    };
  }, [isVisible]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!smsConsent) {
      alert("Please check the SMS consent checkbox to receive text updates.");
      return;
    }
    const generatedId = `SKY-${Math.floor(100000 + Math.random() * 900000)}`;
    setAssignedQuoteId(generatedId);

    const payload = {
      ...formData,
      quote_id: generatedId,
      vehicle: 'Priority Dispatch Request (VIP Slot)',
      transport_type: 'Direct Carrier Dispatch ($0 Deposit)',
      price: 'Priority Quote Reserved',
      comments: 'Priority Dispatch Retention Modal Submission ($0 Deposit Lock, SMS Opt-In: Yes)'
    };

    // 1. Direct Browser Dispatch to Google Apps Script Webhook
    try {
      fetch("https://script.google.com/macros/s/AKfycbxjTrpOti2ZPZscPAbgKRTPc3PeAkNyBMCVnieVW2BtnUsnQsiIBp5wKo3JVKb6F43m/exec", {
        method: "POST",
        mode: "no-cors",
        headers: { "Content-Type": "text/plain;charset=utf-8" },
        body: JSON.stringify(payload),
      }).catch((err) => console.warn("Priority dispatch Google webhook notice:", err));
    } catch (gErr) {
      console.error("Priority dispatch Google webhook error:", gErr);
    }

    // 2. Server-side ingestion & Email Alert
    try {
      const baseUrl = (typeof window !== 'undefined' && (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')) ? "http://localhost:8000" : "";
      await fetch(`${baseUrl}/api/save_quote.php`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
    } catch (err) {
      console.error("Priority dispatch backend save notice:", err);
    }

    // 3. Google Ads Live Conversion Pingback
    try {
      if (typeof window !== "undefined" && typeof window.gtag === "function") {
        window.gtag('event', 'conversion', {
          'send_to': 'AW-18396293415',
          'value': 1.0,
          'currency': 'USD'
        });
        window.gtag('event', 'generate_lead', {
          'value': 1.0,
          'currency': 'USD'
        });
      }
    } catch (gTagErr) {
      console.warn("Google Tag priority dispatch notice:", gTagErr);
    }

    setIsSubmitted(true);
    setTimeout(() => {
      setIsVisible(false);
    }, 4500);
  };

  if (!isVisible) return null;

  return (
    <div className="fixed inset-0 z-[120] flex items-center justify-center p-3 sm:p-4 bg-black/85 backdrop-blur-md overflow-hidden">
      {/* Dynamic Animated Fireworks Canvas */}
      <canvas
        ref={canvasRef}
        className="absolute inset-0 w-full h-full pointer-events-none z-0"
      />

      {/* Modal Container */}
      <div className="relative z-10 bg-gradient-to-b from-slate-900 via-slate-900/95 to-slate-950 border border-emerald-500/40 rounded-3xl max-w-lg w-full p-6 sm:p-8 shadow-[0_0_50px_rgba(16,185,129,0.25)] text-slate-100 max-h-[92vh] overflow-y-auto">
        {/* Close Button */}
        <button
          onClick={() => setIsVisible(false)}
          className="absolute top-4 right-4 w-9 h-9 rounded-full bg-white/10 hover:bg-white/20 border border-white/15 flex items-center justify-center text-slate-300 hover:text-white transition-all hover:scale-105"
          aria-label="Close modal"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        {!isSubmitted ? (
          <>
            {/* Trust Header & Badges */}
            <div className="text-center mb-6">
              <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-gradient-to-r from-emerald-500/20 to-cyan-500/20 border border-emerald-400/40 text-emerald-300 text-xs font-bold uppercase tracking-wider mb-3 shadow-sm">
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
                ⚡ Guaranteed VIP Dispatch Slot
              </div>

              <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight leading-tight">
                Lock In Your <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-emerald-400 to-teal-300">$0 Upfront Deposit</span> Quote
              </h2>

              <p className="text-xs sm:text-sm text-slate-300 mt-2 leading-relaxed">
                Direct carrier assignment with 100% price lock &amp; comprehensive cargo insurance ($100k–$1M+). Zero upfront fees to reserve.
              </p>

              {/* 3 Value Pillars */}
              <div className="grid grid-cols-3 gap-2 mt-4 text-[11px] sm:text-xs">
                <div className="bg-white/5 border border-white/10 rounded-xl p-2 text-center">
                  <div className="font-bold text-emerald-400">🛡️ $0 Deposit</div>
                  <div className="text-[10px] text-slate-400">Pay at Pickup</div>
                </div>
                <div className="bg-white/5 border border-white/10 rounded-xl p-2 text-center">
                  <div className="font-bold text-cyan-400">⭐ 4.95 Stars</div>
                  <div className="text-[10px] text-slate-400">1,284+ Loads</div>
                </div>
                <div className="bg-white/5 border border-white/10 rounded-xl p-2 text-center">
                  <div className="font-bold text-indigo-300">⚡ Fast Route</div>
                  <div className="text-[10px] text-slate-400">24/7 Dispatch</div>
                </div>
              </div>
            </div>

            {/* Quick Priority Booking Form */}
            <form onSubmit={handleSubmit} className="space-y-3.5">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Your Full Name *</label>
                  <input
                    required
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    placeholder="John Doe"
                    className="w-full bg-black/60 border border-slate-700 rounded-xl px-3.5 py-2.5 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400 transition"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Phone Number *</label>
                  <input
                    required
                    type="tel"
                    name="phone"
                    value={formData.phone}
                    onChange={handleChange}
                    placeholder="(555) 000-0000"
                    className="w-full bg-black/60 border border-slate-700 rounded-xl px-3.5 py-2.5 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400 transition"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Email Address (For Instant Quote Delivery) *</label>
                <input
                  required
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="john@example.com"
                  className="w-full bg-black/60 border border-slate-700 rounded-xl px-3.5 py-2.5 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400 transition"
                />
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Pickup City / ZIP *</label>
                  <input
                    required
                    type="text"
                    name="origin"
                    value={formData.origin}
                    onChange={handleChange}
                    placeholder="e.g. Chicago, IL"
                    className="w-full bg-black/60 border border-slate-700 rounded-xl px-3.5 py-2.5 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400 transition"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Delivery City / ZIP *</label>
                  <input
                    required
                    type="text"
                    name="destination"
                    value={formData.destination}
                    onChange={handleChange}
                    placeholder="e.g. Miami, FL"
                    className="w-full bg-black/60 border border-slate-700 rounded-xl px-3.5 py-2.5 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400 transition"
                  />
                </div>
              </div>

              {/* Required Unchecked-by-Default SMS Consent Checkbox (RingCentral / TCR Mandated) */}
              <div className="flex items-start gap-2.5 p-2.5 bg-black/60 border border-slate-700 rounded-xl text-left">
                <input
                  id="vip-modal-sms-consent"
                  type="checkbox"
                  required
                  checked={smsConsent}
                  onChange={(e) => setSmsConsent(e.target.checked)}
                  className="mt-0.5 h-4 w-4 rounded border-slate-600 bg-slate-800 text-emerald-400 focus:ring-emerald-400 cursor-pointer"
                />
                <label htmlFor="vip-modal-sms-consent" className="text-[10px] sm:text-[11px] text-slate-300 leading-tight cursor-pointer select-none">
                  I agree to receive SMS messages from <strong>SKY SERVICES LLC</strong> (Sky Auto Services). This includes SMS messages for conversations (external). Message frequency varies. Message and data rates may apply. See privacy policy at <a href="/privacy" className="text-emerald-400 underline font-semibold">https://www.skyautoservices.com/privacy.html</a>. Message HELP for help. Reply STOP to any message to opt out.
                </label>
              </div>

              {/* Submit CTA */}
              <button
                type="submit"
                className="w-full mt-2 bg-gradient-to-r from-emerald-500 via-teal-500 to-cyan-500 text-white font-extrabold py-3.5 rounded-xl shadow-[0_0_25px_rgba(16,185,129,0.45)] hover:shadow-[0_0_35px_rgba(16,185,129,0.7)] transition-all hover:scale-[1.01] active:scale-[0.99] flex items-center justify-center gap-2 text-sm sm:text-base cursor-pointer"
              >
                <span>✨ Lock In My Priority Quote ($0 Deposit)</span>
              </button>

              {/* Direct Call Alternative */}
              <div className="text-center pt-2">
                <a
                  href="tel:+12244490397"
                  className="inline-flex items-center gap-2 text-xs font-semibold text-cyan-400 hover:text-cyan-300 transition underline decoration-cyan-500/40"
                >
                  <svg className="w-3.5 h-3.5 fill-current" viewBox="0 0 24 24">
                    <path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.4 0 .8-.3 1l-2.2 2.2z" />
                  </svg>
                  Prefer to speak with dispatch? Call (224) 449-0397
                </a>
              </div>
            </form>
          </>
        ) : (
          /* Celebration Confirmation State */
          <div className="text-center py-8">
            <div className="w-20 h-20 bg-gradient-to-tr from-emerald-500 to-cyan-400 text-white rounded-full flex items-center justify-center mx-auto mb-5 shadow-[0_0_30px_rgba(16,185,129,0.6)] animate-bounce">
              <svg className="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <h3 className="text-3xl font-extrabold text-white mb-2">Priority Slot Locked! 🎉</h3>
            <p className="text-emerald-300 font-semibold text-sm mb-1">
              Reservation ID: {assignedQuoteId}
            </p>
            <p className="text-slate-300 text-sm max-w-sm mx-auto leading-relaxed mt-2">
              Our direct dispatch desk is reviewing vetted carrier lanes for your route now. We will send your locked rate details to your phone and email momentarily.
            </p>
            <div className="mt-6">
              <button
                onClick={() => setIsVisible(false)}
                className="px-6 py-2.5 rounded-full bg-white/10 hover:bg-white/20 border border-white/20 text-white text-xs font-semibold transition"
              >
                Return to Site
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
