import Link from 'next/link';

export const metadata = {
  title: 'Terms of Service | Sky Auto Services',
  description: 'Terms of Service and Brokerage Agreement for Sky Auto Services LLC (MC-1782670 / USDOT 4504932).',
};

export default function TermsOfService() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 pt-28 pb-20 px-4">
      <div className="max-w-4xl mx-auto bg-slate-900/80 backdrop-blur-xl border border-white/10 rounded-3xl p-8 md:p-12 shadow-2xl">
        <div className="mb-8 border-b border-white/10 pb-6">
          <span className="text-xs font-mono uppercase tracking-widest text-blue-400 font-semibold bg-blue-500/10 px-3 py-1 rounded-full border border-blue-500/20">
            Terms of Service & Broker Agreement
          </span>
          <h1 className="text-3xl md:text-4xl font-bold text-white mt-4 mb-2">
            Terms of Service
          </h1>
          <p className="text-sm text-slate-400">
            Effective Date: August 2026 · Sky Services LLC (MC-1782670 / USDOT 4504932)
          </p>
        </div>

        <div className="space-y-8 text-slate-300 leading-relaxed text-sm md:text-base">
          <section className="space-y-3">
            <h2 className="text-xl font-semibold text-white">1. Service Agreement</h2>
            <p>
              Sky Services LLC acts as a licensed and bonded property broker registered with the Federal Motor Carrier Safety Administration (FMCSA) under MC-1782670 and USDOT 4504932. By submitting a quote request or booking an auto transport order, you authorize Sky Auto Services to act as your representative in arranging vehicle transportation with fully insured motor carriers.
            </p>
          </section>

          <section className="space-y-3">
            <h2 className="text-xl font-semibold text-white">2. $0 Upfront Deposit Policy</h2>
            <p>
              We do not charge any upfront booking deposit. Payment is authorized and collected only after a vetted carrier has been officially scheduled and dispatched to pick up your vehicle.
            </p>
          </section>

          <section className="space-y-3">
            <h2 className="text-xl font-semibold text-white">3. Insurance & Carrier Liability</h2>
            <p>
              All assigned motor carriers maintain active commercial auto haul insurance policies up to $1,000,000. Prior to loading, a joint vehicle inspection must be conducted and documented on the official Bill of Lading (BOL). The assigned carrier is primarily liable for transit claims.
            </p>
          </section>

          <section className="space-y-3">
            <h2 className="text-xl font-semibold text-white">4. Cancellation & Order Changes</h2>
            <p>
              Orders may be cancelled at any time prior to carrier assignment with zero penalty. If a cancellation occurs after carrier dispatch, standard logistical dispatch fees may apply.
            </p>
          </section>

          <section className="space-y-3">
            <h2 className="text-xl font-semibold text-white">5. SMS Terms of Service</h2>
            <p className="bg-white/5 border border-white/10 rounded-xl p-4 text-slate-200">
              By opting into SMS from a web form or other medium, you are agreeing to receive SMS messages from <strong>SKY SERVICES LLC</strong>. This includes SMS messages for conversations (external). Message frequency varies. Message and data rates may apply. See privacy policy at <a href="https://www.skyautoservices.com/privacy" className="text-blue-400 underline font-semibold hover:text-blue-300">https://www.skyautoservices.com/privacy.html</a>. Message <strong>HELP</strong> for help. Reply <strong>STOP</strong> to any message to opt out.
            </p>
            <ul className="list-disc pl-6 space-y-2 text-slate-300">
              <li><strong className="text-white">Message Frequency:</strong> Message frequency varies based on transaction status and transport inquiry (approx. 2–4 messages per quote/order inquiry).</li>
              <li><strong className="text-white">Message &amp; Data Rates:</strong> Standard message and data rates may apply depending on your wireless carrier.</li>
              <li><strong className="text-white">Opt-Out / STOP:</strong> You can unsubscribe from SMS notifications at any time by texting <strong className="text-white">STOP</strong> to any message. You will receive a single confirmation message verifying your opt-out.</li>
              <li><strong className="text-white">Customer Assistance:</strong> For support, text <strong className="text-white">HELP</strong> or contact our dispatch desk at (224) 449-0397 or sales@skyservicesllc.com.</li>
              <li><strong className="text-white">Carrier Liability:</strong> Mobile carriers are not liable for delayed or undelivered messages.</li>
            </ul>
          </section>

          <section className="space-y-3">
            <h2 className="text-xl font-semibold text-white">6. Contact Information</h2>
            <div className="bg-white/5 border border-white/10 rounded-xl p-4 text-slate-300 space-y-1 font-mono text-xs md:text-sm">
              <p><strong className="text-white">Corporate Entity:</strong> Sky Services LLC</p>
              <p><strong className="text-white">Address:</strong> 1004 Sycamore Dr, Streamwood, IL 60107, USA</p>
              <p><strong className="text-white">Dispatch Phone:</strong> (224) 449-0397</p>
              <p><strong className="text-white">Email:</strong> sales@skyservicesllc.com</p>
            </div>
          </section>
        </div>

        <div className="mt-10 pt-6 border-t border-white/10 flex flex-wrap justify-between items-center gap-4">
          <Link href="/" className="inline-flex items-center gap-2 text-sm text-blue-400 hover:text-blue-300 font-semibold transition">
            ← Return to Instant Quote Calculator
          </Link>
          <Link href="/privacy" className="text-xs text-slate-400 hover:text-white transition">
            View Privacy Policy →
          </Link>
        </div>
      </div>
    </main>
  );
}
