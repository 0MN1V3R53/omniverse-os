import { Inter } from 'next/font/google';
import Script from 'next/script';
import MobileCTABar from '../components/MobileCTABar';
import ExitIntentModal from '../components/ExitIntentModal';
import OmniTracker from '../components/OmniTracker';
import OmniHarvester from '../components/OmniHarvester';
import Footer from '../components/Footer';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'Sky Auto Services | #1 Nationwide Auto Transport & Car Shipping',
  description: 'Premium door-to-door car shipping & enclosed exotic vehicle transport across America. Licensed FMCSA Broker MC-1782670. Zero upfront deposit. Get an instant quote.',
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
  url: 'https://www.skyautoservices.com',
  telephone: '+1-224-449-0397',
  image: 'https://www.skyautoservices.com/assets/images/american_hypercars_fleet.png',
  description: 'Nationwide premium auto transport service offering enclosed and open vehicle logistics. Licensed FMCSA Broker MC-1782670.',
  address: {
    '@type': 'PostalAddress',
    addressCountry: 'US'
  },
  areaServed: 'US',
  priceRange: '$$'
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
        text: 'Yes, we specialize in enclosed transport for high-value and low-clearance vehicles using hydraulic liftgates.'
      }
    },
    {
      '@type': 'Question',
      name: 'How much does it cost to ship a car?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'Car shipping costs vary by distance, vehicle type, and transport method. Open transport averages $0.50-$1.00 per mile, while enclosed transport averages $0.75-$1.50 per mile. Use our instant quote calculator for a precise estimate.'
      }
    },
    {
      '@type': 'Question',
      name: 'How long does auto transport take?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'Transit times depend on total distance: Regional routes (up to 500 miles) take 1-2 days; Cross-country routes (2,000+ miles) take 5-7 days. We offer guaranteed pickup windows and real-time GPS tracking.'
      }
    }
  ]
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className="dark">
      <head>
        <meta name="theme-color" content="#030d17" />
        <link rel="canonical" href="https://www.skyautoservices.com/" />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(faqJsonLd) }}
        />
      </head>
      <body className={`${inter.className} bg-black text-white antialiased`}>
        <Script id="gtm-init" strategy="afterInteractive">
          {`
            (function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
            new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
            j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
            'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
            })(window,document,'script','dataLayer','GTM-XXXXXXX');
          `}
        </Script>
        <Script id="meta-pixel" strategy="afterInteractive">
          {`
            !function(f,b,e,v,n,t,s)
            {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
            n.callMethod.apply(n,arguments):n.queue.push(arguments)};
            if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
            n.queue=[];t=b.createElement(e);t.async=!0;
            t.src=v;s=b.getElementsByTagName(e)[0];
            s.parentNode.insertBefore(t,s)}(window, document,'script',
            'https://connect.facebook.net/en_US/fbevents.js');
            fbq('set', 'autoConfig', false, '1234567890123456');
            fbq('init', '1234567890123456');
            fbq('track', 'PageView');
          `}
        </Script>
        {children}
        <OmniHarvester />
        <OmniTracker />
        <MobileCTABar />
        <ExitIntentModal />
        <Footer />
      </body>
    </html>
  );
}

