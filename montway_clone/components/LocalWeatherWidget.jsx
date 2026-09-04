"use client";
import React, { useEffect, useState } from 'react';

const STATE_CENTROIDS = {
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

const STATE_NAMES_TO_ABBR = {
  "alabama": "AL", "arizona": "AZ", "arkansas": "AR", "california": "CA",
  "colorado": "CO", "connecticut": "CT", "delaware": "DE", "florida": "FL", "georgia": "GA",
  "hawaii": "HI", "idaho": "ID", "illinois": "IL", "indiana": "IN", "iowa": "IA",
  "kansas": "KS", "kentucky": "KY", "louisiana": "LA", "maine": "ME", "maryland": "MD",
  "massachusetts": "MA", "michigan": "MI", "minnesota": "MN", "mississippi": "MS", "missouri": "MO",
  "montana": "MT", "nebraska": "NE", "nevada": "NV", "new hampshire": "NH", "new jersey": "NJ",
  "new mexico": "NM", "new york": "NY", "north carolina": "NC", "north dakota": "ND", "ohio": "OH",
  "oklahoma": "OK", "oregon": "OR", "pennsylvania": "PA", "rhode island": "RI", "south carolina": "SC",
  "south dakota": "SD", "tennessee": "TN", "texas": "TX", "utah": "UT", "vermont": "VT",
  "virginia": "VA", "washington": "WA", "west virginia": "WV", "wisconsin": "WI", "wyoming": "WY",
  "district of columbia": "DC"
};

export default function LocalWeatherWidget({ stateName }) {
  const [weather, setWeather] = useState(null);

  useEffect(() => {
    if (!stateName) return;
    const abbr = STATE_NAMES_TO_ABBR[stateName.toLowerCase()];
    if (!abbr) return;
    
    const centroid = STATE_CENTROIDS[abbr];
    if (!centroid) return;

    const cacheKey = `weather_${stateName.toLowerCase()}`;
    const cachedStr = sessionStorage.getItem(cacheKey);
    if (cachedStr) {
      const cached = JSON.parse(cachedStr);
      if (Date.now() - cached.timestamp < 3600000) {
        setWeather(cached.data);
        return;
      }
    }

    fetch(`https://api.open-meteo.com/v1/forecast?latitude=${centroid.lat}&longitude=${centroid.lon}&current_weather=true&temperature_unit=fahrenheit`)
      .then(res => res.json())
      .then(data => {
        if (data && data.current_weather) {
          sessionStorage.setItem(cacheKey, JSON.stringify({
            timestamp: Date.now(),
            data: data.current_weather
          }));
          setWeather(data.current_weather);
        }
      })
      .catch(err => console.error("Weather fetch error", err));
  }, [stateName]);

  if (!weather) return null;

  return (
    <div className="bg-black/60 backdrop-blur-md border border-white/10 p-4 rounded-xl flex items-center gap-4 max-w-sm">
      <div className="text-4xl">🌤️</div>
      <div>
        <h4 className="text-white font-bold text-lg">Local Weather</h4>
        <p className="text-gray-300 text-2xl font-black">{Math.round(weather.temperature)}°F</p>
        <p className="text-emerald-400 text-sm">Perfect conditions for auto transport</p>
      </div>
    </div>
  );
}
