// GesKio — menú mobile, scrollspy y año del footer
document.addEventListener('DOMContentLoaded', () => {
  var menuBtn = document.getElementById('menuBtn');
  var links = document.getElementById('links');

  function cerrarMenu() {
    if (!links || !menuBtn) return;
    links.classList.remove('abierto');
    menuBtn.setAttribute('aria-expanded', 'false');
    menuBtn.setAttribute('aria-label', 'Abrir menú');
  }

  if (menuBtn && links) {
    menuBtn.addEventListener('click', () => {
      var abierto = links.classList.toggle('abierto');
      menuBtn.setAttribute('aria-expanded', String(abierto));
      menuBtn.setAttribute('aria-label', abierto ? 'Cerrar menú' : 'Abrir menú');
    });
    links.querySelectorAll('a').forEach((a) => a.addEventListener('click', cerrarMenu));
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && links.classList.contains('abierto')) {
        cerrarMenu();
        menuBtn.focus();
      }
    });
    document.addEventListener('click', (e) => {
      if (links.classList.contains('abierto') && !e.target.closest('.nav')) cerrarMenu();
    });
  }

  // scrollspy: marca la sección visible (solo donde existan data-spy)
  var secciones = document.querySelectorAll('[data-spy]');
  var anclas = links ? Array.from(links.querySelectorAll('a[href^="#"]')) : [];
  if (secciones.length && anclas.length && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver((entradas) => {
      entradas.forEach((ent) => {
        if (!ent.isIntersecting) return;
        var id = '#' + ent.target.id;
        anclas.forEach((a) => {
          a.classList.toggle('activo', a.getAttribute('href') === id);
          if (a.getAttribute('href') === id) a.setAttribute('aria-current', 'true');
          else a.removeAttribute('aria-current');
        });
      });
    }, { rootMargin: '-40% 0px -55% 0px' });
    secciones.forEach((s) => io.observe(s));
  }

  // año del footer
  var anio = document.getElementById('anio');
  if (anio) anio.textContent = new Date().getFullYear();
});
