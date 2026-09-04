import os
from bs4 import BeautifulSoup
import re

base_dir = '/Users/silversurfer/Documents/Omniverse2'
source_html_path = os.path.join(base_dir, 'public_html_local', 'index.html')

with open(source_html_path, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# Extract key elements
head_html = ""
for tag in soup.head.contents:
    if tag.name in ['link', 'script', 'meta', 'style']:
        # Fix relative paths to point to public_html_local
        tag_str = str(tag)
        tag_str = tag_str.replace('href="/_next/', 'href="../../public_html_local/_next/')
        tag_str = tag_str.replace('src="/_next/', 'src="../../public_html_local/_next/')
        tag_str = tag_str.replace('href="/assets/', 'href="../../public_html_local/assets/')
        tag_str = tag_str.replace('src="/assets/', 'src="../../public_html_local/assets/')
        head_html += tag_str + "\n"

nav = soup.find('nav')
nav_str = str(nav) if nav else ""
nav_str = nav_str.replace('src="/assets/', 'src="../../public_html_local/assets/')

footer = soup.find('footer')
footer_str = str(footer) if footer else ""

quote_calc = soup.find(id='quote-calculator')
quote_calc_str = str(quote_calc) if quote_calc else ""

# The styling used for cards in the live site:
# class="w-full bg-zinc-900/60 backdrop-blur-xl border border-white/10 rounded-2xl md:rounded-[2rem] shadow-2xl p-4 sm:p-6 md:p-10 lg:p-14"

# ---------------------------------------------------------
# 1. MONTWAY LAYOUT (Homepage)
# ---------------------------------------------------------
montway_index = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <title>Sky Auto Services | Montway Layout</title>
    {head_html}
    <style>
        .montway-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }}
        @media (max-width: 1024px) {{ .montway-grid {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body class="__className_f367f3 bg-black text-white antialiased">
    {nav_str}
    
    <main class="min-h-screen bg-black pt-28">
        <!-- MONTWAY SIDE-BY-SIDE HERO -->
        <section class="relative w-full py-16">
            <div class="absolute inset-0 z-0 opacity-40" style="background-image:url('../../public_html_local/assets/images/american_hypercars_fleet.png');background-size:cover;background-position:center;filter:brightness(0.6)">
                <div class="absolute inset-0 bg-gradient-to-t from-black via-black/80 to-transparent"></div>
            </div>
            
            <div class="relative z-20 max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8">
                <div class="montway-grid items-center">
                    <div>
                        <h1 class="text-4xl md:text-6xl font-extrabold text-white tracking-tight mb-6 leading-tight">
                            Ship Your Car with <br/> <span class="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-blue-500">Absolute Confidence</span>
                        </h1>
                        <p class="text-xl text-gray-300 mb-8 max-w-2xl">
                            Join over 1M+ satisfied customers. We provide zero-upfront deposit, fully insured, door-to-door auto transport nationwide. Get your instant quote today.
                        </p>
                        <div class="flex flex-wrap gap-4 mb-8">
                            <div class="bg-white/10 border border-white/20 rounded-lg p-4 flex items-center gap-3">
                                <span class="text-2xl">⭐</span>
                                <div>
                                    <div class="text-sm text-gray-400">Google Reviews</div>
                                    <div class="font-bold">4.9 / 5.0 Rating</div>
                                </div>
                            </div>
                            <div class="bg-white/10 border border-white/20 rounded-lg p-4 flex items-center gap-3">
                                <span class="text-2xl">🛡️</span>
                                <div>
                                    <div class="text-sm text-gray-400">Protection</div>
                                    <div class="font-bold">100% Insured</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- INJECT THE LIVE QUOTE CALCULATOR HERE -->
                    <div class="w-full">
                        {quote_calc_str}
                    </div>
                </div>
            </div>
        </section>

        <!-- MONTWAY DENSE DATA SECTION -->
        <section class="py-20 bg-zinc-950">
            <div class="max-w-[1200px] mx-auto px-4">
                <div class="text-center mb-16">
                    <h2 class="text-3xl md:text-5xl font-bold mb-4">How Auto Transport Works</h2>
                    <p class="text-gray-400 text-lg">A seamless, 3-step process designed for zero friction.</p>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                    <div class="bg-zinc-900/60 border border-white/10 rounded-2xl p-8">
                        <div class="text-emerald-400 font-extrabold text-4xl mb-4">01</div>
                        <h3 class="text-xl font-bold mb-3">Quote & Book Online</h3>
                        <p class="text-gray-400">Use our instant calculator to get a guaranteed price. Book your shipment with $0 upfront. You only pay when your carrier is officially dispatched.</p>
                    </div>
                    <div class="bg-zinc-900/60 border border-white/10 rounded-2xl p-8">
                        <div class="text-emerald-400 font-extrabold text-4xl mb-4">02</div>
                        <h3 class="text-xl font-bold mb-3">We Pick Up Your Vehicle</h3>
                        <p class="text-gray-400">Our vetted, fully insured carrier will arrive at your door. We perform a full 22-point inspection before loading your vehicle onto the transport.</p>
                    </div>
                    <div class="bg-zinc-900/60 border border-white/10 rounded-2xl p-8">
                        <div class="text-emerald-400 font-extrabold text-4xl mb-4">03</div>
                        <h3 class="text-xl font-bold mb-3">Receive Your Car</h3>
                        <p class="text-gray-400">Track your vehicle in real-time. Upon delivery, perform a final inspection and pay the remaining balance directly to the driver.</p>
                    </div>
                </div>
            </div>
        </section>
        
        <section class="py-20 bg-black">
            <div class="max-w-[1000px] mx-auto px-4">
                <h2 class="text-3xl font-bold mb-8 text-center">Frequently Asked Questions</h2>
                <div class="space-y-4">
                    <div class="bg-zinc-900/40 border border-white/10 rounded-xl p-6">
                        <h4 class="font-bold text-lg mb-2">Can I put personal items in my car?</h4>
                        <p class="text-gray-400">Yes, you may place up to 100 lbs of personal items in the trunk of the vehicle. Items must be secured in a box or suitcase. The carrier's insurance does not cover personal items.</p>
                    </div>
                    <div class="bg-zinc-900/40 border border-white/10 rounded-xl p-6">
                        <h4 class="font-bold text-lg mb-2">What is the difference between open and enclosed transport?</h4>
                        <p class="text-gray-400">Open transport is the industry standard—it is safe, cost-effective, and exposes your car to the same elements it would face driving on the highway. Enclosed transport utilizes a fully covered trailer to protect high-value, exotic, or classic vehicles from all weather and road debris.</p>
                    </div>
                </div>
            </div>
        </section>

    </main>

    {footer_str}
</body>
</html>"""

with open(os.path.join(base_dir, 'competitor_mockups', 'montway_layout', 'index.html'), 'w', encoding='utf-8') as f:
    f.write(montway_index)

# ---------------------------------------------------------
# 2. MONTWAY LAYOUT (State Template - CA)
# ---------------------------------------------------------
montway_state = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <title>California Auto Transport | Sky Auto Services</title>
    {head_html}
    <style>
        .montway-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }}
        @media (max-width: 1024px) {{ .montway-grid {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body class="__className_f367f3 bg-black text-white antialiased">
    {nav_str}
    
    <main class="min-h-screen bg-black pt-28">
        <!-- CA STATE HERO -->
        <section class="relative w-full py-20">
            <div class="absolute inset-0 z-0 opacity-50" style="background-image:url('https://images.unsplash.com/photo-1449034446853-66c86144b0ad?auto=format&fit=crop&q=80');background-size:cover;background-position:center;filter:brightness(0.6)">
                <div class="absolute inset-0 bg-gradient-to-t from-black via-black/80 to-transparent"></div>
            </div>
            
            <div class="relative z-20 max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8">
                <div class="montway-grid items-center">
                    <div>
                        <h1 class="text-4xl md:text-6xl font-extrabold text-white tracking-tight mb-6 leading-tight">
                            California <br/> <span class="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-blue-500">Auto Transport</span>
                        </h1>
                        <p class="text-xl text-gray-300 mb-8 max-w-2xl">
                            Whether you're moving to Los Angeles, San Francisco, or San Diego, Sky Auto Services provides the most reliable California car shipping network.
                        </p>
                    </div>
                    
                    <div class="w-full">
                        {quote_calc_str}
                    </div>
                </div>
            </div>
        </section>

        <!-- CA ROUTE DATA SECTION -->
        <section class="py-20 bg-zinc-950">
            <div class="max-w-[1000px] mx-auto px-4">
                <h2 class="text-3xl font-bold mb-6">Shipping a Car to or from California</h2>
                <p class="text-gray-400 text-lg mb-8 leading-relaxed">
                    California is the largest auto transport hub in the United States. With major logistics corridors like Interstate 5 running north-to-south, and I-10 bridging the coast to Florida, our carriers navigate the Golden State daily. 
                </p>
                
                <div class="bg-zinc-900/60 border border-white/10 rounded-2xl overflow-hidden shadow-2xl">
                    <table class="w-full text-left">
                        <thead class="bg-black/50 border-b border-white/10">
                            <tr>
                                <th class="p-4 text-emerald-400 font-bold uppercase text-sm tracking-wider">Popular Route</th>
                                <th class="p-4 text-emerald-400 font-bold uppercase text-sm tracking-wider">Distance</th>
                                <th class="p-4 text-emerald-400 font-bold uppercase text-sm tracking-wider">Est. Transit Time</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-white/10">
                            <tr class="hover:bg-white/5">
                                <td class="p-4 text-gray-200">Los Angeles, CA ➔ New York, NY</td>
                                <td class="p-4 text-gray-400">2,790 miles</td>
                                <td class="p-4 text-gray-400">7-9 Days</td>
                            </tr>
                            <tr class="hover:bg-white/5">
                                <td class="p-4 text-gray-200">San Francisco, CA ➔ Austin, TX</td>
                                <td class="p-4 text-gray-400">1,760 miles</td>
                                <td class="p-4 text-gray-400">4-6 Days</td>
                            </tr>
                            <tr class="hover:bg-white/5">
                                <td class="p-4 text-gray-200">San Diego, CA ➔ Miami, FL</td>
                                <td class="p-4 text-gray-400">2,650 miles</td>
                                <td class="p-4 text-gray-400">6-8 Days</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </section>
    </main>

    {footer_str}
</body>
</html>"""

with open(os.path.join(base_dir, 'competitor_mockups', 'montway_layout', 'state_template.html'), 'w', encoding='utf-8') as f:
    f.write(montway_state)


# ---------------------------------------------------------
# 3. SHERPA LAYOUT (Homepage)
# ---------------------------------------------------------
# Sherpa centers the quote calculator massively on the hero image.
sherpa_index = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <title>Sky Auto Services | Sherpa Layout</title>
    {head_html}
</head>
<body class="__className_f367f3 bg-black text-white antialiased">
    {nav_str}
    
    <main class="min-h-screen bg-black pt-28">
        <!-- SHERPA CENTRAL HERO -->
        <section class="relative w-full py-24 flex flex-col items-center justify-center min-h-[85vh]">
            <div class="absolute inset-0 z-0 opacity-50" style="background-image:url('../../public_html_local/assets/images/american_hypercars_fleet.png');background-size:cover;background-position:center;filter:brightness(0.6)">
                <div class="absolute inset-0 bg-gradient-to-t from-black via-black/50 to-black"></div>
            </div>
            
            <div class="relative z-20 w-full max-w-5xl mx-auto px-4 text-center">
                <h1 class="text-4xl md:text-7xl font-extrabold text-white tracking-tight mb-4">
                    The Sky Auto <span class="text-emerald-400">Price Lock</span> Promise
                </h1>
                <p class="text-xl md:text-2xl text-gray-300 mb-12">
                    Data-driven pricing. No hidden fees. Zero bait-and-switch tactics.
                </p>
                
                <!-- INJECT LIVE QUOTE CALCULATOR CENTERED -->
                <div class="max-w-[1000px] mx-auto text-left">
                    {quote_calc_str}
                </div>
                
                <div class="mt-8 inline-block bg-emerald-500/10 border border-emerald-400/30 text-emerald-400 font-bold px-6 py-3 rounded-full text-sm uppercase tracking-wider backdrop-blur-md">
                    🛡️ Backed by our 100% Price Lock Guarantee
                </div>
            </div>
        </section>

        <!-- SHERPA DATA PRICING SECTION -->
        <section class="py-24 bg-zinc-950">
            <div class="max-w-6xl mx-auto px-4">
                <div class="text-center mb-16">
                    <h2 class="text-3xl md:text-5xl font-bold mb-4">How We Calculate Your Rate</h2>
                    <p class="text-gray-400 text-lg max-w-3xl mx-auto">
                        Unlike traditional brokers who "guess" market rates, our algorithm analyzes historical load board data, current fuel indexes, and seasonal carrier demand to guarantee a price that moves your car without delays.
                    </p>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
                    <div>
                        <div class="space-y-8">
                            <div class="flex gap-4">
                                <div class="w-12 h-12 rounded-full bg-blue-500/20 text-blue-400 flex items-center justify-center font-bold text-xl shrink-0">1</div>
                                <div>
                                    <h4 class="text-xl font-bold text-white mb-2">Distance & Route Geometry</h4>
                                    <p class="text-gray-400">Pricing scales inversely with distance. Short regional trips (0-500 miles) average $1.00/mile, while cross-country routes (2000+ miles) drop closer to $0.40/mile due to highway efficiency.</p>
                                </div>
                            </div>
                            <div class="flex gap-4">
                                <div class="w-12 h-12 rounded-full bg-blue-500/20 text-blue-400 flex items-center justify-center font-bold text-xl shrink-0">2</div>
                                <div>
                                    <h4 class="text-xl font-bold text-white mb-2">Vehicle Size & Weight</h4>
                                    <p class="text-gray-400">SUVs and trucks occupy more physical space and weight capacity on a hauler, slightly increasing the fuel burden and therefore the rate compared to standard sedans.</p>
                                </div>
                            </div>
                            <div class="flex gap-4">
                                <div class="w-12 h-12 rounded-full bg-blue-500/20 text-blue-400 flex items-center justify-center font-bold text-xl shrink-0">3</div>
                                <div>
                                    <h4 class="text-xl font-bold text-white mb-2">Seasonality (Snowbird Routes)</h4>
                                    <p class="text-gray-400">During Winter, routes heading South (NY to FL) experience massive demand spikes, driving rates up. In Spring, the reverse occurs.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="bg-zinc-900/80 border border-white/10 p-8 rounded-3xl shadow-2xl">
                        <h3 class="text-2xl font-bold mb-6 text-center border-b border-white/10 pb-4">Average Market Rates</h3>
                        <table class="w-full text-left">
                            <thead class="text-gray-400 text-sm uppercase">
                                <tr>
                                    <th class="py-3">Mileage Bracket</th>
                                    <th class="py-3">Est. Cost</th>
                                    <th class="py-3 text-right">Per Mile</th>
                                </tr>
                            </thead>
                            <tbody class="text-white divide-y divide-white/10">
                                <tr><td class="py-4">0 - 500 Miles</td><td class="py-4">$450 - $650</td><td class="py-4 text-right text-emerald-400">$1.05</td></tr>
                                <tr><td class="py-4">500 - 1,000 Miles</td><td class="py-4">$650 - $950</td><td class="py-4 text-right text-emerald-400">$0.85</td></tr>
                                <tr><td class="py-4">1,000 - 2,000 Miles</td><td class="py-4">$950 - $1,350</td><td class="py-4 text-right text-emerald-400">$0.65</td></tr>
                                <tr><td class="py-4">2,000+ Miles</td><td class="py-4">$1,200 - $1,650</td><td class="py-4 text-right text-emerald-400">$0.55</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </section>

    </main>

    {footer_str}
</body>
</html>"""

with open(os.path.join(base_dir, 'competitor_mockups', 'sherpa_layout', 'index.html'), 'w', encoding='utf-8') as f:
    f.write(sherpa_index)


# ---------------------------------------------------------
# 4. SHERPA LAYOUT (State Template - TX)
# ---------------------------------------------------------
sherpa_state = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <title>Texas Auto Transport | Sky Auto Services</title>
    {head_html}
</head>
<body class="__className_f367f3 bg-black text-white antialiased">
    {nav_str}
    
    <main class="min-h-screen bg-black pt-28">
        <!-- TX STATE HERO -->
        <section class="relative w-full py-24 flex flex-col items-center justify-center min-h-[75vh]">
            <div class="absolute inset-0 z-0 opacity-50" style="background-image:url('https://images.unsplash.com/photo-1531218150217-5afc73bf2ae9?auto=format&fit=crop&q=80');background-size:cover;background-position:center;filter:brightness(0.5)">
                <div class="absolute inset-0 bg-gradient-to-t from-black via-black/60 to-black"></div>
            </div>
            
            <div class="relative z-20 w-full max-w-5xl mx-auto px-4 text-center">
                <h1 class="text-4xl md:text-7xl font-extrabold text-white tracking-tight mb-4">
                    Texas <span class="text-emerald-400">Auto Transport</span>
                </h1>
                <p class="text-xl text-gray-300 mb-10 max-w-2xl mx-auto">
                    Direct shipping to Dallas, Houston, and Austin. Backed by the Sky Auto Price Lock Promise.
                </p>
                
                <div class="max-w-[900px] mx-auto text-left">
                    {quote_calc_str}
                </div>
            </div>
        </section>

        <!-- TX DATA SECTION -->
        <section class="py-20 bg-zinc-950">
            <div class="max-w-5xl mx-auto px-4">
                <div class="bg-zinc-900/60 border border-white/10 p-10 rounded-[2rem] shadow-2xl mb-12">
                    <h2 class="text-3xl font-bold mb-6">Navigating the Texas Triangle</h2>
                    <p class="text-gray-400 text-lg leading-relaxed mb-6">
                        Texas spans over 800 miles across. Over 70% of our Texas shipments are routed through the "Texas Triangle" (Dallas-Fort Worth, Houston, San Antonio, and Austin). Because carrier volume is exceptionally high in these hubs, we offer expedited pickups and highly competitive rates for these cities.
                    </p>
                    <p class="text-gray-400 text-lg leading-relaxed">
                        <strong>Open vs. Enclosed in TX:</strong> While Open Transport is standard, the intense Texas summer heat and sudden hail storms prompt many luxury and classic car owners to opt for our premium Enclosed Transport service.
                    </p>
                </div>

                <h3 class="text-2xl font-bold mb-6 text-center">Average Texas Transport Costs</h3>
                <div class="bg-black border border-white/10 rounded-2xl overflow-hidden">
                    <table class="w-full text-left">
                        <thead class="bg-white/5 border-b border-white/10">
                            <tr>
                                <th class="p-4 text-gray-400 font-bold uppercase text-xs">Route</th>
                                <th class="p-4 text-gray-400 font-bold uppercase text-xs">Transit</th>
                                <th class="p-4 text-gray-400 font-bold uppercase text-xs">Open Rate</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-white/10 text-gray-300 text-sm md:text-base">
                            <tr class="hover:bg-white/5">
                                <td class="p-4 font-semibold text-white">Dallas, TX ➔ Los Angeles, CA</td>
                                <td class="p-4">4 - 6 Days</td>
                                <td class="p-4 text-emerald-400 font-bold">$850 - $1,150</td>
                            </tr>
                            <tr class="hover:bg-white/5">
                                <td class="p-4 font-semibold text-white">Houston, TX ➔ Miami, FL</td>
                                <td class="p-4">3 - 5 Days</td>
                                <td class="p-4 text-emerald-400 font-bold">$750 - $950</td>
                            </tr>
                            <tr class="hover:bg-white/5">
                                <td class="p-4 font-semibold text-white">Austin, TX ➔ Chicago, IL</td>
                                <td class="p-4">3 - 5 Days</td>
                                <td class="p-4 text-emerald-400 font-bold">$800 - $1,050</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

    </main>

    {footer_str}
</body>
</html>"""

with open(os.path.join(base_dir, 'competitor_mockups', 'sherpa_layout', 'state_template.html'), 'w', encoding='utf-8') as f:
    f.write(sherpa_state)

print("Phase 3 UI Extraction and Rebuild Complete!")
