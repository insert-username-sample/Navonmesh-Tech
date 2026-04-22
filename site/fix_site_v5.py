import os
import re

# Fragments
CURSOR = """
<div id="cursor-dot"></div>
<div id="cursor-ring"></div>
"""

def get_nav(prefix="", active_page=None):
    links = [
        ("Home", "index.html"),
        ("Services", "services.html"),
        ("Process", "process.html"),
        ("Portfolio", "showcase.html"),
        ("Blog", "blog.html"),
        ("About", "about.html"),
        ("Contact", "contact.html")
    ]
    
    links_html = ""
    for label, url in links:
        active_class = ' class="active"' if label == active_page else ""
        links_html += f'      <li><a href="{prefix}{url}"{active_class}>{label}</a></li>\n'

    return f"""
<nav class="nav">
  <div class="container nav-container" style="display:flex; align-items:center; justify-content:space-between; width:100%;">
    <a href="{prefix}index.html" class="nav-logo">
      <img src="{prefix}assets/navonmes-white no bg.png" alt="Navonmesh">
      <span>NAVONMESH</span>
    </a>
    <ul class="nav-links">
{links_html}    </ul>
    <div class="nav-right">
      <button class="theme-switch" id="theme-toggle" aria-label="Toggle theme">
        <div class="toggle-icons">
          <span class="moon">🌙</span>
          <span class="sun">☀️</span>
        </div>
      </button>
      <a href="{prefix}contact.html" class="nav-cta">Start a Project</a>
    </div>
  </div>
</nav>
"""

def get_footer(prefix=""):
    return f"""
<footer class="footer">
  <div class="container footer-inner">
    <a href="{prefix}index.html" class="footer-logo">
      <img src="{prefix}assets/navonmes-white no bg.png" alt="Navonmesh">
      <span>NAVONMESH</span>
    </a>
    <ul class="footer-links">
      <li><a href="{prefix}index.html">Home</a></li>
      <li><a href="{prefix}services.html">Services</a></li>
      <li><a href="{prefix}process.html">Process</a></li>
      <li><a href="{prefix}showcase.html">Portfolio</a></li>
      <li><a href="{prefix}blog.html">Blog</a></li>
      <li><a href="{prefix}about.html">About</a></li>
      <li><a href="{prefix}contact.html">Contact</a></li>
    </ul>
    <p class="footer-copy">© 2026 Navonmesh · navonmesh.tech</p>
  </div>
</footer>

<script src="{prefix}js/shared.js"></script>
<script src="{prefix}js/main.js"></script>
"""

def process_file(filepath, prefix=""):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Determine active page
        active_map = {
            "index.html": "Home",
            "services.html": "Services",
            "process.html": "Process",
            "showcase.html": "Portfolio",
            "blog.html": "Blog",
            "about.html": "About",
            "contact.html": "Contact"
        }
        filename = os.path.basename(filepath)
        active_page = active_map.get(filename)
        if "projects" in filepath:
            active_page = "Portfolio"
        if "projects/blog" in filepath:
            active_page = "Blog"

        # Remove existing injections
        content = re.sub(r'<div id="cursor-dot">.*?</div>', '', content, flags=re.DOTALL)
        content = re.sub(r'<div id="cursor-ring">.*?</div>', '', content, flags=re.DOTALL)
        content = re.sub(r'<nav class="nav">.*?</nav>', '', content, flags=re.DOTALL)
        content = re.sub(r'<footer class="footer">.*?</footer>', '', content, flags=re.DOTALL)
        content = re.sub(r'<script src=".*?shared\.js"></script>', '', content)
        content = re.sub(r'<script src=".*?main\.js"></script>', '', content)
        
        # Inject Cursor + Nav
        nav_block = CURSOR + get_nav(prefix, active_page)
        content = re.sub(r'(<body.*?>)', r'\1' + nav_block, content, count=1, flags=re.IGNORECASE)

        # Inject Footer + Scripts
        footer_block = get_footer(prefix)
        content = re.sub(r'(</body>)', footer_block + r'\1', content, count=1, flags=re.IGNORECASE)

        # Standardize project logos size
        if "logo-anim-wrap" in content:
            content = re.sub(r'(<div class="logo-anim-wrap")\s+style="[^"]*"', r'\1', content, flags=re.IGNORECASE)
            def add_logo_anim_class(m):
                full_tag = m.group(0)
                if 'logo-anim' not in full_tag:
                    if 'class="' in full_tag:
                        return full_tag.replace('class="', 'class="logo-anim ')
                    else:
                        return full_tag.replace('<img ', '<img class="logo-anim" ')
                return full_tag
            content = re.sub(r'<img[^>]*alt="[^"]*Logo"[^>]*>', add_logo_anim_class, content, flags=re.IGNORECASE)

        # Global repairs
        content = content.replace("2025 Navonmesh", "2026 Navonmesh")
        content = content.replace("© 2025", "© 2026")
        
        # Fix relative assets
        if prefix:
            content = re.sub(r'src="(?!(http|/|' + re.escape(prefix) + r'))assets/', f'src="{prefix}assets/', content)
            content = re.sub(r'href="(?!(http|/|' + re.escape(prefix) + r'))css/', f'href="{prefix}css/', content)
            content = re.sub(r'src="(?!(http|/|' + re.escape(prefix) + r'))js/', f'src="{prefix}js/', content)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Processed: {filepath}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

# Root files
root_files = ["index.html", "services.html", "process.html", "showcase.html", "blog.html", "about.html", "contact.html", "newsletter.html"]
for f in root_files:
    path = os.path.join(".", f)
    if os.path.exists(path):
        process_file(path, prefix="")

# Project files
if os.path.exists("projects"):
    for f in os.listdir("projects"):
        filepath = os.path.join("projects", f)
        if os.path.isfile(filepath) and f.endswith(".html"):
            process_file(filepath, prefix="../")

if os.path.exists("projects/blog"):
    for f in os.listdir("projects/blog"):
        filepath = os.path.join("projects/blog", f)
        if os.path.isfile(filepath) and f.endswith(".html"):
            process_file(filepath, prefix="../../")
