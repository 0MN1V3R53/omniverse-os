import Script from 'next/script';
import MobileCTABar from '../components/MobileCTABar';
import OmniTracker from '../components/OmniTracker';
import OmniHarvester from '../components/OmniHarvester';
import SecurityGuard from '../components/SecurityGuard';
import Footer from '../components/Footer';
import Navigation from '../components/Navigation';
import './globals.css';

export const metadata = {
  title: 'Sky Auto Services | Nationwide Auto Transport & Car Shipping',
  description: 'Premium door-to-door car shipping & enclosed exotic vehicle transport across America. Licensed FMCSA Broker MC-1782670. $0 deposit. Get your instant quote.',
  keywords: 'enclosed exotic car shipping, luxury vehicle transport, secure supercar shipping, car shipping, auto transport, FMCSA broker, door to door car transport',
  metadataBase: new URL('https://www.skyautoservices.com'),
  alternates: {
    canonical: '/',
  },
  openGraph: {
    title: 'Sky Auto Services | Premium Nationwide Auto Transport',
    description: 'Instant door-to-door vehicle transport quotes. Licensed FMCSA Broker MC-1782670. White-glove enclosed & open car shipping.',
    url: 'https://www.skyautoservices.com',
    siteName: 'Sky Auto Services',
    images: [
      {
        url: 'https://www.skyautoservices.com/assets/images/american_hypercars_fleet.png',
        width: 1200,
        height: 630,
        alt: 'Sky Auto Services – Premium Exotic Car Transport Fleet',
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Sky Auto Services | Premium Nationwide Auto Transport',
    description: 'Instant door-to-door vehicle transport quotes. Licensed FMCSA Broker MC-1782670.',
    images: ['https://www.skyautoservices.com/assets/images/american_hypercars_fleet.png'],
  },
  other: {
    'theme-color': '#030d17',
  },
};

const jsonLd = {
  '@context': 'https://schema.org',
  '@type': 'AutoTransportService',
  name: 'Sky Auto Services',
  legalName: 'Sky Services LLC',
  url: 'https://www.skyautoservices.com',
  telephone: '+1-224-449-0397',
  image: 'https://www.skyautoservices.com/assets/images/american_hypercars_fleet.png',
  description: 'Nationwide premium auto transport service offering enclosed and open vehicle logistics. Licensed FMCSA Broker MC-1782670, USDOT 4504932.',
  address: {
    '@type': 'PostalAddress',
    streetAddress: '3216 N Salk Rd',
    addressLocality: 'Arlington Heights',
    addressRegion: 'IL',
    postalCode: '60004',
    addressCountry: 'US'
  },
  areaServed: {
    '@type': 'Country',
    name: 'United States'
  },
  priceRange: '$$',
  identifier: [
    {
      '@type': 'PropertyValue',
      name: 'FMCSA MC Number',
      value: 'MC-1782670'
    },
    {
      '@type': 'PropertyValue',
      name: 'USDOT Number',
      value: '4504932'
    }
  ],
  aggregateRating: {
    '@type': 'AggregateRating',
    ratingValue: '4.95',
    ratingCount: '1284',
    reviewCount: '1284',
    bestRating: '5',
    worstRating: '1'
  }
};

const faqJsonLd = {
  '@context': 'https://schema.org',
  '@type': 'FAQPage',
  mainEntity: [
    {
      '@type': 'Question',
      name: 'Do you offer enclosed transport for exotic cars?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'Yes, we specialize in enclosed transport for high-value, luxury, and low-clearance vehicles using hydraulic liftgates and soft-tie strapping.'
      }
    },
    {
      '@type': 'Question',
      name: 'How much does it cost to ship a car?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'Car shipping costs vary by distance, vehicle type, and transport method. Open transport averages $0.50-$1.00 per mile, while enclosed transport averages $0.75-$1.50 per mile. Use our instant quote calculator for a 100% price-lock estimate.'
      }
    },
    {
      '@type': 'Question',
      name: 'How long does auto transport take?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'Transit times depend on total distance: Regional routes (up to 500 miles) take 1-2 days; Cross-country routes (2,000+ miles) take 5-7 days. We offer guaranteed pickup windows and 24/7 direct dispatch tracking.'
      }
    },
    {
      '@type': 'Question',
      name: 'Is my vehicle insured during auto transport?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'Yes. Every carrier in our network is thoroughly vetted and carries $100,000 to $1,000,000+ in active primary cargo insurance, with certificate of insurance (COI) verified prior to dispatch.'
      }
    },
    {
      '@type': 'Question',
      name: 'Do you require an upfront deposit?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'No. Sky Auto Services has a strict $0 upfront deposit policy. You pay nothing until your licensed carrier is assigned and scheduled for pickup.'
      }
    }
  ]
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" >
      <head>
        <meta name="theme-color" content="#030d17" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(faqJsonLd) }}
        />
        <Script
          src="https://www.googletagmanager.com/gtag/js?id=AW-18396293415"
          strategy="afterInteractive"
        />
        <Script id="google-tag-init" strategy="afterInteractive">
          {`
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            window.gtag = gtag;
            gtag('js', new Date());
            gtag('config', 'AW-18396293415', {
              page_path: window.location.pathname,
            });
          `}
        </Script>
      </head>
      <body className="font-sans bg-white text-slate-900 antialiased overflow-x-hidden w-full max-w-full">
        <Navigation />
        {children}
        <SecurityGuard />
        <OmniHarvester />
        <OmniTracker />
        <MobileCTABar />
        <Footer />
      </body>
    </html>
  );
}

