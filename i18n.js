// Blosbox Localization Engine - i18n.js
document.addEventListener('DOMContentLoaded', () => {
    console.log("i18n Engine Loaded");
    
    // Supported languages
    const supportedLanguages = ['en', 'fr', 'de', 'it', 'sv', 'nl', 'sq', 'mk'];
    
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
    
    // Clone and mount language selector for mobile view
    const desktopLangDropdown = document.querySelector('.nav-links .lang-dropdown');
    if (desktopLangDropdown && !document.querySelector('.mobile-lang-dropdown')) {
        const mobileLangDropdown = desktopLangDropdown.cloneNode(true);
        mobileLangDropdown.classList.remove('lang-dropdown');
        mobileLangDropdown.classList.add('mobile-lang-dropdown');
        
        // Update IDs in the cloned element to avoid duplicates
        const activeLabel = mobileLangDropdown.querySelector('#activeLangLabel');
        if (activeLabel) activeLabel.id = 'mobileActiveLangLabel';
        
        const navbar = document.querySelector('.navbar');
        const mobileBtn = document.querySelector('.mobile-menu-btn');
        if (navbar && mobileBtn) {
            navbar.insertBefore(mobileLangDropdown, mobileBtn);
            console.log("Dynamically created mobile language switcher");
        }
    }
    
    // Expose language switcher globally
    window.changeLanguage = function(langCode) {
        if (!supportedLanguages.includes(langCode)) return;
        
        console.log("Switching language to:", langCode);
        localStorage.setItem('selected_language', langCode);
        activeLang = langCode;
        
        applyTranslations(langCode);
        updateLanguageSelectorUI(langCode);
        
        // Explicitly close dropdown menus and active states after selecting a language
        const menus = document.querySelectorAll('.lang-dropdown-menu');
        menus.forEach(menu => {
            menu.classList.remove('active');
        });
        
        const dropdowns = document.querySelectorAll('.lang-dropdown, .mobile-lang-dropdown');
        dropdowns.forEach(dropdown => {
            dropdown.classList.remove('active');
        });
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
        
        // Also update mobile active label if it exists
        const mobileActiveLabel = document.getElementById('mobileActiveLangLabel');
        if (mobileActiveLabel) {
            mobileActiveLabel.textContent = lang.toUpperCase();
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
        
        // Mobile language switcher toggle
        const mobileTrigger = document.querySelector('.mobile-lang-dropdown .lang-dropdown-trigger');
        const mobileMenu = document.querySelector('.mobile-lang-dropdown .lang-dropdown-menu');
        
        if (mobileTrigger && mobileMenu) {
            mobileTrigger.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                mobileMenu.classList.toggle('active');
            });
            
            document.addEventListener('click', () => {
                mobileMenu.classList.remove('active');
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
