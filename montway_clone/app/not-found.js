import Link from 'next/link';

export const metadata = {
  title: '404 - Page Not Found | Sky Auto Services',
  description: 'The requested auto transport route or page could not be found. Get an instant car shipping quote or browse all 50 state corridors.',
};

export default function NotFound() {
  return (
    <main className="min-h-screen bg-slate-950 text-white flex flex-col justify-between pt-32 pb-16 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
      {/* Background Glow */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-blue-600/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-10 right-10 w-[400px] h-[400px] bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />

      <div className="max-w-4xl mx-auto text-center relative z-10 my-auto">
        {/* Badge */}
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-blue-500/10 border border-blue-500/30 text-blue-400 text-xs font-semibold uppercase tracking-wider mb-8">
          <span className="w-2 h-2 rounded-full bg-blue-400 animate-pulse" />
          Status Code: 404 • Destination Offline
        </div>

        {/* 404 Heading */}
        <h1 className="text-6xl sm:text-8xl font-extrabold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-cyan-300 to-emerald-400 mb-6">
          404
        </h1>
        <h2 className="text-2xl sm:text-4xl font-bold text-white mb-4">
          This Transport Corridor Took a Detour
        </h2>
        <p className="text-slate-400 text-base sm:text-lg max-w-xl mx-auto mb-10 leading-relaxed">
          The page or route corridor you requested is unavailable or has been relocated. Don&apos;t worry — our nationwide logistics network is active across all 50 states.
        </p>

        {/* Action Cards Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 max-w-3xl mx-auto mb-10 text-left">
          <Link
            href="/"
            className="group p-5 rounded-2xl bg-white/5 border border-white/10 hover:border-blue-400/50 hover:bg-white/10 transition-all duration-200"
          >
            <div className="text-2xl mb-2">⚡</div>
            <h3 className="font-bold text-white text-base group-hover:text-blue-400 transition-colors">
              Instant Quote Calculator ›
            </h3>
            <p className="text-xs text-slate-400 mt-1">
              Calculate exact mileage pricing and book door-to-door transport in 60 seconds.
            </p>
          </Link>

          <Link
            href="/state-to-state-routes/"
            className="group p-5 rounded-2xl bg-white/5 border border-white/10 hover:border-emerald-400/50 hover:bg-white/10 transition-all duration-200"
          >
            <div className="text-2xl mb-2">🗺️</div>
            <h3 className="font-bold text-white text-base group-hover:text-emerald-400 transition-colors">
              50-State Routes Hub ›
            </h3>
            <p className="text-xs text-slate-400 mt-1">
              Browse dedicated inter-state shipping lanes and regional transit schedules.
            </p>
          </Link>

          <Link
            href="/usa-auto-transport-news"
            className="group p-5 rounded-2xl bg-white/5 border border-white/10 hover:border-cyan-400/50 hover:bg-white/10 transition-all duration-200"
          >
            <div className="text-2xl mb-2">📰</div>
            <h3 className="font-bold text-white text-base group-hover:text-cyan-400 transition-colors">
              Transport News & Guides ›
            </h3>
            <p className="text-xs text-slate-400 mt-1">
              Read verified carrier guidelines, seasonal trends, and enclosed auto logistics.
            </p>
          </Link>
        </div>

        {/* Direct Contact & Home CTA */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <Link
            href="/"
            className="w-full sm:w-auto px-8 py-3.5 rounded-full bg-blue-600 hover:bg-blue-500 text-white font-bold text-sm shadow-lg shadow-blue-600/30 transition-all duration-200"
          >
            Return to Homepage
          </Link>
          <a
            href="tel:+12244490397"
            className="w-full sm:w-auto px-8 py-3.5 rounded-full bg-white/10 hover:bg-white/20 border border-white/15 text-white font-bold text-sm transition-all duration-200 flex items-center justify-center gap-2"
          >
            <svg className="w-4 h-4 text-cyan-400 fill-current" viewBox="0 0 24 24">
              <path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.4 0 .8-.3 1l-2.2 2.2z" />
            </svg>
            Call Dispatch: (224) 449-0397
          </a>
        </div>
      </div>

      {/* Footer Trust Bar */}
      <div className="text-center text-xs text-slate-500 border-t border-white/10 pt-6 max-w-4xl mx-auto w-full">
        Sky Auto Services LLC • Licensed FMCSA Property Broker MC-1782670 • USDOT 4504932 • 24/7 Nationwide Vehicle Logistics
      </div>
    </main>
  );
}
