# GesKio — Landing

Sitio estático de presentación con demo interactiva, sin dependencias de ejecución ni paso de build.

## Ejecutar

Desde la raíz del repositorio:

```powershell
python -m http.server 8097 --directory landing
```

Abrir http://localhost:8097. Los recursos usan rutas desde la raíz del sitio.

## Archivos principales

- `index.html`: navegación, demo, resumen de actividad, funciones, guía y FAQ.
- `assets/css/landing.css`: base y presentación de la demo.
- `assets/css/refinements.css`: navegación compacta, resumen conectado y ajustes de composición.
- `assets/js/landing.js`: ventas, stock, pagos, pestañas, navegación móvil y sección activa.
- `assets/fonts/`: Manrope local, licencia OFL incluida.
- `assets/icons/`: Phosphor 2.1.1, licencia MIT incluida.
- `DESIGN.md`: decisiones visuales y restricciones del producto.
- `vercel.json`: configuración estática, redirecciones y cabeceras.

La fotografía generada fue retirada por indicación del usuario. Los importes, clientes y productos de la demo son ficticios; la pestaña conserva el estado en memoria y se reinicia al recargar. No hay formulario de contacto en la landing actual ni transmisión de los datos de la demo.

## Publicación

Proyecto Vercel `geskio`, cuenta `santi2821s-projects`. Desde `landing/`:

```powershell
npx vercel deploy --prod --yes --scope santi2821s-projects
```

Producción: https://geskio.vercel.app

## Verificación de esta revisión

- Navegación móvil: apertura, cierre con Escape, retorno de foco y cierre al seguir un enlace.
- Venta: actualiza caja, stock y resumen de actividad.
- Cobro de fiado: actualiza el saldo del módulo y del resumen.
- Reinicio: restaura todos los módulos y resúmenes.
- Revisión visual de escritorio 1440 px y móvil 390 px.
- Axe WCAG A/AA: sin infracciones automáticas; no sustituye una auditoría manual completa.

No se modificó ni se validó la aplicación de escritorio en este cambio.
