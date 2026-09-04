import os
import glob

# Get all page.js files in the app directory, recursively
app_dir = "/Users/silversurfer/Documents/Omniverse2/sky_next/app"
page_files = []
for root, dirs, files in os.walk(app_dir):
    for f in files:
        if f == "page.js":
            page_files.append(os.path.join(root, f))

for file_path in page_files:
    if "quote-widget" in file_path:
        continue
    # Already did the root page.js manually
    if file_path == os.path.join(app_dir, "page.js"):
        continue
        
    with open(file_path, "r") as f:
        content = f.read()
        
    if "QuoteCalculatorWrapper" in content:
        continue
        
    # Insert import statement
    lines = content.split('\n')
    import_idx = 0
    for i, line in enumerate(lines):
        if line.startswith('import '):
            import_idx = i
            
    lines.insert(import_idx + 1, "import QuoteCalculatorWrapper from '@/components/QuoteCalculatorWrapper';")
    
    # Insert the component before </main>
    new_content = '\n'.join(lines)
    if "</main>" in new_content:
        new_content = new_content.replace("</main>", "      <QuoteCalculatorWrapper />\n    </main>")
    else:
        # Some pages might not have <main> or </main>
        print(f"Warning: No </main> found in {file_path}")
        
    with open(file_path, "w") as f:
        f.write(new_content)
    
    print(f"Injected into {file_path}")
