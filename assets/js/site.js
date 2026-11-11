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
