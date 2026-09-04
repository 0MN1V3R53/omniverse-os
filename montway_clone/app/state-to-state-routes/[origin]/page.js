import React from 'react';
import Link from 'next/link';
import Script from 'next/script';
import fs from 'fs';
import path from 'path';
import QuoteCalculatorWrapper from '@/components/QuoteCalculatorWrapper';
import ALL_STATES from '@/components/data/statesData';
import LocalWeatherWidget from '@/components/LocalWeatherWidget';
import { SITE_CONFIG } from '@/lib/siteConfig';

// Generate static params for all origins
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
    origin: origin.toLowerCase().replace(/\s+/g, '-'),
  }));
}

// Generate dynamic metadata
export async function generateMetadata({ params }) {
  const originSlug = params.origin;
  const originTitle = originSlug.split('-').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');

  return {
    title: `Auto Transport Routes from ${originTitle} | Sky Auto Services`,
    description: `View all interstate car shipping routes departing from ${originTitle}. Get an instant quote for fully-insured door-to-door auto transport.`,
    alternates: {
      canonical: `https://skyautoservices.com/state-to-state-routes/${originSlug}`
    }
  };
}

export default function OriginRoutes({ params }) {
  const filePath = path.join(process.cwd(), 'public', 'assets', 'data', 'state_routes.json');
  let routesData = {};
  
  try {
    const fileContents = fs.readFileSync(filePath, 'utf8');
    routesData = JSON.parse(fileContents);
  } catch (err) {
    console.error("Error reading state_routes.json", err);
  }

  const originSlug = params.origin;
  
  // Find the exact origin key matching the slug
  const originKey = Object.keys(routesData).find(
    (k) => k.toLowerCase().replace(/\s+/g, '-') === originSlug
  );

  const destinations = originKey ? routesData[originKey] : [];
  
  // Determine if a state background image exists, fallback to hypercar
  const stateObj = originKey ? ALL_STATES.find(s => s.state.toLowerCase() === originKey.toLowerCase()) : null;
  const stateBgPath = stateObj ? stateObj.img : '/assets/images/american_hypercars_fleet.png';

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": `Sky Auto Services - ${originKey || 'Auto Transport'}`,
    "description": `Premium auto transport and car shipping services from ${originKey}.`,
    "url": `https://skyautoservices.com/state-to-state-routes/${originSlug}/`,
    "telephone": SITE_CONFIG.phone,
    "address": {
      "@type": "PostalAddress",
      "addressRegion": originKey
    }
  };

  return (
    <main className="min-h-screen bg-white text-slate-900 relative">
      <Script id="origin-schema" type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
      
      {/* Hyper-Localized Hero Section */}
      <section className="relative pt-36 sm:pt-40 lg:pt-44 pb-16 px-4 min-h-[50vh] flex flex-col justify-center border-b border-slate-200 overflow-hidden">
        <div className="absolute inset-0 z-0">
          <img 
            src={stateBgPath} 
            alt={`Auto Transport from ${originKey}`}
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-slate-950/75 backdrop-blur-[2px] z-10"></div>
        </div>
        
        <div className="max-w-6xl mx-auto w-full relative z-20">
          <header className="mb-8">
            <Link href="/state-to-state-routes/" className="text-emerald-400 hover:underline mb-4 inline-flex items-center gap-1.5 font-semibold bg-white/10 px-3.5 py-1.5 rounded-full border border-white/20 text-xs sm:text-sm backdrop-blur-sm transition-colors">
              ← Back to All States
            </Link>
            <h1 className="text-2xl sm:text-4xl md:text-5xl lg:text-6xl font-extrabold mb-4 sm:mb-6 text-white drop-shadow-lg break-normal">
              <span className="inline-block">Auto Transport from</span> <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400 inline-block whitespace-nowrap">{originKey}</span>
            </h1>
            <p className="text-base sm:text-xl md:text-2xl text-slate-200 max-w-3xl drop-shadow-md mb-8">
              Select your destination state below to view detailed route information and get an instant, guaranteed car shipping quote.
            </p>
            <LocalWeatherWidget stateName={originKey} />
          </header>
        </div>
      </section>

      <section className="max-w-6xl mx-auto px-4 py-16">
        {destinations.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 mb-16">
            {destinations.map((route) => {
              const destState = ALL_STATES.find(s => s.state === route.destination);
              const destImg = destState ? destState.img : "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Yosemite_Valley_from_Wawona_Tunnel_view%2C_2020.jpg/1000px-Yosemite_Valley_from_Wawona_Tunnel_view%2C_2020.jpg";
              return (
              <Link
                key={route.slug}
                href={`/routes/${route.slug}`}
                prefetch={false}
                className="relative overflow-hidden rounded-xl border border-zinc-200 shadow-md group h-32 flex items-end p-4 transition-all hover:border-emerald-500 hover:shadow-lg"
              >
                <img 
                  src={destImg} 
                  alt={`Ship to ${route.destination}`} 
                  className="absolute inset-0 w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-slate-900/90 via-slate-900/40 to-transparent transition-opacity group-hover:opacity-90"></div>
                
                <div className="relative z-10 w-full flex items-center justify-between">
                  <div className="flex flex-col w-full overflow-hidden">
                    <span className="text-[10px] text-emerald-400 uppercase font-bold tracking-wider mb-0.5 whitespace-nowrap">Ship To</span>
                    <h2 className="text-[13px] sm:text-sm md:text-base lg:text-lg font-bold text-white group-hover:text-emerald-300 transition-colors shadow-sm whitespace-nowrap tracking-tight">
                      {route.destination}
                    </h2>
                  </div>
                  <div className="text-emerald-400 opacity-0 group-hover:opacity-100 transition-all translate-x-2 group-hover:translate-x-0">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M9 5l7 7-7 7" />
                    </svg>
                  </div>
                </div>
              </Link>
            )})}
          </div>
        ) : (
          <div className="text-center text-slate-500 py-12 bg-white/50 rounded-xl border border-slate-100">
            No routes found for this state.
          </div>
        )}

        <div className="mt-16">
          <QuoteCalculatorWrapper />
        </div>
      </section>
    </main>
  );
}
