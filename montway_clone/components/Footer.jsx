export default function Footer() {
  return (
    <footer className="w-full bg-black border-t border-white/5 py-8 mt-auto z-50 relative">
      <div className="max-w-7xl mx-auto px-4 text-center">
        <div className="mb-8 border-b border-white/10 pb-6">
          <h4 className="text-emerald-400 font-bold mb-3 text-sm uppercase tracking-wider">National Auto Transport Routes</h4>
          <div className="flex flex-wrap justify-center gap-x-4 gap-y-2 text-xs text-gray-400">
            <a href="/routes" className="hover:text-white transition">View All 50 States</a>
            <span className="text-gray-700">|</span>
            <a href="/state-to-state-routes/" className="hover:text-white transition text-emerald-400 font-semibold">State-to-State Routes Hub</a>
            <span className="text-gray-700">|</span>
            <a href="/auto-transport/california/los-angeles/" className="hover:text-white transition">Los Angeles, CA</a>
            <span className="text-gray-700">|</span>
            <a href="/auto-transport/new-york/new-york/" className="hover:text-white transition">New York, NY</a>
            <span className="text-gray-700">|</span>
            <a href="/auto-transport/texas/houston/" className="hover:text-white transition">Houston, TX</a>
            <span className="text-gray-700">|</span>
            <a href="/auto-transport/florida/miami/" className="hover:text-white transition">Miami, FL</a>
            <span className="text-gray-700">|</span>
            <a href="/auto-transport/illinois/chicago/" className="hover:text-white transition">Chicago, IL</a>
            <span className="text-gray-700">|</span>
            <a href="/auto-transport/nevada/las-vegas/" className="hover:text-white transition">Las Vegas, NV</a>
          </div>
        </div>
        <div className="flex justify-center gap-6 text-sm text-gray-400 mb-4">
          <a href="/privacy" className="hover:text-emerald-400 transition">Privacy Policy</a>
          <a href="/terms" className="hover:text-emerald-400 transition">Terms & Conditions</a>
          {/* <a href="/usa-auto-transport-news" className="hover:text-emerald-400 transition">News</a> */}

          {/* <a href="/routes-directory/" className="hover:text-emerald-400 transition text-emerald-500/80">HTML Sitemap</a> */}
        </div>
        <div className="text-xs text-gray-600">
          &copy; {new Date().getFullYear()} Sky Auto Services. All rights reserved. Licensed FMCSA Broker MC-1782670.
        </div>

        {/* OMNIVERSE TECHNOLOGIES FOOTER SIGNATURE */}
        <div className="pt-6 mt-6 border-t border-white/10 flex flex-col items-center justify-center">
          <div className="relative mb-3 group cursor-pointer">
            <div className="absolute -inset-1.5 rounded-full bg-gradient-to-r from-blue-600 to-cyan-500 opacity-50 blur-md group-hover:opacity-100 transition duration-500"></div>
            <img src="/assets/images/omniverse_tech_logo.png" alt="Omniverse Technologies Logo" className="relative h-14 w-14 rounded-full object-cover border border-white/20 p-1 bg-black transition-transform duration-300 group-hover:scale-105" loading="lazy" />
          </div>
          
          <p className="text-xs text-slate-300 font-semibold tracking-wide">
            Designed by <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-400 font-bold">Omniverse Technologies</span>
          </p>
          
          <a href="https://t.me/OmniverseTech" target="_blank" rel="noopener noreferrer" className="mt-2.5 inline-flex items-center gap-1.5 px-4 py-1.5 rounded-full bg-blue-600/20 hover:bg-blue-600/30 border border-blue-500/40 text-cyan-300 text-xs font-mono transition-all hover:scale-105 shadow-sm hover:shadow-cyan-500/20">
            <svg className="w-3.5 h-3.5 fill-current text-cyan-400" viewBox="0 0 24 24">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.75-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z"/>
            </svg>
            <span>Telegram: @OmniverseTech</span>
          </a>
        </div>
      </div>
    </footer>
  );
}
