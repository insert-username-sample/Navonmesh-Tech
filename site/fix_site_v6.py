import os
import re

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        changed = False
        
        # 1. Fix process.html timeline dot
        if "process.html" in filepath:
            # Move dot inside wrap
            if '<div class="timeline-dot"></div>' in content:
                content = content.replace('<div class="timeline-dot"></div>', '')
                content = content.replace('<div class="timeline-line-fill"></div>', 
                                          '<div class="timeline-line-fill"></div>\n    <div class="timeline-dot"></div>')
                changed = True
                print(f"Fixed timeline dot in {filepath}")

        # 2. Audit logos in project pages
        if "projects/" in filepath and filepath.endswith(".html") and "blog/" not in filepath:
            # Ensure the logo-anim exists and has a specific alt
            # In swiftwash, we already have it. Let's make sure others do too.
            # We want to make sure it doesn't have "Navonmesh" in its src or alt unless it's meant to.
            pass

        if changed:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
                
    except Exception as e:
        print(f"Error in {filepath}: {e}")

# Apply to core pages
process_file("process.html")

# Applying to projects
if os.path.exists("projects"):
    for f in os.listdir("projects"):
        if f.endswith(".html"):
            process_file(os.path.join("projects", f))
