import React from "react";
import fs from "fs";
import path from "path";
import Link from "next/link";
import { newsTeam } from "../../../lib/newsTeam";

// Generate Static Params for all news articles
export async function generateStaticParams() {
  const filePath = path.join(process.cwd(), "public/data/news_articles.json");
  try {
    const fileContents = fs.readFileSync(filePath, "utf8");
    const articles = JSON.parse(fileContents);
    return articles.map((article) => ({
      slug: article.slug,
    }));
  } catch (err) {
    console.error("Error reading articles json", err);
    return [];
  }
}

// Generate SEO Metadata
export async function generateMetadata({ params }) {
  const { slug } = params;
  const filePath = path.join(process.cwd(), "public/data/news_articles.json");
  const fileContents = fs.readFileSync(filePath, "utf8");
  const articles = JSON.parse(fileContents);
  const article = articles.find((a) => a.slug === slug);

  if (!article) return { title: "Not Found" };

  return {
    title: `${article.title} | Sky Auto Transport News`,
    description: article.excerpt,
    openGraph: {
      title: article.title,
      description: article.excerpt,
      images: [article.backgroundImage],
      type: "article",
    },
  };
}

export default function ArticlePage({ params }) {
  const { slug } = params;
  const filePath = path.join(process.cwd(), "public/data/news_articles.json");
  const fileContents = fs.readFileSync(filePath, "utf8");
  const articles = JSON.parse(fileContents);
  const article = articles.find((a) => a.slug === slug);

  if (!article) {
    return <div className="min-h-screen flex items-center justify-center text-2xl font-bold">Article Not Found</div>;
  }

  const author = newsTeam.find((a) => a.id === article.authorId) || newsTeam[0];
  const dateStr = new Date(article.publishedAt).toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" });

  // Generate JSON-LD Schema
  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "NewsArticle",
    "headline": article.title,
    "image": [article.backgroundImage],
    "datePublished": article.publishedAt,
    "author": [{
        "@type": "Person",
        "name": author.name,
        "url": `https://www.skyautoservices.com/author/${author.id}`
      }]
  };

  return (
    <div className="bg-white min-h-screen">
      {/* JSON-LD Script Injection */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />

      {/* Hero Header */}
      <div 
        className="relative min-h-[580px] flex items-end justify-center bg-slate-900 bg-cover bg-center bg-no-repeat bg-fixed pt-36 pb-16 md:pt-44 md:pb-20"
        style={{ backgroundImage: `url(${article.backgroundImage})` }}
      >
        <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-900/70 to-slate-900/40"></div>
        
        {/* Back to News Button (Positioned safely below the fixed header) */}
        <div className="absolute top-36 left-4 sm:left-6 md:top-32 md:left-12 z-30">
          <Link 
            href="/usa-auto-transport-news" 
            className="inline-flex items-center gap-2 text-white bg-slate-900/80 hover:bg-blue-600 border border-white/20 backdrop-blur-md px-4 py-2 rounded-full text-sm font-semibold transition-all duration-300 shadow-xl hover:shadow-blue-500/30 hover:-translate-x-1"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            <span>Back to News</span>
          </Link>
        </div>
        
        <div className="relative z-10 w-full max-w-4xl mx-auto px-6 text-center animate-in fade-in slide-in-from-bottom-8 duration-700">
          <div className="mb-4">
            {article.tags.map(tag => (
              <span key={tag} className="inline-block bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-widest mx-1 mb-2 shadow-md">
                {tag}
              </span>
            ))}
          </div>
          <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-extrabold text-white mb-6 leading-tight drop-shadow-lg">
            {article.title}
          </h1>
          <div className="flex flex-wrap items-center justify-center text-slate-300 gap-4">
            <div className="flex items-center">
                <img src={author.avatar} alt={author.name} className="w-12 h-12 rounded-full border-2 border-slate-400 mr-3 shadow-md object-cover" />
                <div className="text-left">
                    <p className="text-white font-semibold">{author.name}</p>
                    <p className="text-xs text-slate-400">{author.role}</p>
                </div>
            </div>
            <div className="hidden sm:block h-8 w-px bg-slate-600"></div>
            <div className="text-left">
                <p className="text-xs uppercase tracking-wider text-slate-400">Published</p>
                <p className="text-white font-medium text-sm">{dateStr}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content Area */}
      <main className="max-w-4xl mx-auto px-6 py-16">
        
        {/* Article Body */}
        <article className="prose prose-lg md:prose-xl prose-slate max-w-none prose-a:text-blue-600 hover:prose-a:text-blue-500 mb-16" dangerouslySetInnerHTML={{ __html: article.content }}>
        </article>
        
        <hr className="border-slate-200 mb-12" />

        {/* Author Bio Section */}
        <div className="bg-slate-50 rounded-2xl p-8 flex flex-col md:flex-row items-center md:items-start shadow-sm border border-slate-100 mb-12">
          <img src={author.avatar} alt={author.name} className="w-24 h-24 rounded-full border-4 border-white shadow-lg mb-4 md:mb-0 md:mr-6 object-cover" />
          <div className="text-center md:text-left">
            <h3 className="text-2xl font-bold text-slate-900 mb-1">Written by {author.name}</h3>
            <p className="text-blue-600 font-medium mb-3">{author.role} at Sky Auto Services</p>
            <p className="text-slate-600 text-sm leading-relaxed">{author.bio}</p>
          </div>
        </div>

        {/* Call-to-Action & Quick Navigation */}
        <div className="bg-gradient-to-r from-blue-900 to-indigo-950 rounded-3xl p-8 md:p-10 text-white shadow-xl flex flex-col md:flex-row items-center justify-between gap-6 mb-12">
          <div>
            <h3 className="text-2xl font-bold mb-2">Need to Ship Your Vehicle?</h3>
            <p className="text-blue-200 text-sm max-w-lg">Get an instant, transparent auto transport quote backed by our licensed carrier network and zero upfront deposit.</p>
          </div>
          <div className="flex flex-wrap gap-4">
            <Link 
              href="/#quote-calculator" 
              className="bg-blue-500 hover:bg-blue-400 text-white font-bold py-3 px-6 rounded-full transition-all shadow-lg hover:shadow-blue-500/50"
            >
              Calculate Quote
            </Link>
            <Link 
              href="/usa-auto-transport-news" 
              className="bg-white/10 hover:bg-white/20 border border-white/30 text-white font-medium py-3 px-6 rounded-full transition-all"
            >
              &larr; More Articles
            </Link>
          </div>
        </div>

      </main>
    </div>
  );
}
