"use client";
import React, { useState, useEffect, useMemo, useRef } from "react";
import QuoteResultModal from "./QuoteResultModal";

const STATE_ABBR = {
  Alabama: "AL", Arizona: "AZ", Arkansas: "AR", California: "CA",
  Colorado: "CO", Connecticut: "CT", Delaware: "DE", Florida: "FL", Georgia: "GA",
  Hawaii: "HI", Idaho: "ID", Illinois: "IL", Indiana: "IN", Iowa: "IA",
  Kansas: "KS", Kentucky: "KY", Louisiana: "LA", Maine: "ME", Maryland: "MD",
  Massachusetts: "MA", Michigan: "MI", Minnesota: "MN", Mississippi: "MS", Missouri: "MO",
  Montana: "MT", Nebraska: "NE", Nevada: "NV", "New Hampshire": "NH", "New Jersey": "NJ",
  "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", Ohio: "OH",
  Oklahoma: "OK", Oregon: "OR", Pennsylvania: "PA", "Rhode Island": "RI", "South Carolina": "SC",
  "South Dakota": "SD", Tennessee: "TN", Texas: "TX", Utah: "UT", Vermont: "VT",
  Virginia: "VA", Washington: "WA", "West Virginia": "WV", Wisconsin: "WI", Wyoming: "WY",
  "District of Columbia": "DC",
};

const US_STATE_CENTROIDS = {
  AL: { lat: 32.806671, lon: -86.791130 }, AK: { lat: 61.370716, lon: -152.404419 },
  AZ: { lat: 34.048927, lon: -111.093735 }, AR: { lat: 34.799999, lon: -92.199997 },
  CA: { lat: 36.778259, lon: -119.417931 }, CO: { lat: 39.550053, lon: -105.782066 },
  CT: { lat: 41.603221, lon: -73.087749 }, DE: { lat: 38.910832, lon: -75.527672 },
  FL: { lat: 27.664827, lon: -81.515755 }, GA: { lat: 33.040619, lon: -83.643074 },
  HI: { lat: 21.094318, lon: -157.498337 }, ID: { lat: 44.068203, lon: -114.742043 },
  IL: { lat: 40.633125, lon: -89.398529 }, IN: { lat: 40.267194, lon: -86.134902 },
  IA: { lat: 41.878003, lon: -93.097702 }, KS: { lat: 39.011902, lon: -98.484246 },
  KY: { lat: 37.839333, lon: -84.270020 }, LA: { lat: 31.244823, lon: -92.145024 },
  ME: { lat: 45.253783, lon: -69.445469 }, MD: { lat: 39.045755, lon: -76.641273 },
  MA: { lat: 42.407211, lon: -71.382437 }, MI: { lat: 44.314844, lon: -85.602364 },
  MN: { lat: 46.729553, lon: -94.685900 }, MS: { lat: 32.354668, lon: -89.398528 },
  MO: { lat: 37.964253, lon: -91.831833 }, MT: { lat: 46.879682, lon: -110.362566 },
  NE: { lat: 41.492537, lon: -99.901813 }, NV: { lat: 38.802610, lon: -116.419389 },
  NH: { lat: 43.452492, lon: -71.563896 }, NJ: { lat: 40.058324, lon: -74.405661 },
  NM: { lat: 34.519940, lon: -105.870090 }, NY: { lat: 43.299428, lon: -74.217933 },
  NC: { lat: 35.759573, lon: -79.019300 }, ND: { lat: 47.551493, lon: -101.002012 },
  OH: { lat: 40.417287, lon: -82.907123 }, OK: { lat: 35.007752, lon: -97.092877 },
  OR: { lat: 44.000000, lon: -120.500000 }, PA: { lat: 41.203322, lon: -77.194525 },
  RI: { lat: 41.580095, lon: -71.477429 }, SC: { lat: 33.836081, lon: -81.163725 },
  SD: { lat: 43.969515, lon: -99.901813 }, TN: { lat: 35.517491, lon: -86.580447 },
  TX: { lat: 31.968599, lon: -99.901810 }, UT: { lat: 39.320980, lon: -111.093731 },
  VT: { lat: 44.558803, lon: -72.577841 }, VA: { lat: 37.431573, lon: -78.656894 },
  WA: { lat: 47.751074, lon: -120.740135 }, WV: { lat: 38.597626, lon: -80.454903 },
  WI: { lat: 43.784440, lon: -88.787868 }, WY: { lat: 43.075968, lon: -107.290283 },
  DC: { lat: 38.907192, lon: -77.036871 },
};

// ─── COMPLETE ALL-50-STATE PRICING TABLE ───────────────────────────────────
// Types: "Hub" | "Snowbird" | "Standard" | "Rural"
// Hub = high-volume corridor discount, Rural = dispatch surcharge
const STATE_PRICING_DATA = {
  AL: { baseRate: 0.92, type: "Standard", hub: "Birmingham" },
  AK: { baseRate: 1.80, type: "Rural",    hub: "Anchorage" },
  AZ: { baseRate: 0.95, type: "Snowbird", hub: "Phoenix" },
  AR: { baseRate: 0.96, type: "Standard", hub: "Little Rock" },
  CA: { baseRate: 0.90, type: "Hub",      hub: "Los Angeles" },
  CO: { baseRate: 1.10, type: "Standard", hub: "Denver" },
  CT: { baseRate: 0.97, type: "Standard", hub: "Hartford" },
  DE: { baseRate: 0.96, type: "Standard", hub: "Wilmington" },
  FL: { baseRate: 0.85, type: "Snowbird", hub: "Miami" },
  GA: { baseRate: 0.89, type: "Hub",      hub: "Atlanta" },
  HI: { baseRate: 2.20, type: "Rural",    hub: "Honolulu" },
  ID: { baseRate: 1.25, type: "Rural",    hub: "Boise" },
  IL: { baseRate: 0.92, type: "Hub",      hub: "Chicago" },
  IN: { baseRate: 0.94, type: "Standard", hub: "Indianapolis" },
  IA: { baseRate: 1.00, type: "Standard", hub: "Des Moines" },
  KS: { baseRate: 1.02, type: "Standard", hub: "Wichita" },
  KY: { baseRate: 0.95, type: "Standard", hub: "Louisville" },
  LA: { baseRate: 0.93, type: "Standard", hub: "New Orleans" },
  ME: { baseRate: 1.18, type: "Rural",    hub: "Portland" },
  MD: { baseRate: 0.93, type: "Hub",      hub: "Baltimore" },
  MA: { baseRate: 0.96, type: "Hub",      hub: "Boston" },
  MI: { baseRate: 1.00, type: "Standard", hub: "Detroit" },
  MN: { baseRate: 1.05, type: "Standard", hub: "Minneapolis" },
  MS: { baseRate: 0.97, type: "Standard", hub: "Jackson" },
  MO: { baseRate: 0.94, type: "Standard", hub: "St. Louis" },
  MT: { baseRate: 1.50, type: "Rural",    hub: "Billings" },
  NE: { baseRate: 1.05, type: "Standard", hub: "Omaha" },
  NV: { baseRate: 0.92, type: "Hub",      hub: "Las Vegas" },
  NH: { baseRate: 1.10, type: "Standard", hub: "Manchester" },
  NJ: { baseRate: 0.95, type: "Hub",      hub: "Newark" },
  NM: { baseRate: 1.12, type: "Standard", hub: "Albuquerque" },
  NY: { baseRate: 0.95, type: "Hub",      hub: "New York City" },
  NC: { baseRate: 0.92, type: "Standard", hub: "Charlotte" },
  ND: { baseRate: 1.35, type: "Rural",    hub: "Fargo" },
  OH: { baseRate: 0.93, type: "Hub",      hub: "Columbus" },
  OK: { baseRate: 0.98, type: "Standard", hub: "Oklahoma City" },
  OR: { baseRate: 1.08, type: "Standard", hub: "Portland" },
  PA: { baseRate: 0.93, type: "Hub",      hub: "Philadelphia" },
  RI: { baseRate: 0.97, type: "Standard", hub: "Providence" },
  SC: { baseRate: 0.91, type: "Standard", hub: "Columbia" },
  SD: { baseRate: 1.30, type: "Rural",    hub: "Sioux Falls" },
  TN: { baseRate: 0.91, type: "Standard", hub: "Nashville" },
  TX: { baseRate: 0.88, type: "Hub",      hub: "Dallas" },
  UT: { baseRate: 1.05, type: "Standard", hub: "Salt Lake City" },
  VT: { baseRate: 1.20, type: "Rural",    hub: "Burlington" },
  VA: { baseRate: 0.92, type: "Standard", hub: "Richmond" },
  WA: { baseRate: 1.05, type: "Standard", hub: "Seattle" },
  WV: { baseRate: 1.10, type: "Standard", hub: "Charleston" },
  WI: { baseRate: 1.02, type: "Standard", hub: "Milwaukee" },
  WY: { baseRate: 1.45, type: "Rural",    hub: "Cheyenne" },
  DC: { baseRate: 0.93, type: "Hub",      hub: "Washington D.C." },
};

