import MontwayMarketingSections from '@/components/MontwayMarketingSections';
import React from 'react';
import fs from 'fs';
import path from 'path';
import QuoteCalculatorWrapper from '@/components/QuoteCalculatorWrapper';

export async function generateStaticParams() {
  const filePath = path.join(process.cwd(), 'public', 'assets', 'data', 'cities.json');
  if (!fs.existsSync(filePath)) {
    return [];
  }
  const fileContents = fs.readFileSync(filePath, 'utf8');
  const cities = JSON.parse(fileContents);
  
  return cities.map((item) => ({
    state: item.state.toLowerCase().replace(/\s+/g, '-'),
    city: item.city.toLowerCase().replace(/\s+/g, '-')
  }));
}

// Next.js App Router Metadata Generator
export async function generateMetadata({ params }) {
  const stateStr = decodeURIComponent(params.state);
  const cityStr = decodeURIComponent(params.city);
  
  const state = stateStr.split('-').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
  const city = cityStr.split('-').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');

  return {
    title: `Auto Transport in ${city}, ${state} | Sky Auto Services`,
    description: `Premium door-to-door auto transport in ${city}, ${state}. Zero upfront deposit. Safe and reliable car shipping with top-rated carriers.`,
    alternates: {
      canonical: `https://www.skyautoservices.com/auto-transport/${stateStr}/${cityStr}`
    }
  };
}

