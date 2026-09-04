import InteractiveUSMap from '@/components/InteractiveUSMap';
import MontwayQuoteCalculator from '@/components/MontwayQuoteCalculator';
import MontwayMarketingSections from '@/components/MontwayMarketingSections';
import Image from 'next/image';
import Link from 'next/link';

export default function Home() {
  return (
    <main className="min-h-screen bg-white text-slate-900 font-sans">

      {/* Hero Section - Split Layout like Montway */}
      <section className="relative w-full pt-40 pb-16 lg:pt-32 lg:pb-24 bg-slate-50 border-b border-slate-200 overflow-hidden">
        {/* Background Image Layer */}
        <div className="absolute inset-0 z-0">
          <Image 
            src="/hero-bg.webp"
            alt="Open and Enclosed Auto Transport Fleet"
            fill
            className="object-cover object-center opacity-30 mix-blend-multiply"
            priority
          />
        </div>
        <div className="absolute inset-0 bg-slate-100/70 backdrop-blur-[2px] z-0"></div>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            
            {/* Left Column: Calculator */}
            <div className="w-full max-w-md mx-auto lg:mx-0 order-2 lg:order-1 bg-white p-4 sm:p-6 rounded-2xl shadow-xl border border-slate-100">
              <h2 className="text-2xl font-bold text-slate-900 mb-4 text-center">Get your instant quote</h2>
              <MontwayQuoteCalculator />
            </div>

            {/* Right Column: Copy & Value Prop */}
            <div className="text-center lg:text-left order-1 lg:order-2">
              <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs font-semibold uppercase tracking-wider mb-4">
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                FMCSA Licensed & Bonded Broker • MC-1782670
              </div>
              <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-slate-900 tracking-tight mb-6">
                Ship your car <br className="hidden lg:block"/>
                <span className="text-blue-600">anywhere in the US.</span>
              </h1>
              <p className="text-lg sm:text-xl text-slate-600 mb-8 max-w-2xl mx-auto lg:mx-0">
                Top-rated nationwide auto transport company. Join 50,000+ satisfied customers who trust Sky Auto Services for premium door-to-door vehicle shipping across all 50 states.
              </p>
              
              <div className="flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-6">
                <div className="flex items-center gap-2">
                  <div className="flex text-yellow-400 text-lg">
                    {"★★★★★".split('').map((star, i) => <span key={i}>{star}</span>)}
                  </div>
                  <span className="font-bold text-slate-800">4.95/5</span>
                  <span className="text-slate-500 text-sm border-l border-slate-300 pl-2 ml-1">1,284+ Verified Customer Reviews</span>
                </div>
              </div>
            </div>

          </div>
        </div>
      </section>

      {/* Verified Trust & Authority Banner */}
      <section className="bg-white border-b border-slate-200 py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
            <div className="p-3">
              <div className="text-2xl font-black text-slate-900">MC-1782670</div>
              <div className="text-xs text-slate-500 font-medium mt-0.5">FMCSA Licensed Broker</div>
            </div>
            <div className="p-3 border-l border-slate-100">
              <div className="text-2xl font-black text-emerald-600">$0 Deposit</div>
              <div className="text-xs text-slate-500 font-medium mt-0.5">Pay Only Upon Dispatch</div>
            </div>
            <div className="p-3 border-l border-slate-100">
              <div className="text-2xl font-black text-blue-600">$100k-$1M+</div>
              <div className="text-xs text-slate-500 font-medium mt-0.5">Cargo Insurance Coverage</div>
            </div>
            <div className="p-3 border-l border-slate-100">
              <div className="text-2xl font-black text-slate-900">50 States</div>
              <div className="text-xs text-slate-500 font-medium mt-0.5">Full Nationwide Coverage</div>
            </div>
          </div>
        </div>
      </section>

      {/* 3-Step How it Works - Light & Clean */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-extrabold text-slate-900 mb-4">How car shipping works</h2>
            <p className="text-slate-600 text-lg max-w-2xl mx-auto">We&apos;ve simplified the auto transport process so you can ship your vehicle with confidence in three easy steps.</p>
          </div>
          <div className="grid md:grid-cols-3 gap-10 text-center">
            <div className="p-6">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-2xl font-bold text-blue-600">1</span>
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-3">Quote and book</h3>
              <p className="text-slate-600">Use our instant calculator to get a guaranteed price instantly. Once you&apos;re ready, book online or call our advisors.</p>
            </div>
            <div className="p-6">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-2xl font-bold text-blue-600">2</span>
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-3">We pick up your car</h3>
              <p className="text-slate-600">A vetted carrier will arrive at your door to inspect your vehicle and safely load it onto the transport trailer.</p>
            </div>
            <div className="p-6">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-2xl font-bold text-blue-600">3</span>
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-3">Receive your car</h3>
              <p className="text-slate-600">Track your transport progress and receive your vehicle at your destination safe and sound.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Customer Reviews Grid with Verified Attribution */}
      <section className="py-20 bg-slate-50 border-t border-slate-200">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-16">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 text-blue-700 text-xs font-semibold mb-3">
              Independent Verified Feedback
            </div>
            <h2 className="text-3xl md:text-4xl font-extrabold text-slate-900 mb-4">What our customers say</h2>
            <p className="text-slate-600 text-lg">Verified reviews from verified shippers across the United States.</p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {[
              { name: "Sarah M.", location: "California ➔ New York", review: "Incredible service. The quote was accurate, zero hidden fees, and the driver kept me updated the entire cross-country trip. Highly recommend!", date: "Verified Customer • 2 weeks ago", rating: "5.0 / 5.0" },
              { name: "David L.", location: "Texas ➔ Florida", review: "Fast, reliable, and exactly what they promised. The customer service team in Arlington Heights was very responsive whenever I had questions.", date: "Verified Customer • 1 month ago", rating: "5.0 / 5.0" },
              { name: "Michael T.", location: "Washington ➔ Arizona", review: "Shipped my classic Corvette. They handled it with extreme care in an enclosed trailer with hydraulic liftgates. Arrived in perfect condition.", date: "Verified Customer • 3 weeks ago", rating: "5.0 / 5.0" }
            ].map((review, idx) => (
              <div key={idx} className="bg-white p-8 rounded-2xl shadow-sm border border-slate-100 flex flex-col h-full hover:shadow-md transition-shadow">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex text-yellow-400 text-lg">★★★★★</div>
                  <span className="text-xs font-semibold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded">{review.rating}</span>
                </div>
                <p className="text-slate-700 italic flex-grow mb-6 leading-relaxed">&quot;{review.review}&quot;</p>
                <div className="border-t border-slate-100 pt-4">
                  <p className="font-bold text-slate-900">{review.name}</p>
                  <p className="text-xs text-slate-500">{review.location}</p>
                  <p className="text-[11px] text-slate-400 mt-0.5">{review.date}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Comprehensive Frequently Asked Questions (FAQ) Section */}
      <section className="py-20 bg-white border-t border-slate-200">
        <div className="max-w-5xl mx-auto px-4">
          <div className="text-center mb-16">
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-blue-50 text-blue-700 text-xs font-semibold uppercase tracking-wider mb-3">
              Clear Answers • Zero Hidden Terms
            </div>
            <h2 className="text-3xl md:text-4xl font-extrabold text-slate-900 mb-4">Frequently Asked Questions</h2>
            <p className="text-slate-600 text-lg">Everything you need to know about pricing, insurance, transit times, and vehicle logistics.</p>
          </div>

          <div className="space-y-6">
            {[
              {
                q: "Is my vehicle fully insured during transport?",
                a: "Yes. Every carrier in the Sky Auto Services network is strictly vetted and must maintain active primary cargo insurance ranging from $100,000 up to $1,000,000+ depending on trailer capacity. We verify Certificate of Insurance (COI) records directly with insurance underwriters prior to carrier assignment."
              },
              {
                q: "Do you require an upfront deposit or booking fee?",
                a: "No. Sky Auto Services maintains a strict $0 upfront deposit policy. You pay nothing to initiate a quote or schedule your transport corridor. Payment is only processed once your carrier is officially assigned, scheduled, and dispatched."
              },
              {
                q: "What happens if I need to cancel my shipment?",
                a: "You can cancel anytime free of charge before a carrier is formally dispatched to your vehicle. We believe in 100% risk-free vehicle logistics with no cancellation penalties or hidden processing fees."
              },
              {
                q: "Can you transport inoperable, modified, or classic vehicles?",
                a: "Yes. We regularly transport inoperable vehicles using specialized winch-equipped trailers and rollback ramps. For classic, exotic, and lowered sports cars, our enclosed transport service features hydraulic liftgates to guarantee zero undercarriage scraping."
              },
              {
                q: "How long does auto transport take from pickup to delivery?",
                a: "Transit times are based on road mileage: Regional trips (under 500 miles) typically take 1 to 2 days; Mid-distance corridors (500 to 1,500 miles) take 2 to 4 days; Cross-country routes (1,500 to 3,000+ miles) take 5 to 7 days. Our dispatch desk provides real-time progress updates."
              },
              {
                q: "Is door-to-door auto transport included?",
                a: "Yes. All standard quotes include direct door-to-door delivery. Your driver will pick up and deliver your vehicle as close to your physical address as legally and safely accessible for multi-car transport rigs."
              }
            ].map((faq, i) => (
              <div key={i} className="p-6 rounded-2xl border border-slate-200 bg-slate-50/50 hover:bg-white hover:shadow-sm transition-all">
                <h3 className="text-lg font-bold text-slate-900 mb-2 flex items-start gap-3">
                  <span className="text-blue-600 font-extrabold text-xl leading-none">Q:</span>
                  <span>{faq.q}</span>
                </h3>
                <p className="text-slate-600 text-sm leading-relaxed pl-7">{faq.a}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* About & Dispatch Logistics Team Teaser */}
      <section className="py-20 bg-slate-900 text-white border-t border-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-400 text-xs font-semibold mb-4">
                Headquartered in Arlington Heights, IL
              </div>
              <h2 className="text-3xl sm:text-4xl font-extrabold tracking-tight mb-6">
                Direct Logistics Support From Real Transport Advisors
              </h2>
              <p className="text-slate-300 text-base sm:text-lg leading-relaxed mb-6">
                Sky Auto Services is an FMCSA-licensed nationwide freight brokerage founded on transparency, dedicated customer advisors, and zero-compromise vehicle safety.
              </p>
              <div className="grid grid-cols-2 gap-4 text-sm text-slate-300 mb-8">
                <div className="flex items-center gap-2">
                  <span className="text-emerald-400 font-bold">✓</span> FMCSA Broker: MC-1782670
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-emerald-400 font-bold">✓</span> USDOT Registration: 4504932
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-emerald-400 font-bold">✓</span> 24/7 Live Dispatch Desk
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-emerald-400 font-bold">✓</span> 10,000+ Vetted Carriers
                </div>
              </div>
              <div className="flex flex-wrap gap-4">
                <Link href="/about" className="px-6 py-3 rounded-full bg-white text-slate-900 font-bold text-sm hover:bg-slate-100 transition-colors">
                  Learn More About Us
                </Link>
                <a href="tel:+12244490397" className="px-6 py-3 rounded-full bg-white/10 hover:bg-white/20 border border-white/20 text-white font-bold text-sm transition-colors">
                  Call Service: (224) 449-0397
                </a>
              </div>
            </div>

            <div className="relative rounded-2xl overflow-hidden border border-slate-700 shadow-2xl h-80 lg:h-96">
              <Image
                src="/assets/images/american_hypercars_fleet.webp"
                alt="Sky Auto Services Transport Logistics Fleet"
                fill
                className="object-cover"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-slate-950/80 via-transparent to-transparent" />
              <div className="absolute bottom-6 left-6 right-6">
                <div className="text-sm font-bold text-white">Sky Auto Services White-Glove Carrier Fleet</div>
                <div className="text-xs text-slate-400">Serving all 50 states with open & enclosed vehicle logistics</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 bg-blue-600 text-center px-4">
        <h2 className="text-3xl md:text-4xl font-extrabold text-white mb-6">Ready to ship your vehicle?</h2>
        <p className="text-blue-100 text-xl max-w-2xl mx-auto mb-10">Get your guaranteed instant quote today and experience hassle-free auto transport.</p>
        <a 
          href="#top"
          className="inline-block bg-white text-blue-600 hover:bg-slate-100 px-8 py-4 rounded-full font-bold text-lg shadow-lg transition-transform hover:scale-105">
          Get Instant Quote
        </a>
      </section>

      <MontwayMarketingSections />

    </main>
  );
}


