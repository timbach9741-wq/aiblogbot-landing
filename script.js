// Fade-in animation on scroll
const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
};

const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

document.addEventListener('DOMContentLoaded', () => {
    const animatedElements = document.querySelectorAll('.glass-card, .guide-card, .price-card, .hero-content');

    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
        observer.observe(el);
    });

    // 우측 하단 플로팅 버튼: 화면을 어느 정도 내려야 나타나고, 맨 위로 버튼은 클릭 시 부드럽게 스크롤
    const floatingActions = document.getElementById('floating-actions');
    const scrollTopBtn = document.getElementById('scroll-top-btn');

    if (floatingActions) {
        const toggleFloatingActions = () => {
            if (window.scrollY > 400) {
                floatingActions.classList.add('is-visible');
            } else {
                floatingActions.classList.remove('is-visible');
            }
        };
        toggleFloatingActions();
        window.addEventListener('scroll', toggleFloatingActions, { passive: true });
    }

    if (scrollTopBtn) {
        scrollTopBtn.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }
});
