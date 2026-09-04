# CONTEXT 14: FULLSTACK WEB, SEO & E-COMMERCE ARCHITECTURE

## 1. Modern Full-Stack Web Architecture
- **Frameworks**: Next.js 15 (App Router, Server Components, Server Actions), React 19, Vue 3 / Nuxt 3, Vite, Astro, Tailwind CSS v4, Radix UI.
- **Rendering Strategies**:
  - Incremental Static Regeneration (ISR) for high-traffic product/content catalogs.
  - Edge Server-Side Rendering (SSR) for personalized checkouts, dashboards, and geo-routed pages.
- **State Management & Data Fetching**: Zustand, TanStack React Query, SWR, Server Actions with Zod runtime schema validation.

---

## 2. Enterprise Technical SEO & Programmatic Scaling
- **Crawl Budget & URL Architecture**:
  - Strict hierarchical canonicalization avoiding duplicate query-parameter indexing.
  - Multi-tier dynamic XML sitemaps partitioned by category/index with `<lastmod>` validation.
  - Cloudflare edge worker crawler detection and bot management.
- **Structured Data & Semantic Entities (JSON-LD)**:
  - Automated injection of rich Schema.org entities: `Organization`, `WebSite`, `Product`, `Offer`, `AggregateRating`, `FAQPage`, `BreadcrumbList`, `LocalBusiness`.
  - Semantic entity clustering and topical authority silos to dominate Google Search engine results.
- **Core Web Vitals Enforcement**:
  - **LCP (Largest Contentful Paint)**: $< 2.0\text{s}$ via `fetchpriority="high"`, AVIF/WebP responsive images, and critical CSS inlining.
  - **INP (Interaction to Next Paint)**: $< 150\text{ms}$ via UI main-thread decoupling, Web Workers, and non-blocking event handlers.
  - **CLS (Cumulative Layout Shift)**: $< 0.05$ via explicit image aspect ratios and skeleton layout containers.

---

## 3. E-Commerce, Payment Gateways & Ledger Invariants
- **Payment Processing**:
  - Stripe API (Payment Intents, Setup Intents, Customer Sessions, Stripe Elements).
  - Multi-gateway fallback (PayPal, Adyen, Apple Pay, Google Pay).
  - Idempotent webhook ingestion with cryptographic signature validation (`stripe-signature`) and replay protection.
- **Transactional Ledger Invariants**:
  - Double-entry balance reconciliation for merchant payouts, refund reserves, and processing fees.
  - Integer minor-currency representation (cents, pence, satoshis) across all pricing calculators and invoice generators.
- **Security & Compliance**:
  - PCI-DSS Level 1 compliance guidelines: Zero storage of unmasked PANs or CVVs.
  - CSRF tokens, strict Content Security Policy (CSP), and Rate Limiting (Token Bucket algorithm via Redis).