// ─── SNOWBIRD STATES (Southern destinations) ────────────────────────────────
const SNOWBIRD_SOUTH = new Set(["FL", "AZ", "NV", "TX", "SC", "GA", "AL", "LA", "MS"]);
// Northern states that get winter surcharge
const WINTER_NORTH = new Set(["MT", "ND", "SD", "WY", "MN", "ME", "VT", "NH", "WI", "MI", "AK", "ID"]);

// ─── HELPER: get state abbr from resolved geo label or formData field ────────
function extractStateAbbr(label) {
  if (!label) return null;
  const v = label.trim().toLowerCase();
  
  if (/^\d{5}/.test(v)) {
    const z = parseInt(v.substring(0, 5), 10);
    if (z >= 90000 && z <= 96199) return "CA";
    if (z >= 32000 && z <= 34999) return "FL";
    if (z >= 82000 && z <= 83199) return "WY";
    if (z >= 80000 && z <= 81699) return "CO";
    if (z >= 59000 && z <= 59999) return "MT";
    if (z >= 10000 && z <= 14999) return "NY";
    if (z >= 75000 && z <= 79999) return "TX";
    if (z >= 60000 && z <= 62999) return "IL";
    if (z >= 30000 && z <= 31999) return "GA";
    return null;
  }

  const parts = label.trim().split(/[,\s]+/);
  for (let i = parts.length - 1; i >= 0; i--) {
    const candidate = parts[i].toUpperCase();
    if (STATE_PRICING_DATA[candidate]) return candidate;
  }
  for (const [name, abbr] of Object.entries(STATE_ABBR)) {
    if (label.toLowerCase().includes(name.toLowerCase())) return abbr;
  }
  return null;
}

// ─── MASTER PRICING ENGINE ───────────────────────────────────────────────────
function calculateSkyAutoPrice({ miles, vehicleType, vehicleCondition, vehicleValue, transportType, originLabel, destLabel }) {
  const month = new Date().getMonth() + 1; // 1-12

  // 1. Determine state abbrs
  const originAbbr = extractStateAbbr(originLabel);
  const destAbbr   = extractStateAbbr(destLabel);

  const originData = STATE_PRICING_DATA[originAbbr] || { baseRate: 1.15, type: "Standard" };
  const destData   = STATE_PRICING_DATA[destAbbr]   || { baseRate: 1.15, type: "Standard" };

  // 2. Average the origin/destination base rates
  let baseRate = (originData.baseRate + destData.baseRate) / 2;

  // 3. Distance tier decay multiplier
  let distanceMult = 1.15;
  if (miles > 2000)      distanceMult = 0.80;
  else if (miles > 1000) distanceMult = 0.90;
  else if (miles > 500)  distanceMult = 1.00;
  else if (miles <= 199) distanceMult = 2.60;

  let effectiveRate = baseRate * distanceMult;
  if (miles <= 199) {
    // Ensure base rate shown for short hauls (<= 199 miles) is between $2.15 and $3.15 / mile
    effectiveRate = Math.min(3.15, Math.max(2.15, effectiveRate));
  }
  let baseCost = miles * effectiveRate;

  // 4. Route popularity (Hub vs Rural)
  const originType = originData.type;
  const destType   = destData.type;
  if ((originType === "Hub" || originType === "Snowbird") &&
      (destType   === "Hub" || destType   === "Snowbird")) {
    baseCost *= 0.90; // Hub-to-Hub: −10%
  } else if (originType === "Rural" && destType === "Rural") {
    baseCost *= 1.25; // Rural-to-Rural: +25%
  }

  // 5. Seasonal modifier
  let seasonalMult = 1.00;
  // Snowbird south season (Oct–Dec)
  if ([10, 11, 12].includes(month) && SNOWBIRD_SOUTH.has(destAbbr) && !SNOWBIRD_SOUTH.has(originAbbr)) {
    seasonalMult = 1.20;
  }
  // Return north season (April–May)
  else if ([4, 5].includes(month) && SNOWBIRD_SOUTH.has(originAbbr) && !SNOWBIRD_SOUTH.has(destAbbr)) {
    seasonalMult = 1.18;
  }
  // Winter surcharge for northern/rural states (Dec–Feb)
  else if ([12, 1, 2].includes(month) && (WINTER_NORTH.has(originAbbr) || WINTER_NORTH.has(destAbbr))) {
    seasonalMult = 1.10;
  }
  baseCost *= seasonalMult;

  // 6. Vehicle type flat surcharges
  const FLAT_SURCHARGES = {
    sedan: 0, suv_small: 200, suv_large: 250, pickup_half: 150,
    pickup_heavy: 350, van: 200, sports_car: 350, classic: 100,
    motorcycle: -100, ev: 350, heavy: 500
  };
  const vSurcharge = FLAT_SURCHARGES[vehicleType] ?? 0;
  baseCost += vSurcharge;

  // 7. Inoperable vehicle flat fee
  let inoperableSurcharge = 0;
  if (vehicleCondition === "inoperable") {
    inoperableSurcharge = 150;
    baseCost += 150;
  }

  // 8. Transport type multiplier (enclosed = ×1.40 over open)
  const TRANSPORT_MULTS = {
    open_standard: 1.00,
    enclosed_standard: 1.40,
    enclosed_liftgate: 1.60,
    express_expedited: 1.90,
  };
  const TRANSPORT_MINS = {
    open_standard: 399,
    enclosed_standard: 599,
    enclosed_liftgate: 799,
    express_expedited: 999,
  };
  const transportMult = TRANSPORT_MULTS[transportType] || 1.00;
  const transportMin  = TRANSPORT_MINS[transportType]  || 399;
  let cost = baseCost * transportMult;
  const transportSurcharge = cost - baseCost;

  // 9. Vehicle value (insurance premium)
  let valueSurcharge = 0;
  if (vehicleValue === "50k_100k") {
    valueSurcharge = cost * 0.15;
    cost *= 1.15;
  } else if (vehicleValue === "over_100k") {
    valueSurcharge = cost * 0.30;
    cost *= 1.30;
  }

  // 10. Apply floor (prices start from $399)
  cost = Math.max(cost, transportMin, 399);

  // 11. Round to nearest $5 for clean display
  const mid = Math.max(399, Math.round(cost / 5) * 5);
  const lo  = Math.max(399, Math.round((cost * 0.90) / 5) * 5);
  const hi  = Math.max(399, Math.round((cost * 1.10) / 5) * 5);

  const etaDays = Math.max(1, Math.ceil(miles / 450));
  const eta = etaDays === 1 ? "1 day" : `${etaDays} days`;

  return {
    mid, lo, hi, eta, miles,
    originAbbr, destAbbr,
    breakdown: {
      baseRate: parseFloat(effectiveRate.toFixed(3)),
      baseMilesCost: Math.round(miles * effectiveRate),
      seasonalMult,
      routeType: originType === "Rural" && destType === "Rural" ? "Rural-Rural (+25%)" :
                 ((originType === "Hub" || originType === "Snowbird") && (destType === "Hub" || destType === "Snowbird")) ? "Hub-Hub (−10%)" : "Standard",
      vehicleSurcharge: vSurcharge,
      inoperableSurcharge,
      transportSurcharge: Math.round(transportSurcharge),
      valueSurcharge: Math.round(valueSurcharge),
    }
  };
}

