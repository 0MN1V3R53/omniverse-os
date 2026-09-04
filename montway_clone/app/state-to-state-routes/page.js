import MontwayMarketingSections from '@/components/MontwayMarketingSections';
import React from 'react';
import Link from 'next/link';
import fs from 'fs';
import path from 'path';
import QuoteCalculatorWrapper from '@/components/QuoteCalculatorWrapper';
import ALL_STATES from '@/components/data/statesData';
export const metadata = {
  title: 'State to State Auto Transport Routes | Sky Auto Services',
  description: 'View our directory of interstate auto transport routes. Select your origin state to find top-rated, fully-insured door-to-door car shipping options.',
  alternates: {
    canonical: 'https://skyautoservices.com/state-to-state-routes/'
  }
};

export default function StateToStateHub() {
  const filePath = path.join(process.cwd(), 'public', 'assets', 'data', 'state_routes.json');
  let routesData = {};
  
  try {
    const fileContents = fs.readFileSync(filePath, 'utf8');
    routesData = JSON.parse(fileContents);
  } catch (err) {
    console.error("Error reading state_routes.json", err);
  }

  const origins = Object.keys(routesData);

  return (
    <main className="min-h-screen bg-white text-slate-900 pt-36 sm:pt-40 lg:pt-44 pb-16 px-4">
      <div className="max-w-6xl mx-auto">
        <header className="mb-12 text-center">
          <h1 className="text-3xl sm:text-4xl md:text-5xl font-extrabold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-emerald-600">
            State-to-State Auto Transport
          </h1>
          <p className="text-base sm:text-lg md:text-xl text-slate-600 max-w-3xl mx-auto">
            Select your origin state below to explore all available nationwide shipping routes.
          </p>
        </header>

        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
          {origins.map((state) => {
            const stateSlug = state.toLowerCase().replace(/\s+/g, '-');
            const destState = ALL_STATES.find(s => s.state === state);
            const destImg = destState ? destState.img : "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Yosemite_Valley_from_Wawona_Tunnel_view%2C_2020.jpg/1000px-Yosemite_Valley_from_Wawona_Tunnel_view%2C_2020.jpg";
            return (
              <Link
                key={state}
                href={`/state-to-state-routes/${stateSlug}/`}
                className="relative overflow-hidden rounded-xl border border-slate-200 shadow-sm group h-24 sm:h-28 flex items-end justify-center p-2.5 sm:p-3 transition-all hover:border-emerald-500 hover:shadow-md"
              >
                <img 
                  src={destImg} 
                  alt={`${state} Auto Transport`} 
                  className="absolute inset-0 w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-slate-950/95 via-slate-900/50 to-transparent transition-opacity group-hover:opacity-90"></div>
                <h2 className="relative z-10 text-[12px] sm:text-sm md:text-base font-bold text-white group-hover:text-emerald-300 transition-colors text-center truncate tracking-tight w-full px-1 drop-shadow">
                  {state}
                </h2>
              </Link>
            );
          })}
        </div>
      </div>
          <QuoteCalculatorWrapper />
      <MontwayMarketingSections />
    </main>
  );
}
