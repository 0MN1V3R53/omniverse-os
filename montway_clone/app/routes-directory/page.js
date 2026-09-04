import QuoteCalculatorWrapper from '@/components/QuoteCalculatorWrapper';
import MontwayMarketingSections from '@/components/MontwayMarketingSections';
import React from 'react';
import Link from 'next/link';
import fs from 'fs';
import path from 'path';

export const metadata = {
  title: 'Full Routes Directory | Sky Auto Services',
  description: 'Complete HTML sitemap directory for all 3,148 state-to-state auto transport routes provided by Sky Auto Services.',
  alternates: {
    canonical: 'https://skyautoservices.com/routes-directory/'
  }
};

export default function RoutesDirectory() {
  const filePath = path.join(process.cwd(), 'public', 'assets', 'data', 'state_routes.json');
  let routesData = {};
  
  try {
    const fileContents = fs.readFileSync(filePath, 'utf8');
    routesData = JSON.parse(fileContents);
  } catch (err) {
    console.error("Error reading state_routes.json", err);
  }

  return (
    <main className="min-h-screen bg-white text-slate-900 pt-36 sm:pt-40 lg:pt-44 pb-16 px-4">
      <div className="max-w-7xl mx-auto">
        <header className="mb-12 border-b border-slate-200 pb-8 text-center max-w-4xl mx-auto">
          <h1 className="text-3xl sm:text-4xl md:text-5xl font-extrabold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-emerald-600">
            Complete Auto Transport Routes Directory
          </h1>
          <p className="text-base sm:text-lg md:text-xl text-slate-600">
            A comprehensive index of all state-to-state car shipping routes we service across the United States.
          </p>
        </header>

        <div className="space-y-12">
          {Object.keys(routesData).sort().map((originState) => {
            const destinations = routesData[originState];
            
            return (
              <section key={originState} className="bg-slate-50/70 p-6 rounded-2xl border border-slate-200">
                <h2 className="text-xl sm:text-2xl font-bold text-slate-900 mb-6 border-b border-slate-200 pb-2">
                  Shipping from {originState}
                </h2>
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                  {destinations.map((route) => (
                    <Link
                      key={route.slug}
                      href={`/routes/${route.slug}`}
                      className="text-sm text-slate-600 hover:text-blue-600 hover:underline transition-colors block truncate"
                      title={`${originState} to ${route.destination} Auto Transport`}
                    >
                      {originState} to {route.destination}
                    </Link>
                  ))}
                </div>
              </section>
            );
          })}
        </div>
      </div>
      <QuoteCalculatorWrapper />
        <MontwayMarketingSections />
    </main>
  );
}
