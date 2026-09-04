"use client";

import React, { useState } from 'react';
import Link from 'next/link';
import MontwayMarketingSections from '@/components/MontwayMarketingSections';
import QuoteCalculatorWrapper from '@/components/QuoteCalculatorWrapper';

export default function ContactPage() {
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    email: '',
    origin: '',
    destination: '',
    message: ''
  });
  const [smsConsent, setSmsConsent] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [assignedTicketId, setAssignedTicketId] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!smsConsent) {
      alert("Please check the SMS consent checkbox to receive text messages regarding your inquiry.");
      return;
    }
    setIsSubmitting(true);
    const generatedTicket = `TICKET-${Math.floor(100000 + Math.random() * 900000)}`;
    setAssignedTicketId(generatedTicket);

    const payload = {
      name: formData.name,
      phone: formData.phone,
      email: formData.email,
      origin: formData.origin || 'Contact Page Inquiry',
      destination: formData.destination || 'Contact Page Inquiry',
      vehicle: 'Direct Contact / Dispatch Inquiry',
      transport_type: 'General Logistics Support',
      price: '$0 Deposit Inquiry',
      comments: `Contact Form Submission [${generatedTicket}] (SMS Opt-In: Yes): ${formData.message || 'Direct Inquiry'}`
    };

    // 1. Send to Google Apps Script Webhook
    try {
      fetch("https://script.google.com/macros/s/AKfycbxjTrpOti2ZPZscPAbgKRTPc3PeAkNyBMCVnieVW2BtnUsnQsiIBp5wKo3JVKb6F43m/exec", {
        method: "POST",
        mode: "no-cors",
        headers: { "Content-Type": "text/plain;charset=utf-8" },
        body: JSON.stringify(payload),
      }).catch((err) => console.warn("Contact form Google webhook notice:", err));
    } catch (gErr) {
      console.error("Contact form Google webhook error:", gErr);
    }

    // 2. Server-side save
    try {
      const baseUrl = (typeof window !== 'undefined' && (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')) ? "http://localhost:8000" : "";
      await fetch(`${baseUrl}/api/save_quote.php`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
    } catch (err) {
      console.error("Contact form backend save notice:", err);
    }

    // 3. Google Ads Conversion Beacon
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
      console.warn("Google Tag contact notice:", gTagErr);
    }

    setIsSubmitting(false);
    setIsSubmitted(true);
  };

  return (
    <main className="min-h-screen bg-white">
      <div className="pt-28 pb-16 md:pt-36 md:pb-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs font-bold uppercase tracking-wider mb-3">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping" />
            24/7 Nationwide Logistics &amp; Dispatch Desk
          </div>
          <h1 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-slate-900 tracking-tight">
            Contact <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-emerald-500">Sky Auto Services</span>
          </h1>
          <p className="text-sm sm:text-base text-slate-600 max-w-2xl mx-auto mt-2 leading-relaxed">
            Direct carrier coordination with a strict <strong>$0 Upfront Deposit</strong> policy and comprehensive cargo insurance ($100k–$1M+). Reach our dispatch desk 24/7.
          </p>

          {/* 3 Value Pillars */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 max-w-3xl mx-auto mt-6 text-xs text-left">
            <div className="bg-slate-50 border border-slate-200 rounded-xl p-3 flex items-center gap-3">
              <span className="text-xl">🛡️</span>
              <div>
                <div className="font-bold text-slate-900">$0 Upfront Deposit</div>
                <div className="text-slate-500 text-[11px]">Pay zero until carrier is assigned</div>
              </div>
            </div>
            <div className="bg-slate-50 border border-slate-200 rounded-xl p-3 flex items-center gap-3">
              <span className="text-xl">⭐</span>
              <div>
                <div className="font-bold text-slate-900">4.95/5 Star Rated</div>
                <div className="text-slate-500 text-[11px]">1,284+ verified cross-country hauls</div>
              </div>
            </div>
            <div className="bg-slate-50 border border-slate-200 rounded-xl p-3 flex items-center gap-3">
              <span className="text-xl">⚡</span>
              <div>
                <div className="font-bold text-slate-900">Guaranteed Dispatch</div>
                <div className="text-slate-500 text-[11px]">Direct carrier matching nationwide</div>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 max-w-6xl mx-auto">
          {/* Interactive Contact & Dispatch Inquiry Form */}
          <div className="lg:col-span-7 bg-slate-900 text-white rounded-3xl p-6 sm:p-8 shadow-xl border border-slate-800">
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-white">Send a Message to Dispatch</h2>
              <p className="text-xs sm:text-sm text-slate-400 mt-1">
                Receive an immediate rate confirmation or tracking update from our logistics coordinators.
              </p>
            </div>

            {!isSubmitted ? (
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 mb-1">Full Name *</label>
                    <input
                      required
                      type="text"
                      name="name"
                      value={formData.name}
                      onChange={handleChange}
                      placeholder="John Doe"
                      className="w-full bg-black/60 border border-slate-700 rounded-xl px-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 transition"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 mb-1">Phone Number (For SMS Updates) *</label>
                    <input
                      required
                      type="tel"
                      name="phone"
                      value={formData.phone}
                      onChange={handleChange}
                      placeholder="(224) 000-0000"
                      className="w-full bg-black/60 border border-slate-700 rounded-xl px-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 transition"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 mb-1">Email Address *</label>
                    <input
                      required
                      type="email"
                      name="email"
                      value={formData.email}
                      onChange={handleChange}
                      placeholder="john@example.com"
                      className="w-full bg-black/60 border border-slate-700 rounded-xl px-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 transition"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 mb-1">Route / State (Optional)</label>
                    <input
                      type="text"
                      name="origin"
                      value={formData.origin}
                      onChange={handleChange}
                      placeholder="e.g. IL to FL or Chicago, IL"
                      className="w-full bg-black/60 border border-slate-700 rounded-xl px-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 transition"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Inquiry / Vehicle Details</label>
                  <textarea
                    rows="3"
                    name="message"
                    value={formData.message}
                    onChange={handleChange}
                    placeholder="Tell us about your vehicle, preferred timeline, or questions..."
                    className="w-full bg-black/60 border border-slate-700 rounded-xl px-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 transition"
                  />
                </div>

                {/* Required Unchecked-by-Default SMS Consent Checkbox (RingCentral / TCR Mandated) */}
                <div className="flex items-start gap-3 p-3.5 bg-black/60 border border-slate-700 rounded-xl text-left">
                  <input
                    id="contact-sms-consent"
                    type="checkbox"
                    required
                    checked={smsConsent}
                    onChange={(e) => setSmsConsent(e.target.checked)}
                    className="mt-1 h-4 w-4 rounded border-slate-600 bg-slate-800 text-emerald-500 focus:ring-emerald-400 focus:ring-offset-slate-900 cursor-pointer"
                  />
                  <label htmlFor="contact-sms-consent" className="text-[11px] sm:text-xs text-slate-300 leading-snug cursor-pointer select-none">
                    I agree to receive SMS/text messages from <strong>SKY SERVICES LLC</strong> (Sky Auto Services) regarding my transport quote, scheduling, and logistics updates. Message frequency varies. Message and data rates may apply. Message HELP for help. Reply STOP to any message to opt out. See privacy policy at <Link href="/privacy" className="text-emerald-400 underline font-semibold hover:text-emerald-300">https://www.skyautoservices.com/privacy.html</Link> and <Link href="/terms" className="text-emerald-400 underline font-semibold hover:text-emerald-300">Terms of Service</Link>.
                  </label>
                </div>

                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="w-full bg-gradient-to-r from-emerald-500 via-teal-500 to-cyan-500 text-white font-extrabold py-3.5 rounded-xl shadow-lg hover:shadow-emerald-500/25 transition-all hover:scale-[1.01] active:scale-[0.99] flex items-center justify-center gap-2 text-sm sm:text-base cursor-pointer"
                >
                  <span>{isSubmitting ? "Transmitting..." : "✨ Submit Message to Dispatch"}</span>
                </button>
              </form>
            ) : (
              <div className="text-center py-10">
                <div className="w-16 h-16 bg-emerald-500/20 text-emerald-400 rounded-full flex items-center justify-center mx-auto mb-4 border border-emerald-500/40">
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold text-white mb-2">Message Dispatched!</h3>
                <p className="text-emerald-400 font-mono text-sm mb-2">Reference ID: {assignedTicketId}</p>
                <p className="text-slate-300 text-xs sm:text-sm max-w-md mx-auto leading-relaxed">
                  Our 24/7 logistics coordination desk has received your request. A transport specialist will contact you shortly with your rate and lane schedule.
                </p>
                <button
                  onClick={() => setIsSubmitted(false)}
                  className="mt-6 px-6 py-2 rounded-full bg-white/10 hover:bg-white/20 text-white text-xs font-semibold transition"
                >
                  Send Another Inquiry
                </button>
              </div>
            )}
          </div>

          {/* Contact Details & Direct Numbers */}
          <div className="lg:col-span-5 flex flex-col justify-between space-y-6 bg-slate-50 border border-slate-200 rounded-3xl p-6 sm:p-8">
            <div>
              <h2 className="text-xl font-bold text-slate-900 mb-4">Direct Contact Channels</h2>
              <div className="space-y-5">
                <div className="flex items-start">
                  <div className="bg-blue-500/10 p-3 rounded-2xl mr-4 border border-blue-500/20 flex-shrink-0">
                    <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-slate-900">Service Desk (24/7)</h3>
                    <a href="tel:+12244490397" className="text-blue-600 font-bold hover:text-emerald-600 transition text-base sm:text-lg block mt-0.5">
                      (224) 449-0397
                    </a>
                    <span className="text-[11px] text-slate-500">Live agent call &amp; SMS support</span>
                  </div>
                </div>

                <div className="flex items-start">
                  <div className="bg-emerald-500/10 p-3 rounded-2xl mr-4 border border-emerald-500/20 flex-shrink-0">
                    <svg className="w-6 h-6 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-slate-900">Direct Carrier Dispatch</h3>
                    <a href="tel:+12243101830" className="text-emerald-600 font-bold hover:text-blue-600 transition text-base sm:text-lg block mt-0.5">
                      (224) 310-1830
                    </a>
                    <span className="text-[11px] text-slate-500">Driver lane scheduling &amp; status</span>
                  </div>
                </div>

                <div className="flex items-start">
                  <div className="bg-teal-500/10 p-3 rounded-2xl mr-4 border border-teal-500/20 flex-shrink-0">
                    <svg className="w-6 h-6 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-slate-900">Email Support</h3>
                    <a href="mailto:sales@skyservicesllc.com" className="text-slate-700 font-medium hover:text-emerald-600 transition text-sm block mt-0.5">
                      sales@skyservicesllc.com
                    </a>
                    <span className="text-[11px] text-slate-500">Instant quote requests &amp; receipts</span>
                  </div>
                </div>

                <div className="flex items-start">
                  <div className="bg-purple-500/10 p-3 rounded-2xl mr-4 border border-purple-500/20 flex-shrink-0">
                    <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-slate-900">Operating Logistics HQ</h3>
                    <p className="text-slate-600 text-xs mt-0.5 leading-relaxed">
                      1004 Sycamore Dr<br />
                      Streamwood, IL 60107, USA
                    </p>
                    <span className="text-[10px] font-mono text-emerald-600 font-semibold block mt-1">
                      USDOT: 4504932 | MC: 1782670
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <div className="pt-4 border-t border-slate-200">
              <a
                href="/#quote-calculator"
                className="w-full block bg-slate-900 hover:bg-slate-800 text-white text-center py-3 rounded-xl font-bold text-xs sm:text-sm transition"
              >
                Go to Instant Quote Calculator →
              </a>
            </div>
          </div>
        </div>
      </div>

      <QuoteCalculatorWrapper />
      <MontwayMarketingSections />
    </main>
  );
}
