import os
import bs4
from glob import glob
import re

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
"""

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = bs4.BeautifulSoup(html, 'html.parser')

    changed = False

    quotecard = soup.find('div', id='quotecard')
    if quotecard:
        # Check if already processed
        if not quotecard.find('iframe', id='quote-widget-iframe'):
            quotecard.clear()
            iframe = soup.new_tag('iframe', 
                                  src='/quote-widget', 
                                  style='width: 100%; min-height: 640px; border: none; overflow: hidden;', 
                                  id='quote-widget-iframe', 
                                  title='Quote Calculator')
            quotecard.append(iframe)
            changed = True

    # Remove the vanilla JS block
    for script in soup.find_all('script'):
        if script.string and "fetch('/backend/save_quote.php')" in script.string:
            script.decompose()
            changed = True

    # Inject CSS if not present
    head = soup.find('head')
    if head and 'injected mobile quote widget css' not in html:
        style_tag = soup.new_tag('style')
        style_tag.string = css_injected
        head.append(style_tag)
        changed = True

    if changed:
        # bs4 sometimes outputs self-closing tags for things that shouldn't be, 
        # but html.parser is generally okay. We'll format it back to string.
        out_html = str(soup)
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(out_html)
        return True
    return False

if __name__ == "__main__":
    # Test on one file first
    test_file = os.path.join(routes_dir, "alabama-to-alaska-auto-transport.html")
    if os.path.exists(test_file):
        print(f"Testing on {test_file}")
        updated = update_file(test_file)
        print(f"Updated: {updated}")
    else:
        print("Test file not found!")
