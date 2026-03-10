document.addEventListener('DOMContentLoaded', () => {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
                
                if (entry.target.classList.contains('skill-bar-container')) {
                    const bars = entry.target.querySelectorAll('.skill-progress');
                    bars.forEach(bar => {
                        const width = bar.getAttribute('data-width');
                        bar.style.width = width + '%';
                    });
                }
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.animate-on-scroll, .skill-bar-container').forEach(el => {
        observer.observe(el);
    });
    
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        
        const hero = document.querySelector('.hero-section');
        if (hero) {
            hero.style.transform = `translateY(${scrolled * 0.3}px)`;
        }
    });
    
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    document.querySelectorAll('.skill-progress').forEach(bar => {
        const width = bar.style.width;
        bar.setAttribute('data-width', width.replace('%', ''));
        bar.style.width = '0';
    });
});