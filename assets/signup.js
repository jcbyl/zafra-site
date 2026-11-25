/* zafratrading.com — signup forms + click tracking.
   Each signup posts to /signup (saved to Supabase site_leads + mailed to info@zafratrading.com).
   Every click on "Join" / "Inquire" posts to /track with the headline variant, box, source and UTM tags.
   Campaign tags are kept from the first visit that carried them, so a signup stays attributed to its link. */
(function () {
  var UTM = ['utm_source', 'utm_medium', 'utm_campaign'];
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };

  // First-touch campaign tags + referrer (persisted so they survive a visit to /story and back).
  var tags = {};
  try { tags = JSON.parse(store.get('zafra-utm') || '{}') || {}; } catch (e) { tags = {}; }
  var q = new URLSearchParams(location.search), fresh = false;
  UTM.forEach(function (k) {
    var v = (q.get(k) || '').trim().slice(0, 120);
    if (v) { tags[k] = v; fresh = true; }
  });
  if (fresh) store.set('zafra-utm', JSON.stringify(tags));

  var ref = document.referrer || '';
  if (ref) {
    try {
      var h = new URL(ref).hostname.replace(/^www\./, '');
      if (h === 'zafratrading.com') ref = store.get('zafra-ref') || '';
      else store.set('zafra-ref', ref);
    } catch (e) { ref = ''; }
  } else {
    ref = store.get('zafra-ref') || '';
  }

  // One id per tab, so clicks and the signup that follows can be lined up.
  var sid = '';
  try { sid = sessionStorage.getItem('zafra-session') || ''; } catch (e) {}
  if (!sid) {
    sid = (crypto.randomUUID && crypto.randomUUID()) || String(Date.now() + Math.random());
    try { sessionStorage.setItem('zafra-session', sid); } catch (e) {}
  }

  function ctx() {
    var src = tags.utm_source || 'direct';
    if (src === 'direct' && ref) { try { src = new URL(ref).hostname.replace(/^www\./, ''); } catch (e) {} }
    return {
      hero: window.zafraHero ? window.zafraHero() : 'hero-NA',
      source: src,
      utm_source: tags.utm_source || '',
      utm_medium: tags.utm_medium || '',
      utm_campaign: tags.utm_campaign || '',
      referrer: ref,
      page_url: location.origin + location.pathname,
      session_id: sid
    };
  }

  // Google Tag Manager reads page parameters and events from window.dataLayer (GA4 is set up inside the container).
  var dl = (window.dataLayer = window.dataLayer || []);
  function gtm(event, extra) {
    var c = ctx(), m = {
      hero_variant: c.hero,
      source: c.source,
      utm_source: c.utm_source,
      utm_medium: c.utm_medium,
      utm_campaign: c.utm_campaign
    };
    for (var k in extra || {}) m[k] = extra[k];
    if (event) m.event = event;
    dl.push(m);
  }
  gtm(); // page parameters: present on every page view

  function track(box) {
    var body = ctx();
    body.event = 'click';
    body.box = box;
    gtm('signup_click', { box: box });
    fetch('/track', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
      keepalive: true
    }).catch(function () {});
  }

  document.querySelectorAll('form.signup').forEach(function (form) {
    var box = form.getAttribute('data-box');
    var list = form.getAttribute('data-list');
    var btn = form.querySelector('.signup-btn');
    var loaded = Date.now();
    var clicked = 0;

    btn.addEventListener('click', function () { clicked = Date.now(); track(box); });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (btn.disabled) return;
      if (Date.now() - clicked > 1500) track(box); // submitted with the Enter key: no click was counted
      btn.disabled = true;
      form.classList.remove('failed');

      var body = ctx();
      body.list = list;
      body.box = box;
      body.ts = loaded;
      body.hp = form.querySelector('.hp') ? form.querySelector('.hp').value : '';
      ['name', 'email', 'business', 'location', 'message'].forEach(function (n) {
        var f = form.elements[n];
        if (f) body[n] = f.value;
      });

      fetch('/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      })
        .then(function (r) { return r.json(); })
        .then(function (j) {
          if (j && j.ok) {
            gtm('signup', { list: list, box: box });
            form.reset();
            form.classList.add('done');
            var ok = form.querySelector('.signup-ok');
            if (ok) ok.focus();
          } else {
            throw new Error('not_ok');
          }
        })
        .catch(function () {
          form.classList.add('failed');
          btn.disabled = false;
        });
    });
  });
})();
