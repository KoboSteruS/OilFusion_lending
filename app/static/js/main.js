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
        initProductsSlider();
        initAuraCloudSlider(); // AuraCloud slider
    });
    
    // ===== Мобильное меню =====
    function initMobileMenu() {
        const navbarToggle = document.getElementById('navbarToggle');
        const navbarMenu = document.getElementById('navbarMenu');
        
        if (!navbarToggle || !navbarMenu) return;
        
        navbarToggle.addEventListener('click', function() {
            navbarMenu.classList.toggle('active');
            navbarToggle.classList.toggle('active');
            
            // Добавляем/убираем класс для анимации иконки
            if (navbarMenu.classList.contains('active')) {
                navbarToggle.classList.add('active');
            } else {
                navbarToggle.classList.remove('active');
            }
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

    // ===== Слайдер продуктов =====
    function initProductsSlider() {
        const slider = document.getElementById('productsSlider');
        const prevBtn = document.getElementById('productsPrev');
        const nextBtn = document.getElementById('productsNext');
        const dotsContainer = document.getElementById('productsDots');
        
        if (!slider || !prevBtn || !nextBtn) return;
        
        const cards = slider.querySelectorAll('.product-card');
        const cardWidth = 350; // 320px + 30px gap
        let currentIndex = 0;
        let autoScrollInterval;
        
        // Создаем индикаторы
        function createDots() {
            if (!dotsContainer) return;
            
            dotsContainer.innerHTML = '';
            const totalSlides = Math.ceil(cards.length / 3); // Показываем по 3 карточки
            
            for (let i = 0; i < totalSlides; i++) {
                const dot = document.createElement('div');
                dot.className = 'slider-dot';
                if (i === 0) dot.classList.add('active');
                dot.addEventListener('click', () => goToSlide(i));
                dotsContainer.appendChild(dot);
            }
        }
        
        // Переход к слайду
        function goToSlide(index) {
            const totalSlides = Math.ceil(cards.length / 3);
            currentIndex = Math.max(0, Math.min(index, totalSlides - 1));
            
            slider.scrollTo({
                left: currentIndex * cardWidth * 3,
                behavior: 'smooth'
            });
            
            updateDots();
            updateButtons();
        }
        
        // Обновление индикаторов
        function updateDots() {
            if (!dotsContainer) return;
            const dots = dotsContainer.querySelectorAll('.slider-dot');
            dots.forEach((dot, index) => {
                dot.classList.toggle('active', index === currentIndex);
            });
        }
        
        // Обновление кнопок
        function updateButtons() {
            const totalSlides = Math.ceil(cards.length / 3);
            prevBtn.disabled = currentIndex === 0;
            nextBtn.disabled = currentIndex === totalSlides - 1;
        }
        
        // Автопрокрутка
        function startAutoScroll() {
            autoScrollInterval = setInterval(() => {
                const totalSlides = Math.ceil(cards.length / 3);
                if (currentIndex < totalSlides - 1) {
                    goToSlide(currentIndex + 1);
                } else {
                    goToSlide(0);
                }
            }, 5000); // 5 секунд
        }
        
        function stopAutoScroll() {
            if (autoScrollInterval) {
                clearInterval(autoScrollInterval);
            }
        }
        
        // Обработчики событий
        prevBtn.addEventListener('click', () => {
            stopAutoScroll();
            goToSlide(currentIndex - 1);
            startAutoScroll();
        });
        
        nextBtn.addEventListener('click', () => {
            stopAutoScroll();
            goToSlide(currentIndex + 1);
            startAutoScroll();
        });
        
        // Остановка автопрокрутки при наведении
        slider.addEventListener('mouseenter', stopAutoScroll);
        slider.addEventListener('mouseleave', startAutoScroll);
        
        // Инициализация
        createDots();
        updateButtons();
        startAutoScroll();
    }

    // ===== AuraCloud Слайдер До/После =====
    function initAuraCloudSlider() {
        const slider = document.getElementById('auracloudSlider');
        if (!slider) return;

        const handle = slider.querySelector('.slider-handle');
        const afterImage = slider.querySelector('.after-image');
        const sliderButton = slider.querySelector('.slider-button');
        
        if (!handle || !afterImage || !sliderButton) return;

        let isDragging = false;
        let startX = 0;
        let currentX = 0;

        // Обработчики мыши
        sliderButton.addEventListener('mousedown', startDrag);
        handle.addEventListener('mousedown', startDrag);
        
        // Обработчики касания для мобильных
        sliderButton.addEventListener('touchstart', startDrag, { passive: false });
        handle.addEventListener('touchstart', startDrag, { passive: false });

        function startDrag(e) {
            isDragging = true;
            startX = e.type === 'mousedown' ? e.clientX : e.touches[0].clientX;
            currentX = startX;
            
            document.addEventListener('mousemove', drag);
            document.addEventListener('mouseup', stopDrag);
            document.addEventListener('touchmove', drag, { passive: false });
            document.addEventListener('touchend', stopDrag);
            
            e.preventDefault();
        }

        function drag(e) {
            if (!isDragging) return;
            
            currentX = e.type === 'mousemove' ? e.clientX : e.touches[0].clientX;
            updateSlider();
            e.preventDefault();
        }

        function stopDrag() {
            isDragging = false;
            document.removeEventListener('mousemove', drag);
            document.removeEventListener('mouseup', stopDrag);
            document.removeEventListener('touchmove', drag);
            document.removeEventListener('touchend', stopDrag);
        }

        function updateSlider() {
            const sliderRect = slider.getBoundingClientRect();
            const sliderWidth = sliderRect.width;
            const relativeX = currentX - sliderRect.left;
            const percentage = Math.max(0, Math.min(100, (relativeX / sliderWidth) * 100));
            
            // Обновляем позицию ручки
            handle.style.left = percentage + '%';
            
            // Обновляем clip-path для изображения "После"
            afterImage.style.clipPath = `polygon(${percentage}% 0%, 100% 0%, 100% 100%, ${percentage}% 100%)`;
        }

        // Обработчик клика по слайдеру
        slider.addEventListener('click', function(e) {
            if (e.target === slider || e.target.classList.contains('slider-container')) {
                const sliderRect = slider.getBoundingClientRect();
                const relativeX = e.clientX - sliderRect.left;
                const percentage = (relativeX / sliderRect.width) * 100;
                
                currentX = e.clientX;
                updateSlider();
            }
        });

        // Инициализация в центре
        updateSlider();
    }

})();





