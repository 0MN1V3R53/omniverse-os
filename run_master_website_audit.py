import os
import re
import json

base_dir = "/Users/silversurfer/Documents/Omniverse2"

results = {
    "project1_skyautoservices": {},
    "project2_executive_audit": {},
    "project3_cyberpunk_console": {},
    "50_states_verification": {},
    "schema_validation": {},
    "performance_indicators": {}
}

# 1. Inspect Project 1 (public_html_local/index.html & sky_next)
p1_index = os.path.join(base_dir, "public_html_local", "index.html")
if os.path.exists(p1_index):
    with open(p1_index, "r", encoding="utf-8") as f:
        content = f.read()
    results["project1_skyautoservices"]["exists"] = True
    results["project1_skyautoservices"]["file_size_bytes"] = len(content)
    results["project1_skyautoservices"]["has_title"] = "<title>" in content
    results["project1_skyautoservices"]["title"] = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE).group(1) if re.search(r"<title>(.*?)</title>", content, re.IGNORECASE) else ""
    results["project1_skyautoservices"]["has_meta_desc"] = 'name="description"' in content
    results["project1_skyautoservices"]["has_shield_logo"] = "assets/images/logo.png" in content or "logo.png" in content
    results["project1_skyautoservices"]["logo_height_css"] = "height: 54px" in content or "height:54px" in content

# 2. Inspect Project 2 (index.html & client_seo_audit_report.html)
p2_index = os.path.join(base_dir, "index.html")
if os.path.exists(p2_index):
    with open(p2_index, "r", encoding="utf-8") as f:
        content = f.read()
    results["project2_executive_audit"]["file_size_bytes"] = len(content)
    # Count states in table and mobile view
    states_found = len(re.findall(r"VPN Node #\d+", content))
    results["project2_executive_audit"]["vpn_nodes_count"] = states_found
    results["project2_executive_audit"]["has_json_ld"] = 'type="application/ld+json"' in content
    results["project2_executive_audit"]["has_aggregate_rating"] = "AggregateRating" in content

# 3. Check 50 US States Verification Dataset
states_list = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia",
    "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland",
    "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
    "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
    "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
]

missing_states = []
if os.path.exists(p2_index):
    with open(p2_index, "r", encoding="utf-8") as f:
        content = f.read()
    for state in states_list:
        if state not in content:
            missing_states.append(state)

results["50_states_verification"]["total_states"] = len(states_list)
results["50_states_verification"]["missing_states"] = missing_states
results["50_states_verification"]["all_50_present"] = len(missing_states) == 0

output_file = os.path.join(base_dir, "master_audit_raw_results.json")
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print("Master Audit Inspection Complete!")
print(json.dumps(results, indent=2))
