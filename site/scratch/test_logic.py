import os

# Check shared.js logic
FILE_CONTENT = """
  const heroLogo = document.querySelector('.logo-anim');
  if (heroLogo && (heroLogo.alt === 'Navonmesh' || heroLogo.src.includes('navonmesh'))) {
    heroLogo.src = isLight ? `${pathPrefix}assets/navonmesh-black.png` : `${pathPrefix}assets/navonmesh-white.png`;
  }
"""

print("Current logic checks for 'navonmesh' in absolute URL.")
print("On navonmesh.in/projects/swiftwash.html, img.src = 'https://navonmesh.in/assets/swiftwash-logo.png'")
print("Result of 'navonmesh' in 'https://navonmesh.in/assets/swiftwash-logo.png':", "navonmesh" in "https://navonmesh.in/assets/swiftwash-logo.png")
