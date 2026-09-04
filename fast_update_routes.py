import os
import re
from glob import glob

routes_dir = "public_html_local/routes"
files = glob(f"{routes_dir}/*.html")

css_injected = """
/* ===== injected mobile quote widget css ===== */
@media (max-width: 1020px) {
    .hero-grid {
        grid-template-columns: 1fr !important;
        gap: 20px !important;
        padding-top: 10px !important;
    }
    .hero-bg {
        height: 100% !important;
        min-height: 1200px !important;
    }
}
@media (max-width: 768px) {
    #quote-widget-iframe {
        min-height: 720px !important;
    }
}
</style>
"""

updated = 0

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    orig_html = html

    html = re.sub(
        r'<div id="quotecard">.*?</div>\n</div>\n<div class="scroll-ind">',
        r'<div id="quotecard">\n<iframe id="quote-widget-iframe" src="/quote-widget" style="width: 100%; min-height: 640px; border: none; overflow: hidden;" title="Quote Calculator"></iframe>\n</div>\n</div>\n<div class="scroll-ind">',
        html,
        flags=re.DOTALL
    )

    html = re.sub(r'<script>.*?fetch\(\'/backend/save_quote\.php\'\).*?</script>', '', html, flags=re.DOTALL)

    if "injected mobile quote widget css" not in html:
        html = html.replace('</style>', css_injected, 1)

    if html != orig_html:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        updated += 1

print(f"Updated {updated} files out of {len(files)}.")
