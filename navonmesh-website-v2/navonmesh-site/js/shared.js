// Detect depth to handle relative paths for assets/links
const isSubDir = window.location.pathname.includes('/projects/');
const basePath = isSubDir ? '../' : '';

const NAV_HTML = `
<div id="cursor-dot"></div>
<div id="cursor-ring"></div>
<nav class="nav">
  <div class="container nav-container" style="display:flex; align-items:center; justify-content:space-between; width:100%;">
    <a href="${basePath}index.html" class="nav-logo">
      <img src="${basePath}assets/navonmes-white no bg.png" alt="Navonmesh">
      <span>NAVONMESH</span>
    </a>
    <ul class="nav-links">
      <li><a href="${basePath}index.html">Home</a></li>
      <li><a href="${basePath}services.html">Services</a></li>
      <li><a href="${basePath}process.html">Process</a></li>
      <li><a href="${basePath}showcase.html">Portfolio</a></li>
      <li><a href="${basePath}blog.html">Blog</a></li>
      <li><a href="${basePath}about.html">About</a></li>
      <li><a href="${basePath}contact.html">Contact</a></li>
    </ul>
    <div class="nav-right">
      <button class="theme-switch" id="theme-toggle" aria-label="Toggle theme">
        <div class="toggle-icons">
          <span class="moon">🌙</span>
          <span class="sun">☀️</span>
        </div>
      </button>
      <a href="${basePath}contact.html" class="nav-cta">Start a Project</a>
    </div>
  </div>
</nav>`;

const FOOTER_HTML = `
<footer class="footer">
  <div class="container footer-inner">
    <a href="${basePath}index.html" class="footer-logo">
      <img src="${basePath}assets/navonmes-white no bg.png" alt="Navonmesh">
      <span>NAVONMESH</span>
    </a>
    <ul class="footer-links">
      <li><a href="${basePath}index.html">Home</a></li>
      <li><a href="${basePath}services.html">Services</a></li>
      <li><a href="${basePath}process.html">Process</a></li>
      <li><a href="${basePath}showcase.html">Portfolio</a></li>
      <li><a href="${basePath}blog.html">Blog</a></li>
      <li><a href="${basePath}about.html">About</a></li>
      <li><a href="${basePath}contact.html">Contact</a></li>
    </ul>
    <p class="footer-copy">© 2025 Navonmesh · navonmesh.tech</p>
  </div>
</footer>`;


// Theme-based branding logic (Favicon + Logos)
function applyBranding() {
  const isLight = document.body.classList.contains('light');
  const pathPrefix = window.location.pathname.includes('/projects/') ? '../' : '';
  
  // Favicon updates
  let favicon = document.querySelector('link[rel="icon"]');
  if (favicon) {
    favicon.href = isLight ? `${pathPrefix}assets/navonmesh-black.png` : `${pathPrefix}assets/navonmesh-white.png`;
  }

  // Navigation & Footer Logos
  const navFooterLogos = document.querySelectorAll('.nav-logo img, .footer-logo img');
  navFooterLogos.forEach(img => {
    img.src = isLight ? `${pathPrefix}assets/navonmesh black no bg.png` : `${pathPrefix}assets/navonmes-white no bg.png`;
  });

  // Hero Animated Logo (The big one)
  const heroLogo = document.querySelector('.logo-anim');
  if (heroLogo) {
    heroLogo.src = isLight ? `${pathPrefix}assets/navonmesh-black.png` : `${pathPrefix}assets/navonmesh-white.png`;
  }

  // Project Showcase Default Logos
  const defaultLogos = document.querySelectorAll('.default-logo');
  defaultLogos.forEach(img => {
    img.src = isLight ? `${pathPrefix}assets/navonmesh-black.png` : `${pathPrefix}assets/navonmesh-white.png`;
  });
}

// Initial apply
// applyBranding();
// Removed manual injections to prevent duplication with hard-coded HTML
// document.body.insertAdjacentHTML('afterbegin', NAV_HTML);
// document.body.insertAdjacentHTML('beforeend', FOOTER_HTML);


// Apply saved theme before paint
if (localStorage.getItem('nm-theme') === 'light') {
  document.body.classList.add('light');
  applyBranding();
}
