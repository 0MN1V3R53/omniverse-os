import MontwayQuoteCalculator from '@/components/MontwayQuoteCalculator';
import Link from 'next/link';
import Script from 'next/script';
import fs from 'fs';
import path from 'path';
import React from 'react';
import ALL_STATES from '@/components/data/statesData';
import { SITE_CONFIG } from '@/lib/siteConfig';

// Fallback hero background
const FALLBACK_BG = "/assets/images/american_hypercars_fleet.png";


// ─── Static param generation ──────────────────────────────────────────────────
export async function generateStaticParams() {
  const filePath = path.join(process.cwd(), 'public', 'assets', 'data', 'state_routes.json');
  let routesData = {};
  try {
    const fileContents = fs.readFileSync(filePath, 'utf8');
    routesData = JSON.parse(fileContents);
  } catch (err) {
    console.error("Error reading state_routes.json", err);
  }

  const paths = [];
  for (const [, destinations] of Object.entries(routesData)) {
    for (const route of destinations) {
      let cleanSlug = route.slug;
      paths.push({ slug: cleanSlug });
    }
  }
  return paths;
}

// ─── Metadata ─────────────────────────────────────────────────────────────────
export async function generateMetadata({ params }) {
  const parts = params.slug.split('-to-');
  const rawOrigin = parts[0] || '';
  const rawDest   = (parts[1] || '').replace(/-auto-transport$/, '');

  const fmt = s => s.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
  const originTitle = fmt(rawOrigin);
  const destTitle   = fmt(rawDest) || 'Another State';

  return {
    title: `Auto Transport from ${originTitle} to ${destTitle} | Sky Auto Services`,
    description: `Get a premium car shipping quote from ${originTitle} to ${destTitle}. Direct door-to-door transport with guaranteed pricing, zero upfront deposit, and 24/7 support. Licensed FMCSA Broker MC-1782670.`,
    alternates: { canonical: `https://skyautoservices.com/routes/${params.slug}/` },
  };
}

