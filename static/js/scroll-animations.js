document.addEventListener('DOMContentLoaded', () => {
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const revealItems = document.querySelectorAll('.reveal, .animate-on-scroll, .skill-bar-container');

    const revealElement = (element) => {
        element.classList.add('fade-in-up');

        if (element.classList.contains('skill-bar-container')) {
            element.querySelectorAll('.skill-progress').forEach((bar) => {
                const width = bar.getAttribute('data-width');
                if (width) {
                    bar.style.width = `${width}%`;
                }
            });
        }
    };

    document.querySelectorAll('.skill-progress').forEach((bar) => {
        const inlineWidth = bar.style.width.replace('%', '');
        if (inlineWidth) {
            bar.setAttribute('data-width', inlineWidth);
        }
        if (!prefersReducedMotion) {
            bar.style.width = '0';
        }
    });

    if (prefersReducedMotion) {
        revealItems.forEach(revealElement);
        return;
    }

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (!entry.isIntersecting) {
                return;
            }

            revealElement(entry.target);
            observer.unobserve(entry.target);
        });
    }, {
        threshold: 0.12,
        rootMargin: '0px 0px -48px 0px',
    });

    revealItems.forEach((element) => observer.observe(element));
});
