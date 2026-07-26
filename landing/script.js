/* ============================================================
   GesKio — Landing JS
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

    /* ---------- Navbar scroll ---------- */
    const nav = document.getElementById('nav');
    const onScroll = () => {
        if (window.scrollY > 20) nav.classList.add('scrolled');
        else nav.classList.remove('scrolled');
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();


    /* ---------- Menú mobile ---------- */
    const navToggle = document.getElementById('navToggle');
    const navLinks = document.getElementById('navLinks');

    navToggle.addEventListener('click', () => {
        navToggle.classList.toggle('active');
        navLinks.classList.toggle('open');
    });
    navLinks.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
        navToggle.classList.remove('active');
        navLinks.classList.remove('open');
    }));


    /* ---------- Toggle tema (dark mode) ---------- */
    const themeToggle = document.getElementById('themeToggle');
    const root = document.documentElement;

    themeToggle.addEventListener('click', () => {
        const isDark = root.getAttribute('data-theme') === 'dark';
        const next = isDark ? 'light' : 'dark';
        root.setAttribute('data-theme', next);
        try { localStorage.setItem('geskio-theme', next); } catch (e) {}
    });

    // Si el sistema cambia y el usuario no eligió manualmente, seguilo
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        let saved = null;
        try { saved = localStorage.getItem('geskio-theme'); } catch (er) {}
        if (!saved) root.setAttribute('data-theme', e.matches ? 'dark' : 'light');
    });


    /* ---------- Scroll reveal ---------- */
    const reveals = document.querySelectorAll('.reveal');
    const io = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const delay = parseInt(entry.target.dataset.delay || '0', 10);
                setTimeout(() => entry.target.classList.add('visible'), delay);
                io.unobserve(entry.target);
            }
        });
    }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });
    reveals.forEach(el => io.observe(el));

    const revealInViewport = () => {
        const vh = window.innerHeight;
        reveals.forEach(el => {
            if (el.classList.contains('visible')) return;
            const r = el.getBoundingClientRect();
            if (r.top < vh - 40 && r.bottom > 0) {
                el.classList.add('visible');
            }
        });
    };
    window.addEventListener('load', revealInViewport);
    setTimeout(revealInViewport, 800);
    let revealTicking = false;
    window.addEventListener('scroll', () => {
        if (revealTicking) return;
        revealTicking = true;
        requestAnimationFrame(() => { revealInViewport(); revealTicking = false; });
    }, { passive: true });


    /* ---------- Marquee (sin huecos en cualquier resolución) ---------- */
    const marqueeTrack = document.querySelector('.marquee-track');
    if (marqueeTrack) {
        const marqueeEl = marqueeTrack.parentElement;
        const baseSet = marqueeTrack.innerHTML;
        const adjustMarquee = () => {
            let guard = 0;
            while (marqueeTrack.scrollWidth < marqueeEl.offsetWidth * 2 && guard < 12) {
                marqueeTrack.insertAdjacentHTML('beforeend', baseSet);
                guard++;
            }
            const half = marqueeTrack.scrollWidth / 2;
            const dur = Math.max(20, Math.min(90, half / 42));
            marqueeTrack.style.animationDuration = dur + 's';
        };
        adjustMarquee();
        window.addEventListener('load', adjustMarquee);
        if (document.fonts && document.fonts.ready) document.fonts.ready.then(adjustMarquee);
        let marqueeTimer;
        window.addEventListener('resize', () => {
            clearTimeout(marqueeTimer);
            marqueeTimer = setTimeout(adjustMarquee, 200);
        });
    }


    /* ---------- Formulario ---------- */
    const form = document.getElementById('contactForm');
    const note = document.getElementById('formNote');

    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const nombre = form.nombre.value.trim();
            const email = form.email.value.trim();
            const emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

            if (!nombre) {
                note.textContent = 'Decime tu nombre para saber a quién escribirle.';
                note.style.color = 'var(--accent)';
                form.nombre.focus();
                return;
            }
            if (!emailOk) {
                note.textContent = 'Ese email no parece válido.';
                note.style.color = 'var(--accent)';
                form.email.focus();
                return;
            }

            const btn = form.querySelector('button[type="submit"]');
            const original = btn.textContent;
            btn.textContent = 'Enviando...';
            btn.disabled = true;

            setTimeout(() => {
                note.textContent = '¡Gracias ' + nombre + '! Te escribimos pronto.';
                note.style.color = '#059669';
                form.reset();
                btn.textContent = original;
                btn.disabled = false;
                setTimeout(() => { note.textContent = ''; }, 6000);
            }, 1100);
        });
    }


    /* ---------- Año footer ---------- */
    const year = document.getElementById('year');
    if (year) year.textContent = new Date().getFullYear();

});
