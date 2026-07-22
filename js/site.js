/* ============================================================
   Todd Shea Real Estate — site behaviour
   ============================================================ */

(function () {
  'use strict';

  /* ---------- Config ----------
     Set ENDPOINT to the URL of the server-side handler that holds the
     Follow Up Boss API key. The key must never live in this file — it
     ships to the browser. Until the endpoint is live, forms fall back
     to a friendly message and log the payload.
  */
  var CONFIG = {
    captureEndpoint: '',              // e.g. https://api.toddshearealtor.com/lead
    instagramEndpoint: '',            // e.g. https://api.toddshearealtor.com/instagram
    instagramProfile: 'https://www.instagram.com/toddshearealtor/'
  };

  /* ---------- Mobile nav ---------- */

  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('nav');

  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.getAttribute('data-open') === 'true';
      nav.setAttribute('data-open', String(!open));
      toggle.setAttribute('aria-expanded', String(!open));
      toggle.textContent = open ? 'Menu' : 'Close';
    });

    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A' && window.innerWidth <= 860) {
        nav.setAttribute('data-open', 'false');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.textContent = 'Menu';
      }
    });
  }

  /* ---------- Testimonial expand / collapse ---------- */

  document.querySelectorAll('[data-quote-toggle]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var body = document.getElementById(btn.getAttribute('aria-controls'));
      if (!body) return;
      var expanded = body.getAttribute('data-expanded') === 'true';
      body.setAttribute('data-expanded', String(!expanded));
      btn.setAttribute('aria-expanded', String(!expanded));
      btn.textContent = expanded ? 'Read more' : 'Read less';
    });
  });

  /* ---------- Off-market / contact capture ----------
     Posts to a server-side endpoint which forwards to Follow Up Boss.
     The FUB API key stays on the server. Never inline it here.
  */

  document.querySelectorAll('[data-capture]').forEach(function (form) {
    var status = form.parentElement.querySelector('[data-capture-status]')
              || document.querySelector('[data-capture-status]');

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      var honeypot = form.querySelector('input[name="company"]');
      if (honeypot && honeypot.value) return;          // bot

      var data = Object.fromEntries(new FormData(form).entries());
      delete data.company;
      data.source = form.getAttribute('data-capture');
      data.page = window.location.pathname;

      var email = (data.email || '').trim();
      if (!email || email.indexOf('@') < 1 || email.lastIndexOf('.') < email.indexOf('@')) {
        say(status, 'Enter a valid email address.', 'error');
        return;
      }

      var btn = form.querySelector('button[type="submit"]');
      if (btn) { btn.disabled = true; btn.dataset.label = btn.textContent; btn.textContent = 'Sending…'; }

      if (!CONFIG.captureEndpoint) {
        console.info('[capture] endpoint not configured — payload:', data);
        say(status, 'Form not connected yet — endpoint pending.', 'ok');
        resetBtn(btn);
        form.reset();
        return;
      }

      fetch(CONFIG.captureEndpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
        .then(function (r) {
          if (!r.ok) throw new Error('Request failed: ' + r.status);
          return r.json().catch(function () { return {}; });
        })
        .then(function () {
          say(status, "You're on the list.", 'ok');
          form.reset();
        })
        .catch(function (err) {
          console.error('[capture]', err);
          say(status, "That didn't go through. Email toddshea@bhhscal.com and I'll add you.", 'error');
        })
        .finally(function () { resetBtn(btn); });
    });
  });

  function say(el, msg, kind) {
    if (!el) return;
    el.textContent = msg;
    el.style.color = kind === 'error' ? 'var(--asphalt)' : 'var(--bone)';
  }

  function resetBtn(btn) {
    if (!btn) return;
    btn.disabled = false;
    if (btn.dataset.label) btn.textContent = btn.dataset.label;
  }

  /* ---------- Instagram feed ----------
     Reads from a server-side endpoint that calls the Instagram Graph API
     with a long-lived token. Token refresh + caching happen server-side;
     the browser only ever sees public post data.
     Expected shape: { data: [ { id, media_url, permalink, caption, media_type } ] }
  */

  var grid = document.querySelector('[data-ig-grid]');

  if (grid && CONFIG.instagramEndpoint) {
    var count = parseInt(grid.getAttribute('data-ig-count'), 10) || 8;

    fetch(CONFIG.instagramEndpoint)
      .then(function (r) {
        if (!r.ok) throw new Error('Instagram request failed: ' + r.status);
        return r.json();
      })
      .then(function (payload) {
        var posts = (payload && payload.data ? payload.data : []).slice(0, count);
        if (!posts.length) return;

        grid.innerHTML = '';
        posts.forEach(function (post) {
          var a = document.createElement('a');
          a.className = 'ig-cell';
          a.href = post.permalink || CONFIG.instagramProfile;
          a.target = '_blank';
          a.rel = 'noopener';

          var img = document.createElement('img');
          img.src = post.media_url || post.thumbnail_url;
          img.loading = 'lazy';
          img.alt = post.caption
            ? post.caption.slice(0, 110).replace(/\s+\S*$/, '') + '…'
            : 'Instagram post from @toddshearealtor';

          a.appendChild(img);
          grid.appendChild(a);
        });
      })
      .catch(function (err) {
        console.error('[instagram]', err);
        // Placeholder cells stay in place on failure — no broken layout.
      });
  }

})();
