/* Navonmesh — main.js */

// ── Theme toggle ───────────────────────────────────────────
const themeBtn = document.getElementById('theme-toggle');
if (themeBtn) {
  themeBtn.addEventListener('click', () => {
    document.body.classList.toggle('light');
    localStorage.setItem('nm-theme', document.body.classList.contains('light') ? 'light' : 'dark');
    if (typeof applyBranding === 'function') applyBranding();
  });
}

// ── Custom Cursor ──────────────────────────────────────────
const dot  = document.getElementById('cursor-dot');
const ring = document.getElementById('cursor-ring');
if (dot && ring && window.innerWidth > 768) {
  let mx = 0, my = 0, rx = 0, ry = 0;
  document.addEventListener('mousemove', e => {
    mx = e.clientX; my = e.clientY;
    dot.style.left = mx + 'px'; dot.style.top = my + 'px';
  });
  (function lerpRing() {
    rx += (mx - rx) * 0.13; ry += (my - ry) * 0.13;
    ring.style.left = rx + 'px'; ring.style.top = ry + 'px';
    requestAnimationFrame(lerpRing);
  })();
  document.querySelectorAll('a, button, .btn, .service-card, .layer-card, .principle-card, .step-content, .form-input, .form-textarea, .form-submit').forEach(el => {
    el.addEventListener('mouseenter', () => document.body.classList.add('cursor-hover'));
    el.addEventListener('mouseleave', () => document.body.classList.remove('cursor-hover'));
  });
}

// ── Nav scroll ─────────────────────────────────────────────
const nav = document.querySelector('.nav');
if (nav) window.addEventListener('scroll', () => { nav.classList.toggle('scrolled', window.scrollY > 60); }, { passive: true });

// ── Scroll reveal ──────────────────────────────────────────
const revealEls = document.querySelectorAll('.reveal');
if (revealEls.length) {
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { threshold: 0.10 });
  revealEls.forEach(el => io.observe(el));
}

// ── Scroll indicator ───────────────────────────────────────
const scrollInd = document.querySelector('.scroll-indicator');
if (scrollInd) window.addEventListener('scroll', () => { scrollInd.classList.toggle('hidden', window.scrollY > 80); }, { passive: true });

// ── Number counter ─────────────────────────────────────────
function animateCount(el) {
  const target = parseFloat(el.dataset.count);
  const suffix = el.dataset.suffix || '';
  const duration = 1800;
  const start = performance.now();
  (function step(now) {
    const p = Math.min((now - start) / duration, 1);
    const ease = 1 - Math.pow(1 - p, 4);
    const val = target * ease;
    el.textContent = (Number.isInteger(target) ? Math.round(val) : val.toFixed(1)) + suffix;
    if (p < 1) requestAnimationFrame(step);
  })(performance.now());
}
const counters = document.querySelectorAll('[data-count]');
if (counters.length) {
  const co = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) { animateCount(e.target); co.unobserve(e.target); } });
  }, { threshold: 0.5 });
  counters.forEach(c => co.observe(c));
}

// ── Active nav link ────────────────────────────────────────
const currentPage = window.location.pathname.split('/').pop() || 'index.html';
document.querySelectorAll('.nav-links a').forEach(a => {
  if (a.getAttribute('href') === currentPage) a.classList.add('active');
});

// ── Contact form ───────────────────────────────────────────
const form = document.getElementById('contact-form');
if (form) {
  form.addEventListener('submit', async e => {
    e.preventDefault();
    const btn = form.querySelector('.form-submit');
    btn.textContent = 'Sending…'; btn.disabled = true;
    await new Promise(r => setTimeout(r, 1200));
    form.style.display = 'none';
    const success = document.getElementById('form-success');
    if (success) { success.style.display = 'block'; success.classList.add('show'); }
  });
}

// ── Process page: scroll-driven timeline ──────────────────
(function initTimeline() {
  const wrap    = document.querySelector('.timeline-line-wrap');
  const fill    = document.querySelector('.timeline-line-fill');
  const dot     = document.querySelector('.timeline-dot');
  const section = document.querySelector('.timeline-section');
  const nodes   = document.querySelectorAll('.step-node');
  const steps   = document.querySelectorAll('.timeline-step');

  if (!wrap || !fill || !dot || !section) return;

  // Record each step's vertical midpoint relative to the timeline-line-wrap
  function getStepMids() {
    const wrapTop = wrap.getBoundingClientRect().top + window.scrollY;
    return Array.from(steps).map(step => {
      const r = step.getBoundingClientRect();
      return (r.top + window.scrollY + r.height / 2) - wrapTop;
    });
  }

  function onScroll() {
    const wrapRect  = wrap.getBoundingClientRect();
    const wrapH     = wrap.offsetHeight;
    const scrollTop = window.scrollY || document.documentElement.scrollTop;
    
    // The visual "trigger line" for activating steps
    const triggerPoint = window.innerHeight * 0.55; 
    
    // How far we have scrolled past the start of the timeline line
    const scrollInLine = (scrollTop + triggerPoint) - (wrapRect.top + scrollTop);
    
    // Convert to percentage
    let pct = scrollInLine / wrapH;
    pct = Math.max(0, Math.min(1, pct));

    const pctRelative = pct * 100;

    // Move fill and dot
    fill.style.height = pctRelative + '%';
    dot.style.top     = pctRelative + '%';

    // Light up nodes based on their position relative to the scroll progress
    nodes.forEach((node, i) => {
      const nodeTop = node.getBoundingClientRect().top + scrollTop;
      const wrapTopGlobal = wrapRect.top + scrollTop;
      const nodeOffsetPct = ((nodeTop - wrapTopGlobal) / wrapH) * 100;
      node.classList.toggle('lit', pctRelative >= nodeOffsetPct - 2);
    });
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll(); // run once on load
})();
