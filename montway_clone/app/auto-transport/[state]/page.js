import React from 'react';
import Link from 'next/link';
import Script from 'next/script';
import fs from 'fs';
import path from 'path';
import QuoteCalculatorWrapper from '@/components/QuoteCalculatorWrapper';
import ALL_STATES from '@/components/data/statesData';
import LocalWeatherWidget from '@/components/LocalWeatherWidget';
import MontwayMarketingSections from '@/components/MontwayMarketingSections';
import { SITE_CONFIG } from '@/lib/siteConfig';

export async function generateStaticParams() {
  const filePath = path.join(process.cwd(), 'public', 'assets', 'data', 'state_routes.json');
  let routesData = {};
  try {
    const fileContents = fs.readFileSync(filePath, 'utf8');
    routesData = JSON.parse(fileContents);
  } catch (err) {
    console.error("Error reading state_routes.json", err);
  }

  const origins = Object.keys(routesData);
  return origins.map((origin) => ({
    state: origin.toLowerCase().replace(/\s+/g, '-'),
  }));
}

export async function generateMetadata({ params }) {
  const stateSlug = decodeURIComponent(params.state);
  const stateTitle = stateSlug.split('-').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');

  return {
    title: `Auto Transport in ${stateTitle} | Car Shipping Hub | Sky Auto Services`,
    description: `Direct door-to-door auto transport in ${stateTitle}. View top city shipping hubs, interstate shipping corridors, and get an instant quote with $0 upfront deposit.`,
    alternates: {
      canonical: `https://www.skyautoservices.com/auto-transport/${stateSlug}/`
    }
  };
}

export default function StateAutoTransportHub({ params }) {
  const stateSlug = decodeURIComponent(params.state);
  const stateTitle = stateSlug.split('-').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');

  // Fetch state routes
  const routesFilePath = path.join(process.cwd(), 'public', 'assets', 'data', 'state_routes.json');
  let stateRoutes = [];
  try {
    const fileContents = fs.readFileSync(routesFilePath, 'utf8');
    const routesData = JSON.parse(fileContents);
    // Find matching state key
    const matchKey = Object.keys(routesData).find(
      k => k.toLowerCase().replace(/\s+/g, '-') === stateSlug
    );
    if (matchKey) {
      stateRoutes = routesData[matchKey] || [];
    }
  } catch (err) {
    console.error("Error reading state_routes.json", err);
  }

  // Fetch cities for this state
  const citiesFilePath = path.join(process.cwd(), 'public', 'assets', 'data', 'cities.json');
  let stateCities = [];
  try {
    if (fs.existsSync(citiesFilePath)) {
      const cities = JSON.parse(fs.readFileSync(citiesFilePath, 'utf8'));
      stateCities = cities.filter(
        c => (c.stateSlug === stateSlug) || (c.state.toLowerCase().replace(/\s+/g, '-') === stateSlug)
      );
    }
  } catch (err) {
    console.error("Error reading cities.json", err);
  }

  const stateInfo = ALL_STATES.find(
    s => s.state.toLowerCase().replace(/\s+/g, '-') === stateSlug
  );

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 pt-32 pb-20 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Breadcrumb Navigation */}
        <nav aria-label="Breadcrumb" className="mb-6 flex items-center gap-2 text-xs text-slate-400">
          <Link href="/" className="hover:text-white transition-colors">Home</Link>
          <span>/</span>
          <Link href="/auto-transport/" className="hover:text-white transition-colors">Auto Transport</Link>
          <span>/</span>
          <span className="text-cyan-400 font-semibold">{stateTitle}</span>
        </nav>

        {/* Hero Header */}
        <header className="text-center mb-12">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-cyan-500/10 border border-cyan-400/30 text-cyan-400 text-xs font-semibold uppercase tracking-wider mb-6">
            <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse"></span>
            Direct Door-to-Door Carrier Network • {stateTitle}
          </div>
          <h1 className="text-3xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-white mb-6">
            Auto Transport in <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-cyan-400 to-emerald-400">{stateTitle}</span>
          </h1>
          <p className="text-slate-400 text-base sm:text-lg max-w-3xl mx-auto leading-relaxed">
            Reliable, licensed, and bonded car shipping services to and from {stateTitle}. Choose your metro hub or select an interstate shipping corridor below.
          </p>
        </header>

        {/* Quote Calculator */}
        <section className="mb-16">
          <QuoteCalculatorWrapper />
        </section>

        {/* Local Weather Widget */}
        <section className="mb-16">
          <LocalWeatherWidget stateName={stateTitle} />
        </section>

        {/* City Hubs in this State */}
        {stateCities.length > 0 && (
          <section className="mb-16 bg-slate-900/60 border border-slate-800 rounded-3xl p-8">
            <div className="flex items-center justify-between mb-8 pb-4 border-b border-slate-800">
              <div>
                <h2 className="text-2xl font-bold text-white flex items-center gap-3">
                  <span>🏙️</span> Major Metro Transport Hubs in {stateTitle}
                </h2>
                <p className="text-xs text-slate-400 mt-1">Dedicated terminal and door-to-door delivery centers</p>
              </div>
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
              {stateCities.map((city) => {
                const citySlug = city.citySlug || city.city.toLowerCase().replace(/\s+/g, '-');
                return (
                  <Link
                    key={city.city}
                    href={`/auto-transport/${stateSlug}/${citySlug}/`}
                    className="p-4 rounded-xl bg-slate-800/80 border border-slate-700 hover:border-cyan-400 hover:bg-slate-800 transition-all text-center group"
                  >
                    <div className="text-base font-bold text-white group-hover:text-cyan-300 transition-colors">
                      {city.city}
                    </div>
                    <div className="text-[11px] text-slate-400 mt-1">View Local Routes →</div>
                  </Link>
                );
              })}
            </div>
          </section>
        )}

        {/* Interstate Corridors Departing from this State */}
        {stateRoutes.length > 0 && (
          <section className="mb-16">
            <h2 className="text-2xl sm:text-3xl font-bold text-white mb-8 text-center flex items-center justify-center gap-3">
              <span>🛣️</span> Direct Interstate Routes Departing from {stateTitle}
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {stateRoutes.map((route) => {
                const destState = ALL_STATES.find(s => s.state === route.destination);
                const destImg = destState ? destState.img : (stateInfo ? stateInfo.img : "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Yosemite_Valley_from_Wawona_Tunnel_view%2C_2020.jpg/1000px-Yosemite_Valley_from_Wawona_Tunnel_view%2C_2020.jpg");
                return (
                  <Link
                    key={route.slug}
                    href={`/routes/${route.slug}/`}
                    className="relative overflow-hidden rounded-xl border border-slate-800 shadow-md group h-28 flex items-end justify-center p-3 transition-all hover:border-cyan-500"
                  >
                    <img 
                      src={destImg} 
                      alt={`${stateTitle} to ${route.destination} Car Shipping`} 
                      className="absolute inset-0 w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
                      loading="lazy"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-slate-950/95 via-slate-900/60 to-transparent transition-opacity group-hover:opacity-90"></div>
                    <div className="relative z-10 text-center w-full">
                      <div className="text-xs text-cyan-400 font-semibold tracking-wider uppercase">{stateTitle} to</div>
                      <div className="text-sm font-bold text-white group-hover:text-cyan-300 transition-colors truncate drop-shadow">
                        {route.destination}
                      </div>
                    </div>
                  </Link>
                );
              })}
            </div>
          </section>
        )}

        <MontwayMarketingSections />
      </div>
    </main>
  );
}
