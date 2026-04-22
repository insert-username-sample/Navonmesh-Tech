import os

projects_dir = 'projects'
files = [f for f in os.listdir(projects_dir) if f.endswith('.html')]

for filename in files:
    path = os.path.join(projects_dir, filename)
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 1. Clean up hero-visual (Unified logo-anim style)
    import re
    hero_pattern = r'<div class="hero-visual".*?>\s*<div style="width: 400px;.*?</div>\s*</div>'
    new_hero = '''<div class="hero-visual reveal reveal-delay-2" style="display: flex; justify-content: flex-end;">
      <div class="logo-anim-wrap" style="width: 360px; height: 360px;">
        <div class="logo-glow"></div>
        <div class="logo-ring"></div>
        <div class="logo-ring-2"></div>
        <img src="../assets/navonmes-white no bg.png" alt="Visual" class="logo-anim">
      </div>
    </div>'''
    html = re.sub(hero_pattern, new_hero, html, flags=re.DOTALL)

    # 2. Benchmark panel (weird box fix)
    benchmark_pattern = r'<div style="padding:48px; background:var\(--bg-card\); border:1px solid var\(--accent\); border-radius:24px;">'
    new_benchmark = '<div class="reveal reveal-delay-3"><div class="benchmark-card">'
    html = html.replace(benchmark_pattern, new_benchmark)
    
    # Close div for benchmark card
    if '<div class="benchmark-card">' in html:
        html = html.replace('</div>\s*</div>\s*</div>\s*</section>', '</div></div></div></div></section>')

    # 3. Inline style cleanup for tech-specs
    html = html.replace('<div class="tech-specs" style="margin-top: 40px; display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 24px;">', '<div class="tech-specs">')
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

print("Done.")
