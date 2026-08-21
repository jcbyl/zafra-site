/* ============================================================
   AGENTE WIDGET — JCB customer-facing chat widget
   Avatar: Agente robot (coral #E84118 chat-bubble mascot)
   For Zafra sites: coffee-centric persona (educate on PR
   coffee, then sell). Chatbot-only — no email fallbacks.
   Backend: Hermes api_server (OpenAI-compatible) via tunnel.
   ============================================================ */
(function () {
  var CFG = {
    endpoint: 'https://zafra-chat.jcbindustries.com/v1/chat/completions',
    model: 'zafra',
    apiKey: 'zafra_1JixE5-0c7rSeNxJG5t8s3FwQ8mH6YpK2vL4nA7bR9cD',
    avatar: 'images/widgets/agente-robot-avatar.png',
    name: 'Zafra',
    tagline: 'Ask me about our coffee',
    greeting: "¡Hola! I'm the Zafra assistant — ask me anything about Puerto Rican coffee: our mountain regions, the farmers we buy from, how it's roasted and shipped fresh to your door. ☕",
    offline: "The kettle's still heating — live chat starts soon. Meanwhile, scroll on to see what we carry from the island.",
    coral: '#E84118',
    coralHover: '#C7361A',
    green: '#0E2A1E',
    cream: '#FAF8F3',
    gold: '#C9A54E'
  };

  var state = { open: false, history: [], offline: false };

  /* ---------- styles ---------- */
  var css = document.createElement('style');
  css.textContent = [
    '.agente-btn{position:fixed;bottom:22px;right:22px;width:60px;height:60px;border:none;border-radius:50%;padding:0;cursor:pointer;z-index:9998;',
    'box-shadow:0 6px 24px rgba(232,65,24,.45);background:', CFG.coral, ';transition:transform .2s,box-shadow .2s;}',
    '.agente-btn:hover{transform:translateY(-3px);box-shadow:0 10px 30px rgba(232,65,24,.6);}',
    '.agente-btn img{width:60px;height:60px;border-radius:50%;display:block;}',
    '.agente-btn .agente-dot{position:absolute;top:-2px;right:-2px;width:14px;height:14px;border-radius:50%;background:#3DDC84;border:2.5px solid #fff;}',
    '.agente-panel{position:fixed;bottom:94px;right:22px;width:min(370px,calc(100vw - 32px));height:min(540px,calc(100vh - 140px));',
    'background:', CFG.cream, ';border-radius:16px;box-shadow:0 18px 60px rgba(0,0,0,.35);z-index:9999;display:none;flex-direction:column;overflow:hidden;',
    'font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;text-align:left;}',
    '.agente-panel.open{display:flex;animation:agente-in .22s ease;}',
    '@keyframes agente-in{from{opacity:0;transform:translateY(12px) scale(.98)}to{opacity:1;transform:none}}',
    '.agente-head{display:flex;align-items:center;gap:10px;padding:13px 16px;background:', CFG.green, ';}',
    '.agente-head img{width:38px;height:38px;border-radius:10px;}',
    '.agente-head .t{flex:1;min-width:0;}',
    '.agente-head .t b{display:block;color:#fff;font-size:15px;letter-spacing:.02em;}',
    '.agente-head .t span{display:block;color:rgba(250,248,243,.65);font-size:11.5px;margin-top:1px;}',
    '.agente-head .t span i{display:inline-block;width:7px;height:7px;border-radius:50%;background:#3DDC84;margin-right:5px;}',
    '.agente-x{background:none;border:none;color:rgba(250,248,243,.7);font-size:20px;cursor:pointer;padding:4px 8px;line-height:1;}',
    '.agente-x:hover{color:#fff;}',
    '.agente-msgs{flex:1;overflow-y:auto;padding:14px 14px 8px;display:flex;flex-direction:column;gap:10px;}',
    '.agente-msgs::-webkit-scrollbar{width:5px}.agente-msgs::-webkit-scrollbar-thumb{background:rgba(14,42,30,.2);border-radius:3px}',
    '.agente-m{max-width:82%;padding:10px 13px;border-radius:14px;font-size:13.5px;line-height:1.5;}',
    '.agente-m.bot{background:#fff;color:#26332C;border:1px solid rgba(14,42,30,.1);border-bottom-left-radius:4px;align-self:flex-start;}',
    '.agente-m.user{background:', CFG.coral, ';color:#fff;border-bottom-right-radius:4px;align-self:flex-end;}',
    '.agente-m.typing{color:rgba(38,51,44,.55);font-style:italic;}',
    '.agente-m.typing b{animation:agente-blink 1.2s infinite;}',
    '.agente-m.typing b:nth-child(2){animation-delay:.2s}.agente-m.typing b:nth-child(3){animation-delay:.4s}',
    '@keyframes agente-blink{0%,80%,100%{opacity:.25}40%{opacity:1}}',
    '.agente-foot{display:flex;gap:8px;padding:10px 12px;border-top:1px solid rgba(14,42,30,.08);background:#fff;}',
    '.agente-in{flex:1;border:1px solid rgba(14,42,30,.18);border-radius:22px;padding:10px 15px;font-size:13.5px;outline:none;background:', CFG.cream, ';color:#26332C;}',
    '.agente-in:focus{border-color:', CFG.coral, ';}',
    '.agente-send{width:40px;height:40px;border:none;border-radius:50%;background:', CFG.coral, ';color:#fff;font-size:16px;cursor:pointer;flex:none;transition:background .15s;}',
    '.agente-send:hover{background:', CFG.coralHover, ';}',
    '.agente-send:disabled{background:rgba(14,42,30,.18);cursor:default;}',
    '.agente-brand{font-size:10px;color:rgba(38,51,44,.4);text-align:center;padding:0 0 7px;background:#fff;}',
    '@media(max-width:480px){',
    '.agente-btn{bottom:16px;right:16px;width:54px;height:54px}.agente-btn img{width:54px;height:54px}',
    '.agente-panel{bottom:82px;right:16px;left:16px;width:auto;height:min(560px,calc(100vh - 110px));}}'
  ].join('');
  document.head.appendChild(css);

  /* ---------- markup ---------- */
  var btn = document.createElement('button');
  btn.className = 'agente-btn';
  btn.setAttribute('aria-label', 'Chat with Zafra');
  btn.innerHTML = '<img src="' + CFG.avatar + '" alt="Zafra chat"><span class="agente-dot"></span>';

  var panel = document.createElement('div');
  panel.className = 'agente-panel';
  panel.setAttribute('role', 'dialog');
  panel.setAttribute('aria-label', 'Zafra chat');
  panel.innerHTML = [
    '<div class="agente-head">',
    '<img src="', CFG.avatar, '" alt="">',
    '<div class="t"><b>', CFG.name, '</b><span><i></i>', CFG.tagline, '</span></div>',
    '<button class="agente-x" aria-label="Close chat">&times;</button></div>',
    '<div class="agente-msgs"></div>',
    '<form class="agente-foot"><input class="agente-in" placeholder="Ask about our coffee…" autocomplete="off">',
    '<button class="agente-send" aria-label="Send">&#8593;</button></form>',
    '<div class="agente-brand">Powered by Agente</div>'
  ].join('');

  document.body.appendChild(btn);
  document.body.appendChild(panel);

  var msgs = panel.querySelector('.agente-msgs');
  var input = panel.querySelector('.agente-in');
  var form = panel.querySelector('.agente-foot');
  var send = panel.querySelector('.agente-send');

  /* ---------- chat ---------- */
  function add(text, who) {
    var d = document.createElement('div');
    d.className = 'agente-m ' + who;
    d.textContent = text;
    msgs.appendChild(d);
    msgs.scrollTop = msgs.scrollHeight;
    return d;
  }
  function typing() {
    var d = add('', 'bot typing');
    d.innerHTML = '<b>&#9679;</b> <b>&#9679;</b> <b>&#9679;</b>';
    return d;
  }

  function send_(q) {
    if (!q.trim()) return;
    add(q, 'user');
    input.value = '';
    state.history.push({ role: 'user', content: q });

    if (state.offline) {
      setTimeout(function () { add(CFG.offline, 'bot'); }, 600);
      return;
    }
    var t = typing();
    fetch(CFG.endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + CFG.apiKey },
      body: JSON.stringify({
        model: CFG.model,
        messages: [{ role: 'system', content: CFG.system || '' }].concat(state.history),
        stream: false
      })
    }).then(function (r) {
      if (!r.ok) throw new Error(r.status);
      return r.json();
    }).then(function (j) {
      t.remove();
      var a = (j.choices && j.choices[0] && j.choices[0].message && j.choices[0].message.content) || '';
      add(a || "I'm here — ask me anything about our Puerto Rican coffee.", 'bot');
      state.history.push({ role: 'assistant', content: a });
    }).catch(function () {
      t.remove();
      state.offline = true;
      add(CFG.offline, 'bot');
    });
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    send_(input.value);
  });

  btn.addEventListener('click', function () {
    state.open = !state.open;
    panel.classList.toggle('open', state.open);
    if (state.open) {
      if (!msgs.children.length) add(CFG.greeting, 'bot');
      input.focus();
    }
  });
  panel.querySelector('.agente-x').addEventListener('click', function () {
    state.open = false;
    panel.classList.remove('open');
  });
})();
