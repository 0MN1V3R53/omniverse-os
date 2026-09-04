"use client";
import React, { useState } from 'react';
import Link from 'next/link';
import InteractiveUSMap from './InteractiveUSMap';
import ALL_STATES from './data/statesData';

export default function MontwayMarketingSections() {
  const [showAllStates, setShowAllStates] = useState(false);

  return (
    <>
      {/* ─── How Much Does Car Shipping Cost? ─── */}
      <section className="py-24 bg-white border-t border-slate-200">
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid lg:grid-cols-2 gap-16 items-start">
            {/* Left: Pricing Factors */}
            <div>
              <h2 className="text-3xl md:text-4xl font-extrabold text-slate-900 mb-4">How much do car transport companies charge?</h2>
              <p className="text-slate-600 text-lg mb-8 leading-relaxed">Car shipping costs are based on several factors, including current market trends, carrier availability and fuel prices. Your total cost will also depend on the type of car you want to move, where it needs to go, its condition (operable or inoperable), whether you choose open or enclosed trailer, and finally, the time of year when you book.</p>
              <div className="space-y-4">
                {[
                  { icon: "🚗", label: "Size and weight of vehicle", desc: "Larger, heavier vehicles take up more trailer space and cost more to ship." },
                  { icon: "🔧", label: "The car condition", desc: "Inoperable vehicles require special equipment to load and unload, adding cost." },
                  { icon: "🚛", label: "The transport type", desc: "Open transport is most affordable. Enclosed transport offers premium protection." },
                  { icon: "📍", label: "The shipping distance", desc: "Longer routes cost more overall, but the cost-per-mile typically decreases." },
                  { icon: "📅", label: "Pickup date and season", desc: "Snowbird seasons (fall/spring) drive higher demand and pricing across key corridors." }
                ].map((f, i) => (
                  <div key={i} className="flex items-start gap-4 p-4 rounded-xl border border-slate-100 hover:border-blue-200 hover:bg-blue-50/30 transition-colors cursor-default">
                    <div className="text-2xl flex-shrink-0 w-10 text-center">{f.icon}</div>
                    <div>
                      <div className="font-bold text-slate-800 mb-0.5">{f.label}</div>
                      <div className="text-slate-500 text-sm">{f.desc}</div>
                    </div>
                    <div className="ml-auto text-slate-300 flex-shrink-0">›</div>
                  </div>
                ))}
              </div>
            </div>
            {/* Right: Trust Badge Grid */}
            <div>
              <h3 className="text-2xl font-bold text-slate-900 mb-8">Why ship with Sky Auto Services?</h3>
              <div className="grid grid-cols-2 gap-4">
                {[
                  { icon: "✅", label: "TruePrice Guarantee", desc: "The price you're quoted is the price you pay. Always." },
                  { icon: "👤", label: "Personalized approach", desc: "A dedicated advisor manages your shipment start to finish." },
                  { icon: "🎯", label: "Dedicated advisors", desc: "Real humans, not bots. Available when you need us." },
                  { icon: "🏆", label: "Top-rated company", desc: "Consistently rated #1 by customers across the US." },
                  { icon: "💳", label: "Zero upfront payment", desc: "$0 deposit. Pay only when your carrier is dispatched." },
                  { icon: "🛡️", label: "Insurance coverage", desc: "Every carrier is verified and fully insured. Your car is always protected." },
                  { icon: "🚚", label: "10,000+ auto carriers", desc: "The largest vetted carrier network in the country." },
                  { icon: "📞", label: "24/7 support", desc: "We're here around the clock from quote to delivery." }
                ].map((b, i) => (
                  <div key={i} className="bg-slate-50 border border-slate-200 rounded-xl p-4 hover:shadow-md hover:border-blue-200 transition-all">
                    <div className="text-2xl mb-2">{b.icon}</div>
                    <div className="font-bold text-slate-800 text-sm mb-1">{b.label}</div>
                    <div className="text-slate-500 text-xs leading-relaxed">{b.desc}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ─── Service Type Cards ─── */}
      <section className="py-20 bg-slate-50 border-t border-slate-200">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-14">
            <h2 className="text-3xl md:text-4xl font-extrabold text-slate-900 mb-4">Shipping services for every vehicle</h2>
            <p className="text-slate-600 text-lg max-w-2xl mx-auto">Whatever you drive, we have a transport solution built for it.</p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              { title: "Open auto transport", desc: "The most popular and cost-effective option. Your vehicle travels on an open multi-car trailer — the same method used by dealerships nationwide. Best for standard vehicles and everyday drivers.", badge: "Most Popular", badgeColor: "bg-blue-100 text-blue-700" },
              { title: "Enclosed auto transport", desc: "Premium fully-enclosed trailers with liftgates. Zero exposure to road debris, weather, or the elements. The preferred choice for classic cars, exotics, luxury vehicles, and high-value assets.", badge: "Premium", badgeColor: "bg-amber-100 text-amber-700" },
              { title: "Motorcycle shipping", desc: "Sky Auto Services provides the best year-round motorcycle pricing. We use experienced drivers who have specific expertise with two-wheeled vehicle transport, ensuring your bike arrives without a scratch.", badge: "Specialized", badgeColor: "bg-emerald-100 text-emerald-700" }
            ].map((s, i) => (
              <div key={i} className="bg-white border border-slate-200 rounded-2xl p-8 shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all flex flex-col">
                <span className={`inline-block text-xs font-bold px-3 py-1 rounded-full mb-4 self-start ${s.badgeColor}`}>{s.badge}</span>
                <h3 className="text-xl font-bold text-slate-900 mb-3">{s.title} ›</h3>
                <p className="text-slate-600 text-sm leading-relaxed flex-grow">{s.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ─── State Shipping Cards ─── */}
      <section className="py-20 bg-white border-t border-slate-200">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-14">
            <h2 className="text-3xl md:text-4xl font-extrabold text-slate-900 mb-4">Car shipping services by state</h2>
            <p className="text-slate-600 text-lg max-w-2xl mx-auto">We cover all 50 states. Browse routes by your origin or destination.</p>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
            {ALL_STATES.slice(0, showAllStates ? 50 : 15).map((s, i) => (
              <Link
                key={i}
                href={`/state-to-state-routes/${s.state.toLowerCase().replace(/\s+/g, '-')}`}
                className="group relative rounded-xl overflow-hidden border border-slate-200 hover:border-blue-400 hover:shadow-xl transition-all cursor-pointer min-h-[130px] flex flex-col justify-end"
              >
                <img 
                  src={s.img} 
                  alt={`${s.state} auto transport and vehicle shipping`}
                  className="absolute inset-0 w-full h-full object-cover"
                  loading="lazy"
                  width="280"
                  height="180"
                  onError={(e) => {
                    e.currentTarget.src = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Yosemite_Valley_from_Wawona_Tunnel_view%2C_2020.jpg/1000px-Yosemite_Valley_from_Wawona_Tunnel_view%2C_2020.jpg"; // Generic US landscape fallback
                  }}
                />
                {/* Dark gradient overlay */}
                <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent" />
                {/* Hover brighten */}
                <div className="absolute inset-0 bg-blue-600/0 group-hover:bg-blue-600/20 transition-colors" />
                <div className="relative z-10 p-3">
                  <div className="text-xs font-bold text-blue-300 mb-0.5 uppercase tracking-wider">{s.abbr}</div>
                  <div className="font-bold text-white text-sm group-hover:text-blue-200 transition-colors">{s.state} ›</div>
                </div>
              </Link>
            ))}
          </div>
          <div className="text-center mt-10">
            <button 
              onClick={(e) => { e.preventDefault(); setShowAllStates(!showAllStates); }} 
              className="inline-block border border-blue-600 text-blue-600 hover:bg-blue-600 hover:text-white px-8 py-3 rounded-full font-bold text-sm transition-colors"
            >
              {showAllStates ? "Show less" : "View all 50 states"}
            </button>
          </div>
        </div>
      </section>

      {/* Interactive Map Section */}
      <section className="py-24 bg-slate-50 border-t border-slate-200">
        <div className="max-w-7xl mx-auto px-4">
          <InteractiveUSMap />
        </div>
      </section>
    </>
  );
}
