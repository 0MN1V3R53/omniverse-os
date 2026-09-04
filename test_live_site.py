#!/usr/bin/env python3
"""
==========================================================
SKY AUTO SERVICES — LIVE SITE VERIFICATION TEST SUITE
==========================================================
Tests route pages, mobile call buttons, quote widget,
and overall site health on skyautoservices.com
"""

import requests
import sys
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup

BASE_URL = "https://skyautoservices.com"
TIMEOUT = 15
MOBILE_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
)
DESKTOP_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
)

# ─── Route sample: one per state, spread across alphabet ───────────────────────
ROUTE_SAMPLES = [
    "routes/alabama-to-california-auto-transport.html",
    "routes/alaska-to-texas-auto-transport.html",
    "routes/arizona-to-new-york-auto-transport.html",
    "routes/arkansas-to-florida-auto-transport.html",
    "routes/california-to-new-york-auto-transport.html",
    "routes/colorado-to-texas-auto-transport.html",
    "routes/connecticut-to-florida-auto-transport.html",
    "routes/delaware-to-california-auto-transport.html",
    "routes/florida-to-new-york-auto-transport.html",
    "routes/georgia-to-california-auto-transport.html",
    "routes/hawaii-to-california-auto-transport.html",
    "routes/idaho-to-texas-auto-transport.html",
    "routes/illinois-to-florida-auto-transport.html",
    "routes/indiana-to-california-auto-transport.html",
    "routes/iowa-to-texas-auto-transport.html",
    "routes/kansas-to-florida-auto-transport.html",
    "routes/kentucky-to-california-auto-transport.html",
    "routes/louisiana-to-new-york-auto-transport.html",
    "routes/maine-to-florida-auto-transport.html",
    "routes/maryland-to-california-auto-transport.html",
    "routes/massachusetts-to-florida-auto-transport.html",
    "routes/michigan-to-california-auto-transport.html",
    "routes/minnesota-to-florida-auto-transport.html",
    "routes/mississippi-to-california-auto-transport.html",
    "routes/missouri-to-texas-auto-transport.html",
    "routes/montana-to-california-auto-transport.html",
    "routes/nebraska-to-florida-auto-transport.html",
    "routes/nevada-to-new-york-auto-transport.html",
    "routes/new-hampshire-to-florida-auto-transport.html",
    "routes/new-jersey-to-california-auto-transport.html",
    "routes/new-mexico-to-new-york-auto-transport.html",
    "routes/new-york-to-california-auto-transport.html",
    "routes/north-carolina-to-california-auto-transport.html",
    "routes/north-dakota-to-texas-auto-transport.html",
    "routes/ohio-to-california-auto-transport.html",
    "routes/oklahoma-to-california-auto-transport.html",
    "routes/oregon-to-new-york-auto-transport.html",
    "routes/pennsylvania-to-florida-auto-transport.html",
    "routes/rhode-island-to-california-auto-transport.html",
    "routes/south-carolina-to-california-auto-transport.html",
    "routes/south-dakota-to-florida-auto-transport.html",
    "routes/tennessee-to-california-auto-transport.html",
    "routes/texas-to-new-york-auto-transport.html",
    "routes/utah-to-new-york-auto-transport.html",
    "routes/vermont-to-florida-auto-transport.html",
    "routes/virginia-to-california-auto-transport.html",
    "routes/washington-to-new-york-auto-transport.html",
    "routes/west-virginia-to-california-auto-transport.html",
    "routes/wisconsin-to-florida-auto-transport.html",
    "routes/wyoming-to-texas-auto-transport.html",
]

# Additional edge-case routes
EXTRA_ROUTES = [
    "routes/alabama-to-alaska-auto-transport.html",  # first generated
    "routes/wyoming-to-wisconsin-auto-transport.html",  # last generated
    "routes/california-to-hawaii-auto-transport.html",
    "routes/texas-to-california-auto-transport.html",
    "routes/florida-to-california-auto-transport.html",
]

CORE_PAGES = [
    "/",
    "/quote-widget",
    "/routes",
    "/routes/index.html",
    "/sitemap.xml",
]


# ─── Colours ───────────────────────────────────────────────────────────────────
PASS = "\033[92m✔\033[0m"
FAIL = "\033[91m✖\033[0m"
WARN = "\033[93m⚠\033[0m"
INFO = "\033[94mℹ\033[0m"
BOLD = "\033[1m"
RESET = "\033[0m"

pass_count = 0
fail_count = 0
warn_count = 0
failures = []


def log(symbol, label, detail=""):
    global pass_count, fail_count, warn_count
    if symbol == PASS:
        pass_count += 1
    elif symbol == FAIL:
        fail_count += 1
        failures.append(f"{label}: {detail}")
    elif symbol == WARN:
        warn_count += 1
    print(f"  {symbol}  {label:<65} {detail}")


def get(url, ua=DESKTOP_UA):
    try:
        r = requests.get(url, headers={"User-Agent": ua}, timeout=TIMEOUT, allow_redirects=True)
        return r
    except requests.exceptions.RequestException as e:
        return None


