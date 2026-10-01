document.addEventListener('DOMContentLoaded', () => {
  var form = document.getElementById('form');
  var aviso = document.getElementById('aviso');
  if (!form || !aviso) return;

  function fallar(texto, campo) {
    aviso.textContent = texto;
    aviso.classList.add('error');
    if (campo) campo.focus();
  }

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    var nombre = form.nombre.value.trim();
    var email = form.email.value.trim();
    var mensaje = form.mensaje.value.trim();
    if (!nombre) return fallar('Dejame tu nombre y te escribo.', form.nombre);
    if (!/^\S+@\S+\.\S+$/.test(email)) return fallar('Necesito un email válido para responderte.', form.email);
    if (!mensaje) return fallar('Contame brevemente de tu negocio.', form.mensaje);

    var asunto = 'Prueba GesKio — ' + nombre;
    var cuerpo = 'Nombre: ' + nombre + '\nEmail: ' + email + (mensaje ? '\n\n' + mensaje : '');
    location.href = 'mailto:hola@geskio.com?subject=' + encodeURIComponent(asunto) + '&body=' + encodeURIComponent(cuerpo);

    form.reset();
    aviso.classList.remove('error');
    aviso.textContent = 'Se abre tu correo con el mensaje listo: solo apretá enviar.';
  });
});
