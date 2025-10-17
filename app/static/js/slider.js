/**
 * Слайдер отзывов для OilFusion Landing
 */

(function() {
    'use strict';
    
    document.addEventListener('DOMContentLoaded', function() {
        initReviewsSlider();
    });
    
    function initReviewsSlider() {
        const sliderWrapper = document.querySelector('.reviews-wrapper');
        
        if (!sliderWrapper) return;
        
        const slides = sliderWrapper.querySelectorAll('.review-slide');
        const prevBtn = document.querySelector('.slider-prev');
        const nextBtn = document.querySelector('.slider-next');
        const dotsContainer = document.querySelector('.slider-dots');
        
        if (!slides.length) return;
        
        let currentSlide = 0;
        const totalSlides = slides.length;
        
        // Создание индикаторов
        function createDots() {
            if (!dotsContainer) return;
            
            dotsContainer.innerHTML = '';
            
            for (let i = 0; i < totalSlides; i++) {
                const dot = document.createElement('button');
                dot.classList.add('slider-dot');
                dot.setAttribute('aria-label', `Перейти к отзыву ${i + 1}`);
                
                if (i === 0) {
                    dot.classList.add('active');
                }
                
                dot.addEventListener('click', () => goToSlide(i));
                dotsContainer.appendChild(dot);
            }
        }
        
        // Переход к слайду
        function goToSlide(index) {
            // Ограничиваем индекс
            if (index < 0) {
                currentSlide = totalSlides - 1;
            } else if (index >= totalSlides) {
                currentSlide = 0;
            } else {
                currentSlide = index;
            }
            
            // Обновляем позицию
            const offset = -currentSlide * 100;
            sliderWrapper.style.transform = `translateX(${offset}%)`;
            
            // Обновляем индикаторы
            updateDots();
        }
        
        // Обновление индикаторов
        function updateDots() {
            const dots = dotsContainer?.querySelectorAll('.slider-dot');
            
            if (!dots) return;
            
            dots.forEach((dot, index) => {
                if (index === currentSlide) {
                    dot.classList.add('active');
                } else {
                    dot.classList.remove('active');
                }
            });
        }
        
        // Следующий слайд
        function nextSlide() {
            goToSlide(currentSlide + 1);
        }
        
        // Предыдущий слайд
        function prevSlide() {
            goToSlide(currentSlide - 1);
        }
        
        // Обработчики событий
        if (nextBtn) {
            nextBtn.addEventListener('click', nextSlide);
        }
        
        if (prevBtn) {
            prevBtn.addEventListener('click', prevSlide);
        }
        
        // Автопрокрутка
        let autoplayInterval;
        
        function startAutoplay() {
            autoplayInterval = setInterval(nextSlide, 5000);
        }
        
        function stopAutoplay() {
            clearInterval(autoplayInterval);
        }
        
        // Остановка автопрокрутки при наведении
        sliderWrapper.addEventListener('mouseenter', stopAutoplay);
        sliderWrapper.addEventListener('mouseleave', startAutoplay);
        
        // Свайп на мобильных устройствах
        let touchStartX = 0;
        let touchEndX = 0;
        
        sliderWrapper.addEventListener('touchstart', function(e) {
            touchStartX = e.changedTouches[0].screenX;
        });
        
        sliderWrapper.addEventListener('touchend', function(e) {
            touchEndX = e.changedTouches[0].screenX;
            handleSwipe();
        });
        
        function handleSwipe() {
            const swipeThreshold = 50;
            
            if (touchEndX < touchStartX - swipeThreshold) {
                // Свайп влево
                nextSlide();
            }
            
            if (touchEndX > touchStartX + swipeThreshold) {
                // Свайп вправо
                prevSlide();
            }
        }
        
        // Управление клавиатурой
        document.addEventListener('keydown', function(e) {
            if (e.key === 'ArrowLeft') {
                prevSlide();
            } else if (e.key === 'ArrowRight') {
                nextSlide();
            }
        });
        
        // Инициализация
        createDots();
        startAutoplay();
        
        // Настройка начальной позиции слайдов
        slides.forEach((slide, index) => {
            slide.style.position = 'absolute';
            slide.style.top = '0';
            slide.style.left = `${index * 100}%`;
            slide.style.width = '100%';
        });
        
        sliderWrapper.style.position = 'relative';
        sliderWrapper.style.display = 'flex';
        sliderWrapper.style.transition = 'transform 0.5s ease-in-out';
    }
    
})();





