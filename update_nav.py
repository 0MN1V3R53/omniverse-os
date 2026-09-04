import os

def update_file(path):
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    target = '<span class="flex flex-col leading-none"><span class="text-xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400 tracking-tight group-hover:from-blue-300 group-hover:to-emerald-300 transition-all">SKY <span class="font-extrabold">SERVICES</span></span><span class="text-[10px] uppercase tracking-[0.25em] text-gray-500 mt-0.5">Nationwide Logistics</span></span>'
    
    replacement = '<span class="flex flex-col leading-none"><span class="text-xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400 tracking-tight group-hover:from-blue-300 group-hover:to-emerald-300 transition-all">SKY <span class="font-extrabold">SERVICES</span></span><span class="text-[10px] uppercase tracking-[0.25em] text-gray-500 mt-0.5">Nationwide Logistics</span><span class="text-[9px] font-semibold tracking-wider text-emerald-400/90 mt-1">USDOT: 4504932 | MC: 1782670</span><span class="text-[8px] uppercase tracking-wider text-emerald-400/70 mt-0.5">Licensed &amp; Bonded Broker</span></span>'

    if target in html:
        html = html.replace(target, replacement)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Updated {path}")
    else:
        print(f"Target not found in {path}")

if __name__ == "__main__":
    update_file("public_html_local/index.html")
    update_file("hostinger_site/public_html/index.html")