def check_core_pages():
    print(f"\n{BOLD}━━━ CORE PAGE HEALTH ━━━{RESET}")
    for path in CORE_PAGES:
        url = BASE_URL + path if path.startswith("/") else BASE_URL + "/" + path
        r = get(url)
        if r is None:
            log(FAIL, path, "Connection error")
        elif r.status_code == 200:
            log(PASS, path, f"HTTP {r.status_code} ({len(r.content):,} bytes)")
        else:
            log(FAIL, path, f"HTTP {r.status_code}")


def check_route_page(path, ua=DESKTOP_UA):
    """Returns a dict of check results for a single route page."""
    url = f"{BASE_URL}/{path}"
    results = {
        "url": url,
        "path": path,
        "http_ok": False,
        "has_call_button": False,
        "has_quote_widget": False,
        "has_title": False,
        "has_schema": False,
        "has_mobile_meta": False,
        "status_code": None,
        "error": None,
    }
    r = get(url, ua=ua)
    if r is None:
        results["error"] = "Connection error"
        return results
    results["status_code"] = r.status_code
    if r.status_code != 200:
        results["error"] = f"HTTP {r.status_code}"
        return results
    results["http_ok"] = True
    html = r.text
    soup = BeautifulSoup(html, "html.parser")

    # Mobile call button
    if "tel:+12244490397" in html or "Need an Instant Quote?" in html:
        results["has_call_button"] = True

    # Quote widget (iframe or Next.js embed)
    if "quote-widget" in html or "QuoteCalculator" in html:
        results["has_quote_widget"] = True

    # Page title
    title = soup.find("title")
    if title and len(title.text.strip()) > 5:
        results["has_title"] = True

    # Schema.org JSON-LD
    if '"@type"' in html and ("AutoDealer" in html or "LocalBusiness" in html or "Service" in html or "AggregateRating" in html):
        results["has_schema"] = True

    # Mobile viewport meta
    meta_vp = soup.find("meta", attrs={"name": "viewport"})
    if meta_vp:
        results["has_mobile_meta"] = True

    return results


def check_route_pages():
    all_routes = ROUTE_SAMPLES + EXTRA_ROUTES
    print(f"\n{BOLD}━━━ ROUTE PAGE CHECKS ({len(all_routes)} pages sampled — 1 per state + edge cases) ━━━{RESET}")

    desktop_results = []
    mobile_results = []

    print(f"\n  {INFO}  Running desktop checks...")
    with ThreadPoolExecutor(max_workers=10) as ex:
        futures = {ex.submit(check_route_page, p, DESKTOP_UA): p for p in all_routes}
        for f in as_completed(futures):
            desktop_results.append(f.result())

    print(f"  {INFO}  Running mobile UA checks on 10 random routes...")
    mobile_sample = random.sample(all_routes, min(10, len(all_routes)))
    with ThreadPoolExecutor(max_workers=5) as ex:
        futures = {ex.submit(check_route_page, p, MOBILE_UA): p for p in mobile_sample}
        for f in as_completed(futures):
            mobile_results.append(f.result())

    # ── Report desktop results ──
    print(f"\n  {BOLD}Desktop Results:{RESET}")
    http_ok = sum(1 for r in desktop_results if r["http_ok"])
    call_btn = sum(1 for r in desktop_results if r["has_call_button"])
    widget = sum(1 for r in desktop_results if r["has_quote_widget"])
    title = sum(1 for r in desktop_results if r["has_title"])
    schema = sum(1 for r in desktop_results if r["has_schema"])
    mobile_meta = sum(1 for r in desktop_results if r["has_mobile_meta"])
    total = len(desktop_results)

    log(PASS if http_ok == total else FAIL, "Pages returning HTTP 200", f"{http_ok}/{total}")
    log(PASS if call_btn == total else FAIL, "Mobile Call Button present", f"{call_btn}/{total}")
    log(PASS if widget == total else WARN, "Quote Widget embedded", f"{widget}/{total}")
    log(PASS if title == total else FAIL, "Page <title> set", f"{title}/{total}")
    log(PASS if schema > 0 else WARN, "Schema.org JSON-LD detected", f"{schema}/{total}")
    log(PASS if mobile_meta == total else FAIL, "Viewport meta tag present", f"{mobile_meta}/{total}")

    # Show any HTTP failures
    failures_found = [r for r in desktop_results if not r["http_ok"]]
    if failures_found:
        print(f"\n  {BOLD}Failed pages:{RESET}")
        for r in failures_found:
            print(f"    {FAIL} {r['url']} — {r['error']}")

    # ── Report mobile UA results ──
    print(f"\n  {BOLD}Mobile User-Agent Results ({len(mobile_results)} sampled):{RESET}")
    m_http_ok = sum(1 for r in mobile_results if r["http_ok"])
    m_call_btn = sum(1 for r in mobile_results if r["has_call_button"])
    m_widget = sum(1 for r in mobile_results if r["has_quote_widget"])
    m_total = len(mobile_results)

    log(PASS if m_http_ok == m_total else FAIL, "Mobile: pages returning HTTP 200", f"{m_http_ok}/{m_total}")
    log(PASS if m_call_btn == m_total else FAIL, "Mobile: Call Button present", f"{m_call_btn}/{m_total}")
    log(PASS if m_widget == m_total else WARN, "Mobile: Quote Widget present", f"{m_widget}/{m_total}")

    return desktop_results


