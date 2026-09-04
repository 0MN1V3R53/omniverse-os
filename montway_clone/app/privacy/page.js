import Link from 'next/link';

export const metadata = {
  title: 'Privacy Policy | Sky Auto Services',
  description: 'Official Privacy Policy for Sky Auto Services LLC. Learn how we protect your personal and vehicle transport data.',
};

export default function PrivacyPolicy() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 pt-28 pb-20 px-4">
      <div className="max-w-4xl mx-auto bg-slate-900/80 backdrop-blur-xl border border-white/10 rounded-3xl p-8 md:p-12 shadow-2xl">
        <div className="mb-8 border-b border-white/10 pb-6">
          <span className="text-xs font-mono uppercase tracking-widest text-emerald-400 font-semibold bg-emerald-500/10 px-3 py-1 rounded-full border border-emerald-500/20">
            Legal & Compliance
          </span>
          <h1 className="text-3xl md:text-4xl font-bold text-white mt-4 mb-2">
            Privacy Policy
          </h1>
          <p className="text-sm text-slate-400">
            Last Updated & Effective Date: August 2026 · Sky Services LLC (MC-1782670 / USDOT 4504932)
          </p>
        </div>

        <div className="space-y-8 text-slate-300 leading-relaxed text-sm md:text-base">
          <section className="space-y-3">
            <h2 className="text-xl font-semibold text-white">1. Commitment to Privacy</h2>
            <p>
              Sky Services LLC doing business as Sky Auto Services (&quot;Sky Auto Services,&quot; &quot;we,&quot; &quot;us,&quot; or &quot;our&quot;) is committed to protecting your personal information and respecting your privacy. This Privacy Policy details how we collect, utilize, disclose, and safeguard your data when you interact with our website (<Link href="/" className="text-emerald-400 hover:underline">skyautoservices.com</Link>), submit a quote request, or utilize our nationwide auto transport services.
            </p>
          </section>

          <section className="space-y-3">
            <h2 className="text-xl font-semibold text-white">2. Information We Collect</h2>
            <p>To provide accurate door-to-door auto transport rates and execute vehicle shipments, we collect:</p>
            <ul className="list-disc pl-6 space-y-2 text-slate-300">
              <li><strong className="text-white">Contact & Identity Data:</strong> First name, last name, email address, and phone number.</li>
              <li><strong className="text-white">Vehicle Specifications:</strong> Vehicle year, make, model, operable condition, and modifications (lift kits, low clearance).</li>
              <li><strong className="text-white">Route Logistics:</strong> Pickup ZIP code / city, delivery ZIP code / city, and desired shipping timeframes.</li>
              <li><strong className="text-white">Payment & Billing Data:</strong> Payment details processed directly via encrypted PCI-DSS compliant gateways. We do not store raw card numbers.</li>
            </ul>
          </section>

          <section className="space-y-3">
            <h2 className="text-xl font-semibold text-white">3. Purpose and Use of Data</h2>
            <p>We use your personal and shipment information strictly for legitimate commercial purposes:</p>
            <ul className="list-disc pl-6 space-y-2 text-slate-300">
              <li>Generating instant, binding, and estimated auto transport rate quotes.</li>
              <li>Coordinating carrier assignment with vetted, licensed, and insured FMCSA motor carriers.</li>
              <li>Transmitting real-time shipment status, dispatch tracking, and delivery notifications via SMS/email.</li>
              <li>Customer support and regulatory compliance with federal Department of Transportation rules.</li>
            </ul>
          </section>

          <section className="space-y-3">
            <h2 className="text-xl font-semibold text-white">4. Strict Zero Third-Party Sale & Mobile Non-Disclosure Guarantee</h2>
            <div className="bg-emerald-950/40 border border-emerald-500/30 p-5 rounded-xl text-emerald-200 space-y-3">
              <p>
                <strong>We do not sell, rent, or trade your personal information to third-party data brokers or marketing aggregators.</strong> Your contact details are shared only with the assigned carrier and essential dispatch personnel strictly for the fulfillment of your vehicle shipment.
              </p>
              <p className="border-t border-emerald-500/20 pt-3 text-white font-medium">
                <strong>Mobile Information Non-Disclosure Clause:</strong> No mobile information will be shared with third parties or affiliates for marketing or promotional purposes. All other categories exclude text messaging originator opt-in data and consent; this information will not be shared with any third parties.
              </p>
            </div>
          </section>

          <section className="space-y-3">
            <h2 className="text-xl font-semibold text-white">5. SMS / Text Messaging (A2P 10DLC Compliance)</h2>
            <p>
              If you provide your telephone number when submitting a quote request, you consent to receive transactional and informational SMS text messages from Sky Auto Services regarding your quote, vehicle status, and carrier dispatch:
            </p>
            <ul className="list-disc pl-6 space-y-2 text-slate-300">
              <li><strong className="text-white">Opt-In Consent:</strong> Opt-in data and consent for text messaging will not be shared with any third parties.</li>
              <li><strong className="text-white">Message Frequency:</strong> Message frequency varies based on your shipment activity (typically 2–4 messages per quote inquiry).</li>
              <li><strong className="text-white">Rates:</strong> Message and data rates may apply depending on your mobile carrier.</li>
              <li><strong className="text-white">Opt-Out / STOP:</strong> You can cancel SMS messages at any time by replying <strong className="text-white">STOP</strong> to any text. You will receive a one-time confirmation of your unsubscribe status.</li>
              <li><strong className="text-white">Help / Support:</strong> For assistance, reply <strong className="text-white">HELP</strong> or contact our dispatch team directly at (224) 449-0397 or sales@skyservicesllc.com.</li>
            </ul>
          </section>

          <section className="space-y-3">
            <h2 className="text-xl font-semibold text-white">6. Security and Data Protection</h2>
            <p>
              We implement industry-grade technical and organizational safeguards, including SSL/TLS 256-bit encryption, strict access controls, and regular vulnerability audits to prevent unauthorized data access, loss, or alteration.
            </p>
          </section>

          <section className="space-y-3">
            <h2 className="text-xl font-semibold text-white">7. Contact &amp; Data Officer</h2>
            <p>
              If you have any questions or wish to request data deletion, contact our compliance team:
            </p>
            <div className="bg-white/5 border border-white/10 rounded-xl p-4 text-slate-300 space-y-1 font-mono text-xs md:text-sm">
              <p><strong className="text-white">Entity:</strong> Sky Services LLC</p>
              <p><strong className="text-white">Address:</strong> 1004 Sycamore Dr, Streamwood, IL 60107, USA</p>
              <p><strong className="text-white">Dispatch Phone:</strong> (224) 449-0397 / (224) 310-1830</p>
              <p><strong className="text-white">Email:</strong> sales@skyservicesllc.com</p>
            </div>
          </section>
        </div>

        <div className="mt-10 pt-6 border-t border-white/10 flex flex-wrap justify-between items-center gap-4">
          <Link href="/" className="inline-flex items-center gap-2 text-sm text-emerald-400 hover:text-emerald-300 font-semibold transition">
            ← Return to Instant Quote Calculator
          </Link>
          <Link href="/terms" className="text-xs text-slate-400 hover:text-white transition">
            View Terms of Service →
          </Link>
        </div>
      </div>
    </main>
  );
}
