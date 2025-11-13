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
        initNavbarSections(); // Navbar sections tracking
        initCatalogCtaTracking(); // Tracking CTA кликов каталога
        initLanguageSwitcher(); // Language switcher
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
        
        const visibleNavLinks = Array.from(navLinks).map(link => link.getAttribute('href'));
        let current = sections.length ? sections[0].getAttribute('id') : '';
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            
            if (window.pageYOffset >= sectionTop - 100) {
                const sectionId = section.getAttribute('id');
                if (visibleNavLinks.includes(`#${sectionId}`)) {
                    current = sectionId;
                }
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
    
        if (!slider || !prevBtn || !nextBtn) {
            return;
        }
    
        const cards = Array.from(slider.querySelectorAll('.product-card'));
        if (!cards.length) {
            return;
        }
    
        let currentPage = 0;
        let autoScrollInterval;
        let metrics = buildMetrics();
    
        function getGap() {
            const styles = window.getComputedStyle(slider);
            const gap = parseFloat(styles.columnGap || styles.gap || '0');
            return Number.isNaN(gap) ? 0 : gap;
        }
    
        function buildMetrics() {
            const sliderWidth = slider.clientWidth || slider.getBoundingClientRect().width || 1;
            const gap = getGap();
            const cardRect = cards[0].getBoundingClientRect();
            const cardWidth = cardRect.width || 320;
            const visibleCount = Math.max(1, Math.floor((sliderWidth + gap) / Math.max(cardWidth + gap, 1)));
            const totalPages = Math.max(1, Math.ceil(cards.length / visibleCount));
            const maxScroll = Math.max(0, slider.scrollWidth - sliderWidth);
    
            const pageOffsets = [];
            for (let page = 0; page < totalPages; page += 1) {
                const firstIndex = Math.min(page * visibleCount, Math.max(cards.length - visibleCount, 0));
                const offset = cards[firstIndex]?.offsetLeft ?? 0;
                pageOffsets.push(Math.min(offset, maxScroll));
            }
    
            if (!pageOffsets.includes(maxScroll) && maxScroll > 0) {
                pageOffsets[pageOffsets.length - 1] = maxScroll;
            }
    
            return { gap, cardWidth, visibleCount, totalPages, pageOffsets, maxScroll };
        }
    
        function updateDots() {
            if (!dotsContainer) return;
            dotsContainer.innerHTML = '';
            for (let i = 0; i < metrics.totalPages; i += 1) {
                const dot = document.createElement('div');
                dot.className = 'slider-dot';
                if (i === currentPage) {
                    dot.classList.add('active');
                }
                dot.addEventListener('click', () => {
                    stopAutoScroll();
                    goToPage(i);
                    startAutoScroll();
                }, { passive: true });
                dotsContainer.appendChild(dot);
            }
        }
    
        function updateButtons() {
            prevBtn.disabled = currentPage === 0;
            nextBtn.disabled = currentPage >= metrics.totalPages - 1;
        }
    
        function goToPage(pageIndex, animated = true) {
            const boundedIndex = Math.max(0, Math.min(pageIndex, metrics.totalPages - 1));
            currentPage = boundedIndex;
            const targetLeft = metrics.pageOffsets[boundedIndex] ?? 0;
            slider.scrollTo({
                left: targetLeft,
                behavior: animated ? 'smooth' : 'auto'
            });
            updateButtons();
            if (dotsContainer) {
                const dots = dotsContainer.querySelectorAll('.slider-dot');
                dots.forEach((dot, index) => {
                    dot.classList.toggle('active', index === currentPage);
                });
            }
        }
    
        function startAutoScroll() {
            if (metrics.totalPages <= 1) return;
            stopAutoScroll();
            autoScrollInterval = window.setInterval(() => {
                if (currentPage < metrics.totalPages - 1) {
                    goToPage(currentPage + 1);
                } else {
                    goToPage(0);
                }
            }, 6000);
        }
    
        function stopAutoScroll() {
            if (autoScrollInterval) {
                window.clearInterval(autoScrollInterval);
                autoScrollInterval = undefined;
            }
        }
    
        prevBtn.addEventListener('click', () => {
            stopAutoScroll();
            goToPage(currentPage - 1);
            startAutoScroll();
        });
    
        nextBtn.addEventListener('click', () => {
            stopAutoScroll();
            goToPage(currentPage + 1);
            startAutoScroll();
        });
    
        slider.addEventListener('mouseenter', stopAutoScroll);
        slider.addEventListener('mouseleave', startAutoScroll);
    
        window.addEventListener('resize', () => {
            const previousPage = currentPage;
            metrics = buildMetrics();
            currentPage = Math.min(previousPage, metrics.totalPages - 1);
            updateDots();
            goToPage(currentPage, false);
            updateButtons();
        });
    
        requestAnimationFrame(() => {
            metrics = buildMetrics();
            updateDots();
            updateButtons();
            goToPage(0, false);
            startAutoScroll();
        });
    }

    // ===== Отслеживание кликов по CTA каталога =====
    function initCatalogCtaTracking() {
        const trackableElements = document.querySelectorAll('[data-track-event="catalog-cta"]');
        if (!trackableElements.length) {
            return;
        }

        const pushAnalyticsEvent = (label) => {
            const payload = {
                event: 'catalog_cta_click',
                label,
                timestamp: Date.now()
            };

            if (window.dataLayer && Array.isArray(window.dataLayer)) {
                window.dataLayer.push(payload);
            } else if (typeof window.gtag === 'function') {
                window.gtag('event', 'catalog_cta_click', {
                    event_label: label,
                    event_category: 'catalog',
                    value: Date.now()
                });
            } else {
                console.info('Catalog CTA click', payload);
            }
        };

        trackableElements.forEach((element) => {
            const label = element.dataset.trackLabel || element.textContent.trim();
            element.addEventListener('click', () => pushAnalyticsEvent(label), { passive: true });
        });
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

    // ===== Отслеживание активной секции для navbar =====
    function initNavbarSections() {
        const header = document.querySelector('.header');
        const sections = document.querySelectorAll('section[id]');
        const navLinks = document.querySelectorAll('.nav-link');
        
        function updateActiveSection() {
            const scrollPos = window.scrollY + 100;
            let activeSection = sections.length ? sections[0].getAttribute('id') : '';
            
            sections.forEach(section => {
                const sectionTop = section.offsetTop;
                const sectionHeight = section.offsetHeight;
                const sectionId = section.getAttribute('id');
                
                if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight && visibilityHasLink(sectionId)) {
                    activeSection = sectionId;
                }
            });
            
            // Обновляем классы header
            header.classList.remove('hero-active', 'section-active');
            if (activeSection === 'hero') {
                header.classList.add('hero-active');
            } else {
                header.classList.add('section-active');
            }
            
            // Обновляем активную ссылку в навигации
            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${activeSection}`) {
                    link.classList.add('active');
                }
            });
        }

        function visibilityHasLink(sectionId) {
            return Array.from(navLinks).some(link => link.getAttribute('href') === `#${sectionId}`);
        }
        
        // Отслеживаем скролл
        window.addEventListener('scroll', updateActiveSection);
        
        // Инициализация
        updateActiveSection();
    }

    // ===== Переключатель языка =====
    function initLanguageSwitcher() {
        const langButtons = document.querySelectorAll('.lang-btn');
        
        if (langButtons.length === 0) return;
        
        // Обработчик клика на кнопки языка
        langButtons.forEach(btn => {
            btn.addEventListener('click', function() {
                const selectedLang = this.getAttribute('data-lang');
                
                // Убираем активный класс со всех кнопок
                langButtons.forEach(b => b.classList.remove('active'));
                
                // Добавляем активный класс к выбранной кнопке
                this.classList.add('active');
                
                // Отправляем запрос на сервер для смены языка
                fetch(`/set_language/${selectedLang}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                })
                .then(response => {
                    if (response.ok) {
                        // Перезагружаем страницу для применения нового языка
                        window.location.reload();
                    } else {
                        console.error('Ошибка при смене языка:', response.statusText);
                        // Возвращаем активный класс обратно при ошибке
                        btn.classList.remove('active');
                        langButtons.forEach(b => {
                            if (b.getAttribute('data-lang') === document.documentElement.lang) {
                                b.classList.add('active');
                            }
                        });
                    }
                })
                .catch(error => {
                    console.error('Ошибка сети при смене языка:', error);
                    // Возвращаем активный класс обратно при ошибке
                    btn.classList.remove('active');
                    langButtons.forEach(b => {
                        const currentLangButtons = document.querySelectorAll('.lang-btn.active');
                        if (currentLangButtons.length === 0) {
                            // Если нет активной кнопки, активируем RU по умолчанию
                            if (b.getAttribute('data-lang') === 'ru') {
                                b.classList.add('active');
                            }
                        }
                    });
                });
            });
        });
    }

})();