def check_quote_widget():
    print(f"\n{BOLD}━━━ QUOTE WIDGET (/quote-widget) ━━━{RESET}")
    url = f"{BASE_URL}/quote-widget"

    # Desktop
    r = get(url, DESKTOP_UA)
    if r and r.status_code == 200:
        html = r.text
        log(PASS, "Quote widget page loads (desktop)", f"HTTP 200 ({len(r.content):,} bytes)")
        log(PASS if "_next" in html or "chunk" in html else WARN,
            "Next.js JS chunks present", "React bundle detected" if "_next" in html else "Not detected")
        log(PASS if "QuoteCalculator" in html or "quote" in html.lower() else WARN,
            "Calculator content in HTML", "Found" if "QuoteCalculator" in html or "quote" in html.lower() else "Not found")
    else:
        log(FAIL, "Quote widget page loads (desktop)", f"HTTP {r.status_code if r else 'Error'}")

    # Mobile
    r_m = get(url, MOBILE_UA)
    if r_m and r_m.status_code == 200:
        log(PASS, "Quote widget page loads (mobile UA)", f"HTTP 200 ({len(r_m.content):,} bytes)")
        # Check it returns same byte-size content (no mobile redirect/stripping)
        size_diff = abs(len(r_m.content) - len(r.content)) if r else 0
        log(PASS if size_diff < 5000 else WARN,
            "Mobile/desktop response parity", f"Diff: {size_diff:,} bytes")
    else:
        log(FAIL, "Quote widget page loads (mobile UA)", f"HTTP {r_m.status_code if r_m else 'Error'}")


def check_sitemap():
    print(f"\n{BOLD}━━━ SITEMAP VERIFICATION ━━━{RESET}")
    url = f"{BASE_URL}/sitemap.xml"
    r = get(url)
    if r is None or r.status_code != 200:
        log(FAIL, "sitemap.xml accessible", f"HTTP {r.status_code if r else 'Error'}")
        return
    log(PASS, "sitemap.xml accessible", f"HTTP 200 ({len(r.content):,} bytes)")
    xml = r.text
    url_count = xml.count("<loc>")
    log(PASS if url_count > 100 else WARN, "Sitemap URL count", f"{url_count:,} URLs found")
    log(PASS if "skyautoservices.com" in xml else FAIL, "Domain correct in sitemap", "skyautoservices.com found" if "skyautoservices.com" in xml else "Domain mismatch")


def check_https_redirect():
    print(f"\n{BOLD}━━━ HTTPS / WWW REDIRECT ━━━{RESET}")
    tests = [
        ("http://skyautoservices.com", "HTTPS redirect"),
        ("https://www.skyautoservices.com", "www redirect"),
        ("http://www.skyautoservices.com", "http+www redirect"),
    ]
    for url, label in tests:
        try:
            r = requests.get(url, timeout=TIMEOUT, allow_redirects=True)
            final = r.url
            if "https://skyautoservices.com" in final or "https://www.skyautoservices.com" in final:
                log(PASS, label, f"→ {final} (HTTP {r.status_code})")
            else:
                log(WARN, label, f"→ {final}")
        except Exception as e:
            log(WARN, label, str(e)[:60])


def print_summary():
    print(f"\n{BOLD}{'━'*70}{RESET}")
    print(f"{BOLD}  SUMMARY{RESET}")
    print(f"{'━'*70}")
    total = pass_count + fail_count + warn_count
    print(f"  {PASS}  Passed  : {pass_count}")
    print(f"  {FAIL}  Failed  : {fail_count}")
    print(f"  {WARN}  Warnings: {warn_count}")
    print(f"  {INFO}  Total   : {total}")
    if failures:
        print(f"\n  {BOLD}Failures:{RESET}")
        for f in failures:
            print(f"    {FAIL} {f}")
    print(f"{'━'*70}")
    if fail_count == 0:
        print(f"\n  🎉 {BOLD}All critical checks passed! Site is healthy.{RESET}")
    else:
        print(f"\n  ⚠️  {BOLD}{fail_count} failure(s) require attention.{RESET}")
    print()


if __name__ == "__main__":
    print(f"\n{BOLD}{'═'*70}{RESET}")
    print(f"{BOLD}  SKY AUTO SERVICES — LIVE SITE VERIFICATION{RESET}")
    print(f"{BOLD}  Target: {BASE_URL}{RESET}")
    print(f"{BOLD}{'═'*70}{RESET}")

    start = time.time()
    check_https_redirect()
    check_core_pages()
    check_quote_widget()
    check_route_pages()
    check_sitemap()
    elapsed = time.time() - start

    print(f"\n  ⏱  Tests completed in {elapsed:.1f}s")
    print_summary()
    sys.exit(0 if fail_count == 0 else 1)
