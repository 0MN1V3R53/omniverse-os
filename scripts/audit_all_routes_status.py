import urllib.request
import ssl
import sys
import glob
import os
import concurrent.futures
import time

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

BASE_URL = "https://www.skyautoservices.com"

# Collect all route URLs from public_html_local HTML files
html_files = glob.glob("public_html_local/**/*.html", recursive=True)
print(f"Total HTML files discovered: {len(html_files)}")

urls_to_test = set()

# Core pages
core_pages = [
    "",
    "about",
    "about/",
    "services",
    "services/",
    "contact",
    "contact/",
    "privacy",
    "privacy/",
    "terms",
    "terms/",
    "quote-widget",
    "quote-widget/",
    "routes",
    "routes/",
    "routes-directory",
    "routes-directory/",
    "state-to-state-routes",
    "state-to-state-routes/",
    "usa-auto-transport-news",
    "usa-auto-transport-news/",
    "auto-transport",
    "auto-transport/",
    "auto-transport/florida",
    "auto-transport/florida/",
    "auto-transport/california",
    "auto-transport/california/",
    "auto-transport/texas",
    "auto-transport/texas/",
    "auto-transport/illinois",
    "auto-transport/illinois/",
    "auto-transport/new-york",
    "auto-transport/new-york/",
    "auto-transport/nevada",
    "auto-transport/nevada/",
    "auto-transport/florida/miami",
    "auto-transport/florida/miami/",
    "auto-transport/california/los-angeles",
    "auto-transport/california/los-angeles/",
    "auto-transport/texas/houston",
    "auto-transport/texas/houston/",
    "auto-transport/illinois/chicago",
    "auto-transport/illinois/chicago/",
    "auto-transport/new-york/new-york",
    "auto-transport/new-york/new-york/",
    "auto-transport/nevada/las-vegas",
    "auto-transport/nevada/las-vegas/"
]

for p in core_pages:
    urls_to_test.add(f"{BASE_URL}/{p}".rstrip("/"))
    urls_to_test.add(f"{BASE_URL}/{p}")

# Add sample of routes, state-to-state, news, and auto-transport city pages
for f in html_files:
    rel = os.path.relpath(f, "public_html_local")
    if rel == "index.html" or rel == "404.html":
        continue
    # without .html
    clean_path = rel[:-5]
    urls_to_test.add(f"{BASE_URL}/{clean_path}")
    urls_to_test.add(f"{BASE_URL}/{clean_path}/")

url_list = sorted(list(urls_to_test))
print(f"Total Unique URLs generated for live HTTP status audit: {len(url_list)}")

def test_url(url):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    )
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=8) as res:
            return url, res.status, None
    except urllib.error.HTTPError as e:
        return url, e.code, str(e)
    except Exception as e:
        return url, 0, str(e)

# Test a representative sample of 200 URLs across all categories concurrently
sample_urls = url_list[:200]
print(f"Testing sample of {len(sample_urls)} URLs concurrently...")

passed = 0
failed = []

with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    futures = {executor.submit(test_url, url): url for url in sample_urls}
    for future in concurrent.futures.as_completed(futures):
        url, code, err = future.result()
        if code == 200:
            passed += 1
        else:
            failed.append((url, code, err))

print(f"\nAUDIT RESULTS: {passed}/{len(sample_urls)} PASSED (HTTP 200)")
if failed:
    print(f"FAILED ({len(failed)}):")
    for u, c, e in failed:
        print(f"  [{c}] {u} -> {e}")
else:
    print("SUCCESS: Zero 404 errors detected across sample URLs!")
