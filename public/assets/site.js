(() => {
  const toggle = document.querySelector('.menu-toggle');
  const links = document.querySelector('.nav-links');
  if (toggle && links) toggle.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') === 'true';
    toggle.setAttribute('aria-expanded', String(!open));
    links.style.display = open ? '' : 'flex';
  });
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !reduce) {
    const observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) { entry.target.classList.add('is-visible'); observer.unobserve(entry.target); }
    }), {threshold: 0.12, rootMargin: '0px 0px -35px 0px'});
    reveals.forEach(el => observer.observe(el));
  } else reveals.forEach(el => el.classList.add('is-visible'));
  document.querySelectorAll('[data-year]').forEach(el => el.textContent = new Date().getFullYear());
  const form = document.querySelector('#enquiry-form');
  if (form) { const selected = new URLSearchParams(window.location.search).get('type'); const typeSelect = form.querySelector('[name=type]'); if (selected && typeSelect && [...typeSelect.options].some(o => o.value === selected)) typeSelect.value = selected; }
  if (form) form.addEventListener('submit', async event => {
    event.preventDefault();
    const status = form.querySelector('.form-status'); const submit = form.querySelector('button[type=submit]');
    status.textContent = ''; status.className = 'form-status'; submit.disabled = true; submit.textContent = 'Sending…';
    const data = Object.fromEntries(new FormData(form).entries()); data.privacy = form.querySelector('[name=privacy]').checked;
    try {
      const response = await fetch('/api/enquiry', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
      const result = await response.json();
      if (!response.ok || !result.ok) throw new Error(result.message || 'Unable to send your enquiry.');
      status.textContent = result.message; status.classList.add('success'); form.reset();
    } catch (err) { status.textContent = err.message || 'Something went wrong. Please email quoteflowai@gmail.com.'; status.classList.add('error'); }
    finally { submit.disabled = false; submit.textContent = 'Send enquiry'; }
  });
})();
