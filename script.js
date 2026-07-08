'use strict';

// Header scroll shadow
const header = document.getElementById('header');
if (header) {
  window.addEventListener('scroll', () => {
    header.classList.toggle('scrolled', window.scrollY > 50);
  }, { passive: true });
}

// Mobile menu toggle
const hamburger = document.getElementById('hamburger');
const mobileMenu = document.getElementById('mobileMenu');
if (hamburger && mobileMenu) {
  hamburger.addEventListener('click', () => {
    const isOpen = mobileMenu.classList.toggle('open');
    hamburger.classList.toggle('active', isOpen);
    document.body.style.overflow = isOpen ? 'hidden' : '';
  });

  document.querySelectorAll('.mobile-nav-link').forEach(link => {
    link.addEventListener('click', () => {
      hamburger.classList.remove('active');
      mobileMenu.classList.remove('open');
      document.body.style.overflow = '';
    });
  });
}

// Intersection Observer for fade-in animations
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const siblings = entry.target.parentElement.querySelectorAll('.fade-in:not(.visible)');
        let delay = 0;
        siblings.forEach((sibling, j) => {
          if (sibling === entry.target) delay = j * 80;
        });
        setTimeout(() => entry.target.classList.add('visible'), delay);
        observer.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.08, rootMargin: '0px 0px -40px 0px' }
);
document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));

// Smooth scroll for in-page anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', (e) => {
    const href = anchor.getAttribute('href');
    const target = href.length > 1 ? document.querySelector(href) : null;
    if (target) {
      e.preventDefault();
      const offset = (document.getElementById('header')?.offsetHeight || 72) + 20;
      window.scrollTo({ top: target.offsetTop - offset, behavior: 'smooth' });
    }
  });
});

// Blog category filter
const filterBtns = document.querySelectorAll('.filter-btn');
const blogCards = document.querySelectorAll('.blog-card[data-category]');
if (filterBtns.length) {
  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const category = btn.dataset.category;
      blogCards.forEach(card => {
        const show = category === 'all' || card.dataset.category === category;
        card.style.display = show ? '' : 'none';
      });
    });
  });
}

// Scroll-to-top button
const scrollTopBtn = document.createElement('button');
scrollTopBtn.className = 'scroll-top-btn';
scrollTopBtn.setAttribute('aria-label', 'ページトップへ戻る');
scrollTopBtn.textContent = '↑';
document.body.appendChild(scrollTopBtn);
window.addEventListener('scroll', () => {
  scrollTopBtn.classList.toggle('visible', window.scrollY > 300);
}, { passive: true });
scrollTopBtn.addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});

// Contact form — Formspree
const FORMSPREE_ENDPOINT = 'https://formspree.io/f/xeebwrpz';

const contactForm = document.getElementById('contactForm');
if (contactForm) {
  contactForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    let valid = true;

    contactForm.querySelectorAll('[required]').forEach(field => {
      const empty = !field.value.trim();
      field.style.borderColor = empty ? '#e53e3e' : '';
      if (empty) valid = false;
    });

    const privacy = contactForm.querySelector('#privacy');
    if (privacy && !privacy.checked) {
      valid = false;
      privacy.parentElement.style.color = '#e53e3e';
    }

    if (!valid) return;

    const submitBtn = contactForm.querySelector('.form-submit .btn');
    submitBtn.textContent = '送信中...';
    submitBtn.disabled = true;

    try {
      const res = await fetch(FORMSPREE_ENDPOINT, {
        method: 'POST',
        body: new FormData(contactForm),
        headers: { 'Accept': 'application/json' }
      });

      if (res.ok) {
        submitBtn.textContent = '✓ 送信が完了しました。担当者よりご連絡いたします。';
        submitBtn.style.background = '#376B54';
        contactForm.querySelectorAll('input, select, textarea').forEach(f => f.disabled = true);
      } else {
        throw new Error('server error');
      }
    } catch {
      submitBtn.textContent = '送信に失敗しました。お電話でご連絡ください。';
      submitBtn.style.background = '#e53e3e';
      submitBtn.disabled = false;
    }
  });

  contactForm.querySelectorAll('[required]').forEach(field => {
    field.addEventListener('input', () => { field.style.borderColor = ''; });
  });
}
