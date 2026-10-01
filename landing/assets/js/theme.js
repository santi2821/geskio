document.addEventListener('DOMContentLoaded', () => {
  var btn = document.getElementById('temaBtn');
  if (!btn) return;
  btn.addEventListener('click', () => {
    var root = document.documentElement;
    var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('geskio-theme', next); } catch (e) {}
  });
});
