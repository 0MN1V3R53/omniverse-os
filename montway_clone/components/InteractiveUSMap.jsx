'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { US_STATE_PATHS } from './data/usStatePaths';

const STATE_DATA = {
  "AL": { name: "Alabama", abbr: "AL", baseRate: 0.92, type: "Standard", hub: "Birmingham", routes: 72, eta: "1-3 days", weatherCoords: { lat: 32.81, lon: -86.79 } },
  "AK": { name: "Alaska", abbr: "AK", baseRate: 1.80, type: "Rural", hub: "Anchorage", routes: 45, eta: "7-10 days", weatherCoords: { lat: 61.37, lon: -152.40 } },
  "AZ": { name: "Arizona", abbr: "AZ", baseRate: 0.95, type: "Snowbird", hub: "Phoenix", routes: 84, eta: "2-4 days", weatherCoords: { lat: 34.05, lon: -111.09 } },
  "AR": { name: "Arkansas", abbr: "AR", baseRate: 0.96, type: "Standard", hub: "Little Rock", routes: 68, eta: "1-3 days", weatherCoords: { lat: 34.80, lon: -92.20 } },
  "CA": { name: "California", abbr: "CA", baseRate: 0.90, type: "Hub", hub: "Los Angeles", routes: 120, eta: "3-5 days", weatherCoords: { lat: 36.77, lon: -119.41 } },
  "CO": { name: "Colorado", abbr: "CO", baseRate: 1.10, type: "Standard", hub: "Denver", routes: 78, eta: "2-4 days", weatherCoords: { lat: 39.55, lon: -105.78 } },
  "CT": { name: "Connecticut", abbr: "CT", baseRate: 0.97, type: "Standard", hub: "Hartford", routes: 65, eta: "1-3 days", weatherCoords: { lat: 41.60, lon: -73.09 } },
  "DE": { name: "Delaware", abbr: "DE", baseRate: 0.96, type: "Standard", hub: "Wilmington", routes: 58, eta: "1-2 days", weatherCoords: { lat: 38.91, lon: -75.53 } },
  "FL": { name: "Florida", abbr: "FL", baseRate: 0.85, type: "Snowbird", hub: "Miami", routes: 115, eta: "2-4 days", weatherCoords: { lat: 27.99, lon: -81.76 } },
  "GA": { name: "Georgia", abbr: "GA", baseRate: 0.89, type: "Hub", hub: "Atlanta", routes: 96, eta: "1-3 days", weatherCoords: { lat: 33.04, lon: -83.64 } },
  "HI": { name: "Hawaii", abbr: "HI", baseRate: 2.20, type: "Rural", hub: "Honolulu", routes: 40, eta: "10-14 days", weatherCoords: { lat: 21.09, lon: -157.50 } },
  "ID": { name: "Idaho", abbr: "ID", baseRate: 1.25, type: "Rural", hub: "Boise", routes: 62, eta: "3-5 days", weatherCoords: { lat: 44.07, lon: -114.74 } },
  "IL": { name: "Illinois", abbr: "IL", baseRate: 0.92, type: "Hub", hub: "Chicago", routes: 110, eta: "1-3 days", weatherCoords: { lat: 40.63, lon: -89.39 } },
  "IN": { name: "Indiana", abbr: "IN", baseRate: 0.94, type: "Standard", hub: "Indianapolis", routes: 82, eta: "1-3 days", weatherCoords: { lat: 40.27, lon: -86.13 } },
  "IA": { name: "Iowa", abbr: "IA", baseRate: 1.00, type: "Standard", hub: "Des Moines", routes: 70, eta: "1-3 days", weatherCoords: { lat: 41.88, lon: -93.10 } },
  "KS": { name: "Kansas", abbr: "KS", baseRate: 1.02, type: "Standard", hub: "Wichita", routes: 72, eta: "2-4 days", weatherCoords: { lat: 39.01, lon: -98.48 } },
  "KY": { name: "Kentucky", abbr: "KY", baseRate: 0.95, type: "Standard", hub: "Louisville", routes: 75, eta: "1-3 days", weatherCoords: { lat: 37.84, lon: -84.27 } },
  "LA": { name: "Louisiana", abbr: "LA", baseRate: 0.93, type: "Standard", hub: "New Orleans", routes: 80, eta: "2-4 days", weatherCoords: { lat: 31.24, lon: -92.15 } },
  "ME": { name: "Maine", abbr: "ME", baseRate: 1.18, type: "Rural", hub: "Portland", routes: 55, eta: "2-4 days", weatherCoords: { lat: 45.25, lon: -69.45 } },
  "MD": { name: "Maryland", abbr: "MD", baseRate: 0.93, type: "Hub", hub: "Baltimore", routes: 76, eta: "1-3 days", weatherCoords: { lat: 39.05, lon: -76.64 } },
  "MA": { name: "Massachusetts", abbr: "MA", baseRate: 0.96, type: "Hub", hub: "Boston", routes: 85, eta: "1-3 days", weatherCoords: { lat: 42.41, lon: -71.38 } },
  "MI": { name: "Michigan", abbr: "MI", baseRate: 1.00, type: "Standard", hub: "Detroit", routes: 88, eta: "1-3 days", weatherCoords: { lat: 44.31, lon: -85.60 } },
  "MN": { name: "Minnesota", abbr: "MN", baseRate: 1.05, type: "Standard", hub: "Minneapolis", routes: 82, eta: "2-4 days", weatherCoords: { lat: 46.73, lon: -94.69 } },
  "MS": { name: "Mississippi", abbr: "MS", baseRate: 0.97, type: "Standard", hub: "Jackson", routes: 68, eta: "1-3 days", weatherCoords: { lat: 32.35, lon: -89.40 } },
  "MO": { name: "Missouri", abbr: "MO", baseRate: 0.94, type: "Standard", hub: "St. Louis", routes: 86, eta: "1-3 days", weatherCoords: { lat: 37.96, lon: -91.83 } },
  "MT": { name: "Montana", abbr: "MT", baseRate: 1.50, type: "Rural", hub: "Billings", routes: 58, eta: "3-5 days", weatherCoords: { lat: 46.96, lon: -109.53 } },
  "NE": { name: "Nebraska", abbr: "NE", baseRate: 1.05, type: "Standard", hub: "Omaha", routes: 66, eta: "2-4 days", weatherCoords: { lat: 41.49, lon: -99.90 } },
  "NV": { name: "Nevada", abbr: "NV", baseRate: 0.92, type: "Hub", hub: "Las Vegas", routes: 90, eta: "2-4 days", weatherCoords: { lat: 38.80, lon: -116.42 } },
  "NH": { name: "New Hampshire", abbr: "NH", baseRate: 1.10, type: "Standard", hub: "Manchester", routes: 60, eta: "1-3 days", weatherCoords: { lat: 43.45, lon: -71.56 } },
  "NJ": { name: "New Jersey", abbr: "NJ", baseRate: 0.95, type: "Hub", hub: "Newark", routes: 92, eta: "1-2 days", weatherCoords: { lat: 40.06, lon: -74.41 } },
  "NM": { name: "New Mexico", abbr: "NM", baseRate: 1.12, type: "Standard", hub: "Albuquerque", routes: 74, eta: "2-4 days", weatherCoords: { lat: 34.52, lon: -105.87 } },
  "NY": { name: "New York", abbr: "NY", baseRate: 0.95, type: "Hub", hub: "New York City", routes: 118, eta: "1-3 days", weatherCoords: { lat: 43.29, lon: -75.52 } },
  "NC": { name: "North Carolina", abbr: "NC", baseRate: 0.92, type: "Standard", hub: "Charlotte", routes: 94, eta: "1-3 days", weatherCoords: { lat: 35.76, lon: -79.02 } },
  "ND": { name: "North Dakota", abbr: "ND", baseRate: 1.35, type: "Rural", hub: "Fargo", routes: 54, eta: "3-5 days", weatherCoords: { lat: 47.55, lon: -101.00 } },
  "OH": { name: "Ohio", abbr: "OH", baseRate: 0.93, type: "Hub", hub: "Columbus", routes: 98, eta: "1-3 days", weatherCoords: { lat: 40.42, lon: -82.91 } },
  "OK": { name: "Oklahoma", abbr: "OK", baseRate: 0.98, type: "Standard", hub: "Oklahoma City", routes: 76, eta: "2-4 days", weatherCoords: { lat: 35.01, lon: -97.09 } },
  "OR": { name: "Oregon", abbr: "OR", baseRate: 1.08, type: "Standard", hub: "Portland", routes: 80, eta: "3-5 days", weatherCoords: { lat: 44.00, lon: -120.50 } },
  "PA": { name: "Pennsylvania", abbr: "PA", baseRate: 0.93, type: "Hub", hub: "Philadelphia", routes: 102, eta: "1-3 days", weatherCoords: { lat: 41.20, lon: -77.19 } },
  "RI": { name: "Rhode Island", abbr: "RI", baseRate: 0.97, type: "Standard", hub: "Providence", routes: 52, eta: "1-2 days", weatherCoords: { lat: 41.58, lon: -71.48 } },
  "SC": { name: "South Carolina", abbr: "SC", baseRate: 0.91, type: "Standard", hub: "Columbia", routes: 82, eta: "1-3 days", weatherCoords: { lat: 33.84, lon: -81.16 } },
  "SD": { name: "South Dakota", abbr: "SD", baseRate: 1.30, type: "Rural", hub: "Sioux Falls", routes: 56, eta: "3-5 days", weatherCoords: { lat: 43.97, lon: -99.90 } },
  "TN": { name: "Tennessee", abbr: "TN", baseRate: 0.91, type: "Standard", hub: "Nashville", routes: 90, eta: "1-3 days", weatherCoords: { lat: 35.52, lon: -86.58 } },
  "TX": { name: "Texas", abbr: "TX", baseRate: 0.88, type: "Hub", hub: "Dallas", routes: 135, eta: "2-4 days", weatherCoords: { lat: 31.96, lon: -99.90 } },
  "UT": { name: "Utah", abbr: "UT", baseRate: 1.05, type: "Standard", hub: "Salt Lake City", routes: 76, eta: "2-4 days", weatherCoords: { lat: 39.32, lon: -111.09 } },
  "VT": { name: "Vermont", abbr: "VT", baseRate: 1.20, type: "Rural", hub: "Burlington", routes: 50, eta: "1-3 days", weatherCoords: { lat: 44.56, lon: -72.58 } },
  "VA": { name: "Virginia", abbr: "VA", baseRate: 0.92, type: "Standard", hub: "Richmond", routes: 90, eta: "1-3 days", weatherCoords: { lat: 37.43, lon: -78.66 } },
  "WA": { name: "Washington", abbr: "WA", baseRate: 1.05, type: "Standard", hub: "Seattle", routes: 88, eta: "3-5 days", weatherCoords: { lat: 47.75, lon: -120.74 } },
  "WV": { name: "West Virginia", abbr: "WV", baseRate: 1.10, type: "Standard", hub: "Charleston", routes: 62, eta: "1-3 days", weatherCoords: { lat: 38.60, lon: -80.45 } },
  "WI": { name: "Wisconsin", abbr: "WI", baseRate: 1.02, type: "Standard", hub: "Milwaukee", routes: 80, eta: "1-3 days", weatherCoords: { lat: 43.78, lon: -88.78 } },
  "WY": { name: "Wyoming", abbr: "WY", baseRate: 1.45, type: "Rural", hub: "Cheyenne", routes: 56, eta: "3-5 days", weatherCoords: { lat: 43.07, lon: -107.29 } },
  "DC": { name: "District of Columbia", abbr: "DC", baseRate: 0.93, type: "Hub", hub: "Washington D.C.", routes: 60, eta: "1-2 days", weatherCoords: { lat: 38.91, lon: -77.04 } }
};

