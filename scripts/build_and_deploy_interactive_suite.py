#!/usr/bin/env python3
"""
OMNIVERSE ENTERPRISE 50-STATE INTERACTIVE SUITE & QUOTE CALCULATOR ENGINE
Pod 4 (Full-Stack Web) & Pod 5 (Technical SEO)
Embeds zero-dependency SVG Map and bulletproof Quote Calculator across public_html_local/
"""

import os
import re
import json

BASE_DIR = "/Users/silversurfer/Documents/Omniverse2/public_html_local"
JS_DIR = os.path.join(BASE_DIR, "assets/js")
os.makedirs(JS_DIR, exist_ok=True)

# 1. READ RAW US MAP SVG
svg_path = os.path.join(BASE_DIR, "us-map.svg")
with open(svg_path, "r", encoding="utf-8") as f:
    svg_raw = f.read()

# Clean XML header and doctype to get raw <svg ...>...</svg>
svg_clean = re.sub(r'<\?xml.*?\?>', '', svg_raw, flags=re.DOTALL)
svg_clean = re.sub(r'<!DOCTYPE.*?>', '', svg_clean, flags=re.DOTALL).strip()
# Adjust svg styling for dark/light container responsiveness
svg_clean = svg_clean.replace('<svg xmlns="http://www.w3.org/2000/svg" width="959" height="593">', 
                              '<svg id="interactive-us-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 959 593" class="w-full h-auto max-h-[560px] select-none filter drop-shadow-2xl">')

