/**
 * Дополнительные функции плавной прокрутки
 * и анимации при появлении элементов
 */

(function() {
    'use strict';
    
    document.addEventListener('DOMContentLoaded', function() {
        initScrollAnimations();
        initParallax();
    });
    
    // ===== Анимации при прокрутке =====
    function initScrollAnimations() {
        // Проверка поддержки Intersection Observer
        if (!('IntersectionObserver' in window)) {
            // Fallback для старых браузеров - показываем все элементы
            document.querySelectorAll('[data-aos]').forEach(el => {
                el.style.opacity = '1';
                el.style.transform = 'none';
            });
            return;
        }
        
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const target = entry.target;
                    const delay = target.getAttribute('data-aos-delay') || 0;
                    
                    setTimeout(() => {
                        target.classList.add('aos-animate');
                    }, delay);
                    
                    // Прекращаем наблюдение после анимации
                    observer.unobserve(target);
                }
            });
        }, observerOptions);
        
        // Наблюдаем за элементами с data-aos
        document.querySelectorAll('[data-aos]').forEach(el => {
            el.style.opacity = '0';
            
            const effect = el.getAttribute('data-aos');
            
            // Применяем начальные трансформации
            switch(effect) {
                case 'fade-up':
                    el.style.transform = 'translateY(30px)';
                    break;
                case 'fade-down':
                    el.style.transform = 'translateY(-30px)';
                    break;
                case 'fade-left':
                    el.style.transform = 'translateX(30px)';
                    break;
                case 'fade-right':
                    el.style.transform = 'translateX(-30px)';
                    break;
                case 'zoom-in':
                    el.style.transform = 'scale(0.9)';
                    break;
                default:
                    el.style.transform = 'none';
            }
            
            el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            
            observer.observe(el);
        });
        
        // CSS для анимированных элементов
        const style = document.createElement('style');
        style.textContent = `
            .aos-animate {
                opacity: 1 !important;
                transform: none !important;
            }
        `;
        document.head.appendChild(style);
    }
    
    // ===== Параллакс эффект =====
    function initParallax() {
        const parallaxElements = document.querySelectorAll('[data-parallax]');
        
        if (!parallaxElements.length) return;
        
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            
            parallaxElements.forEach(el => {
                const speed = el.getAttribute('data-parallax') || 0.5;
                const yPos = -(scrolled * speed);
                
                el.style.transform = `translateY(${yPos}px)`;
            });
        });
    }
    
    // ===== Счетчики =====
    function initCounters() {
        const counters = document.querySelectorAll('[data-counter]');
        
        if (!counters.length) return;
        
        const observerOptions = {
            threshold: 0.5
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const counter = entry.target;
                    const target = parseInt(counter.getAttribute('data-counter'));
                    const duration = 2000; // 2 секунды
                    const step = target / (duration / 16); // 60 FPS
                    
                    let current = 0;
                    
                    const updateCounter = () => {
                        current += step;
                        
                        if (current < target) {
                            counter.textContent = Math.floor(current);
                            requestAnimationFrame(updateCounter);
                        } else {
                            counter.textContent = target;
                        }
                    };
                    
                    updateCounter();
                    observer.unobserve(counter);
                }
            });
        }, observerOptions);
        
        counters.forEach(counter => {
            observer.observe(counter);
        });
    }
    
    // ===== Прогресс-бары =====
    function initProgressBars() {
        const progressBars = document.querySelectorAll('[data-progress]');
        
        if (!progressBars.length) return;
        
        const observerOptions = {
            threshold: 0.5
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const bar = entry.target;
                    const progress = bar.getAttribute('data-progress');
                    
                    bar.style.width = progress + '%';
                    observer.unobserve(bar);
                }
            });
        }, observerOptions);
        
        progressBars.forEach(bar => {
            bar.style.width = '0%';
            bar.style.transition = 'width 1.5s ease';
            observer.observe(bar);
        });
    }
    
    // Инициализация дополнительных функций
    initCounters();
    initProgressBars();
    
})();





