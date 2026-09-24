# GesKio — Landing

Landing estática (HTML + CSS + JS, sin dependencias ni build). Funciona abriendo `index.html` directo en el browser.

## Estructura

```
landing/
├── index.html              Home: hero, funciones, cómo funciona, FAQ, CTA
├── pages/
│   ├── funciones.html      Detalle de cada módulo (caja, stock, clientes, fiado, dashboard, chat)
│   └── contacto.html       Formulario de contacto + info lateral
└── assets/
    ├── css/
    │   ├── tokens.css      Variables visuales; radios principales compartidos con app/theme.py
    │   ├── base.css        Reset, tipografía, foco, skip-link
    │   ├── layout.css      Nav, footer, secciones, contenedor
    │   ├── components.css  Botones, cards, chips, forms, FAQ, mocks de la app
    │   ├── animations.css  Reveal, keyframes compartidos
    │   └── pages/          CSS específico por página (home, funciones, contacto)
    ├── js/
    │   ├── theme.js        Toggle claro/oscuro con persistencia (localStorage: geskio-theme)
    │   ├── nav.js          Menú mobile (Escape y click fuera incluidos), scrollspy y año del footer
    │   ├── reveal.js       Animaciones de aparición (IntersectionObserver)
    │   ├── accordion.js    Acordeón de FAQ (con aria-controls y recálculo de altura al resize)
    │   ├── mock-live.js    Mock del hero con ventas que van entrando
    │   └── form.js         Valida y arma un mail real (mailto: con asunto y cuerpo)
    └── img/
        └── favicon.svg     Favicon (4 cuadrados de la marca)
```

## Convenciones

- Cada JS es un script plano e independiente (funciona en `file://`, sin ES modules).
- El CSS carga en orden: tokens → base → layout → components → animations → page.
- Los temas claro/oscuro se resuelven en `tokens.css` con `data-theme` en `<html>`.
- El script de tema corre inline en el `<head>` para evitar el flash antes de pintar.
- Apariciones: agregar `class="reveal"` (y opcional `style="--d:.1s"` para escalonar).
- `prefers-reduced-motion` apaga todas las animaciones.