const VEHICLE_TYPES = [
  { id: "sedan", label: "Sedan / Coupe", weight: 3100 },
  { id: "suv_small", label: "Small SUV / Crossover", weight: 3800 },
  { id: "suv_large", label: "Large SUV / Full-Size", weight: 5200 },
  { id: "pickup_half", label: "1/2 Ton Pickup Truck", weight: 5000 },
  { id: "pickup_heavy", label: "Heavy-Duty Pickup (3/4 - 1 ton)", weight: 7000 },
  { id: "van", label: "Minivan / Passenger Van", weight: 4500 },
  { id: "sports_car", label: "Sports Car / Exotic", weight: 3300 },
  { id: "classic", label: "Classic / Antique Vehicle", weight: 3200 },
  { id: "motorcycle", label: "Motorcycle / Powersports", weight: 600 },
  { id: "ev", label: "Electric Vehicle (EV)", weight: 4700 },
  { id: "heavy", label: "Heavy Truck / Commercial", weight: 12000 }
];

const VEHICLE_SURCHARGES = {
  sedan: 0, suv_small: 200, suv_large: 250, pickup_half: 150, pickup_heavy: 350,
  van: 200, sports_car: 350, classic: 100, motorcycle: -100, ev: 350, heavy: 500
};

const TRANSPORT_LEVELS = [
  { id: "open_standard",     label: "Open Carrier Transport",   sub: "Affordable 8-10 car open carrier shipping.",                      multiplier: 1.00, min: 399 },
  { id: "enclosed_standard", label: "Enclosed",                 sub: "Fully enclosed, climate-controlled protection.",                   multiplier: 1.40, min: 599 },
  { id: "enclosed_liftgate", label: "Enclosed Shielded",        sub: "Hydraulic liftgate for extremely low-clearance vehicles.",        multiplier: 1.60, min: 799 },
  { id: "express_expedited", label: "Open Express",             sub: "Priority 24-48 hour dispatch, dedicated trailer.",                multiplier: 1.90, min: 999 },
];

const REQUIRED_FIELDS_STEP = {
  1: ["origin", "destination"],
  2: ["vehicleType", "vehicleYear", "vehicleMake", "vehicleModel", "vehicleValue"],
  3: ["transportType"],
  4: ["firstName", "lastName", "email", "phone", "smsConsent"],
};

const EMAIL_RE = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i;
const PHONE_RE_DIGITS = /^\d{10,15}$/;
const US_ZIP_RE = /^\d{5}(-\d{4})?$/;
const YEAR_RE = /^(19|20)\d{2}$/;

function haversineMiles(a, b) {
  const R = 3958.8;
  const t = Math.PI / 180;
  const dLa = (b.lat - a.lat) * t;
  const dLo = (b.lon - a.lon) * t;
  const h =
    Math.sin(dLa / 2) ** 2 +
    Math.cos(a.lat * t) * Math.cos(b.lat * t) * Math.sin(dLo / 2) ** 2;
  return Math.round(2 * R * Math.asin(Math.sqrt(h)) * 1.18);
}

function normalizeOriginDest(rawValue) {
  const v = (rawValue || "").trim();
  if (!v) return { ok: false, label: "", geo: null };
  if (US_ZIP_RE.test(v)) {
    return {
      ok: true,
      label: v,
      zipOnly: true,
      geo: null,
    };
  }
  const commaParts = v.split(",").map((p) => p.trim()).filter(Boolean);
  let cityPart, statePart;
  if (commaParts.length >= 2) {
    cityPart = commaParts.slice(0, -1).join(", ");
    statePart = commaParts[commaParts.length - 1];
  } else if (v.length >= 2) {
    cityPart = v;
    statePart = "";
  }
  if (statePart && statePart.length > 0) {
    const short = statePart.toUpperCase();
    if (US_STATE_CENTROIDS[short]) {
      return {
        ok: true,
        label: `${cityPart || ""}${cityPart ? ", " : ""}${short}`,
        geo: US_STATE_CENTROIDS[short],
        state: short,
      };
    }
    for (const [name, abbr] of Object.entries(STATE_ABBR)) {
      if (statePart.toLowerCase() === name.toLowerCase()) {
        return {
          ok: true,
          label: `${cityPart || ""}${cityPart ? ", " : ""}${abbr}`,
          geo: US_STATE_CENTROIDS[abbr],
          state: abbr,
        };
      }
    }
  }
  return {
    ok: true,
    label: v,
    geo: null,
  };
}

function resolveGeoFromLookup(inputValue, citiesIndex, stateCentroids, zipCoords = {}) {
  const parsed = normalizeOriginDest(inputValue);
  if (parsed.geo) return { geo: parsed.geo, label: parsed.label, resolved: true };
  const v = (inputValue || "").trim().toLowerCase();
  if (!v) return { geo: null, resolved: false };
  if (US_ZIP_RE.test(v)) {
    const exactZip = (inputValue || "").trim().split("-")[0];
    if (zipCoords && zipCoords[exactZip]) {
      return { geo: zipCoords[exactZip], label: exactZip, resolved: true };
    }
  }
  if (citiesIndex.cityState[v]) {
    const hit = citiesIndex.cityState[v];
    return { geo: hit.geo, label: `${hit.city}, ${hit.state}`, resolved: true };
  }
  const parts = v.split(/[, ]+/).filter(Boolean);
  if (parts.length >= 2) {
    const statePart = parts[parts.length - 1].toUpperCase();
    if (stateCentroids[statePart]) {
      return {
        geo: stateCentroids[statePart],
        label: `${parts.slice(0, -1).map((w) => w[0].toUpperCase() + w.slice(1)).join(" ")}, ${statePart}`,
        resolved: true,
      };
    }
    const last = parts[parts.length - 1];
    for (const [name, abbr] of Object.entries(STATE_ABBR)) {
      if (name.toLowerCase() === last) {
        return {
          geo: stateCentroids[abbr],
          label: `${parts.slice(0, -1).map((w) => w[0].toUpperCase() + w.slice(1)).join(" ")}, ${abbr}`,
          resolved: true,
        };
      }
    }
  }
  if (parts.length === 1) {
    for (const [name, abbr] of Object.entries(STATE_ABBR)) {
      if (name.toLowerCase() === parts[0]) {
        return { geo: stateCentroids[abbr], label: name, resolved: true };
      }
    }
    if (stateCentroids[parts[0].toUpperCase()]) {
      const abbr = parts[0].toUpperCase();
      const name = Object.entries(STATE_ABBR).find(([, a]) => a === abbr)?.[0] || abbr;
      return { geo: stateCentroids[abbr], label: name, resolved: true };
    }
    if (citiesIndex.cityOnly[v]) {
      const hit = citiesIndex.cityOnly[v];
      return { geo: hit.geo, label: `${hit.city}, ${hit.state}`, resolved: true };
    }
  }
  return { geo: null, resolved: false };
}

