import os

def fix_html_content(content):
    style_fix = """
    <style>
        /* Mobile fixes */
        html { -webkit-text-size-adjust: 100%; text-size-adjust: 100%; }
        @media (max-width: 768px) {
            body { font-size: 16px; }
            h1, .hero h1, .d1 { font-size: clamp(2rem, 8vw, 3rem) !important; line-height: 1.1; }
            h2 { font-size: 1.75rem !important; }
            h3 { font-size: 1.5rem !important; }
            h4 { font-size: 1.25rem !important; }
            p { font-size: 1rem !important; line-height: 1.6; }
            
            /* Quote area adjustment */
            .quote-card, .bg-zinc-900\\/50 {
                 padding: 20px 15px !important;
                 margin: 10px !important;
                 border-radius: 16px !important;
            }
            
            /* Form fields */
            input, select, textarea {
                 font-size: 1rem !important; /* Prevents iOS zoom */
                 padding: 10px !important;
            }
        }
    </style>
"""
    if '/* Mobile fixes */' not in content:
        head_end = content.find('</head>')
        if head_end != -1:
            content = content[:head_end] + style_fix + content[head_end:]

    return content

filepath = 'public_html_local/index.html'
try:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content = fix_html_content(content)
    if content != new_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Fixed index.html")
except Exception as e:
    print(f"Error: {e}")
