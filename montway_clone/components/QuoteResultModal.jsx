"use client";
import React from 'react';
import dynamic from 'next/dynamic';

const RouteMap = dynamic(() => import('./RouteMap'), { 
  ssr: false, 
  loading: () => <div className="w-full h-64 md:h-80 bg-slate-800 rounded-xl my-4 animate-pulse flex items-center justify-center border border-slate-700 shadow-lg text-slate-500">Loading Route Map...</div>
});

export default function QuoteResultModal({ isOpen, onClose, priceCalc, formData, submitStatus }) {
  if (!isOpen || !priceCalc?.ready) return null;

  return (
    <div className="fixed inset-0 z-[9999] flex items-start justify-center p-3 sm:p-4 bg-black/80 backdrop-blur-sm overflow-y-auto">
      <div className="bg-slate-900 border border-slate-700 rounded-3xl max-w-2xl w-full p-0 shadow-2xl relative flex flex-col mt-12 sm:mt-16 mb-6 sm:mb-10 max-h-[92vh] overflow-hidden">
        {/* Header Ribbon */}
        <div className="bg-gradient-to-r from-blue-600 to-indigo-600 p-4 text-center relative">
          <h2 className="text-2xl sm:text-3xl font-extrabold text-white">Your Instant Rate is Ready!</h2>
          <p className="text-blue-100 text-xs sm:text-sm mt-0.5 font-medium">$0 Upfront Deposit · Direct Carrier Dispatch · $100k-$1M+ Insurance Included</p>
        </div>

        <button
          onClick={onClose}
          className="absolute top-3 right-4 w-9 h-9 rounded-full bg-black/40 hover:bg-black/60 border border-white/20 text-white/80 hover:text-white transition-all flex items-center justify-center p-1"
          aria-label="Close modal"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M6 18L18 6M6 6l12 12"></path></svg>
        </button>

        <div className="p-5 sm:p-6 overflow-y-auto">
          {/* Price Section */}
          <div className="text-center mb-5 bg-gradient-to-b from-slate-800/80 to-slate-900/80 rounded-2xl p-5 border border-emerald-500/30 shadow-inner">
            <div className="inline-block px-3 py-1 bg-emerald-500/20 border border-emerald-400/40 rounded-full text-emerald-300 text-xs font-bold uppercase tracking-wider mb-2">
              🛡️ 100% Price Lock Guarantee
            </div>
            <div className="text-5xl sm:text-6xl font-black tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 via-teal-300 to-cyan-300 mb-1">
              ${priceCalc.mid.toLocaleString()}
            </div>
            <div className="text-slate-300 text-sm mb-3">Estimated Corridor Range: <span className="font-semibold text-white">${priceCalc.lo.toLocaleString()}</span> – <span className="font-semibold text-white">${priceCalc.hi.toLocaleString()}</span></div>
            
            <div className="bg-black/50 rounded-xl p-3.5 mx-auto max-w-sm mb-3 border border-emerald-500/20 text-left text-xs sm:text-sm">
              <h4 className="font-bold text-emerald-400 uppercase tracking-wider mb-2 border-b border-emerald-500/20 pb-1 flex justify-between items-center">
                <span>Transparent Cost Breakdown</span>
                <span className="text-[10px] text-slate-400 font-mono font-normal">No Hidden Fees</span>
              </h4>
              {priceCalc.breakdown ? (
                <>
                  <div className="flex justify-between items-center text-slate-300 py-0.5">
                    <span>Base Carrier Mile Rate (${priceCalc.breakdown.baseRate.toFixed(2)}/mi)</span>
                    <span className="text-white font-semibold">${priceCalc.breakdown.baseMilesCost.toLocaleString()}</span>
                  </div>
                  
                  <div className="flex justify-between items-center text-slate-300 py-0.5">
                    <span>Vehicle Class: {priceCalc.vehicleLabel || formData.vehicleType}</span>
                    <span className="text-white font-semibold">{priceCalc.breakdown.vehicleSurcharge > 0 ? `+$${priceCalc.breakdown.vehicleSurcharge.toLocaleString()}` : "$0"}</span>
                  </div>
                  
                  <div className="flex justify-between items-center text-slate-300 py-0.5">
                    <span>Condition: {formData.vehicleCondition === 'inoperable' ? 'Inoperable' : 'Operable'}</span>
                    <span className="text-white font-semibold">{priceCalc.breakdown.inoperableSurcharge > 0 ? `+$${priceCalc.breakdown.inoperableSurcharge.toLocaleString()}` : "$0"}</span>
                  </div>
                  
                  <div className="flex justify-between items-center text-slate-300 py-0.5">
                    <span>Transport Tier: {priceCalc.transportLabel || formData.transportType}</span>
                    <span className="text-white font-semibold">{priceCalc.breakdown.transportSurcharge > 0 ? `+$${priceCalc.breakdown.transportSurcharge.toLocaleString()}` : "$0"}</span>
                  </div>
                  
                  <div className="flex justify-between items-center text-slate-300 py-0.5">
                    <span>Vehicle Coverage: {formData.vehicleValue === 'over_100k' ? 'Over $100k' : formData.vehicleValue === '50k_100k' ? '$50k - $100k' : 'Under $50k'}</span>
                    <span className="text-white font-semibold">{priceCalc.breakdown.valueSurcharge > 0 ? `+$${priceCalc.breakdown.valueSurcharge.toLocaleString()}` : "$0"}</span>
                  </div>
                </>
              ) : (
                <>
                  <div className="flex justify-between items-center text-slate-300 py-0.5">
                    <span>Guaranteed Carrier Pay</span>
                    <span className="text-white font-semibold">${Math.round(priceCalc.mid * 0.85).toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between items-center text-slate-300 py-0.5">
                    <span>Brokerage &amp; Logistics Service</span>
                    <span className="text-white font-semibold">${Math.round(priceCalc.mid * 0.15).toLocaleString()}</span>
                  </div>
                </>
              )}
              <div className="flex justify-between items-center text-sm font-bold pt-2 border-t border-emerald-500/30 mt-1 text-emerald-400">
                <span>Total Locked Rate ($0 Deposit Now)</span>
                <span className="text-base">${priceCalc.mid.toLocaleString()}</span>
              </div>
            </div>

            <div className="text-emerald-300 font-semibold text-xs sm:text-sm mt-1">
              ⚡ Estimated Transit Window: <span className="text-white font-bold">{priceCalc.eta}</span>
            </div>
          </div>

          {/* Details Grid */}
          <h3 className="text-sm font-bold text-slate-300 uppercase tracking-wider mb-2.5">Your Route &amp; Vehicle</h3>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5 mb-5 text-xs">
            <div className="bg-black/40 border border-white/10 rounded-xl p-2.5">
              <div className="text-slate-400 text-[10px] uppercase tracking-wider mb-1">Route</div>
              <div className="text-white font-semibold truncate" title={`${priceCalc.originLabel} → ${priceCalc.destLabel}`}>
                {priceCalc.originLabel} → {priceCalc.destLabel}
              </div>
            </div>
            <div className="bg-black/40 border border-white/10 rounded-xl p-2.5">
              <div className="text-slate-400 text-[10px] uppercase tracking-wider mb-1">Vehicle</div>
              <div className="text-white font-semibold truncate">
                {formData.vehicleYear} {formData.vehicleMake} {formData.vehicleModel}
              </div>
            </div>
            <div className="bg-black/40 border border-white/10 rounded-xl p-2.5">
              <div className="text-slate-400 text-[10px] uppercase tracking-wider mb-1">Transport</div>
              <div className="text-white font-semibold truncate">{priceCalc.transport?.label || formData.transportType}</div>
            </div>
            <div className="bg-black/40 border border-white/10 rounded-xl p-2.5">
              <div className="text-slate-400 text-[10px] uppercase tracking-wider mb-1">Distance</div>
              <div className="text-emerald-400 font-bold">{priceCalc.miles.toLocaleString()} mi</div>
            </div>
          </div>
          
          <RouteMap 
            originGeo={priceCalc.originGeo} 
            destGeo={priceCalc.destGeo} 
            miles={priceCalc.miles} 
            midPrice={priceCalc.mid} 
          />

          {/* Company Trust Section */}
          <h3 className="text-sm font-bold text-slate-300 uppercase tracking-wider mt-4 mb-2.5">Why Book With Sky Auto Services?</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 mb-5">
            <div className="flex items-start gap-2.5 bg-white/5 border border-white/10 rounded-xl p-2.5">
              <span className="text-lg">🛡️</span>
              <div>
                <div className="text-white font-bold text-xs">$0 Upfront Deposit</div>
                <div className="text-slate-400 text-[11px]">Pay zero dollars until your carrier is vetted and assigned.</div>
              </div>
            </div>
            <div className="flex items-start gap-2.5 bg-white/5 border border-white/10 rounded-xl p-2.5">
              <span className="text-lg">⭐</span>
              <div>
                <div className="text-white font-bold text-xs">4.95/5 Star Rated Hauler</div>
                <div className="text-slate-400 text-[11px]">Over 1,284+ verified cross-country deliveries.</div>
              </div>
            </div>
            <div className="flex items-start gap-2.5 bg-white/5 border border-white/10 rounded-xl p-2.5">
              <span className="text-lg">🚚</span>
              <div>
                <div className="text-white font-bold text-xs">Door-to-Door Service</div>
                <div className="text-slate-400 text-[11px]">Direct driveway pickup &amp; delivery nationwide.</div>
              </div>
            </div>
            <div className="flex items-start gap-2.5 bg-white/5 border border-white/10 rounded-xl p-2.5">
              <span className="text-lg">📜</span>
              <div>
                <div className="text-white font-bold text-xs">FMCSA Licensed &amp; Bonded</div>
                <div className="text-slate-400 text-[11px]">USDOT: 4504932 | MC-1782670 with full $1M cargo insurance.</div>
              </div>
            </div>
          </div>

          {/* Call Dispatch Action CTA */}
          <div className="flex flex-col sm:flex-row gap-3 mt-2">
            <a
              href="tel:+12244490397"
              className="flex-1 bg-gradient-to-r from-emerald-500 via-teal-500 to-cyan-500 hover:opacity-95 text-white font-extrabold py-3.5 px-4 rounded-xl shadow-[0_0_20px_rgba(16,185,129,0.4)] text-center flex items-center justify-center gap-2 text-sm sm:text-base transition-all hover:scale-[1.01]"
            >
              <svg className="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.4 0 .8-.3 1l-2.2 2.2z"></path></svg>
              <span>Call Dispatch to Lock Slot: (224) 449-0397</span>
            </a>
            <button
              onClick={onClose}
              className="px-6 py-3.5 bg-white/10 hover:bg-white/20 border border-white/20 text-white font-semibold rounded-xl text-xs sm:text-sm transition"
            >
              Close Window
            </button>
          </div>

          <div className="text-center mt-3 text-[11px] text-slate-400">
            {submitStatus?.quoteId ? (
              <span>Your Official Reference Quote ID: <strong className="text-emerald-400 font-mono">{submitStatus.quoteId}</strong></span>
            ) : (
              <span>Quote request active · Licensed FMCSA Logistics Broker</span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
