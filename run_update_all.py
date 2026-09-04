import update_route_pages_mobile
from glob import glob
import os

routes_dir = "public_html_local/routes"
files = glob(f"{routes_dir}/*.html")

updated_count = 0
for filepath in files:
    try:
        updated = update_route_pages_mobile.update_file(filepath)
        if updated:
            updated_count += 1
    except Exception as e:
        print(f"Error on {filepath}: {e}")

print(f"Updated {updated_count} files out of {len(files)}.")
