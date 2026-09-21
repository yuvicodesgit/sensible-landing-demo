/* Sensible /solutions/accounts-payable: interactions + GSAP motion.
   - Tabs, hover-linking and FAQ work without GSAP.
   - GSAP/ScrollTrigger only add motion. If they fail to load (or the visitor prefers reduced
     motion) the "ap-js" class is removed and all content stays visible.
   Load order: gsap.min.js, ScrollTrigger.min.js, then this file (footer). */
(function () {
  'use strict';
  var root = document.querySelector('.ap');
  if (!root) return;
  var $ = function (s, c) { return (c || root).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || root).querySelectorAll(s)); };
  var html = document.documentElement;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var afterPane = function () {};
  var afterField = function () {};

  /* ---------- demo: tabs + hover linking (no GSAP needed) ---------- */
  $$('.ap-demo-tab').forEach(function (t) {
    t.addEventListener('click', function () {
      $$('.ap-demo-tab').forEach(function (x) { x.setAttribute('aria-selected', x === t ? 'true' : 'false'); });
      $$('.ap-pane').forEach(function (p) { p.classList.toggle('on', p.id === 'ap-pane-' + t.dataset.pane); });
      afterPane();
    });
  });
  $$('.ap-pane').forEach(function (pane) {
    function set(e, on) {
      var el = e.target.closest('[data-f]');
      if (!el) return;
      $$('[data-f="' + el.dataset.f + '"]', pane).forEach(function (n) { n.classList.toggle('hl', on); });
    }
    pane.addEventListener('mouseover', function (e) { set(e, true); });
    pane.addEventListener('mouseout', function (e) { set(e, false); });
  });

  /* ---------- fields tabs ---------- */
  $$('.ap-ftab').forEach(function (t) {
    t.addEventListener('click', function () {
      $$('.ap-ftab').forEach(function (x) { x.setAttribute('aria-selected', x === t ? 'true' : 'false'); });
      $$('.ap-fpane').forEach(function (p) { p.classList.toggle('on', p.id === 'ap-f-' + t.dataset.ft); });
      afterField();
    });
  });

  /* ---------- motion ---------- */
  if (!window.gsap || !window.ScrollTrigger || reduce) { html.classList.remove('ap-js'); return; }
  gsap.registerPlugin(ScrollTrigger);

  function splitWords(el) {
    function walk(node, host) {
      Array.prototype.slice.call(node.childNodes).forEach(function (n) {
        if (n.nodeType === 3) {
          var frag = document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(function (part) {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(' ')); return; }
            var w = document.createElement('span'); w.className = 'ap-w';
            var i = document.createElement('span'); i.textContent = part; w.appendChild(i);
            frag.appendChild(w);
          });
          host.replaceChild(frag, n);
        } else if (n.nodeType === 1) { walk(n, n); }
      });
    }
    walk(el, el);
  }

  /* hero */
  var h1 = $('.ap-h1');
  splitWords(h1);
  gsap.set(h1, { opacity: 1 });
  var hrs = $$('.ap-hr');
  var intro = gsap.timeline({ defaults: { ease: 'power3.out' } });
  intro
    .from($$('.ap-h1 .ap-w > span'), { yPercent: 115, duration: 1, stagger: 0.05 }, 0.05)
    .fromTo($$('[data-hero]'), { opacity: 0, y: 22 }, { opacity: 1, y: 0, duration: 0.8, stagger: 0.1 }, 0.1)
    .from(hrs, { opacity: 0, scale: 0.88, transformOrigin: '100% 0%', duration: 1.1, stagger: 0.12 }, 0.1)
    .from($('.ap-demo-wrap'), { y: 56, opacity: 0, duration: 1.1 }, 0.35)
    .from($$('.ap-pane.on .ap-jl'), { opacity: 0, x: -10, duration: 0.4, stagger: 0.022 }, 1.0);

  gsap.to(hrs, { y: '+=10', duration: 4.2, repeat: -1, yoyo: true, ease: 'sine.inOut', stagger: { each: 0.4, from: 'end' } });
  var panel = $('.ap-hero-panel');
  if (panel && window.matchMedia('(hover: hover)').matches) {
    var qx = hrs.map(function (el, i) { return { fn: gsap.quickTo(el, 'x', { duration: 0.9, ease: 'power3' }), k: 8 + i * 7 }; });
    panel.addEventListener('mousemove', function (e) {
      var r = panel.getBoundingClientRect(); var nx = (e.clientX - r.left) / r.width - 0.5;
      qx.forEach(function (q) { q.fn(nx * q.k * -2); });
    });
    panel.addEventListener('mouseleave', function () { qx.forEach(function (q) { q.fn(0); }); });
  }
  afterPane = function () {
    gsap.from($$('.ap-pane.on .ap-jl'), { opacity: 0, x: -10, duration: 0.35, stagger: 0.02, overwrite: true });
    gsap.from($$('.ap-pane.on .ap-doc'), { y: 8, opacity: 0.4, duration: 0.4 });
  };
  afterField = function () {
    gsap.from($$('.ap-fpane.on .ap-frow:not(.h)'), { opacity: 0, y: 10, duration: 0.4, stagger: 0.03, overwrite: true });
  };

  /* chaos -> one schema (scroll-scrubbed) */
  var cs = $$('.ap-cs');
  if (cs.length) {
    cs.forEach(function (el) {
      gsap.set(el, { x: +el.dataset.dx, y: +el.dataset.dy, rotation: +el.dataset.r, transformOrigin: '75px 52px' });
    });
    gsap.timeline({ scrollTrigger: { trigger: '.ap-chaos', start: 'top 70%', end: 'center 42%', scrub: 0.8 } })
      .to(cs, { x: 0, y: 0, rotation: 0, duration: 1, ease: 'power2.inOut', stagger: 0.04 }, 0)
      .to('.ap-chaos-label .a', { opacity: 0, duration: 0.25 }, 0.35)
      .to('.ap-chaos-label .b', { opacity: 1, duration: 0.3 }, 0.6)
      .to('.ap-cs-hl', { opacity: 1, duration: 0.4, stagger: 0.05 }, 0.8);
    /* gentle idle drift while scattered */
    cs.forEach(function (el, i) {
      gsap.to(el, { rotation: '+=' + (i % 2 ? 3 : -3), duration: 3 + (i % 3), repeat: -1, yoyo: true, ease: 'sine.inOut' });
    });
  }

  /* generic reveal */
  ScrollTrigger.batch('[data-reveal]', {
    start: 'top 89%', once: true,
    onEnter: function (els) { gsap.to(els, { opacity: 1, y: 0, duration: 0.85, stagger: 0.09, ease: 'power3.out', overwrite: true }); }
  });

  /* pipeline: cards rise, line-art draws itself */
  $$('.ap-card').forEach(function (card, i) {
    ScrollTrigger.create({
      trigger: card, start: 'top 85%', once: true,
      onEnter: function () {
        gsap.fromTo($$('.ap-draw', card), { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 1.2, stagger: 0.18, ease: 'power2.out', delay: 0.25 + i * 0.05 });
      }
    });
  });
  var scope = $('.ap-scope i');
  if (scope) gsap.from($$('.ap-scope i'), { scaleX: 0, duration: 1.2, ease: 'power3.inOut', stagger: 0.1, scrollTrigger: { trigger: '.ap-scope', start: 'top 90%', once: true } });

  /* validation: checks tick in one by one, numbers count up */
  var rows = $$('.ap-check');
  if (rows.length) {
    gsap.set(rows, { opacity: 0, y: 14 });
    var icons = rows.map(function (r) { return $('.ic', r); });
    gsap.set(icons, { scale: 0 });
    var vt = gsap.timeline({ scrollTrigger: { trigger: '.ap-checks', start: 'top 78%', once: true } });
    rows.forEach(function (r, i) {
      vt.to(r, { opacity: 1, y: 0, duration: 0.5, ease: 'power2.out' }, i * 0.38)
        .to(icons[i], { scale: 1, duration: 0.45, ease: 'back.out(2.6)' }, i * 0.38 + 0.15);
      var res = $('.res[data-count]', r);
      if (res) {
        var target = parseFloat(res.dataset.count); var o = { v: 0 };
        vt.to(o, { v: target, duration: 0.9, ease: 'power2.out', onUpdate: function () {
          res.textContent = '$' + o.v.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        } }, i * 0.38 + 0.1);
      }
    });
    vt.fromTo('.ap-check.flag', { backgroundColor: '#FFE3B8' }, { backgroundColor: '#FFF7EA', duration: 1.1, repeat: 1, yoyo: true }, '>-0.3');
  }

  /* pull-quote: words light up as you scroll */
  var q = $('.ap-qtext');
  if (q) {
    splitWords(q);
    var words = $$('.ap-w', q);
    words.forEach(function (w) { w.style.overflow = 'visible'; });
    gsap.fromTo(words, { opacity: 0.16 }, { opacity: 1, ease: 'none', stagger: 0.12,
      scrollTrigger: { trigger: '.ap-quote', start: 'top 72%', end: 'bottom 62%', scrub: true } });
  }

  window.addEventListener('load', function () { ScrollTrigger.refresh(); });
})();
