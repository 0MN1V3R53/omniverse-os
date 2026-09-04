#!/usr/bin/env python3
"""
OPERATION: GBP-SYNDICATION
Omniverse Tech - Web Development, SEO & Growth Division
Author: @seo_schema_dev & @seo_backlink_outreach

Generates structured Google Business Profile (GBP) update posts pointing back to local route pages to drive local citation signals and Map Pack authority.
"""
import os
import random

ROUTES_DIR = "/Users/silversurfer/Documents/Omniverse2/public_html_local/routes"

POST_TEMPLATES = [
    "Looking for reliable auto transport in {city}? Sky Auto Services offers premium enclosed carrier transport with a $0 upfront deposit. Fully insured and FMCSA licensed. Get your instant quote here: {url}",
    "Need to ship a luxury or exotic car from {city}? We specialize in door-to-door enclosed transport. Trust the experts with your vehicle. Learn more: {url}",
    "Sky Auto Services provides top-rated vehicle shipping for {city}. Whether it's a classic car or daily driver, our network of trusted carriers ensures safe delivery. Check our pricing: {url}"
]

def generate_gbp_posts(num_posts=5):
    if not os.path.exists(ROUTES_DIR):
        print(f"Routes directory not found at {ROUTES_DIR}")
        return

    html_files = [f for f in os.listdir(ROUTES_DIR) if f.endswith(".html")]
    if not html_files:
        print("No route pages found.")
        return

    sampled_files = random.sample(html_files, min(num_posts, len(html_files)))
    
    print("--- GBP SYNDICATION POSTS ---")
    for f in sampled_files:
        slug = f.replace(".html", "")
        city_name = slug.replace("-", " ").title()
        url = f"https://skyautoservices.com/routes/{slug}"
        template = random.choice(POST_TEMPLATES)
        post = template.format(city=city_name, url=url)
        print(f"\n[GBP POST - {city_name}]")
        print(f"Content: {post}")
        print(f"CTA Button: 'Learn more' -> {url}")
        print("-" * 30)

if __name__ == "__main__":
    generate_gbp_posts()
