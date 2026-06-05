/**
 * Luzago Alimentos — AOS, lazy load fade-in e hovers dinâmicos
 */
(function () {
    'use strict';

    var AOS_TARGETS = '.product-item, .product-card, .blog-card, .catalog-item, .review-card, .instagram-card, footer > div > div';
    var HERO_SELECTOR = 'section[class*="hero"] .container, section[class*="hero"] > div > *';

    function initLazyImages() {
        document.querySelectorAll('img[loading="lazy"]').forEach(function (img) {
            if (!img.classList.contains('img-lazy')) {
                img.classList.add('img-lazy');
            }
            function markLoaded() {
                img.classList.add('is-loaded');
            }
            if (img.complete && img.naturalWidth > 0) {
                markLoaded();
            } else {
                img.addEventListener('load', markLoaded, { once: true });
                img.addEventListener('error', markLoaded, { once: true });
            }
        });
    }

    function wrapProductImages() {
        document.querySelectorAll('.product-item img, .catalog-item img').forEach(function (img) {
            var wrap = img.parentElement;
            if (wrap && !wrap.classList.contains('product-item__img-wrap')) {
                wrap.classList.add('product-item__img-wrap');
            }
        });
    }

    function enhanceInstagramCards() {
        document.querySelectorAll('section a[href*="instagram.com"]').forEach(function (link) {
            if (link.querySelector('img')) {
                link.classList.add('instagram-card');
            }
        });
    }

    function enhanceReviewCards() {
        document.querySelectorAll('section h2').forEach(function (h2) {
            if (h2.textContent.indexOf('Avalia') === -1) return;
            var section = h2.closest('section');
            if (!section) return;
            section.querySelectorAll('.bg-white.rounded-lg.shadow').forEach(function (card) {
                card.classList.add('review-card');
            });
        });
    }

    function enhanceSocialIcons() {
        document.querySelectorAll('a[aria-label*="Luzago"]').forEach(function (link) {
            if (link.classList.contains('w-8') && link.classList.contains('h-8')) {
                link.classList.add('social-icon');
            }
        });
    }

    function enhanceNavLinks() {
        document.querySelectorAll('header nav a:not(.btn)').forEach(function (link) {
            link.classList.add('nav-link');
        });
    }

    function enhanceCarousel() {
        document.querySelectorAll('#empresa-carousel-track').forEach(function (track) {
            var shell = track.parentElement;
            if (shell) shell.classList.add('carousel-shell');
        });
    }

    function applyAosAttributes() {
        document.querySelectorAll(AOS_TARGETS).forEach(function (el, i) {
            if (el.hasAttribute('data-aos')) return;
            el.setAttribute('data-aos', 'fade-up');
            el.setAttribute('data-aos-delay', String(Math.min((i % 8) * 60, 360)));
        });

        document.querySelectorAll('section h1, section h2, .blog-article').forEach(function (el, i) {
            if (el.hasAttribute('data-aos')) return;
            el.setAttribute('data-aos', 'fade-up');
            el.setAttribute('data-aos-delay', String(Math.min(i * 40, 200)));
        });

        document.querySelectorAll(HERO_SELECTOR).forEach(function (el, i) {
            if (el.hasAttribute('data-aos')) return;
            el.setAttribute('data-aos', 'fade-up');
            el.setAttribute('data-aos-duration', '800');
            el.setAttribute('data-aos-delay', String(i * 80));
        });
    }

    function initAos() {
        if (typeof AOS === 'undefined') return;
        var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        AOS.init({
            duration: 700,
            easing: 'ease-out-cubic',
            once: true,
            offset: 50,
            disable: reduced
        });
    }

    function boot() {
        wrapProductImages();
        enhanceInstagramCards();
        enhanceReviewCards();
        enhanceSocialIcons();
        enhanceNavLinks();
        enhanceCarousel();
        applyAosAttributes();
        initLazyImages();
        initAos();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', boot);
    } else {
        boot();
    }

    window.LuzagoEffects = {
        refresh: function () {
            wrapProductImages();
            applyAosAttributes();
            initLazyImages();
            if (typeof AOS !== 'undefined') AOS.refresh();
        }
    };
})();
