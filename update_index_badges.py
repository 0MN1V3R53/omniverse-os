import os

def update_badges(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # The HTML part
    target_html = '<div class="flex items-center text-xs sm:text-sm font-semibold text-gray-400"><svg class="w-4 h-4 sm:w-5 sm:h-5 text-emerald-400 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 2a4 4 0 00-4 4v1H5a1 1 0 00-.994.89l-1 9A1 1 0 004 18h12a1 1 0 00.994-1.11l-1-9A1 1 0 0015 7h-1V6a4 4 0 00-4-4zm2 5V6a2 2 0 10-4 0v1h4zm-6 3a1 1 0 112 0 1 1 0 01-2 0zm7-1a1 1 0 100 2 1 1 0 000-2z" clip-rule="evenodd"></path></svg>Enclosed Transport Experts</div>'
    
    new_html_badges = """<div class="flex items-center text-xs sm:text-sm font-semibold text-gray-400"><svg class="w-4 h-4 sm:w-5 sm:h-5 text-emerald-400 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 2a4 4 0 00-4 4v1H5a1 1 0 00-.994.89l-1 9A1 1 0 004 18h12a1 1 0 00.994-1.11l-1-9A1 1 0 0015 7h-1V6a4 4 0 00-4-4zm2 5V6a2 2 0 10-4 0v1h4zm-6 3a1 1 0 112 0 1 1 0 01-2 0zm7-1a1 1 0 100 2 1 1 0 000-2z" clip-rule="evenodd"></path></svg>USDOT: 4504932 | MC: 1782670</div><div class="flex items-center text-xs sm:text-sm font-semibold text-gray-400"><svg class="w-4 h-4 sm:w-5 sm:h-5 text-emerald-400 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 2a4 4 0 00-4 4v1H5a1 1 0 00-.994.89l-1 9A1 1 0 004 18h12a1 1 0 00.994-1.11l-1-9A1 1 0 0015 7h-1V6a4 4 0 00-4-4zm2 5V6a2 2 0 10-4 0v1h4zm-6 3a1 1 0 112 0 1 1 0 01-2 0zm7-1a1 1 0 100 2 1 1 0 000-2z" clip-rule="evenodd"></path></svg>Fully Licensed &amp; Bonded Broker</div>"""
    
    if target_html in content and new_html_badges not in content:
        content = content.replace(target_html, target_html + new_html_badges)
        print(f"Updated HTML in {filepath}")
    else:
        print(f"Target HTML not found or already updated in {filepath}")

    # The JSON string part for Next.js hydration payload
    target_json = r'["$","div","1",{"className":"flex items-center text-xs sm:text-sm font-semibold text-gray-400","children":[["$","svg",null,{"className":"w-4 h-4 sm:w-5 sm:h-5 text-emerald-400 mr-2","fill":"currentColor","viewBox":"0 0 20 20","children":["$","path",null,{"fillRule":"evenodd","d":"M10 2a4 4 0 00-4 4v1H5a1 1 0 00-.994.89l-1 9A1 1 0 004 18h12a1 1 0 00.994-1.11l-1-9A1 1 0 0015 7h-1V6a4 4 0 00-4-4zm2 5V6a2 2 0 10-4 0v1h4zm-6 3a1 1 0 112 0 1 1 0 01-2 0zm7-1a1 1 0 100 2 1 1 0 000-2z","clipRule":"evenodd"}]}],"Enclosed Transport Experts"]}]'
    
    new_json_badges = r',["$","div","2",{"className":"flex items-center text-xs sm:text-sm font-semibold text-gray-400","children":[["$","svg",null,{"className":"w-4 h-4 sm:w-5 sm:h-5 text-emerald-400 mr-2","fill":"currentColor","viewBox":"0 0 20 20","children":["$","path",null,{"fillRule":"evenodd","d":"M10 2a4 4 0 00-4 4v1H5a1 1 0 00-.994.89l-1 9A1 1 0 004 18h12a1 1 0 00.994-1.11l-1-9A1 1 0 0015 7h-1V6a4 4 0 00-4-4zm2 5V6a2 2 0 10-4 0v1h4zm-6 3a1 1 0 112 0 1 1 0 01-2 0zm7-1a1 1 0 100 2 1 1 0 000-2z","clipRule":"evenodd"}]}],"USDOT: 4504932 | MC: 1782670"]}],["$","div","3",{"className":"flex items-center text-xs sm:text-sm font-semibold text-gray-400","children":[["$","svg",null,{"className":"w-4 h-4 sm:w-5 sm:h-5 text-emerald-400 mr-2","fill":"currentColor","viewBox":"0 0 20 20","children":["$","path",null,{"fillRule":"evenodd","d":"M10 2a4 4 0 00-4 4v1H5a1 1 0 00-.994.89l-1 9A1 1 0 004 18h12a1 1 0 00.994-1.11l-1-9A1 1 0 0015 7h-1V6a4 4 0 00-4-4zm2 5V6a2 2 0 10-4 0v1h4zm-6 3a1 1 0 112 0 1 1 0 01-2 0zm7-1a1 1 0 100 2 1 1 0 000-2z","clipRule":"evenodd"}]}],"Fully Licensed & Bonded Broker"]}]'
    
    if target_json in content and new_json_badges not in content:
        content = content.replace(target_json, target_json + new_json_badges)
        print(f"Updated JSON payload in {filepath}")
    else:
        print(f"Target JSON payload not found or already updated in {filepath}")
        
    with open(filepath, 'w') as f:
        f.write(content)

update_badges('/Users/silversurfer/Documents/Omniverse2/public_html_local/index.html')
update_badges('/Users/silversurfer/Documents/Omniverse2/hostinger_site/public_html/index.html')
