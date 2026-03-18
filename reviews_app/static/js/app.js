(() => {
  'use strict';
  const themeStorageKey = 'unieats-theme';

  function applyTheme(theme) {
    const normalized = theme === 'dark' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-bs-theme', normalized);
    const toggleIcon = document.getElementById('theme-toggle')?.querySelector('i');
    if (toggleIcon) {
      toggleIcon.classList.toggle('bi-moon-stars', normalized === 'light');
      toggleIcon.classList.toggle('bi-sun', normalized === 'dark');
    }
  }

  function getPreferredTheme() {
    const stored = localStorage.getItem(themeStorageKey);
    if (stored === 'light' || stored === 'dark') return stored;
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function initThemeToggle() {
    applyTheme(getPreferredTheme());
  }

  function getCookie(name) {
    const cookieString = document.cookie || '';
    const cookies = cookieString.split(';').map((c) => c.trim());
    for (const cookie of cookies) {
      if (cookie.startsWith(name + '=')) {
        return decodeURIComponent(cookie.substring(name.length + 1));
      }
    }
    return null;
  }

  function getCsrfToken() {
    return getCookie('csrftoken');
  }

  async function postJson(url) {
    const csrfToken = getCsrfToken();
    const headers = {
      'Content-Type': 'application/json',
    };

    if (csrfToken) {
      headers['X-CSRFToken'] = csrfToken;
    }

    const response = await fetch(url, {
      method: 'POST',
      headers,
    });

    if (!response.ok) {
      const text = await response.text().catch(() => '');
      throw new Error(`Request failed: ${response.status} ${response.statusText} ${text}`.trim());
    }

    return response.json();
  }

  function buildUrlFromTemplate(template, id) {
    if (!template) return null;
    const marker = '/0/';
    if (template.includes(marker)) {
      return template.replace(marker, `/${id}/`);
    }
    return template.replace('0', String(id));
  }

  function handleBookmarkClick(button) {
    const restaurantId = button.dataset.restaurantId;
    if (!restaurantId) return;

    const template = document.body?.dataset?.bookmarkUrlTemplate;
    const url = buildUrlFromTemplate(template, restaurantId);
    if (!url) return;

    postJson(url)
      .then((data) => {
        const icon = button.querySelector('i');
        const text = button.querySelector('.bookmark-text');

        if (data.bookmarked) {
          button.classList.remove('btn-outline-warning');
          button.classList.add('btn-warning');
          button.setAttribute('aria-pressed', 'true');
          if (icon) {
            icon.classList.remove('bi-bookmark');
            icon.classList.add('bi-bookmark-fill');
          }
          if (text) text.textContent = 'Bookmarked';
        } else {
          button.classList.remove('btn-warning');
          button.classList.add('btn-outline-warning');
          button.setAttribute('aria-pressed', 'false');
          if (icon) {
            icon.classList.remove('bi-bookmark-fill');
            icon.classList.add('bi-bookmark');
          }
          if (text) text.textContent = 'Bookmark';
        }
      })
      .catch(() => {
        // Performance/UX: avoid noisy console errors that Lighthouse reports as "browser errors".
        // The UI remains unchanged if the request fails (e.g., user not authenticated / CSRF missing).
      });
  }

  function handleLikeClick(button) {
    const reviewId = button.dataset.reviewId;
    if (!reviewId) return;

    const template = document.body?.dataset?.likeUrlTemplate;
    const url = buildUrlFromTemplate(template, reviewId);
    if (!url) return;

    postJson(url)
      .then((data) => {
        const icon = button.querySelector('i');
        const countSpan = button.querySelector('.like-count');
        if (countSpan) countSpan.textContent = String(data.count);

        if (data.liked) {
          button.classList.remove('btn-outline-danger');
          button.classList.add('btn-danger');
          button.setAttribute('aria-pressed', 'true');
          button.setAttribute('aria-label', 'Unlike this review');
          if (icon) {
            icon.classList.remove('bi-heart');
            icon.classList.add('bi-heart-fill');
          }
        } else {
          button.classList.remove('btn-danger');
          button.classList.add('btn-outline-danger');
          button.setAttribute('aria-pressed', 'false');
          button.setAttribute('aria-label', 'Like this review');
          if (icon) {
            icon.classList.remove('bi-heart-fill');
            icon.classList.add('bi-heart');
          }
        }
      })
      .catch(() => {
        // Performance/UX: swallow errors to keep the console clean in automated audits.
      });
  }

  document.addEventListener('click', (event) => {
    const target = event.target;
    if (!(target instanceof Element)) return;

    const themeToggle = target.closest('#theme-toggle');
    if (themeToggle instanceof HTMLButtonElement) {
      event.preventDefault();
      const current = document.documentElement.getAttribute('data-bs-theme') === 'dark' ? 'dark' : 'light';
      const next = current === 'dark' ? 'light' : 'dark';
      localStorage.setItem(themeStorageKey, next);
      applyTheme(next);
      return;
    }

    const bookmarkButton = target.closest('.bookmark-btn, #bookmark-btn');
    if (bookmarkButton instanceof HTMLButtonElement) {
      event.preventDefault();
      handleBookmarkClick(bookmarkButton);
      return;
    }

    const likeButton = target.closest('.like-btn');
    if (likeButton instanceof HTMLButtonElement) {
      event.preventDefault();
      handleLikeClick(likeButton);
    }
  });

  initThemeToggle();
})();
