// GesKio — aparición de elementos al hacer scroll
document.addEventListener('DOMContentLoaded', () => {
  var items = document.querySelectorAll('.reveal');
  if (!items.length) return;

  if (!('IntersectionObserver' in window)) {
    items.forEach((el) => el.classList.add('in'));
    return;
  }
  var io = new IntersectionObserver((entradas) => {
    entradas.forEach((ent) => {
      if (ent.isIntersecting) {
        ent.target.classList.add('in');
        io.unobserve(ent.target);
      }
    });
  }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
  items.forEach((el) => io.observe(el));
});