export default function MontwayQuoteCalculator() {
  const [step, setStep] = useState(1);
  const [submitting, setSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState(null);
  const [cities, setCities] = useState([]);
  const [citiesLoading, setCitiesLoading] = useState(true);
  const [zipCoords, setZipCoords] = useState({});
  const [priceRevealed, setPriceRevealed] = useState(false);
  const [errors, setErrors] = useState({});
  const [sessionId, setSessionId] = useState("");
  const [showResultModal, setShowResultModal] = useState(false);
  const [osrmDistance, setOsrmDistance] = useState(null);
  const [isFetchingDistance, setIsFetchingDistance] = useState(false);
  const [priceCalc, setPriceCalc] = useState({ ready: false });

  useEffect(() => {
    try {
      if (typeof window !== "undefined") {
        const stored = window.localStorage.getItem("sky_quote_session_id");
        if (stored) {
          setSessionId(stored);
        } else {
          const nid = `QUOTE-SESSION-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
          window.localStorage.setItem("sky_quote_session_id", nid);
          setSessionId(nid);
        }
      }
    } catch (e) {
      setSessionId(`QUOTE-SESSION-${Date.now()}`);
    }
  }, []);

  const [formData, setFormData] = useState({
    origin: "",
    destination: "",
    vehicleType: "",
    vehicleYear: "",
    vehicleMake: "",
    vehicleModel: "",
    vehicleCondition: "operable",
    vehicleValue: "under_50k",
    transportType: "open_standard",
    pickupDate: "",
    firstName: "",
    lastName: "",
    email: "",
    phone: "",
    comments: "",
  });

  useEffect(() => {
    if (typeof window === "undefined") return;
    let cancelled = false;
    setCitiesLoading(true);
    (async () => {
      try {
        const r = await fetch("/assets/data/cities.json", { cache: "force-cache" });
        if (!r.ok) { if (!cancelled) setCitiesLoading(false); return; }
        const data = await r.json();
        if (cancelled) return;
        setCities(Array.isArray(data) ? data : []);
      } catch (e) { }
      finally { if (!cancelled) setCitiesLoading(false); }
    })();
    (async () => {
      try {
        const r = await fetch("/assets/data/zip_coordinates.json", { cache: "force-cache" });
        if (!r.ok) return;
        const data = await r.json();
        if (cancelled) return;
        setZipCoords(data || {});
      } catch (e) { }
    })();
    return () => { cancelled = true; };
  }, []);

  useEffect(() => {
    if (typeof window !== "undefined" && step > 1) {
      document.getElementById("quote-calculator-top")?.scrollIntoView({ behavior: "smooth" });
    }
  }, [step]);

  const citiesIndex = useMemo(() => {
    const cityState = Object.create(null);
    const cityOnly = Object.create(null);
    (cities || []).forEach((c) => {
      const stateAbbr = STATE_ABBR[c.state] || (US_STATE_CENTROIDS[c.state] ? c.state : null);
      if (!stateAbbr) return;
      const stateCentroid = US_STATE_CENTROIDS[stateAbbr] || { lat: 39.0, lon: -97.0 };
      const key = `${(c.city || "").toLowerCase()}, ${stateAbbr.toLowerCase()}`;
      if (!cityState[key]) {
        cityState[key] = { city: c.city, state: stateAbbr, geo: stateCentroid };
      }
      const ck = (c.city || "").toLowerCase();
      if (!cityOnly[ck]) {
        cityOnly[ck] = { city: c.city, state: stateAbbr, geo: stateCentroid };
      }
    });
    return { cityState, cityOnly };
  }, [cities]);

  const setField = (name, value) => {
    setFormData((prev) => ({ ...prev, [name]: value }));
    setErrors((prev) => {
      if (!prev[name]) return prev;
      const n = { ...prev };
      delete n[name];
      return n;
    });
  };

  const formatPhone = (value) => {
    const digits = value.replace(/\D/g, "");
    if (digits.length <= 3) return digits;
    if (digits.length <= 6) return `(${digits.slice(0, 3)}) ${digits.slice(3)}`;
    return `(${digits.slice(0, 3)}) ${digits.slice(3, 6)}-${digits.slice(6, 10)}`;
  };

  const handleChange = (e) => {
    const t = e.target;
    let val = t.type === "checkbox" ? t.checked : t.value;
    if (t.name === "phone") val = formatPhone(val);
    setField(t.name, val);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      if (step < 4) nextStep();
      else submitQuote();
    }
  };

  const validateStep = (s) => {
    const required = REQUIRED_FIELDS_STEP[s] || [];
    const errs = {};
    for (const f of required) {
      const v = formData[f];
      if (f === "smsConsent") {
        if (!v) {
          errs[f] = "Please check the box to agree to SMS terms.";
        }
        continue;
      }
      if (v === undefined || v === null || (typeof v === "string" && !v.trim())) {
        errs[f] = "This field is required.";
        continue;
      }
      if (typeof v === "string") {
        switch (f) {
          case "origin":
          case "destination": {
            const resolved = resolveGeoFromLookup(v, citiesIndex, US_STATE_CENTROIDS, zipCoords);
            if (!resolved.resolved && !US_ZIP_RE.test(v.trim())) {
              errs[f] = "Enter a valid ZIP, city, or state.";
            }
            break;
          }
          case "vehicleYear":
            if (!YEAR_RE.test(v.trim()) || +v < 1900 || +v > new Date().getFullYear() + 1) {
              errs[f] = `Enter a valid 4-digit year (1900 – ${new Date().getFullYear() + 1}).`;
            }
            break;
          case "email":
            if (!EMAIL_RE.test(v.trim())) errs[f] = "Enter a valid email address.";
            break;
          case "phone": {
            const digits = v.replace(/\D/g, "");
            if (!PHONE_RE_DIGITS.test(digits))
              errs[f] = "Enter a valid 10-15 digit phone number.";
            break;
          }
          default:
            if (!v.trim() || v.trim().length < 2)
              errs[f] = "This field must contain at least 2 characters.";
        }
      }
    }
    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const originResolved = useMemo(() => resolveGeoFromLookup(formData.origin, citiesIndex, US_STATE_CENTROIDS, zipCoords), [formData.origin, citiesIndex, zipCoords]);
  const destResolved = useMemo(() => resolveGeoFromLookup(formData.destination, citiesIndex, US_STATE_CENTROIDS, zipCoords), [formData.destination, citiesIndex, zipCoords]);

  useEffect(() => {
    if (originResolved.geo && destResolved.geo) {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 5000);
      const fetchDistance = async () => {
        try {
          const res = await fetch(`https://router.project-osrm.org/route/v1/driving/${originResolved.geo.lon},${originResolved.geo.lat};${destResolved.geo.lon},${destResolved.geo.lat}?overview=false`, {
            signal: controller.signal
          });
          clearTimeout(timeoutId);
          const data = await res.json();
          if (data.routes && data.routes[0]) {
            setOsrmDistance(Math.round(data.routes[0].distance / 1609.34));
          } else {
            setOsrmDistance(haversineMiles(originResolved.geo, destResolved.geo));
          }
        } catch (e) {
          setOsrmDistance(haversineMiles(originResolved.geo, destResolved.geo));
        }
      };
      fetchDistance();
      return () => { clearTimeout(timeoutId); controller.abort(); };
    } else {
      setOsrmDistance(null);
    }
  }, [originResolved.geo, destResolved.geo]);

  const nextStep = () => {
    if (!validateStep(step)) return;
    const nxt = Math.min(step + 1, 4);
    setStep(nxt);
  };
  const prevStep = () => { setErrors({}); setStep(Math.max(step - 1, 1)); setPriceRevealed(false); };
  const jumpToStep = (s) => {
    if (s >= step) {
      for (let i = step; i < s; i++) if (!validateStep(i)) return;
    }
    setErrors({});
    setStep(s);
    if (s !== 4) setPriceRevealed(false);
  };

  const submitQuote = async () => {
    if (!validateStep(4)) {
      setErrors((prev) => ({ ...prev, _global: "All fields validation failed. Please review highlighted fields." }));
      return;
    }
    
    setSubmitting(true);
    setSubmitStatus({ state: "loading", message: "Calculating your custom quote..." });

    try {
      // Determine base URL for local Next.js vs Production Hostinger
      const baseUrl = (typeof window !== 'undefined' && (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')) 
        ? "http://localhost:8000" : "";

      // 1. Calculate Quote from backend with local fallback
      let live = null;
      let calculatedMiles = osrmDistance;
      if (!calculatedMiles && originResolved?.geo && destResolved?.geo) {
        calculatedMiles = haversineMiles(originResolved.geo, destResolved.geo);
      }
      calculatedMiles = calculatedMiles || 1000;

      try {
        const payload = {
          ...formData,
          distance_miles: calculatedMiles,
          originGeo: originResolved?.geo,
          destGeo: destResolved?.geo
        };
        const calcRes = await fetch(`${baseUrl}/api/calculate_quote.php`, {
          method: "POST",
          headers: { "Content-Type": "application/json", Accept: "application/json" },
          body: JSON.stringify(payload),
        });
        if (calcRes.ok) {
          const calcBody = await calcRes.json();
          if (calcBody.success) live = calcBody.data;
        }
      } catch (err) {
        console.warn("Backend calculation unreachable, falling back to local calculation.");
      }

      if (!live) {
        // ─── SKY AUTO SERVICES MASTER PRICING ENGINE (Frontend Fallback) ────
        const vehicle = VEHICLE_TYPES.find((v) => v.id === formData.vehicleType) || VEHICLE_TYPES[0];
        const transport = TRANSPORT_LEVELS.find((t) => t.id === formData.transportType) || TRANSPORT_LEVELS[0];

        const priceResult = calculateSkyAutoPrice({
          miles: calculatedMiles,
          vehicleType:      formData.vehicleType,
          vehicleCondition: formData.vehicleCondition,
          vehicleValue:     formData.vehicleValue,
          transportType:    formData.transportType,
          originLabel:      originResolved?.label || formData.origin,
          destLabel:        destResolved?.label   || formData.destination,
        });

        live = {
          miles: calculatedMiles,
          mid: priceResult.mid,
          lo:  priceResult.lo,
          hi:  priceResult.hi,
          eta: priceResult.eta,
          vehicleLabel:  vehicle.label,
          transportLabel: transport.label,
          originLabel: originResolved?.label || formData.origin,
          destLabel:   destResolved?.label   || formData.destination,
          originZip: originResolved?.label && US_ZIP_RE.test(originResolved.label) ? originResolved.label : null,
          destZip:   destResolved?.label   && US_ZIP_RE.test(destResolved.label)   ? destResolved.label   : null,
          originGeo: originResolved?.geo,
          destGeo:   destResolved?.geo,
          breakdown: priceResult.breakdown,
        };
      }
      
      setPriceCalc({ ready: true, ...live });
      setPriceRevealed(true);
      
      setSubmitStatus({ state: "loading", message: "Submitting your quote request..." });

      const digits = (formData.phone || "").replace(/\D/g, "");
      const payload = {
        session_id: sessionId,
        origin: formData.origin.trim(),
        destination: formData.destination.trim(),
        distance_miles: live.miles,
        vehicle: `${formData.vehicleYear} ${formData.vehicleMake} ${formData.vehicleModel}`,
        vehicleYear: formData.vehicleYear,
        vehicleMake: formData.vehicleMake,
        vehicleModel: formData.vehicleModel,
        vehicleType: formData.vehicleType,
        vehicleTypeLabel: live.vehicleLabel || formData.vehicleType,
        vehicleCondition: formData.vehicleCondition,
        vehicleValue: formData.vehicleValue,
        transport_type: formData.transportType,
        transport_type_label: live.transportLabel || formData.transportType,
        price: live.mid,
        price_estimate_low: live.lo,
        price_estimate_high: live.hi,
        eta: live.eta,
        pickupDate: formData.pickupDate || null,
        full_name: (formData.firstName + " " + formData.lastName).trim(),
        email: formData.email.trim(),
        phone: digits,
        comments: (formData.comments || "").trim() || null,

        // Phase 2 Spreadsheet Scaffolding
        final_quoted_price: live.mid,
        route_origin_zip: live.originZip || formData.origin.trim(),
        route_destination_zip: live.destZip || formData.destination.trim(),
        more_info: (formData.comments || "").trim() || null,

        data_source_type: "WEBSITE_DIRECT_INTAKE",
        is_live: true,
        is_test: false,
      };

      // 2. Real Live Quote Ingestion & Google Sheets Sync (Dual Redundancy Pipeline)
      let quoteId = "QUOTE-" + Math.floor(Math.random() * 1000000);
      let googleSync = true;

      // Channel A: Direct Client-Side Browser Dispatch to Google Apps Script Webhook
      try {
        const gasPayload = {
          id: quoteId,
          name: payload.full_name,
          full_name: payload.full_name,
          phone: payload.phone,
          email: payload.email,
          origin: payload.origin,
          destination: payload.destination,
          vehicle: payload.vehicle,
          distance: payload.distance_miles,
          distance_miles: payload.distance_miles,
          transport_type: payload.transport_type_label,
          price: typeof payload.price === "number" ? `$${payload.price.toLocaleString()}` : payload.price,
          pickup_date: payload.pickupDate,
          comments: payload.comments
        };

        fetch("https://script.google.com/macros/s/AKfycbxjTrpOti2ZPZscPAbgKRTPc3PeAkNyBMCVnieVW2BtnUsnQsiIBp5wKo3JVKb6F43m/exec", {
          method: "POST",
          mode: "no-cors",
          headers: { "Content-Type": "text/plain;charset=utf-8" },
          body: JSON.stringify(gasPayload),
        }).catch((err) => console.warn("Google Webhook client dispatch notice:", err));
      } catch (gasErr) {
        console.error("Direct Google Apps Script dispatch error:", gasErr);
      }

      // Channel B: Server-Side Hostinger Ingestion & Direct Server Email Alert
      try {
        const baseUrl = (typeof window !== "undefined" && (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1")) ? "http://localhost:8000" : "";
        const saveRes = await fetch(`${baseUrl}/api/save_quote.php`, {
          method: "POST",
          headers: { "Content-Type": "application/json", Accept: "application/json" },
          body: JSON.stringify(payload),
        });
        if (saveRes.ok) {
          const resData = await saveRes.json();
          if (resData.quote_id) quoteId = resData.quote_id;
        }
      } catch (err) {
        console.warn("Backend save_quote server notification:", err);
      }

      // Channel C: Google Ads Live Conversion Pingback
      try {
        if (typeof window !== "undefined" && typeof window.gtag === "function") {
          window.gtag('event', 'conversion', {
            'send_to': 'AW-18396293415',
            'value': 1.0,
            'currency': 'USD',
            'transaction_id': quoteId || String(Date.now())
          });
          window.gtag('event', 'generate_lead', {
            'value': 1.0,
            'currency': 'USD'
          });
        }
      } catch (gtagErr) {
        console.warn("Google Tag conversion dispatch notice:", gtagErr);
      }
      
      setSubmitStatus({
        state: "success",
        message: "Quote request submitted successfully!",
        quoteId: quoteId,
        googleSync: googleSync,
      });
      setShowResultModal(true);
    } catch (e) {
      setSubmitStatus({ state: "error", message: "Unexpected error submitting quote. Please try again." });
    } finally {
      setSubmitting(false);
    }
  };

  const StepIndicator = () => (
    <div className="mb-5">
      <div className="flex justify-between text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">
        <span className={step >= 1 ? "text-blue-600" : ""}>1. Route</span>
        <span className={step >= 2 ? "text-blue-600" : ""}>2. Vehicle</span>
        <span className={step >= 3 ? "text-blue-600" : ""}>3. Transport</span>
      </div>
      <div className="w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">
        <div className="bg-blue-600 h-full transition-all duration-500 ease-out" style={{ width: `${(step / 4) * 100}%` }} />
      </div>
    </div>
  );

  const Err = ({ field }) => errors[field] ? <p className="text-rose-400 text-sm mt-1">{errors[field]}</p> : null;
  const clsBase = "w-full bg-white border border-slate-300 rounded-lg px-4 py-3 text-slate-900 text-lg placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all";
  const clsErr = "w-full bg-white border border-red-500 rounded-lg px-4 py-3 text-slate-900 text-lg placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-red-500 transition-all";

  return (
    <div id="quote-calculator-top" className="text-slate-900 w-full">
      <StepIndicator />

      <form className="space-y-6" onSubmit={(e) => e.preventDefault()} onKeyDown={handleKeyDown} noValidate>
        {step === 1 && (
          <div className="space-y-4 animate-in fade-in slide-in-from-right-4 duration-300">
            <div>
              <label htmlFor="quote-calc-origin" className="block text-base font-medium text-slate-700 mb-1">Origin (Pickup ZIP / City / State) <span className="text-rose-400">*</span></label>
              <input id="quote-calc-origin" type="text" name="origin" value={formData.origin} onChange={handleChange}
                className={errors.origin ? clsErr : clsBase}
                placeholder="e.g., 90210 or Los Angeles, CA"
                aria-invalid={!!errors.origin}
                aria-required="true"
              />
              <Err field="origin" />
            </div>
            <div>
              <label htmlFor="quote-calc-dest" className="block text-base font-medium text-slate-700 mb-1">Destination (Delivery ZIP / City / State) <span className="text-rose-400">*</span></label>
              <input id="quote-calc-dest" type="text" name="destination" value={formData.destination} onChange={handleChange}
                className={errors.destination ? clsErr : clsBase}
                placeholder="e.g., 10001 or New York, NY"
                aria-invalid={!!errors.destination}
                aria-required="true"
              />
              <Err field="destination" />
            </div>
            <div className="flex items-center gap-3 text-sm text-slate-600 bg-blue-500/5 border border-blue-400/20 rounded-lg px-3 py-2">
              <svg className="w-4 h-4 text-blue-300 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M18 10A8 8 0 11 2 10 8 8 0 0118 10zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" /></svg>
              Supports all 50 US states plus DC and any 5-digit ZIP code.
            </div>
          </div>
        )}

        {step === 2 && (
          <div className="space-y-4 animate-in fade-in slide-in-from-right-4 duration-300">
            <div>
              <label className="block text-base font-medium text-slate-700 mb-2">Vehicle Type <span className="text-rose-400">*</span></label>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
                {VEHICLE_TYPES.map((v) => (
                  <label key={v.id}
                    className={`block p-3 border rounded-xl cursor-pointer transition-all text-base ${formData.vehicleType === v.id ? "bg-emerald-50 border-emerald-500" : "bg-slate-50 border-slate-200 hover:border-slate-300"}`}>
                    <input type="radio" name="vehicleType" value={v.id} className="sr-only"
                      checked={formData.vehicleType === v.id} onChange={handleChange} />
                    <div className="font-semibold text-slate-900">{v.label}</div>
                    <div className="text-sm text-slate-600">
                      {VEHICLE_SURCHARGES[v.id] ? `+$${VEHICLE_SURCHARGES[v.id]}` : "Base Price"} · {v.weight.toLocaleString()} lb
                    </div>
                  </label>
                ))}
              </div>
              <Err field="vehicleType" />
            </div>
            <div>
              <label className="block text-base font-medium text-slate-700 mb-2">Vehicle Estimated Value <span className="text-rose-400">*</span></label>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
                <label className={`block p-3 border rounded-xl cursor-pointer transition-all text-base ${formData.vehicleValue === "under_50k" ? "bg-emerald-50 border-emerald-500" : "bg-slate-50 border-slate-200 hover:border-slate-300"}`}>
                  <input type="radio" name="vehicleValue" value="under_50k" className="sr-only" checked={formData.vehicleValue === "under_50k"} onChange={handleChange} />
                  <div className="font-semibold text-slate-900">Under $50k</div>
                </label>
                <label className={`block p-3 border rounded-xl cursor-pointer transition-all text-base ${formData.vehicleValue === "50k_100k" ? "bg-emerald-50 border-emerald-500" : "bg-slate-50 border-slate-200 hover:border-slate-300"}`}>
                  <input type="radio" name="vehicleValue" value="50k_100k" className="sr-only" checked={formData.vehicleValue === "50k_100k"} onChange={handleChange} />
                  <div className="font-semibold text-slate-900">$50k - $100k</div>
                  <div className="text-sm text-emerald-400">+15% Premium</div>
                </label>
                <label className={`block p-3 border rounded-xl cursor-pointer transition-all text-base ${formData.vehicleValue === "over_100k" ? "bg-emerald-50 border-emerald-500" : "bg-slate-50 border-slate-200 hover:border-slate-300"}`}>
                  <input type="radio" name="vehicleValue" value="over_100k" className="sr-only" checked={formData.vehicleValue === "over_100k"} onChange={handleChange} />
                  <div className="font-semibold text-slate-900">Over $100k</div>
                  <div className="text-sm text-emerald-400">+30% Luxury</div>
                </label>
              </div>
              <Err field="vehicleValue" />
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div>
                <label htmlFor="quote-calc-year" className="block text-base font-medium text-slate-700 mb-1">Year <span className="text-rose-400">*</span></label>
                <input id="quote-calc-year" type="text" inputMode="numeric" name="vehicleYear" value={formData.vehicleYear} onChange={handleChange}
                  className={errors.vehicleYear ? clsErr : clsBase} placeholder="2023" maxLength={4}
                  aria-required="true" aria-invalid={!!errors.vehicleYear}
                />
                <Err field="vehicleYear" />
              </div>
              <div>
                <label htmlFor="quote-calc-make" className="block text-base font-medium text-slate-700 mb-1">Make <span className="text-rose-400">*</span></label>
                <input id="quote-calc-make" type="text" name="vehicleMake" value={formData.vehicleMake} onChange={handleChange}
                  className={errors.vehicleMake ? clsErr : clsBase} placeholder="Tesla"
                  aria-required="true" aria-invalid={!!errors.vehicleMake}
                />
                <Err field="vehicleMake" />
              </div>
              <div>
                <label htmlFor="quote-calc-model" className="block text-base font-medium text-slate-700 mb-1">Model <span className="text-rose-400">*</span></label>
                <input id="quote-calc-model" type="text" name="vehicleModel" value={formData.vehicleModel} onChange={handleChange}
                  className={errors.vehicleModel ? clsErr : clsBase} placeholder="Model S"
                  aria-required="true" aria-invalid={!!errors.vehicleModel}
                />
                <Err field="vehicleModel" />
              </div>
            </div>
            <div>
              <label className="block text-base font-medium text-slate-700 mb-2">Vehicle Condition</label>
              <div className="grid grid-cols-2 gap-2">
                <label className={`block p-3 border rounded-xl cursor-pointer transition-all ${formData.vehicleCondition === "operable" ? "bg-emerald-50 border-emerald-500" : "bg-slate-50 border-slate-200 hover:border-slate-300"}`}>
                  <input type="radio" name="vehicleCondition" value="operable" className="sr-only"
                    checked={formData.vehicleCondition === "operable"} onChange={handleChange} />
                  <div className="font-semibold text-slate-900 text-base">Runs &amp; Drives</div>
                  <div className="text-sm text-slate-600">Vehicle can roll on and off the trailer under its own power.</div>
                </label>
                <label className={`block p-3 border rounded-xl cursor-pointer transition-all ${formData.vehicleCondition === "inoperable" ? "bg-emerald-50 border-emerald-500" : "bg-slate-50 border-slate-200 hover:border-slate-300"}`}>
                  <input type="radio" name="vehicleCondition" value="inoperable" className="sr-only"
                    checked={formData.vehicleCondition === "inoperable"} onChange={handleChange} />
                  <div className="font-semibold text-slate-900 text-base">Inoperable / Non-Running</div>
                  <div className="text-sm text-slate-600">Requires winch or forklift to load. +$150 surcharge.</div>
                </label>
              </div>
            </div>
          </div>
        )}

        {step === 3 && (
          <div className="space-y-4 animate-in fade-in slide-in-from-right-4 duration-300">
            {/* Company Info Box */}
            <div className="bg-gradient-to-br from-blue-900/40 to-emerald-900/20 border border-blue-500/30 rounded-xl p-5 mb-2 shadow-lg">
              <div className="flex items-start gap-4">
                <div className="bg-blue-500/10 p-2 rounded-lg border border-blue-400/20 flex-shrink-0 flex items-center justify-center">
                  <img
                    src="/assets/images/logo.png"
                    alt="Sky Auto Services Logo"
                    className="w-8 h-8 object-contain"
                  />
                </div>
                <div>
                  <h4 className="text-slate-900 font-bold text-lg mb-1">Why Sky Auto Services?</h4>
                  <p className="text-slate-700 text-sm leading-relaxed">
                    With over a decade of nationwide auto logistics experience, we provide premium, fully-insured door-to-door transport across all 50 states. Whether it&apos;s an open carrier or our hydraulic-lift enclosed trailers for exotics, your vehicle is handled by vetted, top-tier drivers.
                  </p>
                </div>
              </div>
            </div>

            <div>
              <label className="block text-base font-medium text-slate-700 mb-2">Transport Level <span className="text-rose-400">*</span></label>
              <div className="space-y-2">
                {TRANSPORT_LEVELS.map((t) => (
                  <label key={t.id}
                    className={`block relative p-4 border rounded-xl cursor-pointer transition-all ${formData.transportType === t.id ? "bg-emerald-50 border-emerald-500" : "bg-slate-50 border-slate-200 hover:border-slate-300"}`}>
                    <input type="radio" name="transportType" value={t.id} className="sr-only"
                      checked={formData.transportType === t.id} onChange={handleChange} />
                    <div className="flex justify-between items-start gap-4">
                      <div className="flex-1">
                        <div className="text-slate-900 font-semibold">{t.label}</div>
                        <div className="text-slate-600 text-base">{t.sub}</div>
                      </div>
                      <div className="text-right">
                        <div className="text-sm text-slate-600">tier multiplier</div>
                        <div className="text-slate-900 font-bold">×{t.multiplier.toFixed(2)}</div>
                        <div className="text-sm text-gray-500">min ${t.min}</div>
                      </div>
                      {formData.transportType === t.id && (
                        <svg className="w-6 h-6 text-emerald-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                      )}
                    </div>
                  </label>
                ))}
              </div>
              <Err field="transportType" />
            </div>
            <div>
              <label htmlFor="quote-calc-pickup-date" className="block text-base font-medium text-slate-700 mb-1">Preferred Pickup Timeframe</label>
              <select id="quote-calc-pickup-date" name="pickupDate" value={formData.pickupDate} onChange={handleChange} className={clsBase}>
                <option value="" disabled>Select Timeframe</option>
                <option value="Next 24 hours">Next 24 hours</option>
                <option value="48 hours">48 hours</option>
                <option value="72 hours">72 hours</option>
                <option value="7 days">7 days</option>
                <option value="1 month">1 month</option>
              </select>
            </div>
          </div>
        )}

        {step === 4 && (
          <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-300">
            {priceRevealed ? (
              <div className="bg-gradient-to-br from-emerald-500/15 via-blue-500/10 to-indigo-500/15 border border-emerald-400/30 rounded-2xl p-6 animate-in zoom-in duration-500">
                <h4 className="text-2xl font-bold text-slate-900 mb-1 text-center">Your Instant Price Estimate</h4>
                {citiesLoading ? (
                  <div className="text-slate-700 text-base py-6 text-center">
                    <svg className="animate-spin inline-block w-5 h-5 mr-2 text-emerald-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"></path></svg>
                    Loading route data, please wait…
                  </div>
                ) : priceCalc.ready ? (
                  <>
                    {/* ── Route strip ── */}
                    <div className="flex items-center justify-center gap-2 text-sm text-slate-500 mb-4 flex-wrap">
                      <span className="font-semibold text-slate-700 truncate max-w-[160px]" title={priceCalc.originLabel}>{priceCalc.originLabel}</span>
                      <span className="text-emerald-500 font-black text-lg">→</span>
                      <span className="font-semibold text-slate-700 truncate max-w-[160px]" title={priceCalc.destLabel}>{priceCalc.destLabel}</span>
                      <span className="text-slate-400 hidden sm:inline">·</span>
                      <span className="text-slate-500 hidden sm:inline">{priceCalc.miles?.toLocaleString()} mi</span>
                    </div>

                    {/* ── Big center price ── */}
                    <div className="text-center mb-2">
                      <div className="text-7xl font-black tracking-tight text-emerald-600 leading-none">
                        ${priceCalc.mid.toLocaleString()}
                      </div>
                      <div className="text-slate-500 text-sm mt-2 font-medium">{priceCalc.eta} estimated delivery</div>
                    </div>

                    {/* ── ±10% range band ── */}
                    <div className="bg-white/60 border border-slate-200 rounded-xl px-5 py-3 text-center mb-3">
                      <div className="text-slate-500 text-xs uppercase tracking-widest font-semibold mb-1">Price Range Estimate</div>
                      <div className="flex items-center justify-center gap-3">
                        <span className="text-xl font-bold text-slate-700">${priceCalc.lo.toLocaleString()}</span>
                        <span className="text-slate-400 text-sm font-medium">to</span>
                        <span className="text-xl font-bold text-slate-700">${priceCalc.hi.toLocaleString()}</span>
                      </div>
                      <div className="text-slate-400 text-xs mt-1">±10% of estimated price</div>
                    </div>

                    {/* ── Legal disclaimer ── */}
                    <p className="text-slate-400 text-xs text-center leading-relaxed mb-4 px-2">
                      This is a preliminary estimate only. After initial contact, your final confirmed price may vary within the range shown above based on route availability, vehicle condition, and seasonal demand. Sky Auto Services will provide a binding written quote before any pickup is scheduled.
                    </p>

                    {/* ── Info cards ── */}
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-3 text-sm mb-5 text-left">
                      <div className="bg-white border border-slate-200 rounded-lg p-3 shadow-sm">
                        <div className="text-slate-500 text-xs uppercase tracking-wider font-bold">Vehicle</div>
                        <div className="text-slate-900 font-semibold mt-1 truncate" title={`${formData.vehicleYear} ${formData.vehicleMake} ${formData.vehicleModel}`}>{formData.vehicleYear} {formData.vehicleMake} {formData.vehicleModel}</div>
                      </div>
                      <div className="bg-white border border-slate-200 rounded-lg p-3 shadow-sm">
                        <div className="text-slate-500 text-xs uppercase tracking-wider font-bold">Transport</div>
                        <div className="text-slate-900 font-semibold mt-1">{priceCalc.transportLabel || formData.transportType}</div>
                      </div>
                      <div className="bg-white border border-slate-200 rounded-lg p-3 shadow-sm">
                        <div className="text-slate-500 text-xs uppercase tracking-wider font-bold">ETA</div>
                        <div className="text-slate-900 font-semibold mt-1">{priceCalc.eta}</div>
                      </div>
                    </div>

                    <div className="text-center mt-2">
                      <button 
                        onClick={(e) => { e.preventDefault(); setShowResultModal(true); }}
                        className="px-6 py-3 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-base font-bold transition-all shadow-lg hover:-translate-y-0.5"
                      >
                        View Full Quote Details &amp; Route Map
                      </button>
                    </div>
                  </>
                ) : (
                  <div className="text-slate-700 text-base py-6 text-center">
                    ⚠️ Please go back and enter a valid origin &amp; destination (ZIP code, city, or state name) and select a vehicle type.
                  </div>
                )}
              </div>
            ) : (
              <div className="bg-blue-50 border border-blue-200 rounded-xl p-4 text-center">
                <h4 className="text-xl font-bold text-slate-900 mb-1">Your Quote is Ready!</h4>
                <p className="text-slate-600 text-sm">Enter your contact details below to view your instant rate.</p>
              </div>
            )}

            <div className="space-y-4 border-t border-white/10 pt-5">
              <h4 className="text-3xl font-bold text-slate-900 text-center">Contact Information <span className="block text-rose-400 text-base font-normal mt-1">(All fields required)</span></h4>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label htmlFor="quote-calc-first-name" className="block text-base font-medium text-slate-700 mb-1">First Name <span className="text-rose-400">*</span></label>
                  <input id="quote-calc-first-name" type="text" name="firstName" value={formData.firstName} onChange={handleChange}
                    className={errors.firstName ? clsErr : clsBase} placeholder="John"
                    autoComplete="given-name" aria-required="true" aria-invalid={!!errors.firstName}
                  />
                  <Err field="firstName" />
                </div>
                <div>
                  <label htmlFor="quote-calc-last-name" className="block text-base font-medium text-slate-700 mb-1">Last Name (Surname) <span className="text-rose-400">*</span></label>
                  <input id="quote-calc-last-name" type="text" name="lastName" value={formData.lastName} onChange={handleChange}
                    className={errors.lastName ? clsErr : clsBase} placeholder="Smith"
                    autoComplete="family-name" aria-required="true" aria-invalid={!!errors.lastName}
                  />
                  <Err field="lastName" />
                </div>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label htmlFor="quote-calc-email" className="block text-base font-medium text-slate-700 mb-1">Email <span className="text-rose-400">*</span></label>
                  <input id="quote-calc-email" type="email" name="email" value={formData.email} onChange={handleChange}
                    className={errors.email ? clsErr : clsBase} placeholder="you@example.com"
                    autoComplete="email" aria-required="true" aria-invalid={!!errors.email}
                  />
                  <Err field="email" />
                </div>
                <div>
                  <label htmlFor="quote-calc-phone" className="block text-base font-medium text-slate-700 mb-1">Phone Number <span className="text-rose-400">*</span></label>
                  <input id="quote-calc-phone" type="tel" name="phone" value={formData.phone} onChange={handleChange}
                    className={errors.phone ? clsErr : clsBase} placeholder="(555) 123-4567"
                    autoComplete="tel" aria-required="true" aria-invalid={!!errors.phone}
                  />
                  <Err field="phone" />
                </div>
              </div>
              <div>
                <label htmlFor="quote-calc-comments" className="block text-base font-medium text-slate-700 mb-1">Comments / Special Requirements</label>
                <textarea id="quote-calc-comments" name="comments" rows={3} value={formData.comments} onChange={handleChange}
                  className={clsBase} placeholder="e.g., enclosed with door-to-door pickup, need live tracking, etc." />
              </div>
              {errors._global && (
                <div className="text-rose-400 text-base bg-rose-500/10 border border-rose-500/40 rounded-lg px-3 py-2">{errors._global}</div>
              )}
              {submitStatus && submitStatus.state !== "loading" && (
                <div className={`text-base rounded-lg px-3 py-2 border ${submitStatus.state === "success" ? "text-emerald-300 bg-emerald-500/10 border-emerald-400/40"
                    : "text-rose-400 bg-rose-500/10 border-rose-500/40"
                  }`}>
                  {submitStatus.state === "success"
                    ? <>✓ {submitStatus.message}
                      {submitStatus.quoteId && <span className="block text-sm text-emerald-400/90 mt-0.5">Quote ID: {submitStatus.quoteId} · Sheets sync: {submitStatus.googleSync || "pending"}</span>}
                    </>
                    : <>✗ {submitStatus.message}</>}
                </div>
              )}
            </div>
          </div>
        )}

        <div className="flex flex-col sm:flex-row gap-3 pt-4 sm:flex-wrap w-full">
          {step > 1 && (!submitStatus || submitStatus?.state !== "success") ? (
            <button type="button" onClick={prevStep}
              className="w-full sm:w-auto px-6 py-3 rounded-xl border border-slate-300 text-slate-700 font-semibold hover:bg-slate-50 transition-all">
              ← Back
            </button>
          ) : null}
          {step < 4 ? (
            <button type="button" onClick={nextStep}
              className="w-full sm:w-auto flex-1 bg-gradient-to-r from-blue-600 to-indigo-600 text-white py-3 rounded-xl font-bold hover:shadow-lg transition-all hover:-translate-y-0.5 min-w-0">
              Next Step →
            </button>
          ) : (
            <button type="button"
              onClick={submitQuote}
              disabled={submitting || submitStatus?.state === "success"}
              className={`w-full sm:w-auto flex-1 py-3 rounded-xl font-extrabold transition-all min-w-0 ${submitting || submitStatus?.state === "success"
                  ? "bg-slate-200 text-slate-400 cursor-not-allowed"
                  : "bg-gradient-to-r from-emerald-600 to-teal-600 text-white hover:shadow-lg hover:-translate-y-0.5"
                }`}>
              {submitting ? "Calculating..." :
                submitStatus?.state === "success" ? "✓ Quote Requested" :
                  priceRevealed ? "Resubmit Quote Request" :
                    "Get Free Quote"}
            </button>
          )}
        </div>
        {/* Required Unchecked-by-Default SMS Consent Checkbox (RingCentral / TCR Mandated) */}
        {step === 4 && (
          <div className="mt-4 p-3.5 bg-slate-50 border border-slate-300 rounded-xl text-left">
            <div className="flex items-start gap-3">
              <input
                id="quote-calc-sms-consent"
                type="checkbox"
                required
                checked={formData.smsConsent || false}
                onChange={(e) => setFormData({ ...formData, smsConsent: e.target.checked })}
                className="mt-1 h-4 w-4 rounded border-slate-400 bg-white text-emerald-600 focus:ring-emerald-500 cursor-pointer"
              />
              <label htmlFor="quote-calc-sms-consent" className="text-xs text-slate-700 leading-snug cursor-pointer select-none">
                I agree to receive SMS messages from <strong>SKY SERVICES LLC</strong> (Sky Auto Services). This includes SMS messages for conversations (external). Message frequency varies. Message and data rates may apply. See privacy policy at <a href="/privacy" className="text-blue-600 font-semibold underline hover:text-blue-800">https://www.skyautoservices.com/privacy.html</a>. Message HELP for help. Reply STOP to any message to opt out. View our <a href="/terms" className="text-blue-600 font-semibold underline hover:text-blue-800">Terms of Service</a>.
              </label>
            </div>
            <Err field="smsConsent" />
          </div>
        )}
      </form>
      <QuoteResultModal
        isOpen={showResultModal}
        onClose={() => setShowResultModal(false)}
        priceCalc={priceCalc}
        formData={formData}
        submitStatus={submitStatus}
      />
    </div>
  );
}
