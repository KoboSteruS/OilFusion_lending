/**
 * Основной JavaScript для лендинга OilFusion
 * Обработка интерактивных элементов и анимаций
 */

(function() {
    'use strict';
    
    // ===== Инициализация при загрузке DOM =====
    document.addEventListener('DOMContentLoaded', function() {
        initMobileMenu();
        initBackToTop();
        initSmoothScroll();
        initContactForm();
        initSubscribeForm();
        initBeforeAfterSlider();
        initHeaderScroll();
    });
    
    // ===== Мобильное меню =====
    function initMobileMenu() {
        const navbarToggle = document.getElementById('navbarToggle');
        const navbarMenu = document.getElementById('navbarMenu');
        
        if (!navbarToggle || !navbarMenu) return;
        
        navbarToggle.addEventListener('click', function() {
            navbarMenu.classList.toggle('active');
            navbarToggle.classList.toggle('active');
        });
        
        // Закрытие меню при клике на ссылку
        const navLinks = navbarMenu.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                navbarMenu.classList.remove('active');
                navbarToggle.classList.remove('active');
            });
        });
        
        // Закрытие меню при клике вне его
        document.addEventListener('click', function(event) {
            if (!navbarToggle.contains(event.target) && !navbarMenu.contains(event.target)) {
                navbarMenu.classList.remove('active');
                navbarToggle.classList.remove('active');
            }
        });
    }
    
    // ===== Отслеживание скролла для шапки =====
    function initHeaderScroll() {
        const header = document.querySelector('.header');
        if (!header) return;
        
        let lastScrollY = window.scrollY;
        
        window.addEventListener('scroll', function() {
            const currentScrollY = window.scrollY;
            
            if (currentScrollY > 100) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
            
            lastScrollY = currentScrollY;
        });
    }
    
    // ===== Кнопка "Наверх" =====
    function initBackToTop() {
        const backToTopBtn = document.getElementById('backToTop');
        
        if (!backToTopBtn) return;
        
        // Показ/скрытие кнопки при прокрутке
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                backToTopBtn.classList.add('visible');
            } else {
                backToTopBtn.classList.remove('visible');
            }
        });
        
        // Прокрутка наверх при клике
        backToTopBtn.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    // ===== Плавная прокрутка =====
    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                
                // Игнорируем пустые якоря
                if (href === '#' || href === '#!') {
                    e.preventDefault();
                    return;
                }
                
                const target = document.querySelector(href);
                
                if (target) {
                    e.preventDefault();
                    
                    const headerOffset = 80;
                    const elementPosition = target.getBoundingClientRect().top;
                    const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
                    
                    window.scrollTo({
                        top: offsetPosition,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }
    
    // ===== Форма контактов =====
    function initContactForm() {
        const contactForm = document.getElementById('contactForm');
        
        if (!contactForm) return;
        
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Здесь будет логика отправки формы
            console.log('Форма контактов отправлена');
            
            // Показываем уведомление (временная заглушка)
            alert('Спасибо! Мы свяжемся с вами в ближайшее время.');
            
            // Очищаем форму
            contactForm.reset();
        });
    }
    
    // ===== Форма подписки =====
    function initSubscribeForm() {
        const subscribeForm = document.getElementById('subscribeForm');
        
        if (!subscribeForm) return;
        
        subscribeForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const emailInput = this.querySelector('input[type="email"]');
            const email = emailInput.value;
            
            // Здесь будет логика подписки
            console.log('Подписка на email:', email);
            
            // Показываем уведомление (временная заглушка)
            alert('Спасибо за подписку!');
            
            // Очищаем форму
            subscribeForm.reset();
        });
    }
    
    // ===== Слайдер "До/После" =====
    function initBeforeAfterSlider() {
        const sliderHandle = document.getElementById('sliderHandle');
        
        if (!sliderHandle) return;
        
        const sliderWrapper = sliderHandle.closest('.slider-wrapper');
        const afterImage = sliderWrapper.querySelector('.after-image');
        
        let isDragging = false;
        
        // Начало перетаскивания
        sliderHandle.addEventListener('mousedown', startDragging);
        sliderHandle.addEventListener('touchstart', startDragging);
        
        // Перетаскивание
        document.addEventListener('mousemove', drag);
        document.addEventListener('touchmove', drag);
        
        // Окончание перетаскивания
        document.addEventListener('mouseup', stopDragging);
        document.addEventListener('touchend', stopDragging);
        
        function startDragging(e) {
            isDragging = true;
            e.preventDefault();
        }
        
        function stopDragging() {
            isDragging = false;
        }
        
        function drag(e) {
            if (!isDragging) return;
            
            const rect = sliderWrapper.getBoundingClientRect();
            let x;
            
            if (e.type === 'touchmove') {
                x = e.touches[0].clientX - rect.left;
            } else {
                x = e.clientX - rect.left;
            }
            
            // Ограничиваем движение
            x = Math.max(0, Math.min(x, rect.width));
            
            const percentage = (x / rect.width) * 100;
            
            // Обновляем позицию
            sliderHandle.style.left = percentage + '%';
            afterImage.style.clipPath = `inset(0 ${100 - percentage}% 0 0)`;
        }
    }
    
    // ===== Добавление активного состояния навигации при прокрутке =====
    window.addEventListener('scroll', function() {
        const sections = document.querySelectorAll('section[id]');
        const navLinks = document.querySelectorAll('.nav-link');
        
        let current = '';
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            
            if (window.pageYOffset >= sectionTop - 100) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === '#' + current) {
                link.classList.add('active');
            }
        });
    });
    
    // ===== Ленивая загрузка изображений =====
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                        observer.unobserve(img);
                    }
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
    
})();





