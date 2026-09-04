#!/usr/bin/env python3
"""
OPERATION: SKY-AUTO-BOT-WHISPERER
Omniverse Tech - Web Development, SEO & Growth Division

Phase 3: The Google Crawler Robot
Generates XML sitemaps and robots.txt specifically designed to force Googlebot to ingest our hyperlocal matrix.
"""

import os
from pathlib import Path
import datetime
import logging

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("GooglebotInterface")

LOCAL_ROOT = Path("/Users/silversurfer/Documents/Omniverse2/public_html_local")
ROUTES_DIR = LOCAL_ROOT / "routes"
HYPERLOCAL_DIR = LOCAL_ROOT / "hyperlocal_routes"
BASE_URL = "https://www.skyautoservices.com"

SITEMAP_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>"""

URL_TEMPLATE = """  <url>
    <loc>{url}</loc>
    <lastmod>{date}</lastmod>
    <changefreq>daily</changefreq>
    <priority>{priority}</priority>
  </url>"""

def generate_sitemap_and_robots():
    logger.info("=== OPERATION: SKY-AUTO-BOT-WHISPERER ===")
    
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    urls = []
    
    # 1. Main Pages
    main_pages = ["index.html", "about.html", "services.html", "contact.html"]
    for page in main_pages:
        urls.append(URL_TEMPLATE.format(url=f"{BASE_URL}/{page}", date=today, priority="1.0"))
        
    # 2. State-to-State Routes
    if ROUTES_DIR.exists():
        routes = [f.name for f in ROUTES_DIR.glob("*.html")]
        logger.info(f"Adding {len(routes)} state-to-state routes to sitemap...")
        for route in routes:
            urls.append(URL_TEMPLATE.format(url=f"{BASE_URL}/routes/{route}", date=today, priority="0.8"))
            
    # 3. Hyperlocal Routes
    if HYPERLOCAL_DIR.exists():
        hyperlocal = [f.name for f in HYPERLOCAL_DIR.glob("*.html")]
        logger.info(f"Adding {len(hyperlocal)} hyperlocal routes to sitemap...")
        for route in hyperlocal:
            urls.append(URL_TEMPLATE.format(url=f"{BASE_URL}/hyperlocal_routes/{route}", date=today, priority="0.9"))
            
    # Write Sitemap
    sitemap_path = LOCAL_ROOT / "sitemap.xml"
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(SITEMAP_TEMPLATE.format(urls="\n".join(urls)))
    logger.info(f"✓ sitemap.xml generated at {sitemap_path}")
    
    # Write Robots.txt
    robots_path = LOCAL_ROOT / "robots.txt"
    robots_content = f"""User-agent: *
Allow: /
Disallow: /api/
Disallow: /admin/
Disallow: /private/

Sitemap: {BASE_URL}/sitemap.xml
"""
    with open(robots_path, "w", encoding="utf-8") as f:
        f.write(robots_content)
    logger.info(f"✓ robots.txt generated at {robots_path}")
    
    logger.info("Googlebot Interface initialized successfully.")

if __name__ == "__main__":
    generate_sitemap_and_robots()
