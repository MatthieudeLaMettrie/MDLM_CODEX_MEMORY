(function () {
  'use strict';
  var form = document.getElementById('form');
  var q = document.getElementById('q');
  var log = document.getElementById('log');
  var send = document.getElementById('send');

  function add(cls, text, html) {
    var d = document.createElement('div');
    d.className = 'msg ' + cls;
    if (html !== undefined) { d.innerHTML = html; } else { d.textContent = text; } // html is sanitised on the server
    log.appendChild(d);
    log.scrollTop = log.scrollHeight;
    return d;
  }

  function post(path, body) {
    return fetch(path, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Requested-With': 'fetch' },
      body: body === undefined ? undefined : JSON.stringify(body)
    });
  }

  fetch('/api/me').then(function (r) { return r.json(); }).then(function (j) {
    document.getElementById('user').textContent = j.user || '';
  }).catch(function () {});

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var m = q.value.trim();
    if (!m) { return; }
    q.value = '';
    add('you', 'You: ' + m);
    var wait = add('wait', 'Thinking...');
    send.disabled = true;
    post('/api/chat', { message: m })
      .then(function (r) {
        if (r.status === 401) { throw new Error('Your session expired. Reload the page to sign in again.'); }
        return r.json().then(function (j) { return { ok: r.ok, j: j }; });
      })
      .then(function (res) {
        wait.remove();
        if (!res.ok) {
          add('err', 'Error: ' + (res.j.error || 'request failed') + (res.j.request_id ? ' (ref ' + res.j.request_id + ')' : ''));
        } else {
          add('bot', '', res.j.html);
          if (res.j.tools && res.j.tools.length) { add('meta', 'Tools used: ' + res.j.tools.join(', ')); }
        }
      })
      .catch(function (err) { wait.remove(); add('err', String(err.message || err)); })
      .then(function () { send.disabled = false; q.focus(); });
  });

  document.getElementById('reset').addEventListener('click', function () {
    post('/api/reset').then(function () {
      log.textContent = '';
      add('meta', 'New conversation started');
    });
  });
})();
