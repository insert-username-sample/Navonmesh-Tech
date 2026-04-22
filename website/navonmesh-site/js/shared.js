/* shared.js — injects nav + footer */
const NAV_HTML = `
<div id="cursor-dot"></div>
<div id="cursor-ring"></div>
<nav class="nav">
  <a href="index.html" class="nav-logo">
    <img src="assets/logo.png" alt="Navonmesh">
    NAVONMESH
  </a>
  <ul class="nav-links">
    <li><a href="index.html">Home</a></li>
    <li><a href="services.html">Services</a></li>
    <li><a href="about.html">About</a></li>
    <li><a href="process.html">Process</a></li>
    <li><a href="contact.html">Contact</a></li>
  </ul>
  <a href="contact.html" class="nav-cta">Start a Project</a>
</nav>`;

const FOOTER_HTML = `
<footer class="footer">
  <div class="footer-inner">
    <a href="index.html" class="footer-logo">
      <img src="assets/logo.png" alt="Navonmesh">
      NAVONMESH
    </a>
    <ul class="footer-links">
      <li><a href="index.html">Home</a></li>
      <li><a href="services.html">Services</a></li>
      <li><a href="about.html">About</a></li>
      <li><a href="process.html">Process</a></li>
      <li><a href="contact.html">Contact</a></li>
    </ul>
    <p class="footer-copy">© 2025 Navonmesh · navonmesh.tech</p>
  </div>
</footer>`;

document.body.insertAdjacentHTML('afterbegin', NAV_HTML);
document.body.insertAdjacentHTML('beforeend', FOOTER_HTML);
