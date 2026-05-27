// Blosbox Localization Engine - i18n.js
document.addEventListener('DOMContentLoaded', () => {
    console.log("i18n Engine Loaded");
    
    // Supported languages
    const supportedLanguages = ['en', 'fr', 'sq', 'it', 'de', 'nl', 'sv', 'mk'];
    
    // 1. Determine active language
    let activeLang = localStorage.getItem('selected_language');
    
    if (!activeLang) {
        // Detect browser language
        const browserLang = navigator.language || navigator.userLanguage;
        const shortLang = browserLang.substring(0, 2).toLowerCase();
        
        if (supportedLanguages.includes(shortLang)) {
            activeLang = shortLang;
        } else {
            activeLang = 'en'; // Default fallback
        }
        localStorage.setItem('selected_language', activeLang);
    }
    
    // Expose language switcher globally
    window.changeLanguage = function(langCode) {
        if (!supportedLanguages.includes(langCode)) return;
        
        console.log("Switching language to:", langCode);
        localStorage.setItem('selected_language', langCode);
        activeLang = langCode;
        
        applyTranslations(langCode);
        updateLanguageSelectorUI(langCode);
    };
    
    // 2. Scan DOM and translate
    function applyTranslations(lang) {
        if (typeof translations === 'undefined') {
            console.error("Translation database not found. Make sure translations.js is loaded first.");
            return;
        }
        
        const langData = translations[lang];
        if (!langData) return;
        
        // Translate all elements with data-i18n
        const translateElements = document.querySelectorAll('[data-i18n]');
        translateElements.forEach(el => {
            const key = el.getAttribute('data-i18n');
            if (langData[key] !== undefined) {
                // If it's a form input, translate the placeholder
                if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                    el.setAttribute('placeholder', langData[key]);
                } else {
                    // Update innerHTML to preserve basic formatting tags like strong, br, etc.
                    el.innerHTML = langData[key];
                }
            }
        });
        
        // Update document lang attribute
        document.documentElement.setAttribute('lang', lang);
    }
    
    // 3. Keep Navbar UI synced
    function updateLanguageSelectorUI(lang) {
        // Update selected language display text in dropdown button
        const activeLabel = document.getElementById('activeLangLabel');
        if (activeLabel) {
            activeLabel.textContent = lang.toUpperCase();
        }
        
        // Highlight active language item in dropdown list
        const langOptions = document.querySelectorAll('.lang-item');
        langOptions.forEach(opt => {
            const optLang = opt.getAttribute('data-lang');
            if (optLang === lang) {
                opt.classList.add('active');
            } else {
                opt.classList.remove('active');
            }
        });
    }
    
    // 4. Set up Navbar Dropdown Toggle event listeners
    function setupDropdownListeners() {
        const trigger = document.querySelector('.lang-dropdown-trigger');
        const menu = document.querySelector('.lang-dropdown-menu');
        
        if (trigger && menu) {
            // Toggle dropdown open state
            trigger.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                menu.classList.toggle('active');
            });
            
            // Close dropdown when clicking outside
            document.addEventListener('click', () => {
                menu.classList.remove('active');
            });
        }
        
        // Bind language click selectors
        const langItems = document.querySelectorAll('.lang-item');
        langItems.forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                const lang = item.getAttribute('data-lang');
                window.changeLanguage(lang);
            });
        });
    }
    
    // Initial run
    applyTranslations(activeLang);
    updateLanguageSelectorUI(activeLang);
    setupDropdownListeners();
});
