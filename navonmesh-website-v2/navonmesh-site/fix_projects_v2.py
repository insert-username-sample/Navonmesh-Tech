import os
import re

projects_dir = 'projects'
files = [f for f in os.listdir(projects_dir) if f.endswith('.html')]

for filename in files:
    path = os.path.join(projects_dir, filename)
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 1. Broadly replace the hero-visual with the animated logo core
    # Look for the old div style or the partial replacement
    hero_search = r'<div class="hero-visual".*?>.*?<div style="width: 400px;.*?</div>\s*</div>'
    new_hero = '''<div class="hero-visual reveal reveal-delay-2" style="display: flex; justify-content: flex-end;">
      <div class="logo-anim-wrap" style="width: 360px; height: 360px;">
        <div class="logo-glow"></div>
        <div class="logo-ring"></div>
        <div class="logo-ring-2"></div>
        <img src="../assets/navonmes-white no bg.png" alt="Visual" class="logo-anim">
      </div>
    </div>'''
    html = re.sub(hero_search, new_hero, html, flags=re.DOTALL)

    # 2. Fix the Metric Box (Benchmark Card)
    # Target the rigid inline padding/border style
    metric_box_search = r'<div style="padding:48px; background:var\(--bg-card\); border:1px solid var\(--accent\); border-radius:24px;">\s*<div class="metric"><div class="metric-value">(.*?)</div><div class="metric-label">(.*?)</div></div>\s*<div class="metric"><div class="metric-value">(.*?)</div><div class="metric-label">(.*?)</div></div>'
    
    # New semantic structure
    replacement_box = r'''<div class="reveal reveal-delay-3">
        <div class="benchmark-card">
          <h3 class="label" style="margin-bottom: 32px;">Technical Benchmarks</h3>
          <div class="metric">
            <div class="metric-value">\1</div>
            <div class="metric-label">\2</div>
          </div>
          <div class="metric">
            <div class="metric-value">\3</div>
            <div class="metric-label">\4</div>
          </div>
          <div class="benchmark-footer">
            Performance verified via hardware-in-the-loop and synthetic stress testing.
          </div>
        </div>
      </div>'''
    
    html = re.sub(metric_box_search, replacement_box, html, flags=re.DOTALL)

    # 3. Clean up the squashed tech-specs
    html = html.replace('<div class="tech-specs" style="margin-top: 40px; display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 24px;">', '<div class="tech-specs">')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

print("Batch Fix Complete.")
