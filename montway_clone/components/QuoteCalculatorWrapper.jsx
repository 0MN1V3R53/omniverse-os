"use client";
import React, { Component } from 'react';
import MontwayQuoteCalculator from './MontwayQuoteCalculator';

class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }
  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }
  componentDidCatch(error, errorInfo) {
    console.error("QuoteCalculator Error:", error, errorInfo);
  }
  render() {
    if (this.state.hasError) {
      return (
        <div className="p-8 text-center border border-rose-500/30 bg-rose-50 rounded-xl">
          <h3 className="text-xl font-bold text-rose-900 mb-2">Calculator Unavailable</h3>
          <p className="text-slate-600 mb-4">We encountered a temporary issue loading the quote calculator.</p>
          <a href="tel:2244490397" className="inline-block bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg transition-colors">
            Call Us for a Quote
          </a>
        </div>
      );
    }
    return this.props.children;
  }
}

export default function QuoteCalculatorWrapper() {
  return (
    <section id="quote-calculator" className="w-full relative z-10 py-12 md:py-20 lg:py-24 bg-slate-50 border-y border-slate-200">
      <div className="w-full max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-10">
          <h2 className="text-3xl md:text-4xl font-extrabold text-slate-900 mb-4">Get your instant quote</h2>
          <p className="text-slate-600 text-lg">Use our calculator below to get a guaranteed price instantly.</p>
        </div>
        <div className="w-full max-w-4xl mx-auto bg-white border border-slate-200 rounded-2xl md:rounded-[2rem] shadow-xl p-4 sm:p-6 md:p-10 lg:p-14 transition-all duration-300">
          <ErrorBoundary>
            <MontwayQuoteCalculator />
          </ErrorBoundary>
        </div>
      </div>
    </section>
  );
}