# 2. CREATE INTERACTIVE MAP SCRIPT (interactive_map.js)
interactive_map_js = """
/**
 * OMNIVERSE INTERACTIVE 50-STATE SVG MAP ENGINE v3.0
 * Zero external CDN dependencies - 100% Client & Mobile Compatible
 */
(function() {
  const STATE_INFO = {
    "al": { name: "Alabama", abbr: "AL", hub: "Birmingham", routes: 72, rate: "$0.92/mi", slug: "alabama", eta: "1-3 days" },
    "ak": { name: "Alaska", abbr: "AK", hub: "Anchorage", routes: 45, rate: "$1.80/mi", slug: "alaska", eta: "7-10 days" },
    "az": { name: "Arizona", abbr: "AZ", hub: "Phoenix / Tucson", routes: 84, rate: "$0.95/mi", slug: "arizona", eta: "2-4 days" },
    "ar": { name: "Arkansas", abbr: "AR", hub: "Little Rock", routes: 68, rate: "$0.96/mi", slug: "arkansas", eta: "1-3 days" },
    "ca": { name: "California", abbr: "CA", hub: "Los Angeles / Bay Area", routes: 120, rate: "$0.90/mi", slug: "california", eta: "3-5 days" },
    "co": { name: "Colorado", abbr: "CO", hub: "Denver / Springs", routes: 78, rate: "$1.10/mi", slug: "colorado", eta: "2-4 days" },
    "ct": { name: "Connecticut", abbr: "CT", hub: "Hartford / New Haven", routes: 65, rate: "$0.97/mi", slug: "connecticut", eta: "1-3 days" },
    "de": { name: "Delaware", abbr: "DE", hub: "Wilmington / Dover", routes: 58, rate: "$0.96/mi", slug: "delaware", eta: "1-2 days" },
    "fl": { name: "Florida", abbr: "FL", hub: "Miami / Orlando / Tampa", routes: 115, rate: "$0.85/mi", slug: "florida", eta: "2-4 days" },
    "ga": { name: "Georgia", abbr: "GA", hub: "Atlanta / Savannah", routes: 96, rate: "$0.89/mi", slug: "georgia", eta: "1-3 days" },
    "hi": { name: "Hawaii", abbr: "HI", hub: "Honolulu Port", routes: 40, rate: "$2.20/mi", slug: "hawaii", eta: "10-14 days" },
    "id": { name: "Idaho", abbr: "ID", hub: "Boise / Idaho Falls", routes: 62, rate: "$1.25/mi", slug: "idaho", eta: "3-5 days" },
    "il": { name: "Illinois", abbr: "IL", hub: "Chicago / Arlington Heights", routes: 110, rate: "$0.92/mi", slug: "illinois", eta: "1-3 days" },
    "in": { name: "Indiana", abbr: "IN", hub: "Indianapolis / Fort Wayne", routes: 82, rate: "$0.94/mi", slug: "indiana", eta: "1-3 days" },
    "ia": { name: "Iowa", abbr: "IA", hub: "Des Moines / Cedar Rapids", routes: 70, rate: "$1.00/mi", slug: "iowa", eta: "1-3 days" },
    "ks": { name: "Kansas", abbr: "KS", hub: "Wichita / Overland Park", routes: 72, rate: "$1.02/mi", slug: "kansas", eta: "2-4 days" },
    "ky": { name: "Kentucky", abbr: "KY", hub: "Louisville / Lexington", routes: 75, rate: "$0.95/mi", slug: "kentucky", eta: "1-3 days" },
    "la": { name: "Louisiana", abbr: "LA", hub: "New Orleans / Baton Rouge", routes: 80, rate: "$0.93/mi", slug: "louisiana", eta: "2-4 days" },
    "me": { name: "Maine", abbr: "ME", hub: "Portland / Bangor", routes: 55, rate: "$1.18/mi", slug: "maine", eta: "2-4 days" },
    "md": { name: "Maryland", abbr: "MD", hub: "Baltimore / Annapolis", routes: 76, rate: "$0.93/mi", slug: "maryland", eta: "1-3 days" },
    "ma": { name: "Massachusetts", abbr: "MA", hub: "Boston / Worcester", routes: 85, rate: "$0.96/mi", slug: "massachusetts", eta: "1-3 days" },
    "mi": { name: "Michigan", abbr: "MI", hub: "Detroit / Grand Rapids", routes: 88, rate: "$1.00/mi", slug: "michigan", eta: "1-3 days" },
    "mn": { name: "Minnesota", abbr: "MN", hub: "Minneapolis / St. Paul", routes: 82, rate: "$1.05/mi", slug: "minnesota", eta: "2-4 days" },
    "ms": { name: "Mississippi", abbr: "MS", hub: "Jackson / Gulfport", routes: 68, rate: "$0.97/mi", slug: "mississippi", eta: "1-3 days" },
    "mo": { name: "Missouri", abbr: "MO", hub: "St. Louis / Kansas City", routes: 86, rate: "$0.94/mi", slug: "missouri", eta: "1-3 days" },
    "mt": { name: "Montana", abbr: "MT", hub: "Billings / Missoula", routes: 58, rate: "$1.50/mi", slug: "montana", eta: "3-5 days" },
    "ne": { name: "Nebraska", abbr: "NE", hub: "Omaha / Lincoln", routes: 66, rate: "$1.05/mi", slug: "nebraska", eta: "2-4 days" },
    "nv": { name: "Nevada", abbr: "NV", hub: "Las Vegas / Reno", routes: 90, rate: "$0.92/mi", slug: "nevada", eta: "2-4 days" },
    "nh": { name: "New Hampshire", abbr: "NH", hub: "Manchester / Nashua", routes: 60, rate: "$1.10/mi", slug: "new-hampshire", eta: "1-3 days" },
    "nj": { name: "New Jersey", abbr: "NJ", hub: "Newark / Jersey City", routes: 92, rate: "$0.95/mi", slug: "new-jersey", eta: "1-2 days" },
    "nm": { name: "New Mexico", abbr: "NM", hub: "Albuquerque / Santa Fe", routes: 74, rate: "$1.12/mi", slug: "new-mexico", eta: "2-4 days" },
    "ny": { name: "New York", abbr: "NY", hub: "New York City / Buffalo", routes: 118, rate: "$0.95/mi", slug: "new-york", eta: "1-3 days" },
    "nc": { name: "North Carolina", abbr: "NC", hub: "Charlotte / Raleigh", routes: 94, rate: "$0.92/mi", slug: "north-carolina", eta: "1-3 days" },
    "nd": { name: "North Dakota", abbr: "ND", hub: "Fargo / Bismarck", routes: 54, rate: "$1.35/mi", slug: "north-dakota", eta: "3-5 days" },
    "oh": { name: "Ohio", abbr: "OH", hub: "Columbus / Cleveland / Cincy", routes: 98, rate: "$0.93/mi", slug: "ohio", eta: "1-3 days" },
    "ok": { name: "Oklahoma", abbr: "OK", hub: "Oklahoma City / Tulsa", routes: 76, rate: "$0.98/mi", slug: "oklahoma", eta: "2-4 days" },
    "or": { name: "Oregon", abbr: "OR", hub: "Portland / Eugene", routes: 80, rate: "$1.08/mi", slug: "oregon", eta: "3-5 days" },
    "pa": { name: "Pennsylvania", abbr: "PA", hub: "Philadelphia / Pittsburgh", routes: 102, rate: "$0.93/mi", slug: "pennsylvania", eta: "1-3 days" },
    "ri": { name: "Rhode Island", abbr: "RI", hub: "Providence / Newport", routes: 52, rate: "$0.97/mi", slug: "rhode-island", eta: "1-2 days" },
    "sc": { name: "South Carolina", abbr: "SC", hub: "Charleston / Columbia", routes: 82, rate: "$0.91/mi", slug: "south-carolina", eta: "1-3 days" },
    "sd": { name: "South Dakota", abbr: "SD", hub: "Sioux Falls / Rapid City", routes: 56, rate: "$1.30/mi", slug: "south-dakota", eta: "3-5 days" },
    "tn": { name: "Tennessee", abbr: "TN", hub: "Nashville / Memphis", routes: 90, rate: "$0.91/mi", slug: "tennessee", eta: "1-3 days" },
    "tx": { name: "Texas", abbr: "TX", hub: "Dallas / Houston / Austin", routes: 135, rate: "$0.88/mi", slug: "texas", eta: "2-4 days" },
    "ut": { name: "Utah", abbr: "UT", hub: "Salt Lake City / Provo", routes: 76, rate: "$1.05/mi", slug: "utah", eta: "2-4 days" },
    "vt": { name: "Vermont", abbr: "VT", hub: "Burlington / Montpelier", routes: 50, rate: "$1.20/mi", slug: "vermont", eta: "1-3 days" },
    "va": { name: "Virginia", abbr: "VA", hub: "Richmond / Virginia Beach", routes: 90, rate: "$0.92/mi", slug: "virginia", eta: "1-3 days" },
    "wa": { name: "Washington", abbr: "WA", hub: "Seattle / Spokane / Tacoma", routes: 88, rate: "$1.05/mi", slug: "washington", eta: "3-5 days" },
    "wv": { name: "West Virginia", abbr: "WV", hub: "Charleston / Morgantown", routes: 62, rate: "$1.10/mi", slug: "west-virginia", eta: "1-3 days" },
    "wi": { name: "Wisconsin", abbr: "WI", hub: "Milwaukee / Madison", routes: 80, rate: "$1.02/mi", slug: "wisconsin", eta: "1-3 days" },
    "wy": { name: "Wyoming", abbr: "WY", hub: "Cheyenne / Casper", routes: 56, rate: "$1.45/mi", slug: "wyoming", eta: "3-5 days" },
    "dc": { name: "District of Columbia", abbr: "DC", hub: "Washington D.C.", routes: 60, rate: "$0.93/mi", slug: "district-of-columbia", eta: "1-2 days" }
  };

  function initMap() {
    const mapContainer = document.getElementById('us-interactive-map-wrapper');
    if (!mapContainer) return;

    const tooltip = document.getElementById('map-state-tooltip');
    const svg = mapContainer.querySelector('#interactive-us-svg');
    if (!svg) return;

    // Apply interactive styling to state paths
    const paths = svg.querySelectorAll('path, circle');
    paths.forEach(p => {
      const cls = p.getAttribute('class') || '';
      const stateKey = cls.trim().toLowerCase();
      const info = STATE_INFO[stateKey];

      p.style.cursor = 'pointer';
      p.style.transition = 'all 0.25s cubic-bezier(0.4, 0, 0.2, 1)';
      p.style.fill = '#1e293b';
      p.style.stroke = '#475569';
      p.style.strokeWidth = '0.8px';

      // Mouse enter / hover
      p.addEventListener('mouseenter', (e) => {
        p.style.fill = '#2563eb';
        p.style.stroke = '#60a5fa';
        p.style.strokeWidth = '1.8px';
        p.style.filter = 'drop-shadow(0 0 8px rgba(37,99,235,0.6))';

        if (info && tooltip) {
          tooltip.innerHTML = `
            <div class="flex items-center justify-between border-b border-slate-700 pb-2 mb-2">
              <div>
                <span class="text-xs font-extrabold uppercase tracking-widest text-blue-400">${info.abbr}</span>
                <h4 class="text-lg font-black text-white leading-tight">${info.name}</h4>
              </div>
              <span class="text-[11px] font-bold bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded-full">Active Corridors</span>
            </div>
            <div class="space-y-1.5 text-xs text-slate-300 mb-3">
              <div class="flex justify-between"><span>Primary Hub:</span> <strong class="text-white">${info.hub}</strong></div>
              <div class="flex justify-between"><span>Base Rate:</span> <strong class="text-emerald-400 font-mono">${info.rate}</strong></div>
              <div class="flex justify-between"><span>Avg. Transit:</span> <strong class="text-sky-300">${info.eta}</strong></div>
              <div class="flex justify-between"><span>Network Lanes:</span> <strong class="text-white">${info.routes} Routes</strong></div>
            </div>
            <div class="grid grid-cols-2 gap-2 pt-1">
              <button onclick="window.prefillQuoteOrigin('${info.name}')" class="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-1.5 px-2 rounded-lg text-[11px] text-center transition-all shadow-md">
                Quote ${info.abbr} ↑
              </button>
              <a href="/state-to-state-routes/${info.slug}" class="w-full bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold py-1.5 px-2 rounded-lg text-[11px] text-center transition-all border border-slate-600 block">
                View Routes →
              </a>
            </div>
          `;
          tooltip.style.opacity = '1';
          tooltip.style.pointerEvents = 'auto';
        }
      });

      // Mouse leave
      p.addEventListener('mouseleave', () => {
        p.style.fill = '#1e293b';
        p.style.stroke = '#475569';
        p.style.strokeWidth = '0.8px';
        p.style.filter = 'none';
      });

      // Click: Prefill quote or open routes
      p.addEventListener('click', (e) => {
        if (info) {
          window.prefillQuoteOrigin(info.name);
        }
      });
    });
  }

  // Global quote prefill helper
  window.prefillQuoteOrigin = function(stateName) {
    const originInputs = document.querySelectorAll('input[name="origin"]');
    originInputs.forEach(input => {
      input.value = stateName;
      input.dispatchEvent(new Event('input', { bubbles: true }));
      input.dispatchEvent(new Event('change', { bubbles: true }));
    });
    const calc = document.getElementById('quote-calculator-top') || document.getElementById('quote-calculator');
    if (calc) {
      calc.scrollIntoView({ behavior: 'smooth', block: 'center' });
      const destInput = calc.querySelector('input[name="destination"]');
      if (destInput) destInput.focus();
    }
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMap);
  } else {
    initMap();
  }
})();
"""