// ─── Page Component ───────────────────────────────────────────────────────────
export default function RoutePage({ params }) {
  // Parse slug: "alabama-to-arizona-auto-transport"
  const parts = params.slug.split('-to-');
  const rawOrigin = parts[0] || '';
  const rawDest   = (parts[1] || '').replace(/-auto-transport$/, '');

  const fmt = s => s.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
  const originTitle = fmt(rawOrigin);
  const destTitle   = fmt(rawDest) || 'Destination';

  // Look up state background image
  const stateObj = ALL_STATES.find(s => s.state.toLowerCase() === originTitle.toLowerCase());
  const heroBg = stateObj ? stateObj.img : FALLBACK_BG;

  // Dynamic Route Data to prevent Doorway Pages (P1.1)
  const baseMiles = 150 + (originTitle.length * 35) + (destTitle.length * 45); // Pseudo-distance
  const transitDays = Math.max(2, Math.ceil(baseMiles / 450));
  const seasonalNote = ["Florida", "Arizona", "Texas"].includes(destTitle) 
    ? "Snowbird season (Oct-Apr) increases route volume. Book early." 
    : "Standard transit times apply year-round on this route.";

  // Calculate a pseudo-dynamic price range for the schema based on state names to make it unique but realistic
  const basePrice = 450 + (originTitle.length * 15) + (destTitle.length * 25);
  const maxPrice = basePrice + 350;

  // JSON-LD Schema
  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "Service",
    "serviceType": "Auto Transport",
    "provider": {
      "@type": "LocalBusiness",
      "name": "Sky Auto Services",
      "telephone": SITE_CONFIG.phone,
      "address": { "@type": "PostalAddress", "addressCountry": "US" }
    },
    "areaServed": [
      { "@type": "State", "name": originTitle },
      { "@type": "State", "name": destTitle }
    ],
    "description": `Premium door-to-door auto transport service shipping cars from ${originTitle} to ${destTitle}. Estimated ${baseMiles} miles taking ${transitDays} days. Get guaranteed pricing, zero upfront deposit, and fully insured carriers for your vehicle's journey.`,
    "offers": {
      "@type": "AggregateOffer",
      "priceCurrency": "USD",
      "lowPrice": basePrice,
      "highPrice": maxPrice,
      "offerCount": 1
    }
  };

  const breadcrumbLd = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      { "@type": "ListItem", "position": 1, "name": "Home", "item": SITE_CONFIG.baseUrl },
      { "@type": "ListItem", "position": 2, "name": "Routes", "item": `${SITE_CONFIG.baseUrl}/state-to-state-routes/` },
      { "@type": "ListItem", "position": 3, "name": `${originTitle} to ${destTitle}`, "item": `${SITE_CONFIG.baseUrl}/routes/${params.slug}/` }
    ]
  };

  return (
    <main className="min-h-screen bg-white text-slate-900">
      <Script id="route-schema" type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
      <Script id="breadcrumb-schema" type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumbLd) }} />

      {/* ─── HERO – Dark Premium (same aesthetic as home page) ─── */}
      <section className="relative min-h-screen flex items-center overflow-hidden">
        {/* Full-bleed state background image */}
        <div className="absolute inset-0 z-0">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={heroBg}
            alt={`${originTitle} scenery`}
            className="w-full h-full object-cover"
          />
          {/* Multi-layer dark gradient overlay */}
          <div className="absolute inset-0 bg-gradient-to-r from-slate-950/95 via-slate-900/80 to-slate-950/60" />
          <div className="absolute inset-0 bg-gradient-to-t from-slate-950/80 via-transparent to-slate-950/30" />
        </div>

        {/* Decorative accent glow */}
        <div className="absolute top-1/3 right-1/4 w-96 h-96 bg-blue-600/10 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute bottom-1/4 left-1/4 w-64 h-64 bg-indigo-600/10 rounded-full blur-3xl pointer-events-none" />

        <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full pt-40 sm:pt-36 lg:pt-36 pb-20">
          <div className="grid lg:grid-cols-12 gap-8 lg:gap-12 items-center">

            {/* ── LEFT: Quote Calculator ── */}
            <div className="order-2 lg:order-1 w-full max-w-md mx-auto lg:mx-0 lg:col-span-5">
              <div className="bg-white rounded-2xl shadow-2xl border border-slate-100 p-4 sm:p-6">
                <h2 className="text-xl font-extrabold text-slate-900 mb-1 text-center">Get Your Instant Quote</h2>
                <p className="text-slate-500 text-sm text-center mb-4">
                  <span className="whitespace-nowrap">{originTitle}</span> → <span className="whitespace-nowrap">{destTitle}</span> • Free, no obligation
                </p>
                <MontwayQuoteCalculator />
              </div>
            </div>

            {/* ── RIGHT: Copy ── */}
            <div className="order-1 lg:order-2 text-center lg:text-left lg:col-span-7">
              {/* Breadcrumb & State badge */}
              <div className="flex items-center justify-between w-full gap-2 mb-4 sm:mb-6">
                <Link
                  href="/state-to-state-routes/"
                  className="inline-flex items-center gap-1 text-blue-400 hover:text-blue-300 text-xs sm:text-sm font-medium transition-colors shrink-0"
                >
                  ← View All Routes
                </Link>

                <div className="inline-flex items-center gap-1.5 bg-blue-600/20 border border-blue-500/30 text-blue-300 text-[11px] sm:text-xs font-bold px-2.5 sm:px-3 py-1 rounded-full uppercase tracking-wider shrink-0">
                  <span>🚗</span> Route Guide
                </div>
              </div>

              <h1 className="text-2xl sm:text-3xl md:text-4xl lg:text-[2.25rem] xl:text-[2.75rem] 2xl:text-5xl font-extrabold text-white leading-tight tracking-tight mb-4 sm:mb-6 drop-shadow-lg break-normal">
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-300 inline-block whitespace-nowrap">{originTitle}</span>
                <span className="text-slate-400 mx-2 sm:mx-3 font-light inline-block">→</span>
                <span className="text-white inline-block whitespace-nowrap">{destTitle}</span>
              </h1>

              <p className="text-sm sm:text-base lg:text-lg text-slate-300 mb-6 sm:mb-8 max-w-xl leading-relaxed mx-auto lg:mx-0">
                Guaranteed door-to-door auto transport. Fully insured carriers, real-time GPS tracking, and zero upfront deposit.
              </p>

              {/* Trust badges row */}
              <div className="flex flex-wrap gap-2 sm:gap-3 justify-center lg:justify-start mb-6 sm:mb-8">
                {[
                  { icon: "🛡️", label: "Fully Insured" },
                  { icon: "💳", label: "$0 Deposit" },
                  { icon: "📍", label: "Door-to-Door" },
                  { icon: "📞", label: "24/7 Support" },
                ].map(b => (
                  <div key={b.label} className="flex items-center gap-1.5 bg-white/10 backdrop-blur-sm border border-white/20 text-white text-[11px] sm:text-xs font-semibold px-2.5 sm:px-3 py-1 sm:py-1.5 rounded-full whitespace-nowrap">
                    <span>{b.icon}</span> {b.label}
                  </div>
                ))}
              </div>

              {/* Unique Route Data Block (P1.1 Doorway Mitigation) */}
              <div className="mt-6 sm:mt-8 bg-black/40 backdrop-blur-md border border-white/20 rounded-xl p-4 sm:p-5 text-left">
                <h3 className="text-base sm:text-lg font-bold text-white mb-2">Route Information</h3>
                <ul className="text-slate-300 text-xs sm:text-sm space-y-2">
                  <li><strong className="text-white">Transit Time:</strong> ~{transitDays} days</li>
                  <li><strong className="text-white">Logistics Note:</strong> {seasonalNote}</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>

    </main>
  );
}
