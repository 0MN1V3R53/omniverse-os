import React from 'react';
import Link from 'next/link';
import fs from 'fs';
import path from 'path';
import QuoteCalculatorWrapper from '@/components/QuoteCalculatorWrapper';
import ALL_STATES from '@/components/data/statesData';
import MontwayMarketingSections from '@/components/MontwayMarketingSections';

export const metadata = {
  title: 'Nationwide Auto Transport Directory & City Hubs | Sky Auto Services',
  description: 'Explore door-to-door auto transport services across all 50 US states and major metropolitan cities. Calculate exact rates and book licensed, bonded carriers.',
  alternates: {
    canonical: 'https://www.skyautoservices.com/auto-transport/'
  }
};

export default function AutoTransportDirectoryPage() {
  const filePath = path.join(process.cwd(), 'public', 'assets', 'data', 'cities.json');
  let cities = [];
  try {
    if (fs.existsSync(filePath)) {
      cities = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    }
  } catch (err) {
    console.error("Error reading cities.json", err);
  }

  // Group cities by state
  const stateMap = {};
  cities.forEach(item => {
    const sSlug = item.stateSlug || item.state.toLowerCase().replace(/\s+/g, '-');
    if (!stateMap[sSlug]) {
      stateMap[sSlug] = {
        stateName: item.state,
        stateSlug: sSlug,
        cities: []
      };
    }
    stateMap[sSlug].cities.push(item);
  });

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 pt-32 pb-20 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <header className="text-center mb-16">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-cyan-500/10 border border-cyan-400/30 text-cyan-400 text-xs font-semibold uppercase tracking-wider mb-6">
            <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse"></span>
            50-State Logistics Network • All Major US Metros
          </div>
          <h1 className="text-3xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-white mb-6">
            Nationwide <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-cyan-400 to-emerald-400">Auto Transport Directory</span>
          </h1>
          <p className="text-slate-400 text-base sm:text-lg max-w-3xl mx-auto leading-relaxed">
            Select a state or city below to view local auto transport hubs, regional highway corridors, and verified door-to-door carrier routes with zero upfront deposit.
          </p>
        </header>

        <section className="mb-20">
          <QuoteCalculatorWrapper />
        </section>

        <section className="mb-16">
          <h2 className="text-2xl sm:text-3xl font-bold text-white mb-8 text-center flex items-center justify-center gap-3">
            <span>🗺️</span> Browse Auto Transport by State &amp; Metro Hub
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {ALL_STATES.map((st) => {
              const stateSlug = st.state.toLowerCase().replace(/\s+/g, '-');
              const stateData = stateMap[stateSlug];
              const stateCities = stateData?.cities || [];

              return (
                <div key={st.state} className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 hover:border-cyan-500/40 transition-all">
                  <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-800">
                    <Link 
                      href={`/auto-transport/${stateSlug}/`}
                      className="text-lg font-bold text-white hover:text-cyan-400 transition-colors flex items-center gap-2"
                    >
                      <span>{st.state}</span>
                      <span className="text-xs text-slate-500 font-mono">({st.code})</span>
                    </Link>
                    <Link
                      href={`/auto-transport/${stateSlug}/`}
                      className="text-xs text-cyan-400 hover:text-cyan-300 font-semibold"
                    >
                      State Hub →
                    </Link>
                  </div>
                  {stateCities.length > 0 ? (
                    <div className="flex flex-wrap gap-2">
                      {stateCities.map((c) => {
                        const citySlug = c.citySlug || c.city.toLowerCase().replace(/\s+/g, '-');
                        return (
                          <Link
                            key={c.city}
                            href={`/auto-transport/${stateSlug}/${citySlug}/`}
                            className="text-xs px-2.5 py-1 rounded-lg bg-slate-800/80 text-slate-300 hover:bg-cyan-500/20 hover:text-cyan-300 border border-slate-700/50 transition-colors"
                          >
                            {c.city}
                          </Link>
                        );
                      })}
                    </div>
                  ) : (
                    <p className="text-xs text-slate-500 italic">Full state coverage available</p>
                  )}
                </div>
              );
            })}
          </div>
        </section>

        <MontwayMarketingSections />
      </div>
    </main>
  );
}
