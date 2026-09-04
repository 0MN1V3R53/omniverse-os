import MontwayMarketingSections from '@/components/MontwayMarketingSections';
import QuoteCalculatorWrapper from '@/components/QuoteCalculatorWrapper';

export const metadata = {
  title: 'About Sky Auto Services | Elite Auto Transport Network',
  description: 'Learn about Sky Auto Services, the premier nationwide exotic and luxury car shipping logistics network. Fully insured, FMCSA licensed.',
};

export default function AboutPage() {
  return (
    <main className="min-h-screen bg-white">
      <div className="pt-32 pb-16 md:pt-40 md:pb-24 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-6xl font-bold text-slate-900 mb-6">
            About <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400">Sky Auto Services</span>
          </h1>
          <p className="text-xl text-slate-600 max-w-3xl mx-auto leading-relaxed">
            We are more than just a car shipping company. We are a logistics network dedicated to the safe, secure, and timely delivery of the world&apos;s most valuable vehicles.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center mb-24">
          <div className="relative rounded-2xl overflow-hidden border border-slate-200 shadow-2xl h-96">
            <div className="absolute inset-0 bg-gradient-to-tr from-blue-600/20 to-emerald-600/20"></div>
            <img 
              src="/assets/images/american_hypercars_fleet.webp" 
              alt="Sky Auto Services Premium Fleet" 
              className="w-full h-full object-cover opacity-90"
              loading="lazy"
              width="800"
              height="600"
            />
          </div>
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 text-blue-700 text-xs font-semibold uppercase tracking-wider mb-4">
              Headquartered in Arlington Heights, IL
            </div>
            <h2 className="text-3xl font-bold text-slate-900 mb-6">Our Mission & Company Background</h2>
            <p className="text-slate-600 mb-4 text-base leading-relaxed">
              Founded on the principles of transparency, reliability, and precision engineering logistics, Sky Auto Services operates as a licensed nationwide freight brokerage (MC-1782670, USDOT 4504932).
            </p>
            <p className="text-slate-600 mb-6 text-base leading-relaxed">
              We provide white-glove, zero-stress auto transport for dealerships, collectors, and everyday drivers alike. By leveraging state-of-the-art enclosed trailers and rigorous carrier vetting, we eliminate the risks traditionally associated with moving high-value assets.
            </p>
            <ul className="space-y-3">
              <li className="flex items-center text-slate-700 text-sm font-medium">
                <svg className="w-5 h-5 text-emerald-500 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                Licensed FMCSA Property Broker (MC-1782670 • USDOT 4504932)
              </li>
              <li className="flex items-center text-slate-700 text-sm font-medium">
                <svg className="w-5 h-5 text-emerald-500 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                $100K - $1M+ Active Primary Cargo Insurance Verification
              </li>
              <li className="flex items-center text-slate-700 text-sm font-medium">
                <svg className="w-5 h-5 text-emerald-500 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                $0 Upfront Deposit • Pay Only When Carrier Is Dispatched
              </li>
              <li className="flex items-center text-slate-700 text-sm font-medium">
                <svg className="w-5 h-5 text-emerald-500 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                24/7 Dedicated Logistics Advisors & Direct Driver Updates
              </li>
            </ul>
          </div>
        </div>
      </div>
      <QuoteCalculatorWrapper />
      <MontwayMarketingSections />
    </main>
  );
}
