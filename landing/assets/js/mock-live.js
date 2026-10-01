document.addEventListener('DOMContentLoaded', () => {
  var num = document.getElementById('mockNum');
  var toast = document.getElementById('mockToast');
  var toastTexto = document.getElementById('mockToastTexto');
  var barras = document.querySelectorAll('#mockChart i');
  if (!num || !toast || !barras.length) return;

  var total = 5900;
  var productos = ['Coca-Cola 500ml', 'Alfajor chocolate', 'Golosinas x10', 'Pan lácteo', 'Gaseosa litro'];
  var importes = [900, 450, 1200, 750, 1100];
  var activa = 6;

  function formato(v) {
    return '$' + v.toLocaleString('es-AR');
  }

  function ventaNueva() {
    var i = Math.floor(Math.random() * productos.length);
    total += importes[i];
    num.textContent = formato(total);
    toastTexto.textContent = productos[i] + ' — ' + formato(importes[i]);
    toast.style.opacity = '0';
    setTimeout(() => { toast.style.opacity = '1'; }, 60);
    var alta = barras[activa];
    if (alta) {
      var h = parseInt(alta.dataset.h || '70', 10);
      alta.dataset.h = Math.min(h + 6, 100);
      alta.style.height = alta.dataset.h + '%';
      alta.classList.add('alta');
    }
  }

  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  setInterval(() => {
    if (Math.random() < 0.65) ventaNueva();
  }, 3800);
});
