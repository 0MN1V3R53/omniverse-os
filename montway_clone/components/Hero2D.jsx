"use client";
import React, { useEffect, useRef } from 'react';
import { gsap } from 'gsap';

export default function Hero2D() {
  const heroRef = useRef(null);
  const titleRef = useRef(null);
  const textRef = useRef(null);
  const bgRef = useRef(null);

  useEffect(() => {
    const ctx = gsap.context(() => {
      // Background slow zoom
      gsap.to(bgRef.current, {
        scale: 1.1,
        duration: 20,
        ease: 'none',
        repeat: -1,
        yoyo: true
      });

      // Text reveal stagger
      gsap.from([titleRef.current, textRef.current], {
        y: 50,
        opacity: 0,
        duration: 1.2,
        stagger: 0.2,
        ease: 'power4.out',
        delay: 0.2
      });
    }, heroRef);

    return () => ctx.revert();
  }, []);

  return (
    <section ref={heroRef} className="relative w-full min-h-[100svh] min-h-screen flex flex-col justify-center overflow-hidden bg-black py-32">
      {/* Background Image — resolves from sky_next/public/assets/images/ */}
      <div 
        ref={bgRef}
        className="absolute inset-0 z-0 opacity-50"
        style={{
          backgroundImage: "url('/assets/images/american_hypercars_fleet.png')",
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          filter: 'brightness(0.6)'
        }}
      >
        <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-black" />
      </div>

      {/* Glow Effect */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[60vw] h-[60vw] rounded-full bg-emerald-500/10 blur-[100px] z-10 pointer-events-none mix-blend-screen animate-pulse duration-1000"></div>

      <div className="relative z-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h1 ref={titleRef} className="text-3xl sm:text-4xl md:text-5xl lg:text-7xl font-extrabold text-white tracking-tight mb-6 break-normal">
          Absolute <br className="sm:hidden" />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-blue-500 inline-block whitespace-nowrap">Liability Shielding.</span>
        </h1>
        <p ref={textRef} className="mt-4 text-base sm:text-lg md:text-xl lg:text-2xl text-gray-300 max-w-3xl mx-auto">
          Zero-friction transport for high-value assets. Build your custom exotic transport protocol in seconds and secure your asset.
        </p>
        
        {/* Trust badges right in hero */}
        <div className="mt-8 sm:mt-10 flex flex-wrap justify-center gap-4 sm:gap-6 opacity-80">
          <div className="flex items-center text-xs sm:text-sm font-semibold text-gray-400">
            <svg className="w-4 h-4 sm:w-5 sm:h-5 text-emerald-400 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"></path></svg>
            Fully Insured Cargo
          </div>
          <div className="flex items-center text-xs sm:text-sm font-semibold text-gray-400">
            <svg className="w-4 h-4 sm:w-5 sm:h-5 text-emerald-400 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 2a4 4 0 00-4 4v1H5a1 1 0 00-.994.89l-1 9A1 1 0 004 18h12a1 1 0 00.994-1.11l-1-9A1 1 0 0015 7h-1V6a4 4 0 00-4-4zm2 5V6a2 2 0 10-4 0v1h4zm-6 3a1 1 0 112 0 1 1 0 01-2 0zm7-1a1 1 0 100 2 1 1 0 000-2z" clipRule="evenodd"></path></svg>
            Enclosed Transport Experts
          </div>
          <div className="flex items-center text-xs sm:text-sm font-semibold text-gray-400">
            <svg className="w-4 h-4 sm:w-5 sm:h-5 text-emerald-400 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 2a4 4 0 00-4 4v1H5a1 1 0 00-.994.89l-1 9A1 1 0 004 18h12a1 1 0 00.994-1.11l-1-9A1 1 0 0015 7h-1V6a4 4 0 00-4-4zm2 5V6a2 2 0 10-4 0v1h4zm-6 3a1 1 0 112 0 1 1 0 01-2 0zm7-1a1 1 0 100 2 1 1 0 000-2z" clipRule="evenodd"></path></svg>
            USDOT: 4504932 | MC: 1782670
          </div>
          <div className="flex items-center text-xs sm:text-sm font-semibold text-gray-400">
            <svg className="w-4 h-4 sm:w-5 sm:h-5 text-emerald-400 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 2a4 4 0 00-4 4v1H5a1 1 0 00-.994.89l-1 9A1 1 0 004 18h12a1 1 0 00.994-1.11l-1-9A1 1 0 0015 7h-1V6a4 4 0 00-4-4zm2 5V6a2 2 0 10-4 0v1h4zm-6 3a1 1 0 112 0 1 1 0 01-2 0zm7-1a1 1 0 100 2 1 1 0 000-2z" clipRule="evenodd"></path></svg>
            Fully Licensed & Bonded Broker
          </div>
        </div>
      </div>
    </section>
  );
}