export default function InteractiveUSMap() {
  const [selectedState, setSelectedState] = useState(null);
  const [hoveredState, setHoveredState] = useState(null);
  const [weather, setWeather] = useState(null);
  const [weatherLoading, setWeatherLoading] = useState(false);

  const selectState = (abbr) => {
    const data = STATE_DATA[abbr] || { 
      name: abbr, 
      abbr, 
      baseRate: 1.00, 
      type: "Standard", 
      hub: "Statewide Routes", 
      routes: 60, 
      eta: "2-4 days",
      weatherCoords: { lat: 39.82, lon: -98.57 }
    };
    setSelectedState(data);
    fetchWeather(data);
  };

  const closeStateModal = (e) => {
    if (e) e.stopPropagation();
    setSelectedState(null);
    setWeather(null);
  };

  const fetchWeather = async (state) => {
    if (!state.weatherCoords) return;
    setWeatherLoading(true);
    try {
      const res = await fetch(
        `https://api.open-meteo.com/v1/forecast?latitude=${state.weatherCoords.lat}&longitude=${state.weatherCoords.lon}&current_weather=true&temperature_unit=fahrenheit`
      );
      const data = await res.json();
      if (data && data.current_weather) {
        setWeather(data.current_weather);
      } else {
        setWeather({ temperature: 74, windspeed: 8 });
      }
    } catch (e) {
      setWeather({ temperature: 72, windspeed: 6 });
    } finally {
      setWeatherLoading(false);
    }
  };

  const prefillAndScroll = (stateName) => {
    if (typeof window !== 'undefined') {
      const originInput = document.getElementById('quote-calc-origin') || document.querySelector('input[name="origin"]');
      if (originInput) {
        originInput.value = stateName;
        originInput.dispatchEvent(new Event('input', { bubbles: true }));
        originInput.dispatchEvent(new Event('change', { bubbles: true }));
      }
      const calc = document.getElementById('quote-calculator-top') || document.getElementById('quote-calculator');
      if (calc) {
        calc.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }
  };

  return (
    <div className="relative w-full max-w-6xl mx-auto my-6 select-none">
      {/* Title Header */}
      <div className="text-center mb-8">
        <h2 className="text-3xl md:text-4xl font-extrabold text-slate-900 mb-3 tracking-tight">
          Interactive Pricing Map
        </h2>
        <p className="text-slate-500 text-lg">
          Click any state to see local shipping rates and get an instant quote
        </p>
      </div>

      {/* Map Card Container */}
      <div 
        className="map-container relative w-full rounded-3xl overflow-hidden shadow-2xl border border-slate-200 bg-slate-900 flex items-center justify-center min-h-[480px] lg:min-h-[560px]"
        onClick={closeStateModal}
      >
        {/* Floating Instructions Badge (when no state is active) */}
        {!selectedState && (
          <div className="absolute top-6 left-0 right-0 flex flex-col items-center pointer-events-none z-20">
            <span className="bg-slate-900/90 backdrop-blur-md border border-slate-700 text-slate-200 text-sm font-medium px-5 py-2 rounded-full shadow-xl">
              👆 Click any state for pricing
            </span>
          </div>
        )}

        {/* Zero-Dependency SVG Vector Map */}
        <div className="w-full h-full p-3 sm:p-6 flex items-center justify-center">
          <svg
            viewBox="0 0 959 593"
            className="w-full h-auto max-h-[520px] select-none filter drop-shadow-2xl"
            xmlns="http://www.w3.org/2000/svg"
          >
            <defs>
              <pattern id="flag-pattern-us" patternUnits="userSpaceOnUse" width="800" height="600">
                <rect width="800" height="600" fill="#1e293b" />
              </pattern>
            </defs>

            {Object.entries(US_STATE_PATHS).map(([abbr, info]) => {
              const isSelected = selectedState && selectedState.abbr === abbr;
              const isHovered = hoveredState === abbr;

              if (info.circle) {
                return (
                  <circle
                    key={abbr}
                    cx={info.circle.cx}
                    cy={info.circle.cy}
                    r={info.circle.r + (isSelected ? 4 : isHovered ? 2 : 0)}
                    fill={isSelected ? '#2563eb' : isHovered ? '#3b82f6' : '#475569'}
                    stroke={isSelected ? '#93c5fd' : isHovered ? '#60a5fa' : '#334155'}
                    strokeWidth={isSelected ? 2.5 : 1}
                    className="cursor-pointer transition-all duration-200"
                    onClick={(e) => {
                      e.stopPropagation();
                      selectState(abbr);
                    }}
                    onMouseEnter={() => setHoveredState(abbr)}
                    onMouseLeave={() => setHoveredState(null)}
                  >
                    <title>{info.name}</title>
                  </circle>
                );
              }

              return (
                <path
                  key={abbr}
                  d={info.d}
                  fill={isSelected ? '#2563eb' : isHovered ? '#1d4ed8' : '#1e293b'}
                  stroke={isSelected ? '#60a5fa' : isHovered ? '#93c5fd' : '#334155'}
                  strokeWidth={isSelected ? 2 : isHovered ? 1.5 : 0.8}
                  className="cursor-pointer transition-colors duration-150"
                  onClick={(e) => {
                    e.stopPropagation();
                    selectState(abbr);
                  }}
                  onMouseEnter={() => setHoveredState(abbr)}
                  onMouseLeave={() => setHoveredState(null)}
                >
                  <title>{info.name}</title>
                </path>
              );
            })}
          </svg>
        </div>

        {/* Floating State Detail Popover Modal */}
        {selectedState && (
          <div 
            className="absolute inset-0 z-40 flex items-center justify-center p-4 bg-black/40 backdrop-blur-[2px]"
            onClick={closeStateModal}
          >
            <div 
              className="w-full max-w-sm bg-slate-900/95 backdrop-blur-xl border border-slate-700/80 rounded-2xl shadow-2xl text-white p-6 relative animate-in zoom-in-95 duration-200"
              onClick={(e) => e.stopPropagation()}
            >
              {/* Header */}
              <div className="flex items-center justify-between mb-3 border-b border-slate-800 pb-3">
                <div>
                  <h3 className="text-2xl font-extrabold leading-tight text-white">
                    {selectedState.name}
                  </h3>
                  <span className="text-xs font-bold bg-blue-600 text-white px-2.5 py-0.5 rounded-full mt-1 inline-block">
                    {selectedState.type} Route Corridor
                  </span>
                </div>
                <button
                  onClick={closeStateModal}
                  className="w-8 h-8 flex items-center justify-center rounded-full bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition-colors text-base font-bold flex-shrink-0"
                  aria-label="Close"
                >
                  ✕
                </button>
              </div>

              {/* Weather Bar */}
              <div className="h-7 mb-3 flex items-center">
                {weatherLoading ? (
                  <div className="text-slate-400 text-xs animate-pulse">
                    🌤️ Updating live corridor weather…
                  </div>
                ) : weather ? (
                  <div className="flex items-center gap-3 text-sky-400 font-semibold text-sm">
                    <span>🌤️ {weather.temperature}°F</span>
                    <span>💨 {weather.windspeed} mph</span>
                    <span className="text-slate-500 text-xs font-normal">Live Conditions</span>
                  </div>
                ) : (
                  <div className="text-slate-400 text-xs">
                    🌤️ 74°F · 6 mph
                  </div>
                )}
              </div>

              {/* Base Rates Per Mile */}
              <div className="bg-slate-800/90 rounded-xl border border-slate-700/60 p-3.5 mb-4 space-y-2">
                <div className="text-xs font-bold uppercase tracking-widest text-slate-400 mb-2">
                  Estimated Base Rate / Mile
                </div>
                <div className="flex justify-between items-center text-sm border-b border-slate-700/50 pb-1.5">
                  <span className="text-slate-300 font-medium">Standard Sedan</span>
                  <span className="font-mono text-emerald-400 font-bold">
                    ${(selectedState.baseRate * 1.0).toFixed(2)}/mi
                  </span>
                </div>
                <div className="flex justify-between items-center text-sm border-b border-slate-700/50 pb-1.5">
                  <span className="text-slate-300 font-medium">Heavy SUV / Truck</span>
                  <span className="font-mono text-emerald-400 font-bold">
                    ${(selectedState.baseRate * 1.3).toFixed(2)}/mi
                  </span>
                </div>
                <div className="flex justify-between items-center text-sm">
                  <span className="text-slate-300 font-medium">Enclosed Trailer</span>
                  <span className="font-mono text-emerald-400 font-bold">
                    ${(selectedState.baseRate * 1.6).toFixed(2)}/mi
                  </span>
                </div>
              </div>

              {/* Route Perks Bullet List */}
              <ul className="text-xs text-slate-300 space-y-1.5 mb-5">
                <li className="flex items-center gap-2">
                  <span className="text-amber-400 font-bold">⚡</span>
                  <span>Summer Peak: Guaranteed dispatch &amp; tracking</span>
                </li>
                <li className="flex items-center gap-2">
                  <span className="text-blue-400 font-bold">📍</span>
                  <span>Primary Hub: <strong className="text-white">{selectedState.hub}</strong> &amp; Statewide</span>
                </li>
                <li className="flex items-center gap-2">
                  <span className="text-emerald-400 font-bold">🛡️</span>
                  <span>Full $100k–$1M+ Cargo Insurance Included</span>
                </li>
              </ul>

              {/* Action Buttons */}
              <div className="space-y-2">
                <button
                  onClick={() => {
                    prefillAndScroll(selectedState.name);
                    closeStateModal();
                  }}
                  className="block w-full text-center py-3 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-xl transition-all shadow-lg hover:shadow-emerald-500/25 text-sm"
                >
                  Get Instant Quote for {selectedState.name} →
                </button>
                <Link
                  href={`/state-to-state-routes/${selectedState.name.toLowerCase().replace(/\s+/g, '-')}`}
                  className="block w-full text-center py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white font-semibold rounded-xl transition-colors text-xs border border-slate-700"
                >
                  View All {selectedState.name} Shipping Routes ›
                </Link>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
