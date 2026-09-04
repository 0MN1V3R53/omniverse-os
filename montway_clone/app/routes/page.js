import MontwayMarketingSections from '@/components/MontwayMarketingSections';
import React from 'react';
import Link from 'next/link';
import fs from 'fs';
import path from 'path';
import QuoteCalculatorWrapper from '@/components/QuoteCalculatorWrapper';

export const metadata = {
  title: 'Nationwide Service Areas & Auto Transport Routes | Sky Auto Services',
  description: 'View our complete directory of nationwide auto transport routes. We offer fully-insured, premium car shipping services across all 50 US states.',
  alternates: {
    canonical: 'https://www.skyautoservices.com/routes'
  }
};

export default function RoutesDirectory() {
  // Read and parse cities.json data at build time
  const filePath = path.join(process.cwd(), 'public', 'assets', 'data', 'cities.json');
  let cities = [];
  try {
    const fileContents = fs.readFileSync(filePath, 'utf8');
    cities = JSON.parse(fileContents);
  } catch (err) {
    console.error("Error reading cities.json", err);
  }

  // Group cities by state
  const groupedByState = cities.reduce((acc, current) => {
    const stateName = current.state;
    if (!acc[stateName]) {
      acc[stateName] = [];
    }
    acc[stateName].push(current.city);
    return acc;
  }, {});

  // Sort states alphabetically
  const sortedStates = Object.keys(groupedByState).sort();

  return (
    <main className="min-h-screen bg-white text-slate-900 pt-36 sm:pt-40 lg:pt-44 pb-16 px-4">
      <div className="max-w-6xl mx-auto">
        <header className="mb-12 text-center">
          <h1 className="text-3xl sm:text-4xl md:text-5xl font-extrabold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-emerald-600">
            Nationwide Transport Routes
          </h1>
          <p className="text-base sm:text-lg md:text-xl text-slate-600 max-w-3xl mx-auto">
            Sky Auto Services provides top-rated, fully-insured vehicle shipping across major transit corridors in the United States. Select your state below to view local service areas.
          </p>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {sortedStates.map((state) => {
            // Sort cities within each state alphabetically
            const sortedCities = [...groupedByState[state]].sort();
            const stateSlug = state.toLowerCase().replace(/\s+/g, '-');

            return (
              <section key={state} className="bg-slate-50/80 border border-slate-200 rounded-2xl p-6 shadow-sm hover:shadow-md transition-shadow">
                <h2 className="text-xl sm:text-2xl font-bold mb-4 text-slate-900 border-b border-slate-200 pb-2">
                  {state}
                </h2>
                <ul className="space-y-2">
                  {sortedCities.map((city) => {
                    const citySlug = city.toLowerCase().replace(/\s+/g, '-');
                    return (
                      <li key={city}>
                        <Link
                          href={`/auto-transport/${stateSlug}/${citySlug}/`}
                          className="text-slate-600 hover:text-blue-600 hover:underline transition-colors block py-1 text-sm font-medium"
                        >
                          {city} Auto Transport
                        </Link>
                      </li>
                    );
                  })}
                </ul>
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
