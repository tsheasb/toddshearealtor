/* ============================================================
   Scroll motion — Todd Shea Real Estate

   Three effects, all opt-in via data attributes so nothing moves
   unless it's marked:

     [data-reveal]        fade + rise as the element enters view
     [data-count]         odometer counter for the proof stats
     [data-parallax]      slow drift on the hero media

   Everything is disabled when the visitor has asked for reduced
   motion, and every animated element is visible by default — the
   JS removes visibility, so a JS failure leaves a readable page
   rather than a blank one.
   ============================================================ */

(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)');

  if (reduced.matches || !('IntersectionObserver' in window)) return;

  /* Mark the document so CSS can hide the pre-reveal state only when
     JS is running and motion is welcome. */
  document.documentElement.setAttribute('data-motion', 'on');

  /* ---------- 1. Reveal on enter ---------- */

  var revealObserver = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      var el = entry.target;
      var delay = parseInt(el.getAttribute('data-reveal-delay'), 10) || 0;
      setTimeout(function () { el.setAttribute('data-revealed', 'true'); }, delay);
      revealObserver.unobserve(el);
    });
  }, { rootMargin: '0px 0px -12% 0px', threshold: 0.05 });

  document.querySelectorAll('[data-reveal]').forEach(function (el) {
    revealObserver.observe(el);
  });

  /* ---------- 2. Odometer counters ---------- */

  function animateCount(el) {
    var raw = el.getAttribute('data-count');          // e.g. "116"
    var prefix = el.getAttribute('data-count-prefix') || '';
    var suffix = el.getAttribute('data-count-suffix') || '';
    var target = parseFloat(raw);
    if (isNaN(target)) return;

    var duration = 1400;
    var start = null;

    function easeOutCubic(t) { return 1 - Math.pow(1 - t, 3); }

    function step(ts) {
      if (start === null) start = ts;
      var p = Math.min((ts - start) / duration, 1);
      var value = Math.round(easeOutCubic(p) * target);
      el.textContent = prefix + value + suffix;
      if (p < 1) requestAnimationFrame(step);
      else el.textContent = prefix + target + suffix;
    }
    requestAnimationFrame(step);
  }

  var countObserver = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      animateCount(entry.target);
      countObserver.unobserve(entry.target);
    });
  }, { threshold: 0.4 });

  document.querySelectorAll('[data-count]').forEach(function (el) {
    // Seed with the final value so the number is correct before it animates
    // and if anything goes wrong mid-flight.
    var prefix = el.getAttribute('data-count-prefix') || '';
    var suffix = el.getAttribute('data-count-suffix') || '';
    el.textContent = prefix + el.getAttribute('data-count') + suffix;
    countObserver.observe(el);
  });

  /* ---------- 3. Hero parallax ---------- */

  var parallaxEls = [].slice.call(document.querySelectorAll('[data-parallax]'));

  if (parallaxEls.length) {
    var ticking = false;

    function onScroll() {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        var y = window.pageYOffset;
        parallaxEls.forEach(function (el) {
          var speed = parseFloat(el.getAttribute('data-parallax')) || 0.25;
          var rect = el.parentElement.getBoundingClientRect();
          // Only move while the container is anywhere near the viewport
          if (rect.bottom < -200 || rect.top > window.innerHeight + 200) return;
          el.style.transform = 'translate3d(0,' + (y * speed) + 'px,0)';
        });
        ticking = false;
      });
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }


  /* ---------- 4. Scroll-scaled media ----------
     Property and portrait images drift/scale very slightly while their
     container crosses the viewport. Small numbers on purpose: enough to
     feel alive, not enough to notice as an effect. */

  var scaleEls = [].slice.call(document.querySelectorAll('[data-scroll-scale]'));

  /* ---------- 5. Word-by-word headline ---------- */

  document.querySelectorAll('[data-words]').forEach(function (el) {
    if (el.getAttribute('data-words-done')) return;
    var words = el.textContent.trim().split(/\s+/);
    el.textContent = '';
    words.forEach(function (word, i) {
      var outer = document.createElement('span');
      outer.className = 'word';
      var inner = document.createElement('span');
      inner.className = 'word__inner';
      inner.textContent = word;
      inner.style.transitionDelay = (i * 70) + 'ms';
      outer.appendChild(inner);
      el.appendChild(outer);
      if (i < words.length - 1) el.appendChild(document.createTextNode(' '));
    });
    el.setAttribute('data-words-done', 'true');
  });

  var wordObserver = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      entry.target.setAttribute('data-words-in', 'true');
      wordObserver.unobserve(entry.target);
    });
  }, { threshold: 0.2 });

  document.querySelectorAll('[data-words]').forEach(function (el) {
    wordObserver.observe(el);
  });

  /* ---------- 6. Stripe draw ---------- */

  var stripeObserver = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      entry.target.setAttribute('data-drawn', 'true');
      stripeObserver.unobserve(entry.target);
    });
  }, { threshold: 0.25, rootMargin: '0px 0px -5% 0px' });

  document.querySelectorAll('.stripes').forEach(function (el) {
    stripeObserver.observe(el);
  });

  /* Safety net: if anything hasn't drawn by the time the page has been
     scrolled to the bottom, draw it. Guards against a stripe sitting in
     a container that never crosses the threshold. */
  window.addEventListener('scroll', function () {
    if (window.innerHeight + window.pageYOffset < document.body.scrollHeight - 4) return;
    document.querySelectorAll('.stripes:not([data-drawn])').forEach(function (el) {
      el.setAttribute('data-drawn', 'true');
    });
    document.querySelectorAll('[data-reveal]:not([data-revealed])').forEach(function (el) {
      el.setAttribute('data-revealed', 'true');
    });
  }, { passive: true });

  /* ---------- 7. Combined scroll loop ----------
     One rAF loop drives both parallax and scroll-scale so we never
     stack listeners. */

  var markEls = [].slice.call(document.querySelectorAll('[data-scroll-rotate]'));

  if (scaleEls.length || markEls.length) {
    var t2 = false;
    function onScroll2() {
      if (t2) return;
      t2 = true;
      requestAnimationFrame(function () {
        var vh = window.innerHeight;

        scaleEls.forEach(function (el) {
          var r = el.getBoundingClientRect();
          if (r.bottom < 0 || r.top > vh) return;
          // progress: 0 when entering bottom, 1 when leaving top
          var prog = 1 - (r.top + r.height) / (vh + r.height);
          prog = Math.max(0, Math.min(1, prog));
          var scale = 1.06 - (prog * 0.06);        // 1.06 -> 1.00
          el.style.transform = 'scale(' + scale.toFixed(4) + ')';
        });

        markEls.forEach(function (el) {
          var r = el.getBoundingClientRect();
          if (r.bottom < 0 || r.top > vh) return;
          var prog = 1 - (r.top + r.height) / (vh + r.height);
          prog = Math.max(0, Math.min(1, prog));
          var deg = (prog - 0.5) * 14;             // -7deg -> +7deg
          el.style.transform = 'rotate(' + deg.toFixed(2) + 'deg)';
        });

        t2 = false;
      });
    }
    window.addEventListener('scroll', onScroll2, { passive: true });
    onScroll2();
  }

  /* If the visitor flips on reduced motion mid-session, stop everything. */
  reduced.addEventListener('change', function (e) {
    if (!e.matches) return;
    document.documentElement.removeAttribute('data-motion');
    parallaxEls.forEach(function (el) { el.style.transform = ''; });
    scaleEls.forEach(function (el) { el.style.transform = ''; });
    markEls.forEach(function (el) { el.style.transform = ''; });
  });

})();