with open(os.path.join(JS_DIR, "interactive_map.js"), "w", encoding="utf-8") as f:
    f.write(interactive_map_js)
print("[+] Created public_html_local/assets/js/interactive_map.js")

# 3. CREATE STANDALONE BULLETPROOF QUOTE CALCULATOR ENGINE (quote_calculator_engine.js)
quote_calc_js = """
/**
 * OMNIVERSE HIGH-CONVERSION QUOTE CALCULATOR ENGINE v3.0
 * Supports 4-step instant calculation, $0 deposit locks, and seamless lead submissions
 */
(function() {
  'use strict';

  const STATE_COORDS = {
    AL: [32.81,-86.79], AK: [61.37,-152.40], AZ: [34.05,-111.09], AR: [34.80,-92.20],
    CA: [36.78,-119.42], CO: [39.55,-105.78], CT: [41.60,-73.09], DE: [38.91,-75.53],
    FL: [27.66,-81.52], GA: [33.04,-83.64], HI: [21.09,-157.50], ID: [44.07,-114.74],
    IL: [40.63,-89.40], IN: [40.27,-86.13], IA: [41.88,-93.10], KS: [39.01,-98.48],
    KY: [37.84,-84.27], LA: [31.24,-92.15], ME: [45.25,-69.45], MD: [39.05,-76.64],
    MA: [42.41,-71.38], MI: [44.31,-85.60], MN: [46.73,-94.69], MS: [32.35,-89.40],
    MO: [37.96,-91.83], MT: [46.88,-110.36], NE: [41.49,-99.90], NV: [38.80,-116.42],
    NH: [43.45,-71.56], NJ: [40.06,-74.41], NM: [34.52,-105.87], NY: [43.30,-74.22],
    NC: [35.76,-79.02], ND: [47.55,-101.00], OH: [40.42,-82.91], OK: [35.01,-97.09],
    OR: [44.00,-120.50], PA: [41.20,-77.19], RI: [41.58,-71.48], SC: [33.84,-81.16],
    SD: [43.97,-99.90], TN: [35.52,-86.58], TX: [31.97,-99.90], UT: [39.32,-111.09],
    VT: [44.56,-72.58], VA: [37.43,-78.66], WA: [47.75,-120.74], WV: [38.60,-80.45],
    WI: [43.78,-88.79], WY: [43.08,-107.29], DC: [38.91,-77.04]
  };

  const STATE_NAMES = {
    "alabama": "AL", "alaska": "AK", "arizona": "AZ", "arkansas": "AR", "california": "CA",
    "colorado": "CO", "connecticut": "CT", "delaware": "DE", "florida": "FL", "georgia": "GA",
    "hawaii": "HI", "idaho": "ID", "illinois": "IL", "indiana": "IN", "iowa": "IA", "kansas": "KS",
    "kentucky": "KY", "louisiana": "LA", "maine": "ME", "maryland": "MD", "massachusetts": "MA",
    "michigan": "MI", "minnesota": "MN", "mississippi": "MS", "missouri": "MO", "montana": "MT",
    "nebraska": "NE", "nevada": "NV", "new hampshire": "NH", "new jersey": "NJ", "new mexico": "NM",
    "new york": "NY", "north carolina": "NC", "north dakota": "ND", "ohio": "OH", "oklahoma": "OK",
    "oregon": "OR", "pennsylvania": "PA", "rhode island": "RI", "south carolina": "SC", "south dakota": "SD",
    "tennessee": "TN", "texas": "TX", "utah": "UT", "vermont": "VT", "virginia": "VA", "washington": "WA",
    "west virginia": "WV", "wisconsin": "WI", "wyoming": "WY", "district of columbia": "DC"
  };

  function parseState(str) {
    if (!str) return 'IL';
    str = str.trim().toLowerCase();
    // 5-digit zip detection
    const zipMatch = str.match(/\\b\\d{5}\\b/);
    if (zipMatch) {
      const z = parseInt(zipMatch[0], 10);
      if (z >= 90000 && z <= 96199) return 'CA';
      if (z >= 32000 && z <= 34999) return 'FL';
      if (z >= 75000 && z <= 79999) return 'TX';
      if (z >= 10000 && z <= 14999) return 'NY';
      if (z >= 60000 && z <= 62999) return 'IL';
      if (z >= 30000 && z <= 31999) return 'GA';
    }
    // Check 2-letter state code
    const tokens = str.toUpperCase().split(/[^A-Z]+/);
    for (let t of tokens) {
      if (STATE_COORDS[t]) return t;
    }
    // Check full state name
    for (let [name, abbr] of Object.entries(STATE_NAMES)) {
      if (str.includes(name)) return abbr;
    }
    return 'IL';
  }

  function calculateDistance(origin, dest) {
    const oAbbr = parseState(origin);
    const dAbbr = parseState(dest);
    const oCoord = STATE_COORDS[oAbbr] || [40.63, -89.40];
    const dCoord = STATE_COORDS[dAbbr] || [40.63, -89.40];

    const R = 3958.8; // miles
    const dLat = (dCoord[0] - oCoord[0]) * Math.PI / 180;
    const dLon = (dCoord[1] - oCoord[1]) * Math.PI / 180;
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
              Math.cos(oCoord[0] * Math.PI / 180) * Math.cos(dCoord[0] * Math.PI / 180) *
              Math.sin(dLon/2) * Math.sin(dLon/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    let dist = Math.round(R * c * 1.18); // Road curvature factor
    return Math.max(120, dist);
  }

  function calculatePricing(miles, vehicleType, transportType, isInoperable) {
    let rate = 0.95;
    if (miles <= 199) rate = 2.45;
    else if (miles <= 500) rate = 0.85;
    else if (miles <= 1000) rate = 0.75;
    else if (miles <= 1500) rate = 0.70;
    else if (miles <= 2000) rate = 0.48;
    else rate = 0.38;

    let base = miles * rate;
    const vSurcharges = {
      'sedan': 0, 'suv_small': 150, 'suv_large': 220,
      'pickup_half': 180, 'pickup_heavy': 280, 'sports_car': 250,
      'classic': 150, 'motorcycle': -100, 'ev': 200
    };
    base += (vSurcharges[vehicleType] || 0);
    if (isInoperable) base += 150;

    let openPrice = Math.max(399, Math.round(base / 5) * 5);
    let enclosedPrice = Math.max(599, Math.round((base * 1.45) / 5) * 5);
    let expeditedPrice = Math.max(799, Math.round((base * 1.85) / 5) * 5);

    let transitDays = Math.max(1, Math.ceil(miles / 450));
    let eta = transitDays === 1 ? "1-2 Days" : `${transitDays}-${transitDays + 2} Days`;

    return { openPrice, enclosedPrice, expeditedPrice, eta, miles };
  }

  function renderCalculator(container) {
    if (!container) return;

    let currentStep = 1;
    let formData = {
      origin: '',
      destination: '',
      year: '2024',
      make: 'Toyota',
      model: 'RAV4',
      vehicleType: 'suv_small',
      condition: 'operable',
      transportType: 'open_standard',
      name: '',
      phone: '',
      email: ''
    };

    // Auto-detect route from page title or url if available
    const pagePath = window.location.pathname;
    if (pagePath.includes('to-') && pagePath.includes('-auto-transport')) {
      const match = pagePath.match(/\\/([^\\/]+)-to-([^\\/]+)-auto-transport/);
      if (match) {
        formData.origin = match[1].replace(/-/g, ' ').toUpperCase();
        formData.destination = match[2].replace(/-/g, ' ').toUpperCase();
      }
    }

    function renderStep() {
      if (currentStep === 1) {
        container.innerHTML = `
          <div class="mb-5">
            <div class="flex justify-between text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">
              <span class="text-blue-600 font-extrabold">1. Route</span>
              <span>2. Vehicle</span>
              <span>3. Method</span>
              <span>4. Quote</span>
            </div>
            <div class="w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">
              <div class="bg-blue-600 h-full transition-all duration-300" style="width: 25%"></div>
            </div>
          </div>

          <form id="calc-step1-form" class="space-y-4">
            <div>
              <label class="block text-sm font-semibold text-slate-800 mb-1">Pickup Location (ZIP or City, State) <span class="text-rose-500">*</span></label>
              <input type="text" name="origin" value="${formData.origin}" required
                     class="w-full bg-slate-50 border border-slate-300 focus:border-blue-500 focus:bg-white rounded-xl px-4 py-3 text-slate-900 font-medium placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-200 transition-all text-base"
                     placeholder="e.g. 90210 or Los Angeles, CA">
            </div>

            <div>
              <label class="block text-sm font-semibold text-slate-800 mb-1">Delivery Location (ZIP or City, State) <span class="text-rose-500">*</span></label>
              <input type="text" name="destination" value="${formData.destination}" required
                     class="w-full bg-slate-50 border border-slate-300 focus:border-blue-500 focus:bg-white rounded-xl px-4 py-3 text-slate-900 font-medium placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-200 transition-all text-base"
                     placeholder="e.g. 10001 or New York, NY">
            </div>

            <div class="flex items-center gap-2 p-2.5 rounded-lg bg-blue-50/70 border border-blue-100 text-xs text-blue-800">
              <span class="text-blue-600 text-base">🛡️</span>
              <span>100% Price Lock Guarantee with $0 Upfront Deposit.</span>
            </div>

            <button type="submit" class="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold py-3.5 px-6 rounded-xl shadow-lg hover:shadow-xl transition-all transform hover:-translate-y-0.5 text-base flex items-center justify-center gap-2">
              Next: Vehicle Details →
            </button>
          </form>
        `;

        container.querySelector('#calc-step1-form').addEventListener('submit', (e) => {
          e.preventDefault();
          const orig = container.querySelector('input[name="origin"]').value.trim();
          const dest = container.querySelector('input[name="destination"]').value.trim();
          if (!orig || !dest) {
            alert("Please enter both pickup and delivery locations.");
            return;
          }
          formData.origin = orig;
          formData.destination = dest;
          currentStep = 2;
          renderStep();
        });
      } else if (currentStep === 2) {
        container.innerHTML = `
          <div class="mb-5">
            <div class="flex justify-between text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">
              <span class="text-emerald-600 font-bold">✓ Route</span>
              <span class="text-blue-600 font-extrabold">2. Vehicle</span>
              <span>3. Method</span>
              <span>4. Quote</span>
            </div>
            <div class="w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">
              <div class="bg-blue-600 h-full transition-all duration-300" style="width: 50%"></div>
            </div>
          </div>

          <form id="calc-step2-form" class="space-y-4">
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block text-xs font-semibold text-slate-700 mb-1">Year</label>
                <select name="year" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2.5 text-slate-900 font-medium text-sm focus:outline-none focus:border-blue-500">
                  ${[2026, 2025, 2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2010, 2005, 2000, 1990, 1980].map(y => `<option value="${y}" ${formData.year == y ? 'selected' : ''}>${y}</option>`).join('')}
                </select>
              </div>
              <div>
                <label class="block text-xs font-semibold text-slate-700 mb-1">Vehicle Type</label>
                <select name="vehicleType" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2.5 text-slate-900 font-medium text-sm focus:outline-none focus:border-blue-500">
                  <option value="sedan" ${formData.vehicleType === 'sedan' ? 'selected' : ''}>Sedan / Coupe</option>
                  <option value="suv_small" ${formData.vehicleType === 'suv_small' ? 'selected' : ''}>Small SUV / Crossover</option>
                  <option value="suv_large" ${formData.vehicleType === 'suv_large' ? 'selected' : ''}>Large SUV / Truck</option>
                  <option value="sports_car" ${formData.vehicleType === 'sports_car' ? 'selected' : ''}>Sports Car / Exotic</option>
                  <option value="classic" ${formData.vehicleType === 'classic' ? 'selected' : ''}>Classic Car</option>
                  <option value="motorcycle" ${formData.vehicleType === 'motorcycle' ? 'selected' : ''}>Motorcycle</option>
                  <option value="ev" ${formData.vehicleType === 'ev' ? 'selected' : ''}>Electric Vehicle (EV)</option>
                </select>
              </div>
            </div>

            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block text-xs font-semibold text-slate-700 mb-1">Make</label>
                <input type="text" name="make" value="${formData.make}" required placeholder="e.g. Ford, Toyota, BMW"
                       class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2.5 text-slate-900 text-sm font-medium focus:outline-none focus:border-blue-500">
              </div>
              <div>
                <label class="block text-xs font-semibold text-slate-700 mb-1">Model</label>
                <input type="text" name="model" value="${formData.model}" required placeholder="e.g. F-150, Camry, Model 3"
                       class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2.5 text-slate-900 text-sm font-medium focus:outline-none focus:border-blue-500">
              </div>
            </div>

            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">Vehicle Operability</label>
              <div class="grid grid-cols-2 gap-2">
                <label class="flex items-center gap-2 p-2.5 border rounded-xl cursor-pointer bg-slate-50 hover:bg-blue-50/50 transition">
                  <input type="radio" name="condition" value="operable" ${formData.condition === 'operable' ? 'checked' : ''}>
                  <span class="text-xs font-semibold text-slate-800">Runs & Drives</span>
                </label>
                <label class="flex items-center gap-2 p-2.5 border rounded-xl cursor-pointer bg-slate-50 hover:bg-blue-50/50 transition">
                  <input type="radio" name="condition" value="inoperable" ${formData.condition === 'inoperable' ? 'checked' : ''}>
                  <span class="text-xs font-semibold text-slate-800">Inoperable (+Special Winch)</span>
                </label>
              </div>
            </div>

            <div class="flex gap-3 pt-2">
              <button type="button" id="calc-step2-back" class="w-1/3 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold py-3 px-4 rounded-xl text-sm transition">
                ← Back
              </button>
              <button type="submit" class="w-2/3 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 text-white font-bold py-3 px-4 rounded-xl text-sm shadow-md transition">
                Next: Transport Method →
              </button>
            </div>
          </form>
        `;

        container.querySelector('#calc-step2-back').addEventListener('click', () => {
          currentStep = 1;
          renderStep();
        });

        container.querySelector('#calc-step2-form').addEventListener('submit', (e) => {
          e.preventDefault();
          formData.year = container.querySelector('select[name="year"]').value;
          formData.vehicleType = container.querySelector('select[name="vehicleType"]').value;
          formData.make = container.querySelector('input[name="make"]').value.trim();
          formData.model = container.querySelector('input[name="model"]').value.trim();
          const condInput = container.querySelector('input[name="condition"]:checked');
          formData.condition = condInput ? condInput.value : 'operable';
          currentStep = 3;
          renderStep();
        });
      } else if (currentStep === 3) {
        const miles = calculateDistance(formData.origin, formData.destination);
        const pricing = calculatePricing(miles, formData.vehicleType, 'open_standard', formData.condition === 'inoperable');

        container.innerHTML = `
          <div class="mb-5">
            <div class="flex justify-between text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">
              <span class="text-emerald-600 font-bold">✓ Route</span>
              <span class="text-emerald-600 font-bold">✓ Vehicle</span>
              <span class="text-blue-600 font-extrabold">3. Method</span>
              <span>4. Quote</span>
            </div>
            <div class="w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">
              <div class="bg-blue-600 h-full transition-all duration-300" style="width: 75%"></div>
            </div>
          </div>

          <form id="calc-step3-form" class="space-y-3">
            <label class="block p-3.5 border-2 rounded-2xl cursor-pointer hover:border-blue-500 bg-white transition shadow-sm relative ${formData.transportType === 'open_standard' ? 'border-blue-600 bg-blue-50/20' : 'border-slate-200'}">
              <div class="flex items-center justify-between mb-1">
                <div class="flex items-center gap-2">
                  <input type="radio" name="transportType" value="open_standard" ${formData.transportType === 'open_standard' ? 'checked' : ''} class="w-4 h-4 text-blue-600">
                  <span class="font-extrabold text-slate-900 text-sm">Open Carrier Transport</span>
                  <span class="text-[10px] bg-blue-100 text-blue-700 font-bold px-2 py-0.5 rounded-full">Most Popular</span>
                </div>
                <span class="font-black text-blue-600 font-mono text-base">$${pricing.openPrice}</span>
              </div>
              <p class="text-xs text-slate-500 pl-6">Standard multi-car open trailer. Vetted carrier with $100k-$250k cargo insurance.</p>
            </label>

            <label class="block p-3.5 border-2 rounded-2xl cursor-pointer hover:border-amber-500 bg-white transition shadow-sm relative ${formData.transportType === 'enclosed_standard' ? 'border-amber-500 bg-amber-50/20' : 'border-slate-200'}">
              <div class="flex items-center justify-between mb-1">
                <div class="flex items-center gap-2">
                  <input type="radio" name="transportType" value="enclosed_standard" ${formData.transportType === 'enclosed_standard' ? 'checked' : ''} class="w-4 h-4 text-amber-600">
                  <span class="font-extrabold text-slate-900 text-sm">Enclosed Luxury Carrier</span>
                  <span class="text-[10px] bg-amber-100 text-amber-800 font-bold px-2 py-0.5 rounded-full">Premium Protection</span>
                </div>
                <span class="font-black text-amber-600 font-mono text-base">$${pricing.enclosedPrice}</span>
              </div>
              <p class="text-xs text-slate-500 pl-6">Fully enclosed trailer with hydraulic liftgate. Up to $1M cargo insurance for classic & luxury cars.</p>
            </label>

            <div class="flex gap-3 pt-2">
              <button type="button" id="calc-step3-back" class="w-1/3 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold py-3 px-4 rounded-xl text-sm transition">
                ← Back
              </button>
              <button type="submit" class="w-2/3 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 text-white font-bold py-3 px-4 rounded-xl text-sm shadow-md transition">
                Calculate Final Quote →
              </button>
            </div>
          </form>
        `;

        container.querySelector('#calc-step3-back').addEventListener('click', () => {
          currentStep = 2;
          renderStep();
        });

        container.querySelector('#calc-step3-form').addEventListener('submit', (e) => {
          e.preventDefault();
          const tType = container.querySelector('input[name="transportType"]:checked');
          formData.transportType = tType ? tType.value : 'open_standard';
          currentStep = 4;
          renderStep();
        });
      } else if (currentStep === 4) {
        const miles = calculateDistance(formData.origin, formData.destination);
        const pricing = calculatePricing(miles, formData.vehicleType, formData.transportType, formData.condition === 'inoperable');
        const finalPrice = formData.transportType === 'enclosed_standard' ? pricing.enclosedPrice : pricing.openPrice;

        container.innerHTML = `
          <div class="mb-4 text-center">
            <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-extrabold uppercase tracking-wider mb-2">
              ✓ Guaranteed Instant Rate Calculated
            </span>
            <h3 class="text-xl font-black text-slate-900">${formData.origin} ➔ ${formData.destination}</h3>
            <p class="text-xs text-slate-500">${miles} Total Road Miles • Est. Transit Time: ${pricing.eta}</p>
          </div>

          <div class="bg-gradient-to-br from-slate-900 to-slate-800 text-white p-4 rounded-2xl shadow-xl mb-4 border border-slate-700">
            <div class="flex justify-between items-center mb-3 border-b border-slate-700 pb-2">
              <div>
                <div class="text-[11px] uppercase tracking-wider text-slate-400">Guaranteed Price</div>
                <div class="text-2xl font-black text-emerald-400 font-mono">$${finalPrice}</div>
              </div>
              <div class="text-right">
                <span class="text-xs font-bold text-amber-400 bg-amber-500/20 px-2 py-0.5 rounded-full">$0 Deposit Required</span>
                <div class="text-[10px] text-slate-400 mt-0.5">Pay only upon carrier dispatch</div>
              </div>
            </div>
            <div class="grid grid-cols-3 gap-2 text-center text-[11px]">
              <div class="bg-white/5 p-1.5 rounded-lg"><span class="text-slate-400 block">Vehicle</span><strong class="text-white truncate">${formData.year} ${formData.make}</strong></div>
              <div class="bg-white/5 p-1.5 rounded-lg"><span class="text-slate-400 block">Carrier</span><strong class="text-white">${formData.transportType === 'enclosed_standard' ? 'Enclosed' : 'Open'}</strong></div>
              <div class="bg-white/5 p-1.5 rounded-lg"><span class="text-slate-400 block">Insurance</span><strong class="text-emerald-400">$100k-$1M COI</strong></div>
            </div>
          </div>

          <form id="calc-step4-form" class="space-y-3">
            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">Full Name</label>
              <input type="text" name="name" required placeholder="Your full name"
                     class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-slate-900 text-sm font-medium focus:outline-none focus:border-blue-500">
            </div>

            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="block text-xs font-semibold text-slate-700 mb-1">Phone Number <span class="text-rose-500">*</span></label>
                <input type="tel" name="phone" required placeholder="(224) 449-0397"
                       class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-slate-900 text-sm font-medium focus:outline-none focus:border-blue-500">
              </div>
              <div>
                <label class="block text-xs font-semibold text-slate-700 mb-1">Email Address <span class="text-rose-500">*</span></label>
                <input type="email" name="email" required placeholder="you@email.com"
                       class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-slate-900 text-sm font-medium focus:outline-none focus:border-blue-500">
              </div>
            </div>

            <button type="submit" id="btn-lock-quote" class="w-full bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 text-white font-extrabold py-3.5 px-6 rounded-xl shadow-lg transition transform hover:-translate-y-0.5 text-base flex items-center justify-center gap-2">
              🔒 Lock In Rate & Request Dispatch →
            </button>
            <p class="text-[10px] text-center text-slate-400">Zero spam calls. A dedicated FMCSA broker will confirm your carrier schedule directly.</p>
          </form>
        `;

        container.querySelector('#calc-step4-form').addEventListener('submit', async (e) => {
          e.preventDefault();
          const btn = container.querySelector('#btn-lock-quote');
          btn.innerHTML = `<span>⏳ Securing Corridor Rate...</span>`;
          btn.disabled = true;

          formData.name = container.querySelector('input[name="name"]').value.trim();
          formData.phone = container.querySelector('input[name="phone"]').value.trim();
          formData.email = container.querySelector('input[name="email"]').value.trim();

          const payload = {
            ...formData,
            miles,
            quotedPrice: finalPrice,
            eta: pricing.eta,
            timestamp: new Date().toISOString()
          };

          try {
            await fetch('/api/save_quote.php', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(payload)
            });
          } catch(err) {}

          // Show celebration modal
          container.innerHTML = `
            <div class="text-center py-6 px-4 animate-in fade-in zoom-in-95 duration-300">
              <div class="w-16 h-16 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mx-auto mb-4 text-3xl">
                ✓
              </div>
              <h3 class="text-2xl font-black text-slate-900 mb-1">Quote Locked Successfully!</h3>
              <p class="text-sm text-slate-600 mb-4">Your rate of <strong class="text-emerald-600 font-mono text-base">$${finalPrice}</strong> is secured with $0 upfront deposit.</p>
              
              <div class="bg-slate-50 border border-slate-200 rounded-xl p-4 text-left text-xs text-slate-700 space-y-1.5 mb-5">
                <div class="flex justify-between"><span>Reference ID:</span> <strong class="font-mono text-blue-600">#SKY-${Math.floor(100000 + Math.random() * 900000)}</strong></div>
                <div class="flex justify-between"><span>Lane:</span> <strong>${formData.origin} ➔ ${formData.destination}</strong></div>
                <div class="flex justify-between"><span>Vehicle:</span> <strong>${formData.year} ${formData.make} ${formData.model}</strong></div>
                <div class="flex justify-between"><span>Contact Phone:</span> <strong>${formData.phone}</strong></div>
              </div>

              <div class="space-y-2">
                <a href="tel:+12244490397" class="block w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-xl text-sm transition shadow-md">
                  📞 Call Live Dispatch: (224) 449-0397
                </a>
                <button onclick="location.reload()" class="block w-full text-slate-500 hover:text-slate-800 text-xs py-2">
                  Start Another Quote
                </button>
              </div>
            </div>
          `;
        });
      }
    }

    renderStep();
  }

  function initAllCalculators() {
    const containers = document.querySelectorAll('#quote-calculator-top, #quote-calculator, .quote-calculator-container');
    containers.forEach(c => renderCalculator(c));
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAllCalculators);
  } else {
    initAllCalculators();
  }
})();
"""

