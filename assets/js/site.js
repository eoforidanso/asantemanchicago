// Mobile nav toggle
const toggle = document.querySelector('.nav-toggle');
const nav = document.querySelector('.nav');
if (toggle && nav) {
  toggle.addEventListener('click', () => {
    nav.style.top = document.querySelector('.site-header').getBoundingClientRect().bottom + 'px';
    const open = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', open);
    document.body.style.overflow = open ? 'hidden' : '';
  });
}

// Reveal sections as they scroll into view
const els = document.querySelectorAll('.reveal');
if ('IntersectionObserver' in window) {
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -8% 0px' });
  window.__io = io;
  els.forEach((el) => io.observe(el));
} else {
  els.forEach((el) => el.classList.add('in'));
}

// Footer year
document.querySelectorAll('[data-year]').forEach((el) => { el.textContent = new Date().getFullYear(); });

// Forms: until a form service is connected, turn the answers into an email
// in the visitor's own mail app, addressed to the association.
document.querySelectorAll('form[data-mailto]').forEach((form) => {
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const lines = [];
    form.querySelectorAll('input, select, textarea').forEach((el) => {
      if (!el.name || el.type === 'submit') return;
      const label = el.dataset.label || el.closest('label')?.querySelector('span')?.textContent.replace('*', '').trim() || el.name;
      if (el.type === 'checkbox') { if (el.checked) lines.push(`${label}: Yes`); return; }
      if (el.value.trim()) lines.push(`${label}: ${el.value.trim()}`);
    });
    const subject = form.dataset.subject || 'Website enquiry';
    const href = `mailto:${form.dataset.mailto}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(lines.join('\n'))}`;
    window.location.href = href;
    const status = form.querySelector('.form-status');
    if (status) status.classList.add('show');
  });
});

/* ==========================================================
   2026 pass: header, staggered reveals, statement, counters,
   Akan day-name finder, court explorer
   ========================================================== */
const reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

// Header hairline once the page scrolls
const siteHeader = document.querySelector('.site-header');
if (siteHeader) {
  const onScroll = () => siteHeader.classList.toggle('scrolled', window.scrollY > 8);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
}

// Stagger children of [data-stagger]
document.querySelectorAll('[data-stagger]').forEach((group) => {
  [...group.children].forEach((child, i) => {
    child.classList.add('reveal');
    child.style.setProperty('--d', `${Math.min(i, 6) * 50}ms`);
    if (window.__io) window.__io.observe(child); else child.classList.add('in');
  });
});

// Statement: words light up with scroll
const statement = document.querySelector('.statement');
if (statement) {
  const words = statement.textContent.trim().split(/\s+/);
  statement.textContent = '';
  const spans = words.map((w) => {
    const s = document.createElement('span');
    s.className = 'w';
    s.textContent = w;
    statement.append(s, ' ');
    return s;
  });
  const paint = () => {
    if (reduceMotion) { spans.forEach((s) => s.classList.add('lit')); return; }
    const r = statement.getBoundingClientRect();
    const vh = window.innerHeight;
    const p = Math.min(1, Math.max(0, (vh * 0.85 - r.top) / (vh * 0.35 + r.height)));
    const n = Math.round(p * spans.length);
    spans.forEach((s, i) => s.classList.toggle('lit', i < n));
  };
  paint();
  window.addEventListener('scroll', paint, { passive: true });
  window.addEventListener('resize', paint);
}

// Count-up numbers
const counters = document.querySelectorAll('.count[data-count]');
if (counters.length && 'IntersectionObserver' in window && !reduceMotion) {
  const fmt = (n) => Math.round(n).toLocaleString('en-US');
  counters.forEach((c) => { c.textContent = (c.dataset.prefix || '') + '0'; });
  const co = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (!e.isIntersecting) return;
      const el = e.target, to = Number(el.dataset.count), start = performance.now(), dur = 1100;
      const tick = (t) => {
        const k = Math.min(1, (t - start) / dur), eased = 1 - Math.pow(1 - k, 3);
        el.textContent = (el.dataset.prefix || '') + fmt(to * eased);
        if (k < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
      co.unobserve(el);
    });
  }, { threshold: 0.6 });
  counters.forEach((c) => co.observe(c));
}

