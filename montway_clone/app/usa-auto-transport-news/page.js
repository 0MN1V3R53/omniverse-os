"use client";
import React, { useState, useEffect, useMemo } from "react";
import Link from "next/link";
import { newsTeam } from "../../lib/newsTeam";

const ITEMS_PER_PAGE = 12;

export default function UsaAutoTransportNews() {
  const [allArticles, setAllArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  
  // Filters & Pagination
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedTag, setSelectedTag] = useState("All");
  const [currentPage, setCurrentPage] = useState(1);

  useEffect(() => {
    fetch(`/data/news_articles.json?t=${new Date().getTime()}`)
      .then((res) => res.json())
      .then((data) => {
        setAllArticles(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error loading articles:", err);
        setLoading(false);
      });
  }, []);

  // Derived Tags
  const availableTags = useMemo(() => {
    if (!allArticles.length) return ["All"];
    const tags = new Set();
    allArticles.forEach(a => {
      if (a.tags) a.tags.forEach(t => tags.add(t));
    });
    return ["All", ...Array.from(tags).slice(0, 7)];
  }, [allArticles]);

  // Derived Filtered Articles
  const filteredArticles = useMemo(() => {
    return allArticles.filter(article => {
      const matchesSearch = article.title.toLowerCase().includes(searchQuery.toLowerCase()) || 
                            article.excerpt.toLowerCase().includes(searchQuery.toLowerCase());
      const matchesTag = selectedTag === "All" || (article.tags && article.tags.includes(selectedTag));
      return matchesSearch && matchesTag;
    });
  }, [allArticles, searchQuery, selectedTag]);

  // Derived Display Articles
  const isDefaultView = currentPage === 1 && !searchQuery && selectedTag === "All";
  const featuredArticle = isDefaultView ? filteredArticles[0] : null;
  
  const gridArticlesSource = isDefaultView ? filteredArticles.slice(1) : filteredArticles;
  const totalPages = Math.ceil(gridArticlesSource.length / ITEMS_PER_PAGE);
  
  const paginatedArticles = useMemo(() => {
    const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
    return gridArticlesSource.slice(startIndex, startIndex + ITEMS_PER_PAGE);
  }, [gridArticlesSource, currentPage]);

  // Handlers
  const handleSearch = (e) => {
    setSearchQuery(e.target.value);
    setCurrentPage(1);
  };

  const handleTagClick = (tag) => {
    setSelectedTag(tag);
    setCurrentPage(1);
  };

  const handlePageChange = (newPage) => {
    if (newPage >= 1 && newPage <= totalPages) {
      setCurrentPage(newPage);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
  };

  const getAuthor = (id) => {
    return newsTeam.find(a => a.id === id) || newsTeam[0];
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 pt-32 pb-24 px-6">
        <div className="max-w-7xl mx-auto">
          {/* Skeleton Hero */}
          <div className="w-full h-64 md:h-96 bg-slate-200 animate-pulse rounded-3xl mb-12"></div>
          {/* Skeleton Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[1, 2, 3, 4, 5, 6].map(i => (
              <div key={i} className="bg-white rounded-2xl h-96 shadow-sm border border-slate-100 p-6 flex flex-col">
                <div className="w-full h-48 bg-slate-200 animate-pulse rounded-xl mb-4"></div>
                <div className="w-3/4 h-6 bg-slate-200 animate-pulse rounded mb-2"></div>
                <div className="w-full h-4 bg-slate-200 animate-pulse rounded mb-2"></div>
                <div className="w-5/6 h-4 bg-slate-200 animate-pulse rounded mt-auto"></div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 pt-24 pb-24 font-sans text-slate-900">
      
      {/* Header & Controls Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-12 mt-8">
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-8 mb-10">
          <div>
            <h1 className="text-5xl md:text-6xl font-black tracking-tight text-slate-900 mb-4">
              Industry <span className="text-blue-600">News</span>
            </h1>
            <p className="text-lg text-slate-600 max-w-2xl">
              The nation&apos;s most trusted source for auto transport routes, logistics insights, and industry updates.
            </p>
          </div>
          
          {/* Search Bar (Glassmorphism) */}
          <div className="w-full md:w-96 relative group">
            <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <svg className="h-5 w-5 text-slate-400 group-focus-within:text-blue-500 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <input
              type="text"
              placeholder="Search articles..."
              value={searchQuery}
              onChange={handleSearch}
              className="w-full pl-11 pr-4 py-3.5 bg-white/70 backdrop-blur-md border border-slate-200 rounded-2xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
            />
          </div>
        </div>

        {/* Filter Chips */}
        <div className="flex flex-wrap gap-2 mb-8">
          {availableTags.map(tag => (
            <button
              key={tag}
              onClick={() => handleTagClick(tag)}
              className={`px-4 py-2 rounded-full text-sm font-semibold transition-all duration-300 ${
                selectedTag === tag 
                  ? "bg-slate-900 text-white shadow-md transform scale-105" 
                  : "bg-white text-slate-600 hover:bg-slate-100 border border-slate-200"
              }`}
            >
              {tag}
            </button>
          ))}
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Featured Hero Article */}
        {featuredArticle && (
          <Link href={`/usa-auto-transport-news/${featuredArticle.slug}`}>
            <div className="group relative w-full h-[500px] md:h-[600px] rounded-[2rem] overflow-hidden mb-16 shadow-2xl cursor-pointer">
              <img 
                src={featuredArticle.backgroundImage} 
                alt={featuredArticle.title}
                className="absolute inset-0 w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-1000 ease-out"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-slate-900/90 via-slate-900/40 to-transparent"></div>
              
              <div className="absolute bottom-0 left-0 w-full p-8 md:p-12">
                <div className="inline-block bg-blue-600 text-white text-xs font-bold px-4 py-1.5 rounded-full uppercase tracking-wider mb-4 shadow-lg">
                  Featured {featuredArticle.tags && `• ${featuredArticle.tags[0]}`}
                </div>
                <h2 className="text-3xl md:text-5xl font-bold text-white mb-4 leading-tight group-hover:text-blue-300 transition-colors">
                  {featuredArticle.title}
                </h2>
                <p className="text-lg text-slate-200 max-w-3xl mb-6 line-clamp-2">
                  {featuredArticle.excerpt}
                </p>
                <div className="flex items-center">
                  <img src={getAuthor(featuredArticle.authorId).avatar} alt="Author" className="w-12 h-12 rounded-full border-2 border-white/50 mr-4 shadow-md" />
                  <div>
                    <p className="text-white font-semibold">{getAuthor(featuredArticle.authorId).name}</p>
                    <p className="text-slate-300 text-sm">{formatDate(featuredArticle.publishedAt)}</p>
                  </div>
                </div>
              </div>
            </div>
          </Link>
        )}

        {/* Dynamic CSS Grid for Remaining Articles */}
        {paginatedArticles.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-8 gap-y-12">
            {paginatedArticles.map((article, idx) => {
              const author = getAuthor(article.authorId);
              return (
                <Link href={`/usa-auto-transport-news/${article.slug}`} key={article.id}>
                  <div className="group flex flex-col h-full cursor-pointer">
                    {/* Image Container with Overflow Hidden */}
                    <div className="relative h-64 rounded-3xl overflow-hidden mb-6 shadow-md shadow-slate-200/50">
                      <img 
                        src={article.backgroundImage} 
                        alt={article.title}
                        className="w-full h-full object-cover transform group-hover:scale-110 transition-transform duration-700 ease-out"
                        loading="lazy"
                        width="400"
                        height="260"
                      />
                      {article.tags && article.tags[0] && (
                        <div className="absolute top-4 left-4 bg-white/90 backdrop-blur-sm text-slate-900 text-xs font-bold px-3 py-1.5 rounded-full uppercase tracking-wider shadow-sm">
                          {article.tags[0]}
                        </div>
                      )}
                    </div>
                    
                    {/* Text Content */}
                    <div className="flex flex-col flex-grow px-2">
                      <div className="flex items-center mb-3 text-xs text-blue-600 font-semibold tracking-wide uppercase">
                        <span>{formatDate(article.publishedAt)}</span>
                        <span className="mx-2">•</span>
                        <span>{author.name}</span>
                      </div>
                      <h3 className="text-2xl font-bold text-slate-900 mb-3 group-hover:text-blue-600 transition-colors line-clamp-3 leading-snug">
                        {article.title}
                      </h3>
                      <p className="text-slate-600 text-base flex-grow line-clamp-3 leading-relaxed">
                        {article.excerpt}
                      </p>
                    </div>
                  </div>
                </Link>
              );
            })}
          </div>
        ) : (
          <div className="text-center py-24">
            <h3 className="text-2xl font-bold text-slate-700 mb-2">No articles found</h3>
            <p className="text-slate-500">Try adjusting your search or filters.</p>
          </div>
        )}

        {/* Beautiful Pagination */}
        {totalPages > 1 && (
          <div className="mt-20 flex items-center justify-center space-x-2 border-t border-slate-200 pt-10">
            <button 
              onClick={() => handlePageChange(currentPage - 1)}
              disabled={currentPage === 1}
              className="px-4 py-2 rounded-xl bg-white border border-slate-200 text-slate-600 font-medium hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors shadow-sm"
            >
              Previous
            </button>
            
            <div className="hidden sm:flex items-center space-x-1">
              {[...Array(totalPages)].map((_, i) => {
                const page = i + 1;
                // Simple logic to show bounded page numbers (e.g. 1 2 3 ... 84)
                if (
                  page === 1 || 
                  page === totalPages || 
                  (page >= currentPage - 1 && page <= currentPage + 1)
                ) {
                  return (
                    <button
                      key={page}
                      onClick={() => handlePageChange(page)}
                      className={`w-10 h-10 rounded-xl flex items-center justify-center font-semibold transition-all ${
                        currentPage === page 
                          ? "bg-blue-600 text-white shadow-md" 
                          : "bg-white text-slate-600 border border-slate-200 hover:bg-slate-50 shadow-sm"
                      }`}
                    >
                      {page}
                    </button>
                  );
                }
                
                // Show ellipsis if there's a gap
                if (
                  (page === 2 && currentPage > 3) || 
                  (page === totalPages - 1 && currentPage < totalPages - 2)
                ) {
                  return <span key={page} className="px-2 text-slate-400">...</span>;
                }
                
                return null;
              })}
            </div>

            <span className="sm:hidden text-slate-600 font-medium px-4">
              Page {currentPage} of {totalPages}
            </span>

            <button 
              onClick={() => handlePageChange(currentPage + 1)}
              disabled={currentPage === totalPages}
              className="px-4 py-2 rounded-xl bg-white border border-slate-200 text-slate-600 font-medium hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors shadow-sm"
            >
              Next
            </button>
          </div>
        )}

      </div>
    </div>
  );
}
