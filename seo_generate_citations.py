import csv
import os

CITATION_TARGETS = [
    "Google Business Profile",
    "Bing Places for Business",
    "Yelp for Business",
    "Apple Maps Connect",
    "Yellow Pages",
    "BBB",
    "MapQuest",
    "Superpages",
    "Foursquare",
    "Citysearch",
    "Yahoo Local"
]

NAP_DATA = {
    "Business Name": "Sky Auto Services",
    "Address": "Nationwide / USA",
    "Phone (Service)": "(224) 449-0397",
    "Phone (Dispatch)": "(224) 310-1830",
    "Website": "https://www.skyautoservices.com",
    "Primary Category": "Auto Transport",
    "Description": "Premium door-to-door car shipping & enclosed exotic vehicle transport across America. Licensed FMCSA Broker MC-1782670."
}

def generate_citations_csv():
    output_file = "public_html_local/assets/data/citations.csv"
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Write headers
        writer.writerow(["Aggregator/Directory", "Business Name", "Address", "Phone (Service)", "Phone (Dispatch)", "Website", "Primary Category", "Description", "Status"])
        
        # Write rows
        for target in CITATION_TARGETS:
            writer.writerow([
                target,
                NAP_DATA["Business Name"],
                NAP_DATA["Address"],
                NAP_DATA["Phone (Service)"],
                NAP_DATA["Phone (Dispatch)"],
                NAP_DATA["Website"],
                NAP_DATA["Primary Category"],
                NAP_DATA["Description"],
                "Pending Submission"
            ])
            
    print(f"[SUCCESS] Generated citation matrix for {len(CITATION_TARGETS)} high-DA aggregators at {output_file}")

if __name__ == "__main__":
    generate_citations_csv()
