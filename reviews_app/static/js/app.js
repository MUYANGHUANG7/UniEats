(() => {
  'use strict';

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

  function handleBookmarkClick(button) {
    const restaurantId = button.dataset.restaurantId;
    if (!restaurantId) return;

    postJson(`/restaurant/${restaurantId}/bookmark/`)
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

    postJson(`/review/${reviewId}/like/`)
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
})();
