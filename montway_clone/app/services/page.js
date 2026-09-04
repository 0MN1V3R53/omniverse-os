import MontwayMarketingSections from '@/components/MontwayMarketingSections';
import QuoteCalculatorWrapper from '@/components/QuoteCalculatorWrapper';

export const metadata = {
  title: 'Our Services | Sky Auto Services',
  description: 'Explore our premium auto transport services: Enclosed shipping, exotic car logistics, and nationwide door-to-door delivery.',
};

export default function ServicesPage() {
  const services = [
    {
      title: 'Enclosed Auto Transport',
      description: 'Maximum protection for exotics, classics, and high-value vehicles. Hard-sided trailers with hydraulic liftgates ensure zero exposure to the elements and road debris.',
      icon: (
        <svg className="w-8 h-8 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path></svg>
      )
    },
    {
      title: 'Open Auto Transport',
      description: 'The industry standard for daily drivers and standard vehicles. Cost-effective, reliable, and fast door-to-door delivery across all 50 states.',
      icon: (
        <svg className="w-8 h-8 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"></path></svg>
      )
    },
    {
      title: 'Exotic & Hypercar Logistics',
      description: 'Specialized low-clearance handling. Our drivers are trained in maneuvering high-horsepower, low-ground-clearance hypercars safely onto flatbeds and enclosed carriers.',
      icon: (
        <svg className="w-8 h-8 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
      )
    }
  ];

  return (
    <main className="min-h-screen bg-white">
      <div className="pt-32 pb-16 md:pt-40 md:pb-24 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="text-center mb-20">
          <h1 className="text-4xl md:text-6xl font-bold text-slate-900 mb-6">
            Premium <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400">Transport Services</span>
          </h1>
          <p className="text-xl text-slate-600 max-w-3xl mx-auto">
            From vintage classics to modern hypercars, we provide tailored logistics solutions to meet the exact requirements of your vehicle.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {services.map((service, idx) => (
            <div key={idx} className="bg-white/50 backdrop-blur-md border border-slate-200 rounded-2xl p-8 hover:border-emerald-500/50 transition-colors duration-300">
              <div className="bg-white/50 w-16 h-16 rounded-xl flex items-center justify-center mb-6 border border-slate-100">
                {service.icon}
              </div>
              <h2 className="text-2xl font-bold text-slate-900 mb-4">{service.title}</h2>
              <p className="text-slate-600 leading-relaxed">
                {service.description}
              </p>
            </div>
          ))}
        </div>
      </div>
          <QuoteCalculatorWrapper />
      <MontwayMarketingSections />
    </main>
  );
}