export default function LocationPage({ params }) {
  const stateStr = decodeURIComponent(params.state);
  const cityStr = decodeURIComponent(params.city);

  const state = stateStr.split('-').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
  const city = cityStr.split('-').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');

  // Fetch enriched data
  const filePath = path.join(process.cwd(), 'public', 'assets', 'data', 'cities.json');
  let cityData = null;
  if (fs.existsSync(filePath)) {
    const fileContents = fs.readFileSync(filePath, 'utf8');
    const cities = JSON.parse(fileContents);
    cityData = cities.find(c => c.stateSlug === stateStr && c.citySlug === cityStr);
  }

  const highways = cityData?.highways || [];
  const nearestAuction = cityData?.nearest_auction || "Major Regional Auto Auction";
  const weatherAdvisory = cityData?.weather_advisory || "Check local weather conditions for the best transport method.";
  const topLanes = cityData?.top_lanes || [
    { destination: "Miami, FL", distance: "1,200 miles", transit_time: "3-5 Days" },
    { destination: "Los Angeles, CA", distance: "2,000 miles", transit_time: "5-7 Days" }
  ];

  const stateLogistics = {
    "Illinois": "connecting via I-90, I-55, and I-294",
    "Florida": "connecting via I-95, I-75, and I-4",
    "Texas": "connecting via I-10, I-35, and I-45",
    "California": "connecting via I-5, I-10, and I-80",
    "New York": "connecting via I-87, I-90, and I-495"
  };
  // Use enriched highways if available, otherwise fallback to stateLogistics
  const routeDetails = highways.length > 0 ? `connecting via ${highways.join(', ')}` : (stateLogistics[state] || `major state highways and interstate transit corridors`);

  const jsonLd = {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "AutoTransportService",
        "name": `Sky Auto Services ${city}`,
        "provider": {
          "@type": "AutomotiveBusiness",
          "name": "Sky Auto Services",
          "url": "https://www.skyautoservices.com",
          "telephone": "+1-224-449-0397",
          "image": "https://www.skyautoservices.com/assets/images/american_hypercars_fleet.png"
        },
        "areaServed": {
          "@type": "City",
          "name": city,
          "containedInPlace": {
            "@type": "State",
            "name": state,
            "containedInPlace": {
              "@type": "Country",
              "name": "USA"
            }
          }
        },
        "description": `Premium door-to-door vehicle shipping services in ${city}, ${state}.`
      },
      {
        "@type": "FAQPage",
        "mainEntity": [
          {
            "@type": "Question",
            "name": `How much does it cost to ship a car to or from ${city}?`,
            "acceptedAnswer": {
              "@type": "Answer",
              "text": `The cost to ship a car to or from ${city}, ${state} depends on the vehicle size, total distance, and whether you choose open or enclosed carrier transport. Request an instant quote with zero upfront deposit.`
            }
          },
          {
            "@type": "Question",
            "name": `How long does auto transport take in ${state}?`,
            "acceptedAnswer": {
              "@type": "Answer",
              "text": `Transit times to and from ${state} typically range from 1-3 days for regional routes and 5-7 days for cross-country vehicle shipping. We offer fast dispatch and real-time tracking.`
            }
          }
        ]
      },
      {
        "@type": "LocalBusiness",
        "name": "Sky Services LLC",
        "address": {
          "@type": "PostalAddress",
          "streetAddress": "3216 N Salk Rd",
          "addressLocality": "Arlington Heights",
          "addressRegion": "IL",
          "postalCode": "60004",
          "addressCountry": "US"
        },
        "telephone": "(224) 449-0397",
        "url": "https://www.skyautoservices.com",
        "areaServed": {
          "@type": "City",
          "name": city,
          "containedInPlace": {
            "@type": "State",
            "name": state,
            "containedInPlace": {
              "@type": "Country",
              "name": "USA"
            }
          }
        }
      }
    ]
  };

  return (
    <main className="min-h-screen bg-white text-slate-900 pt-36 sm:pt-40 lg:pt-44 pb-16 px-4">
      {/* Schema Injection */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      
      <div className="max-w-4xl mx-auto">
        <header className="mb-12 text-center max-w-3xl mx-auto">
          <h1 className="text-3xl sm:text-4xl md:text-5xl font-extrabold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-cyan-600">
            Top-Rated {city} Auto Transport
          </h1>
          <p className="text-base sm:text-lg md:text-xl text-slate-600">
            Secure, fully-insured vehicle shipping to and from {city}, {state}.
          </p>
        </header>

        <section className="bg-slate-900 border border-slate-800 rounded-xl p-8 mb-8 shadow-xl">
          <h2 className="text-2xl font-bold mb-4 border-b border-slate-800 pb-2">Shipping Your Car to or from {city}?</h2>
          <p className="text-slate-300 leading-relaxed mb-6">
            Sky Auto Services offers premium door-to-door auto logistics across the {state} region, {routeDetails}. Whether you require open carrier transport or enclosed luxury shipping, we guarantee top-rated carriers, fast pickup times, and $0 upfront deposit.
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div className="bg-blue-900/10 border border-blue-500/20 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-blue-300 mb-2 flex items-center gap-2">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                Fast & Secure Transit
              </h3>
              <p className="text-sm text-slate-400">
                Average regional transit takes 1-3 days. Cross-country shipping takes 5-7 days. Real-time GPS tracking is standard on all {city} routes.
              </p>
            </div>
            <div className="bg-emerald-900/10 border border-emerald-500/20 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-emerald-300 mb-2 flex items-center gap-2">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
                Fully Insured & Licensed
              </h3>
              <p className="text-sm text-slate-400">
                100% comprehensive carrier coverage included. FMCSA Licensed Broker MC-1782670 covering {city} and surrounding metros.
              </p>
            </div>
          </div>
          
          {/* LOCAL LOGISTICS DATA SECTION */}
          <div className="mb-8 p-6 bg-slate-950 border border-slate-700 rounded-lg">
            <h3 className="text-xl font-bold mb-4 text-white">Local {city} Transport Logistics</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-slate-300">
              {highways.length > 0 && (
                <div>
                  <strong className="text-cyan-400 block mb-1">🛣️ Major Highway Corridors:</strong>
                  {highways.join(', ')}
                </div>
              )}
              <div>
                <strong className="text-cyan-400 block mb-1">🏛️ Local Industry Hubs:</strong>
                Proximity to {nearestAuction}
              </div>
              <div className="md:col-span-2 mt-2">
                <strong className="text-cyan-400 block mb-1">🌤️ Seasonal Transport Advisory:</strong>
                <p className="bg-slate-800/50 p-3 rounded">{weatherAdvisory}</p>
              </div>
            </div>
          </div>

          <div className="mb-8">
            <h3 className="text-xl font-bold mb-4 text-white border-b border-slate-800 pb-2">Top Outbound Lanes from {city}</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm text-slate-300">
                <thead className="bg-slate-800/50 text-slate-200">
                  <tr>
                    <th className="p-3 rounded-tl-lg">Destination</th>
                    <th className="p-3">Distance</th>
                    <th className="p-3 rounded-tr-lg">Estimated Transit Time</th>
                  </tr>
                </thead>
                <tbody>
                  {topLanes.map((lane, idx) => (
                    <tr key={idx} className="border-b border-slate-800/50 last:border-0 hover:bg-slate-800/30 transition-colors">
                      <td className="p-3 font-semibold text-white">{lane.destination}</td>
                      <td className="p-3 text-cyan-300">{lane.distance}</td>
                      <td className="p-3">{lane.transit_time}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <h2 className="text-2xl font-bold mb-4 border-b border-slate-800 pb-2 text-white">Frequently Asked Questions</h2>
          <div className="space-y-4">
            <div className="bg-slate-800/50 p-4 rounded-lg">
              <h4 className="font-semibold text-white mb-1">How much does it cost to ship a car to or from {city}?</h4>
              <p className="text-slate-400 text-sm">The cost to ship a car to or from {city}, {state} depends on the vehicle size, total distance, and whether you choose open or enclosed carrier transport. Request an instant quote with zero upfront deposit.</p>
            </div>
            <div className="bg-slate-800/50 p-4 rounded-lg">
              <h4 className="font-semibold text-white mb-1">How long does auto transport take in {state}?</h4>
              <p className="text-slate-400 text-sm">Transit times to and from {state} typically range from 1-3 days for regional routes and 5-7 days for cross-country vehicle shipping. We offer fast dispatch and real-time tracking.</p>
            </div>
          </div>
        </section>

        <div className="mt-12 pt-8 border-t border-slate-800 text-center mb-16">
          <div className="inline-block bg-slate-900/80 rounded-xl p-8 border border-slate-700 shadow-2xl">
            <h3 className="text-xl font-bold text-white mb-2 flex items-center justify-center gap-2">
              <svg className="w-6 h-6 text-yellow-400" fill="currentColor" viewBox="0 0 20 20"><path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" /><path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clipRule="evenodd" /></svg>
              Fully Licensed and Bonded Auto Transport Broker
            </h3>
            <p className="text-slate-400 font-mono text-lg tracking-wider">
              USDOT: 4504932 | MC: 1782670
            </p>
          </div>
        </div>

      </div>
          <QuoteCalculatorWrapper />
      <MontwayMarketingSections />
    </main>
  );
}
