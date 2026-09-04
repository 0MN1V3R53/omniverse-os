#!/usr/bin/env python3
"""
Deep SEO Audit Script for Sky Auto Services
Audits robots.txt, sitemaps, and a sample of 3,148 route pages for complete SEO compliance.
"""
import os
import glob
from bs4 import BeautifulSoup
import json

ROOT_DIR = "/Users/silversurfer/Documents/Omniverse2/public_html_local"
ROUTES_DIR = os.path.join(ROOT_DIR, "routes")

def audit_robots_txt():
    print("=== ROBOTS.TXT AUDIT ===")
    robots_path = os.path.join(ROOT_DIR, "robots.txt")
    if not os.path.exists(robots_path):
        print("FAIL: robots.txt not found.")
        return False
    with open(robots_path, "r") as f:
        content = f.read()
    if "User-Agent: *" in content and "Sitemap: " in content:
        print("PASS: robots.txt is well-formed and includes Sitemap directive.")
        return True
    else:
        print("FAIL: robots.txt missing User-Agent or Sitemap directive.")
        return False

def audit_sitemap():
    print("\n=== SITEMAP AUDIT ===")
    sitemap_path = os.path.join(ROOT_DIR, "sitemap.xml")
    if not os.path.exists(sitemap_path):
        print("FAIL: sitemap.xml not found.")
        return False
    with open(sitemap_path, "r") as f:
        content = f.read()
    if "<urlset" in content and "<loc>" in content:
        url_count = content.count("<loc>")
        print(f"PASS: sitemap.xml is well-formed with {url_count} URLs.")
        return True
    else:
        print("FAIL: sitemap.xml missing standard XML tags.")
        return False

def audit_route_pages():
    print("\n=== ROUTE PAGES HTML AUDIT ===")
    route_files = glob.glob(os.path.join(ROUTES_DIR, "*.html"))
    total_files = len(route_files)
    if total_files == 0:
        print("FAIL: No route pages found.")
        return
        
    print(f"Total route pages found: {total_files}")
    
    metrics = {
        "title": 0,
        "description": 0,
        "viewport": 0,
        "canonical": 0,
        "h1": 0,
        "schema": 0,
        "open_graph": 0
    }
    
    # Audit 100 random pages to avoid memory overhead but get statistically significant result
    import random
    sample = random.sample(route_files, min(100, total_files))
    
    for file in sample:
        with open(file, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
            html_text = str(soup)
            
            if soup.find("title") and soup.title.string: metrics["title"] += 1
            if soup.find("meta", attrs={"name": "description"}): metrics["description"] += 1
            if soup.find("meta", attrs={"name": "viewport"}): metrics["viewport"] += 1
            if soup.find("link", attrs={"rel": "canonical"}): metrics["canonical"] += 1
            if soup.find("h1"): metrics["h1"] += 1
            if '"@type"' in html_text and ("AutoDealer" in html_text or "LocalBusiness" in html_text): metrics["schema"] += 1
            if soup.find("meta", attrs={"property": "og:title"}): metrics["open_graph"] += 1

    sample_size = len(sample)
    for key, value in metrics.items():
        if value == sample_size:
            print(f"PASS: 100% of sampled pages have {key}")
        elif value > 0:
            print(f"WARN: {value}/{sample_size} of sampled pages have {key}")
        else:
            print(f"FAIL: 0/{sample_size} of sampled pages have {key}")

if __name__ == "__main__":
    audit_robots_txt()
    audit_sitemap()
    audit_route_pages()