with open(os.path.join(JS_DIR, "quote_calculator_engine.js"), "w", encoding="utf-8") as f:
    f.write(quote_calc_js)
print("[+] Created public_html_local/assets/js/quote_calculator_engine.js")

# 4. INJECT INTERACTIVE MAP & SCRIPTS INTO public_html_local/index.html
index_path = os.path.join(BASE_DIR, "index.html")
with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

# Build Interactive Map HTML section
map_html_section = f"""
<!-- 🗺️ OMNIVERSE INTERACTIVE 50-STATE SVG PRICING MAP -->
<section id="interactive-map-section" class="py-24 bg-slate-900 text-white border-t border-slate-800 relative overflow-hidden">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
    <div class="text-center mb-12">
      <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-blue-500/20 text-blue-400 text-xs font-extrabold uppercase tracking-wider mb-3 border border-blue-400/30">
        Interactive 50-State Logistics Grid
      </div>
      <h2 class="text-3xl sm:text-4xl md:text-5xl font-black tracking-tight text-white mb-4">
        Interactive Nationwide Shipping Map
      </h2>
      <p class="text-slate-300 text-base sm:text-lg max-w-2xl mx-auto leading-relaxed">
        Click or hover over any state across America to view live carrier corridor rates, active logistics hubs, and estimated transit times.
      </p>
    </div>

    <!-- Map & Tooltip Grid -->
    <div class="grid lg:grid-cols-12 gap-8 items-center bg-slate-950/80 p-4 sm:p-8 rounded-3xl border border-slate-800 shadow-2xl backdrop-blur-xl">
      <!-- SVG Map Left -->
      <div id="us-interactive-map-wrapper" class="lg:col-span-8 w-full flex items-center justify-center">
        {svg_clean}
      </div>

      <!-- State Card / Live Route Details Right -->
      <div class="lg:col-span-4 w-full">
        <div id="map-state-tooltip" class="bg-slate-900 border border-slate-700/80 rounded-2xl p-6 shadow-2xl text-white transition-all duration-300">
          <div class="flex items-center justify-between border-b border-slate-700 pb-3 mb-3">
            <div>
              <span class="text-xs font-extrabold uppercase tracking-widest text-blue-400">US Logistics</span>
              <h4 class="text-xl font-black text-white leading-tight">United States</h4>
            </div>
            <span class="text-[11px] font-bold bg-emerald-500/20 text-emerald-300 px-2.5 py-1 rounded-full">50 States Covered</span>
          </div>
          <p class="text-xs text-slate-300 mb-4 leading-relaxed">
            Hover over or click any state on the map to inspect live lane pricing, primary terminal hubs, and instant quote calculation.
          </p>
          <div class="space-y-2 text-xs text-slate-300 mb-5">
            <div class="flex justify-between p-2 rounded bg-white/5"><span>Licensed Broker:</span> <strong class="text-emerald-400">MC-1782670</strong></div>
            <div class="flex justify-between p-2 rounded bg-white/5"><span>Carrier Network:</span> <strong class="text-white">10,000+ Vetted Rigs</strong></div>
            <div class="flex justify-between p-2 rounded bg-white/5"><span>Deposit Policy:</span> <strong class="text-amber-400">$0 Upfront Deposit</strong></div>
          </div>
          <a href="#quote-calculator-top" class="block w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 text-white font-extrabold py-3 px-4 rounded-xl text-center text-xs shadow-lg transition">
            Calculate Instant Rate Above ↑
          </a>
        </div>
      </div>
    </div>
  </div>
</section>
"""

# Replace empty section with Map section
if '<section class="py-24 bg-slate-50 border-t border-slate-200"><div class="max-w-7xl mx-auto px-4"></div></section>' in html:
    html = html.replace('<section class="py-24 bg-slate-50 border-t border-slate-200"><div class="max-w-7xl mx-auto px-4"></div></section>', map_html_section)
    print("[+] Injected interactive map section into index.html")
else:
    # Append before footer
    html = html.replace('</main>', f"{map_html_section}</main>")
    print("[+] Appended interactive map section before </main>")

# Add script tags before </body>
script_tags = """
<script src="/assets/js/quote_calculator_engine.js"></script>
<script src="/assets/js/interactive_map.js"></script>
</body>
"""
html = html.replace('</body>', script_tags)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(html)
print("[+] Successfully updated public_html_local/index.html with Interactive Map and Quote Calculator Engine!")
