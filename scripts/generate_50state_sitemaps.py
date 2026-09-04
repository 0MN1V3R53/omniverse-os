#!/usr/bin/env python3
"""
Omniverse 50-State Sitemap Index & Partition Generator
Deconstructs monolithic sitemaps into a high-performance multi-tier sitemap architecture
for rapid Googlebot parallel discovery across all 50 US States.
"""

import os
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
PUBLIC_HTML = WORKSPACE_ROOT / "public_html_local"
SITEMAPS_DIR = PUBLIC_HTML / "sitemaps"
SITEMAPS_DIR.mkdir(parents=True, exist_ok=True)

DOMAIN = "https://www.skyautoservices.com"
NOW_ISO = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")

def prettify(elem):
    """Return a pretty-printed XML string for the Element."""
    rough_string = ET.tostring(elem, "utf-8")
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")

def generate_url_elem(urlset, loc, lastmod, changefreq, priority):
    url_elem = ET.SubElement(urlset, "url")
    loc_elem = ET.SubElement(url_elem, "loc")
    loc_elem.text = loc
    lastmod_elem = ET.SubElement(url_elem, "lastmod")
    lastmod_elem.text = lastmod
    freq_elem = ET.SubElement(url_elem, "changefreq")
    freq_elem.text = changefreq
    prio_elem = ET.SubElement(url_elem, "priority")
    prio_elem.text = str(priority)

def build_sitemaps():
    print("🚀 Generating 50-State Partitioned Sitemaps Architecture...")
    
    # 1. Load state_routes.json
    state_routes_path = PUBLIC_HTML / "assets" / "data" / "state_routes.json"
    with open(state_routes_path, "r", encoding="utf-8") as f:
        state_routes = json.load(f)

    # 2. Load existing sitemap.xml for auxiliary URLs (cities, news, core)
    sitemap_path = PUBLIC_HTML / "sitemap.xml"
    city_urls = []
    news_urls = []
    core_urls = [
        f"{DOMAIN}",
        f"{DOMAIN}/services",
        f"{DOMAIN}/about",
        f"{DOMAIN}/contact",
        f"{DOMAIN}/terms",
        f"{DOMAIN}/privacy",
        f"{DOMAIN}/state-to-state-routes/"
    ]

    if sitemap_path.exists():
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        for loc in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
            url = loc.text.strip()
            if "/auto-transport/" in url and url not in city_urls:
                city_urls.append(url)
            elif ("news" in url or "blog" in url or "guide" in url) and url not in news_urls:
                news_urls.append(url)

    sitemap_files_created = []

    # A. Core Pages Sitemap
    core_set = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for url in core_urls:
        generate_url_elem(core_set, url, NOW_ISO, "daily", 1.0 if url == DOMAIN else 0.9)
    core_file = SITEMAPS_DIR / "sitemap_core.xml"
    core_file.write_text(prettify(core_set), encoding="utf-8")
    sitemap_files_created.append("sitemap_core.xml")

    # B. Cities Sitemap
    if city_urls:
        cities_set = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
        for url in city_urls:
            generate_url_elem(cities_set, url, NOW_ISO, "weekly", 0.8)
        cities_file = SITEMAPS_DIR / "sitemap_cities.xml"
        cities_file.write_text(prettify(cities_set), encoding="utf-8")
        sitemap_files_created.append("sitemap_cities.xml")

    # C. Priority Corridors Sitemap (High Demand National Lanes)
    priority_corridors = [
        "california-to-florida-auto-transport",
        "california-to-texas-auto-transport",
        "new-york-to-florida-auto-transport",
        "florida-to-new-york-auto-transport",
        "illinois-to-florida-auto-transport",
        "texas-to-california-auto-transport",
        "texas-to-florida-auto-transport",
        "california-to-washington-auto-transport",
        "massachusetts-to-florida-auto-transport",
        "new-jersey-to-florida-auto-transport",
        "pennsylvania-to-florida-auto-transport",
        "michigan-to-florida-auto-transport",
        "ohio-to-florida-auto-transport",
        "georgia-to-california-auto-transport",
        "arizona-to-california-auto-transport"
    ]
    prio_set = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for slug in priority_corridors:
        url = f"{DOMAIN}/routes/{slug}"
        generate_url_elem(prio_set, url, NOW_ISO, "daily", 1.0)
    prio_file = SITEMAPS_DIR / "sitemap_priority_routes.xml"
    prio_file.write_text(prettify(prio_set), encoding="utf-8")
    sitemap_files_created.append("sitemap_priority_routes.xml")

    # D. News / Freshness Sitemap
    if news_urls:
        news_set = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
        for url in news_urls:
            generate_url_elem(news_set, url, NOW_ISO, "daily", 0.85)
        news_file = SITEMAPS_DIR / "sitemap_news.xml"
        news_file.write_text(prettify(news_set), encoding="utf-8")
        sitemap_files_created.append("sitemap_news.xml")

    # E. 50 State-Specific XML Sitemaps
    for state_name, routes in state_routes.items():
        state_slug = state_name.lower().replace(" ", "-")
        state_xml_filename = f"sitemap_state_{state_slug}.xml"
        state_set = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
        
        for r in routes:
            # Format route slug
            dest_name = r.get("destinationState", "")
            dest_slug = dest_name.lower().replace(" ", "-")
            route_slug = f"{state_slug}-to-{dest_slug}-auto-transport"
            route_url = f"{DOMAIN}/routes/{route_slug}"
            generate_url_elem(state_set, route_url, NOW_ISO, "weekly", 0.8)

        state_file = SITEMAPS_DIR / state_xml_filename
        state_file.write_text(prettify(state_set), encoding="utf-8")
        sitemap_files_created.append(state_xml_filename)

    # F. Master Sitemap Index (sitemap_index.xml)
    sitemapindex = ET.Element("sitemapindex", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for sm_file in sitemap_files_created:
        sitemap_elem = ET.SubElement(sitemapindex, "sitemap")
        loc_elem = ET.SubElement(sitemap_elem, "loc")
        loc_elem.text = f"{DOMAIN}/sitemaps/{sm_file}"
        lastmod_elem = ET.SubElement(sitemap_elem, "lastmod")
        lastmod_elem.text = NOW_ISO

    master_index_file = SITEMAPS_DIR / "sitemap_index.xml"
    master_index_file.write_text(prettify(sitemapindex), encoding="utf-8")

    # Also save master copy to public_html_local/sitemap_index.xml and keep root sitemap.xml updated
    (PUBLIC_HTML / "sitemap_index.xml").write_text(prettify(sitemapindex), encoding="utf-8")

    # G. Update robots.txt
    robots_file = PUBLIC_HTML / "robots.txt"
    robots_content = f"""User-Agent: *
Allow: /
Disallow: /admin
Disallow: /api

User-Agent: GPTBot
User-Agent: Claude-Web
User-Agent: Google-Extended
User-Agent: KimiBot
User-Agent: Bingbot
User-Agent: Googlebot
Allow: /
Allow: /llm-feed.json
Allow: /sitemaps/

Sitemap: {DOMAIN}/sitemaps/sitemap_index.xml
Sitemap: {DOMAIN}/sitemap.xml
Sitemap: {DOMAIN}/sitemaps/sitemap_priority_routes.xml
"""
    robots_file.write_text(robots_content, encoding="utf-8")

    print(f"✅ Successfully created {len(sitemap_files_created)} partitioned XML sitemaps + sitemap_index.xml!")
    print(f"✅ Updated robots.txt with Master Sitemap Index: {DOMAIN}/sitemaps/sitemap_index.xml")

if __name__ == "__main__":
    build_sitemaps()