// Akan day-name finder
const finderInput = document.getElementById('birthdate');
if (finderInput) {
  const DAYS = [
    { en: 'Sunday', tw: 'Kwasiada', m: 'Kwasi', f: 'Akosua' },
    { en: 'Monday', tw: 'Dwoada', m: 'Kwadwo', f: 'Adwoa' },
    { en: 'Tuesday', tw: 'Benada', m: 'Kwabena', f: 'Abena' },
    { en: 'Wednesday', tw: 'Wukuada', m: 'Kwaku', f: 'Akua' },
    { en: 'Thursday', tw: 'Yawoada', m: 'Yaw', f: 'Yaa' },
    { en: 'Friday', tw: 'Fiada', m: 'Kofi', f: 'Afua' },
    { en: 'Saturday', tw: 'Memeneda', m: 'Kwame', f: 'Ama' },
  ];
  const out = document.getElementById('finder-out');
  finderInput.addEventListener('input', () => {
    const v = finderInput.value;
    if (!v) return;
    const [y, m, d] = v.split('-').map(Number);
    const day = DAYS[new Date(y, m - 1, d).getDay()];
    out.innerHTML = `<div class="finder-day">${day.tw}</div>
      <p class="finder-sub">Born on a ${day.en}</p>
      <div class="finder-names"><div><small>If a boy</small><b>${day.m}</b></div><div><small>If a girl</small><b>${day.f}</b></div></div>`;
    out.classList.remove('pop'); void out.offsetWidth; out.classList.add('pop');
  });
}

// Court explorer
const courtData = document.getElementById('court-data');
const divsEl = document.querySelector('.divs');
if (courtData && divsEl) {
  const data = JSON.parse(courtData.textContent);
  const panel = document.querySelector('.div-panel');
  const render = (i) => {
    const d = data[i];
    divsEl.querySelectorAll('button').forEach((b, j) => b.setAttribute('aria-selected', String(j === i)));
    panel.innerHTML = `<div class="div-copy"><h3>${d.name}</h3><p class="role">${d.role}</p><p>${d.blurb}</p></div>
      <div class="div-people">${d.people.map((p) => `<div class="seat"><div class="seat-frame"><img src="${p.photo}" alt="${p.name}" width="315" height="350"></div><div class="stool-title">${p.title}</div><h3>${p.name}</h3></div>`).join('')}</div>`;
    panel.classList.remove('swap'); void panel.offsetWidth; panel.classList.add('swap');
  };
  data.forEach((d, i) => {
    const b = document.createElement('button');
    b.type = 'button'; b.role = 'tab'; b.textContent = d.name;
    b.addEventListener('click', () => render(i));
    divsEl.appendChild(b);
  });
  render(0);
}

