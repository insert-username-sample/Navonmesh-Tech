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

def process_file(filepath, is_project=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Determine active page based on filename
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
    if is_project:
        active_page = "Portfolio"

    prefix = "../" if is_project else ""

    # 1. Clean existing Nav/Footer/Cursor/Scripts
    content = re.sub(r'<div id="cursor-dot">.*?</div>', '', content, flags=re.DOTALL)
    content = re.sub(r'<div id="cursor-ring">.*?</div>', '', content, flags=re.DOTALL)
    content = re.sub(r'<nav class="nav">.*?</nav>', '', content, flags=re.DOTALL)
    content = re.sub(r'<footer class="footer">.*?</footer>', '', content, flags=re.DOTALL)
    content = re.sub(r'<script src=".*?shared\.js"></script>', '', content)
    content = re.sub(r'<script src=".*?main\.js"></script>', '', content)
    
    # 2. Inject Cursor + Nav
    nav_block = CURSOR + get_nav(prefix, active_page)
    content = re.sub(r'(<body.*?>)', r'\1' + nav_block, content, count=1, flags=re.IGNORECASE)

    # 3. Inject Footer + Scripts
    footer_block = get_footer(prefix)
    content = re.sub(r'(</body>)', footer_block + r'\1', content, count=1, flags=re.IGNORECASE)

    # 4. Global Year Replace
    content = content.replace("2025 Navonmesh", "2026 Navonmesh")
    content = content.replace("© 2025", "© 2026")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Processed: {filepath}")

# Root files
root_files = ["index.html", "services.html", "process.html", "showcase.html", "blog.html", "about.html", "contact.html", "newsletter.html"]
for f in root_files:
    path = os.path.join(".", f)
    if os.path.exists(path):
        process_file(path)

# Project files
project_dir = "projects"
if os.path.exists(project_dir):
    for f in os.listdir(project_dir):
        if f.endswith(".html"):
            process_file(os.path.join(project_dir, f), is_project=True)
