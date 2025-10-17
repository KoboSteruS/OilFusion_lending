/**
 * JavaScript для админки OilFusion Landing
 */

(function() {
    'use strict';
    
    document.addEventListener('DOMContentLoaded', function() {
        initAdminFeatures();
        initFormValidation();
        initAutoSave();
    });
    
    // ===== Инициализация функций админки =====
    function initAdminFeatures() {
        // Автоматическое скрытие flash сообщений
        const flashMessages = document.querySelectorAll('.admin-flash');
        flashMessages.forEach(message => {
            setTimeout(() => {
                message.style.opacity = '0';
                setTimeout(() => {
                    message.remove();
                }, 300);
            }, 5000);
        });
        
        // Подтверждение удаления
        const deleteButtons = document.querySelectorAll('.admin-btn-danger');
        deleteButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                if (!confirm('Вы уверены, что хотите удалить этот элемент?')) {
                    e.preventDefault();
                }
            });
        });
    }
    
    // ===== Валидация форм =====
    function initFormValidation() {
        const forms = document.querySelectorAll('.admin-form');
        
        forms.forEach(form => {
            form.addEventListener('submit', function(e) {
                if (!validateForm(form)) {
                    e.preventDefault();
                }
            });
        });
    }
    
    function validateForm(form) {
        let isValid = true;
        const requiredFields = form.querySelectorAll('[required]');
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                showFieldError(field, 'Это поле обязательно для заполнения');
                isValid = false;
            } else {
                clearFieldError(field);
            }
        });
        
        // Валидация email
        const emailFields = form.querySelectorAll('input[type="email"]');
        emailFields.forEach(field => {
            if (field.value && !isValidEmail(field.value)) {
                showFieldError(field, 'Введите корректный email адрес');
                isValid = false;
            }
        });
        
        return isValid;
    }
    
    function showFieldError(field, message) {
        clearFieldError(field);
        
        field.style.borderColor = '#DC3545';
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'admin-field-error';
        errorDiv.textContent = message;
        errorDiv.style.color = '#DC3545';
        errorDiv.style.fontSize = '0.875rem';
        errorDiv.style.marginTop = '4px';
        
        field.parentNode.appendChild(errorDiv);
    }
    
    function clearFieldError(field) {
        field.style.borderColor = '';
        
        const existingError = field.parentNode.querySelector('.admin-field-error');
        if (existingError) {
            existingError.remove();
        }
    }
    
    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
    
    // ===== Автосохранение =====
    function initAutoSave() {
        const textareas = document.querySelectorAll('.admin-form-textarea');
        
        textareas.forEach(textarea => {
            let saveTimeout;
            
            textarea.addEventListener('input', function() {
                clearTimeout(saveTimeout);
                saveTimeout = setTimeout(() => {
                    saveToLocalStorage(textarea);
                }, 2000);
            });
            
            // Восстановление из localStorage при загрузке
            restoreFromLocalStorage(textarea);
        });
    }
    
    function saveToLocalStorage(field) {
        const key = `admin_${field.name}_${window.location.pathname}`;
        localStorage.setItem(key, field.value);
        
        // Показать индикатор сохранения
        showSaveIndicator(field);
    }
    
    function restoreFromLocalStorage(field) {
        const key = `admin_${field.name}_${window.location.pathname}`;
        const savedValue = localStorage.getItem(key);
        
        if (savedValue && !field.value) {
            field.value = savedValue;
        }
    }
    
    function showSaveIndicator(field) {
        const indicator = document.createElement('div');
        indicator.className = 'admin-save-indicator';
        indicator.textContent = 'Сохранено локально';
        indicator.style.cssText = `
            position: absolute;
            top: -30px;
            right: 0;
            background: #28a745;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            z-index: 1000;
            opacity: 0;
            transition: opacity 0.3s ease;
        `;
        
        const container = field.closest('.admin-form-group');
        if (container) {
            container.style.position = 'relative';
            container.appendChild(indicator);
            
            // Показать индикатор
            setTimeout(() => {
                indicator.style.opacity = '1';
            }, 100);
            
            // Скрыть индикатор
            setTimeout(() => {
                indicator.style.opacity = '0';
                setTimeout(() => {
                    indicator.remove();
                }, 300);
            }, 2000);
        }
    }
    
    // ===== Утилиты =====
    
    // Функция для копирования текста в буфер обмена
    window.copyToClipboard = function(text) {
        navigator.clipboard.writeText(text).then(() => {
            showNotification('Текст скопирован в буфер обмена', 'success');
        }).catch(() => {
            showNotification('Ошибка при копировании', 'error');
        });
    };
    
    // Функция для показа уведомлений
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `admin-notification admin-notification-${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? '#28a745' : type === 'error' ? '#dc3545' : '#17a2b8'};
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            z-index: 10000;
            opacity: 0;
            transform: translateX(100%);
            transition: all 0.3s ease;
        `;
        
        document.body.appendChild(notification);
        
        // Показать уведомление
        setTimeout(() => {
            notification.style.opacity = '1';
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        // Скрыть уведомление
        setTimeout(() => {
            notification.style.opacity = '0';
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }
    
    // Функция для предварительного просмотра изображений
    window.previewImage = function(input, previewId) {
        const file = input.files[0];
        const preview = document.getElementById(previewId);
        
        if (file && preview) {
            const reader = new FileReader();
            reader.onload = function(e) {
                preview.src = e.target.result;
                preview.style.display = 'block';
            };
            reader.readAsDataURL(file);
        }
    };
    
    // Функция для подсчета символов в текстовых полях
    function initCharacterCounters() {
        const textareas = document.querySelectorAll('textarea[data-max-length]');
        
        textareas.forEach(textarea => {
            const maxLength = parseInt(textarea.getAttribute('data-max-length'));
            const counter = document.createElement('div');
            counter.className = 'admin-char-counter';
            counter.style.cssText = `
                text-align: right;
                font-size: 0.875rem;
                color: #6c757d;
                margin-top: 4px;
            `;
            
            textarea.parentNode.appendChild(counter);
            
            function updateCounter() {
                const currentLength = textarea.value.length;
                counter.textContent = `${currentLength}/${maxLength}`;
                
                if (currentLength > maxLength) {
                    counter.style.color = '#dc3545';
                } else if (currentLength > maxLength * 0.9) {
                    counter.style.color = '#ffc107';
                } else {
                    counter.style.color = '#6c757d';
                }
            }
            
            textarea.addEventListener('input', updateCounter);
            updateCounter();
        });
    }
    
    // Инициализация счетчиков символов
    initCharacterCounters();
    
})();

