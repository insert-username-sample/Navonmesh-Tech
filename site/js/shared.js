/**
 * Navonmesh Shared Script
 * Manages theme state, logo switching, and global UI behaviors.
 */

// Theme-based branding logic (Favicon + Logos)
function applyBranding() {
  const isLight = document.body.classList.contains('light');
  const isSubDir = window.location.pathname.includes('/projects/');
  const pathPrefix = isSubDir ? '../' : '';
  
  // Favicon updates
  let favicon = document.querySelector('link[rel="icon"]');
  if (favicon) {
    favicon.href = isLight ? `${pathPrefix}assets/navonmesh-black.png` : `${pathPrefix}assets/navonmesh-white.png`;
  }

  // Navigation & Footer Logos
  const navFooterLogos = document.querySelectorAll('.nav-logo img, .footer-logo img');
  navFooterLogos.forEach(img => {
    // Only update if it's the main Navonmesh logo
    if (img.alt === 'Navonmesh' || img.src.includes('navonmesh')) {
        img.src = isLight ? `${pathPrefix}assets/navonmesh black no bg.png` : `${pathPrefix}assets/navonmes-white no bg.png`;
    }
  });

  // Hero Animated Logo (The big one)
  // Only update if it's explicitly class 'logo-anim' AND not already set to a project-specific one
  const heroLogo = document.querySelector('.logo-anim');
  if (heroLogo && (heroLogo.alt === 'Navonmesh' || heroLogo.src.includes('navonmesh'))) {
    heroLogo.src = isLight ? `${pathPrefix}assets/navonmesh-black.png` : `${pathPrefix}assets/navonmesh-white.png`;
  }

  // Project Showcase Default Logos
  const defaultLogos = document.querySelectorAll('.default-logo');
  defaultLogos.forEach(img => {
    img.src = isLight ? `${pathPrefix}assets/navonmesh-black.png` : `${pathPrefix}assets/navonmesh-white.png`;
  });
}

// Apply saved theme state immediately to avoid flash
if (localStorage.getItem('nm-theme') === 'light') {
  document.body.classList.add('light');
}

// Run branding apply
applyBranding();

// Listen for custom theme change events (if needed) or DOM content loaded
document.addEventListener('DOMContentLoaded', () => {
    applyBranding();
});
