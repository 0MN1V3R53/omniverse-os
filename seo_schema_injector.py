import os
import glob
import json

ROUTES_DIR = "public_html_local/routes/"

def inject_schema():
    if not os.path.exists(ROUTES_DIR):
        print(f"Directory {ROUTES_DIR} not found.")
        return

    html_files = glob.glob(os.path.join(ROUTES_DIR, "*.html"))
    print(f"[INIT] Found {len(html_files)} route pages for schema injection.")

    success_count = 0
    schema_block = """<script type="application/ld+json">{"@context":"https://schema.org","@type":"AutoTransportService","name":"Sky Auto Services","url":"https://www.skyautoservices.com","telephone":"+1-224-449-0397","image":"https://www.skyautoservices.com/assets/images/american_hypercars_fleet.png","description":"Nationwide premium auto transport service offering enclosed and open vehicle logistics. Licensed FMCSA Broker MC-1782670.","address":{"@type":"PostalAddress","addressCountry":"US"},"areaServed":"US","priceRange":"$$"}</script>"""

    for file_path in html_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if schema_block in content:
            continue

        if "</head>" in content:
            content = content.replace("</head>", schema_block + "</head>")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            success_count += 1

    print(f"[SUCCESS] Injected JSON-LD Schema into {success_count} route pages.")

if __name__ == "__main__":
    inject_schema()
