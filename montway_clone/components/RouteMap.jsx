"use client";
import React, { useEffect, useRef, useState } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

// Fix default Leaflet icon paths in Next.js
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png",
  iconUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png",
  shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png",
});

export default function RouteMap({ originGeo, destGeo, miles, midPrice }) {
  const mapRef = useRef(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!originGeo || !destGeo || !mapRef.current) return;
    // Fix for React Strict Mode: ensure map isn't already initialized
    const container = mapRef.current;
    if (container != null && container._leaflet_id !== null && container._leaflet_id !== undefined) {
      container._leaflet_id = null;
      container.innerHTML = '';
    }

    // Initialize map
    const map = L.map(container, {
      zoomControl: true,
      dragging: true,
      scrollWheelZoom: true,
    });
    
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: '&copy; OpenStreetMap contributors',
    }).addTo(map);

    // Fix map rendering in modals by tracking size changes
    const resizeObserver = new ResizeObserver(() => {
      if (mapRef.current) {
        map.invalidateSize();
      }
    });
    resizeObserver.observe(mapRef.current);
    
    // Fallback timer just in case
    setTimeout(() => {
      if (mapRef.current) map.invalidateSize();
    }, 250);

    const start = [originGeo.lat, originGeo.lon];
    const end = [destGeo.lat, destGeo.lon];

    const originMarker = L.marker(start).addTo(map).bindPopup("Origin");
    const destMarker = L.marker(end).addTo(map).bindPopup("Destination");
    const markerGroup = L.featureGroup([originMarker, destMarker]);

    // Fetch OSRM route
    fetch(`https://router.project-osrm.org/route/v1/driving/${originGeo.lon},${originGeo.lat};${destGeo.lon},${destGeo.lat}?overview=full&geometries=geojson`)
      .then(res => res.json())
      .then(data => {
        setLoading(false);
        if (data.routes && data.routes[0]) {
          const routeCoordinates = data.routes[0].geometry.coordinates.map(coord => [coord[1], coord[0]]);
          const polyline = L.polyline(routeCoordinates, { color: '#10b981', weight: 4 }).addTo(map);
          map.fitBounds(polyline.getBounds(), { padding: [30, 30] });
        } else {
          map.fitBounds(markerGroup.getBounds(), { padding: [30, 30] });
        }
      })
      .catch(err => {
        setLoading(false);
        map.fitBounds(markerGroup.getBounds(), { padding: [30, 30] });
      });

    return () => {
      resizeObserver.disconnect();
      map.remove();
    };
  }, [originGeo, destGeo]);

  const pricePerMile = miles && miles > 0 ? (midPrice / miles).toFixed(2) : "0.00";

  return (
    <div className="relative w-full rounded-xl overflow-hidden border border-slate-700 my-4 shadow-lg">
      <div className="absolute top-4 left-4 z-[400] bg-black/80 backdrop-blur-md px-4 py-2 rounded-lg border border-slate-700/50 shadow-lg">
        <div className="text-emerald-400 font-black text-xl">${pricePerMile} <span className="text-sm font-normal text-slate-300">/ mile</span></div>
        <div className="text-slate-400 text-xs">{miles?.toLocaleString()} total miles</div>
      </div>
      
      <div className="absolute bottom-4 right-4 z-[400] bg-black/80 backdrop-blur-md px-3 py-1.5 rounded-lg border border-slate-700/50 shadow-lg text-xs text-white cursor-pointer hover:bg-black transition" onClick={() => window.open(`https://www.google.com/maps/dir/${originGeo?.lat},${originGeo?.lon}/${destGeo?.lat},${destGeo?.lon}`, '_blank')}>
        Open in Google Maps ↗
      </div>
      
      {loading && (
        <div className="absolute inset-0 z-[500] flex items-center justify-center bg-slate-900/80 backdrop-blur-sm">
          <svg className="animate-spin h-8 w-8 text-emerald-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"></path></svg>
        </div>
      )}
      
      <div ref={mapRef} className="w-full h-64 md:h-80 z-0 bg-slate-800"></div>
    </div>
  );
}
