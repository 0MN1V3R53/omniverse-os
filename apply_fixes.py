import glob

def apply_fixes(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()

        changed = False

        # 1. Update logo size
        old_logo = '<img src="/assets/images/logo.png" alt="Sky Auto Services Official Shield Logo" class="w-12 h-12 object-contain drop-shadow-md group-hover:scale-105 transition-transform duration-300"/>'
        new_logo = '<img src="/assets/images/logo.png" alt="Sky Auto Services Official Shield Logo" class="w-16 h-16 object-contain drop-shadow-md group-hover:scale-105 transition-transform duration-300"/>'
        if old_logo in html:
            html = html.replace(old_logo, new_logo)
            changed = True
        
        # Another variation where class attribute uses different quotes or spacing? Just in case:
        old_logo2 = 'className="w-12 h-12'
        new_logo2 = 'className="w-16 h-16'
        
        # 2. Update text size in header
        old_text = '<span class="text-[11px] uppercase tracking-[0.25em] text-gray-500 mt-0.5">Nationwide Logistics</span>'
        # wait, the previous was replaced with text-[10px], I changed it in Navigation.jsx to text-[11px]. 
        # I need to match what's currently in public_html_local. Let's do regex or exact string.
        # old span in public_html_local has text-xl and text-[10px]
        old_span = '<span class="flex flex-col leading-none"><span class="text-xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400 tracking-tight group-hover:from-blue-300 group-hover:to-emerald-300 transition-all">SKY <span class="font-extrabold">SERVICES</span></span><span class="text-[10px] uppercase tracking-[0.25em] text-gray-500 mt-0.5">Nationwide Logistics</span><span class="text-[9px] font-semibold tracking-wider text-emerald-400/90 mt-1">USDOT: 4504932 | MC: 1782670</span><span class="text-[8px] uppercase tracking-wider text-emerald-400/70 mt-0.5">Licensed &amp; Bonded Broker</span></span>'
        new_span = '<span class="flex flex-col leading-none"><span class="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400 tracking-tight group-hover:from-blue-300 group-hover:to-emerald-300 transition-all">SKY <span class="font-extrabold">SERVICES</span></span><span class="text-[11px] uppercase tracking-[0.25em] text-gray-500 mt-0.5">Nationwide Logistics</span><span class="text-[9px] font-semibold tracking-wider text-emerald-400/90 mt-1">USDOT: 4504932 | MC: 1782670</span><span class="text-[8px] uppercase tracking-wider text-emerald-400/70 mt-0.5">Licensed &amp; Bonded Broker</span></span>'
        if old_span in html:
            html = html.replace(old_span, new_span)
            changed = True
            
        # 3. Update Hero min-height
        old_hero = '<section class="relative w-full min-h-[80svh] min-h-[80vh] flex items-center overflow-hidden bg-black">'
        new_hero = '<section class="relative w-full min-h-[100svh] min-h-screen flex items-center overflow-hidden bg-black">'
        if old_hero in html:
            html = html.replace(old_hero, new_hero)
            changed = True

        if changed:
            with open(path, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"Updated {path}")
            
    except Exception as e:
        print(f"Error {path}: {e}")

if __name__ == "__main__":
    for p in glob.glob("public_html_local/**/*.html", recursive=True):
        apply_fixes(p)
