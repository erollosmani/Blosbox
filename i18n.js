// Blosbox Localization Engine - i18n.js
document.addEventListener('DOMContentLoaded', () => {
    console.log("i18n Engine Loaded");
    
    // Supported languages
    const supportedLanguages = ['en', 'fr', 'de', 'it', 'sv', 'nl', 'sq', 'mk'];
    
    // Helper to get query parameter
    function getQueryParam(name) {
        try {
            const urlParams = new URLSearchParams(window.location.search);
            return urlParams.get(name);
        } catch (e) {
            return null;
        }
    }

    // Helper for safe localStorage access
    function getStoredLanguage() {
        try {
            return localStorage.getItem('selected_language');
        } catch (e) {
            return null;
        }
    }
    
    function setStoredLanguage(lang) {
        try {
            localStorage.setItem('selected_language', lang);
        } catch (e) {
            // Silently absorb restricted environments exceptions
        }
    }

    // 1. Determine active language (safe URL query param first, then localStorage fallback)
    let activeLang = 'en';
    try {
        activeLang = getQueryParam('lang');
        if (!activeLang) {
            activeLang = getStoredLanguage();
        }
        
        if (!activeLang || !supportedLanguages.includes(activeLang)) {
            // Detect browser language
            try {
                const browserLang = navigator.language || navigator.userLanguage;
                const shortLang = browserLang.substring(0, 2).toLowerCase();
                
                if (supportedLanguages.includes(shortLang)) {
                    activeLang = shortLang;
                } else {
                    activeLang = 'en'; // Default fallback
                }
            } catch (e) {
                activeLang = 'en';
            }
        }
        setStoredLanguage(activeLang);
    } catch (e) {
        console.error("Error determining active language:", e);
        activeLang = 'en';
    }
    
    // Clone and mount language selector for mobile view
    try {
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
    } catch (e) {
        console.error("Error cloning mobile language switcher:", e);
    }
    
    // Expose language switcher globally
    window.changeLanguage = function(langCode) {
        try {
            if (!supportedLanguages.includes(langCode)) return;
            
            console.log("Switching language to:", langCode);
            setStoredLanguage(langCode);
            activeLang = langCode;
            
            applyTranslations(langCode);
            updateLanguageSelectorUI(langCode);
            updateInternalLinks(langCode);
            
            // Explicitly close dropdown menus and active states after selecting a language
            const menus = document.querySelectorAll('.lang-dropdown-menu');
            menus.forEach(menu => {
                try {
                    menu.classList.remove('active');
                } catch (err) {}
            });
            
            const dropdowns = document.querySelectorAll('.lang-dropdown, .mobile-lang-dropdown');
            dropdowns.forEach(dropdown => {
                try {
                    dropdown.classList.remove('active');
                } catch (err) {}
            });

            // Close the mobile navigation drawer if open
            const navLinks = document.querySelector('.nav-links');
            const mobileBtn = document.querySelector('.mobile-menu-btn');
            if (navLinks && navLinks.classList.contains('active')) {
                navLinks.classList.remove('active');
                if (mobileBtn) mobileBtn.innerHTML = '☰';
            }
        } catch (e) {
            console.error("Error inside changeLanguage:", e);
        }
    };
    
    // 2. Scan DOM and translate
    function applyTranslations(lang) {
        try {
            if (typeof translations === 'undefined') {
                console.error("Translation database not found. Make sure translations.js is loaded first.");
                return;
            }
            
            const langData = translations[lang];
            if (!langData) return;
            
            // Translate all elements with data-i18n
            const translateElements = document.querySelectorAll('[data-i18n]');
            translateElements.forEach(el => {
                try {
                    const key = el.getAttribute('data-i18n');
                    if (langData[key] !== undefined) {
                        // If it's a form input, translate the placeholder
                        if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                            el.setAttribute('placeholder', langData[key]);
                        } else {
                            // Preserve the caret span (e.g. dropdown indicator arrow) if present inside the element
                            const caret = el.querySelector('.caret');
                            if (caret) {
                                el.innerHTML = langData[key] + ' ' + caret.outerHTML;
                            } else {
                                el.innerHTML = langData[key];
                            }
                        }
                    }
                } catch (innerErr) {
                    console.error("Error translating element:", el, innerErr);
                }
            });
            
            // Update document lang attribute
            document.documentElement.setAttribute('lang', lang);
        } catch (e) {
            console.error("Error applying translations:", e);
        }
    }
    
    // 3. Keep Navbar UI synced
    function updateLanguageSelectorUI(lang) {
        try {
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
                try {
                    const optLang = opt.getAttribute('data-lang');
                    if (optLang === lang) {
                        opt.classList.add('active');
                    } else {
                        opt.classList.remove('active');
                    }
                } catch (err) {}
            });
        } catch (e) {
            console.error("Error updating language selector UI:", e);
        }
    }
    
    // 4. Set up Navbar Dropdown Toggle event listeners
    function setupDropdownListeners() {
        try {
            // Prevent desktop language trigger click from scrolling page to the top
            const desktopTrigger = document.querySelector('.nav-links .lang-dropdown-trigger');
            if (desktopTrigger) {
                desktopTrigger.addEventListener('click', (e) => {
                    e.preventDefault();
                });
            }
            
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
                try {
                    item.addEventListener('click', (e) => {
                        e.preventDefault();
                        const lang = item.getAttribute('data-lang');
                        window.changeLanguage(lang);
                    });
                } catch (err) {}
            });
        } catch (e) {
            console.error("Error setting up dropdown listeners:", e);
        }
    }
    
    // 5. Update all internal .html links with active lang query parameters
    function updateInternalLinks(lang) {
        try {
            const links = document.querySelectorAll('a');
            links.forEach(link => {
                try {
                    const href = link.getAttribute('href');
                    if (href && !href.startsWith('#') && !href.includes('://') && !href.startsWith('mailto:') && !href.startsWith('tel:')) {
                        // Parse page path to ensure we only target HTML pages or directory links (not PDFs or assets)
                        const cleanPath = href.split('?')[0].split('#')[0];
                        const isHtml = cleanPath.endsWith('.html') || !cleanPath.includes('.');
                        if (!isHtml) return;
                        
                        try {
                            // Extract page path and query params
                            const parts = href.split('?');
                            const basePath = parts[0];
                            const searchParams = new URLSearchParams(parts[1] || '');
                            
                            searchParams.set('lang', lang);
                            link.setAttribute('href', basePath + '?' + searchParams.toString());
                        } catch (e) {
                            // Fail-safe simple query parameter append
                            const cleanHref = href.split('?')[0];
                            link.setAttribute('href', cleanHref + '?lang=' + lang);
                        }
                    }
                } catch (innerErr) {
                    console.error("Error updating single link:", link, innerErr);
                }
            });
        } catch (e) {
            console.error("Error updating internal links:", e);
        }
    }
    
    // Initial run
    try {
        applyTranslations(activeLang);
    } catch (e) {
        console.error("Initial applyTranslations failed:", e);
    }
    
    try {
        updateLanguageSelectorUI(activeLang);
    } catch (e) {
        console.error("Initial updateLanguageSelectorUI failed:", e);
    }
    
    try {
        updateInternalLinks(activeLang);
    } catch (e) {
        console.error("Initial updateInternalLinks failed:", e);
    }
    
    try {
        setupDropdownListeners();
    } catch (e) {
        console.error("Initial setupDropdownListeners failed:", e);
    }
});
