document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.faq-item').forEach((item, i) => {
    var btn = item.querySelector('.faq-pregunta');
    var resp = item.querySelector('.faq-respuesta');
    if (!btn || !resp) return;

    var idPanel = 'faq-panel-' + i;
    resp.id = idPanel;
    btn.setAttribute('aria-controls', idPanel);

    function cerrar() {
      item.classList.remove('abierto');
      btn.setAttribute('aria-expanded', 'false');
      resp.style.maxHeight = '0px';
    }
    function abrir() {
      item.classList.add('abierto');
      btn.setAttribute('aria-expanded', 'true');
      resp.style.maxHeight = resp.scrollHeight + 'px';
    }

    btn.addEventListener('click', () => {
      if (item.classList.contains('abierto')) cerrar();
      else abrir();
    });
  });

  window.addEventListener('resize', () => {
    document.querySelectorAll('.faq-item.abierto .faq-respuesta').forEach((resp) => {
      resp.style.maxHeight = resp.scrollHeight + 'px';
    });
  });
});