// Tabs (3D keys): click or arrow keys
document.querySelectorAll('[data-tabs]').forEach((root) => {
  const tabs = [...root.querySelectorAll('[role="tab"]')];
  const panels = tabs.map((t) => document.getElementById(t.getAttribute('aria-controls')));
  const show = (i) => tabs.forEach((t, j) => {
    t.setAttribute('aria-selected', String(i === j));
    t.tabIndex = i === j ? 0 : -1;
    panels[j].hidden = i !== j;
  });
  tabs.forEach((t, i) => {
    t.addEventListener('click', () => show(i));
    t.addEventListener('keydown', (e) => {
      if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
      const n = (i + (e.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length;
      show(n); tabs[n].focus();
    });
  });
  show(0);
});

// Gallery lightbox
const lb = document.getElementById('lightbox');
if (lb) {
  const shots = [...document.querySelectorAll('.shot')];
  const img = lb.querySelector('img'), cap = lb.querySelector('figcaption');
  let cur = 0;
  const open = (i) => {
    cur = (i + shots.length) % shots.length;
    const s = shots[cur], t = s.querySelector('img');
    img.src = s.dataset.large; img.alt = t.alt; cap.textContent = t.alt;
    if (!lb.open) lb.showModal();
  };
  shots.forEach((s, i) => s.addEventListener('click', () => open(i)));
  lb.querySelector('.lb-close').addEventListener('click', () => lb.close());
  lb.querySelector('.lb-prev').addEventListener('click', () => open(cur - 1));
  lb.querySelector('.lb-next').addEventListener('click', () => open(cur + 1));
  lb.addEventListener('click', (e) => { if (e.target === lb) lb.close(); });
  lb.addEventListener('keydown', (e) => { if (e.key === 'ArrowRight') open(cur + 1); if (e.key === 'ArrowLeft') open(cur - 1); });
}

// Offline support and "Add to Home Screen" (progressive web app)
if ('serviceWorker' in navigator && (location.protocol === 'https:' || location.hostname === 'localhost' || location.hostname === '127.0.0.1')) {
  window.addEventListener('load', () => { navigator.serviceWorker.register('sw.js').catch(() => {}); });
}

/* ==========================================================
   Hero slides: a slow crossfade between five photographs.
   Pauses on hover and focus, has a visible pause button, does not
   autoplay with reduced motion, and swipes on touch screens.
   ========================================================== */
(() => {
  const root = document.getElementById('hr-slides');
  if (!root) return;
  const slides = [...root.querySelectorAll('.hr-slide')];
  const dotsEl = document.querySelector('.hr-dots');
  const lab = document.querySelector('[data-hr-label]');
  const cap = document.querySelector('[data-hr-cap]');
  const pauseBtn = document.querySelector('.hr-pause');
  const hero = root.closest('.hero');
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let cur = 0, timer = null, paused = false;

  const dots = slides.map((s, i) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.setAttribute('aria-label', `Slide ${i + 1} of ${slides.length}: ${s.dataset.label}, ${s.dataset.cap}`);
    b.addEventListener('click', () => { go(i); restart(); });
    dotsEl.appendChild(b);
    return b;
  });
  function go(i) {
    cur = (i + slides.length) % slides.length;
    slides.forEach((s, j) => { s.classList.toggle('is-on', j === cur); s.setAttribute('aria-hidden', String(j !== cur)); });
    dots.forEach((d, j) => d.setAttribute('aria-current', String(j === cur)));
    lab.textContent = slides[cur].dataset.label;
    cap.textContent = slides[cur].dataset.cap;
  }
  const stop = () => { clearInterval(timer); timer = null; };
  const start = () => { if (reduce || paused || timer || document.hidden) return; timer = setInterval(() => go(cur + 1), 7000); };
  const restart = () => { stop(); start(); };

  pauseBtn.addEventListener('click', () => {
    paused = !paused;
    pauseBtn.textContent = paused ? 'Play' : 'Pause';
    pauseBtn.setAttribute('aria-label', paused ? 'Play the slideshow' : 'Pause the slideshow');
    paused ? stop() : start();
  });
  hero.addEventListener('mouseenter', stop);
  hero.addEventListener('mouseleave', start);
  hero.addEventListener('focusin', stop);
  hero.addEventListener('focusout', start);
  document.addEventListener('visibilitychange', () => (document.hidden ? stop() : start()));
  let x0 = null;
  hero.addEventListener('touchstart', (e) => { x0 = e.touches[0].clientX; }, { passive: true });
  hero.addEventListener('touchend', (e) => {
    if (x0 === null) return;
    const dx = e.changedTouches[0].clientX - x0; x0 = null;
    if (Math.abs(dx) > 50) { go(cur + (dx < 0 ? 1 : -1)); restart(); }
  }, { passive: true });

  go(0);
  if (reduce) pauseBtn.hidden = true;
  start();
})();

/* Newsletter forms that post to a service (not the email-app fallback) */
document.querySelectorAll('form.newsletter:not([data-mailto])').forEach((f) => {
  f.addEventListener('submit', () => f.querySelector('.form-status')?.classList.add('show'));
});

/* Exit pop-up: desktop only, once per 30 days, never in the first 10 seconds,
   never on forms or the donate page, and never again after subscribing. */
(() => {
  const pop = document.getElementById('exit-pop');
  if (!pop || document.body.hasAttribute('data-noexit') || typeof pop.showModal !== 'function') return;
  if (!window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;
  const KEY = 'aacm-exit-until';
  const remember = (days) => { try { localStorage.setItem(KEY, String(Date.now() + days * 864e5)); } catch (e) {} };
  try { if (Number(localStorage.getItem(KEY)) > Date.now()) return; } catch (e) {}
  const born = Date.now();
  let shown = false;
  document.addEventListener('mouseout', (e) => {
    if (shown || e.relatedTarget || e.clientY > 0) return;
    if (Date.now() - born < 10000 || document.querySelector('dialog[open]')) return;
    shown = true; pop.showModal(); remember(30);
  });
  pop.querySelectorAll('.exit-close, .exit-skip').forEach((b) => b.addEventListener('click', () => pop.close()));
  pop.addEventListener('click', (e) => { if (e.target === pop) pop.close(); });
  pop.querySelector('form')?.addEventListener('submit', () => { remember(365); setTimeout(() => pop.close(), 2200); });
})();
