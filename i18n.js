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

    // 1. Determine active language (URL path subfolder first e.g. /fr/, /de/, then query param, then localStorage)
    let activeLang = 'en';
    try {
        const pathSegments = window.location.pathname.split('/').filter(Boolean);
        const pathLang = pathSegments.find(p => supportedLanguages.includes(p.toLowerCase()));
        if (pathLang) {
            activeLang = pathLang.toLowerCase();
        } else {
            activeLang = getQueryParam('lang') || getStoredLanguage();
        }
        
        if (!activeLang || !supportedLanguages.includes(activeLang)) {
            activeLang = 'en'; // Default to English for root visitors
        }
        setStoredLanguage(activeLang);
    } catch (e) {
        console.error("Error determining active language:", e);
        activeLang = 'en';
    }
    
    // Expose active language globally
    window.i18n = {
        get currentLang() { return activeLang; },
        supportedLanguages: supportedLanguages
    };
    
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

            // Dispatch event for dynamic apps like calculator
            window.dispatchEvent(new CustomEvent('languageChanged', { detail: { lang: langCode } }));
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

            // Update Dynamic SEO Meta Tags & Hreflang links
            updateSeoMetadata(lang, langData);
        } catch (e) {
            console.error("Error applying translations:", e);
        }
    }

    // Dynamic SEO, Hreflang & OpenGraph updater
    function updateSeoMetadata(lang, langData) {
        try {
            let path = window.location.pathname.split('/').pop().toLowerCase();
            if (!path || path === '' || path === '/') {
                path = 'index.html';
            }
            const rawKey = path.replace('.html', '') || 'home';
            const pageKey = (rawKey === 'index') ? 'home' : rawKey;
            
            // 1. Dynamic Page Title
            const titleKey = 'meta_title_' + pageKey;
            if (langData[titleKey]) {
                document.title = langData[titleKey];
            }
            
            // 2. Meta Description & OpenGraph Description
            const descKey = 'meta_desc_' + pageKey;
            if (langData[descKey]) {
                let metaDesc = document.querySelector('meta[name="description"]');
                if (!metaDesc) {
                    metaDesc = document.createElement('meta');
                    metaDesc.name = 'description';
                    document.head.appendChild(metaDesc);
                }
                metaDesc.setAttribute('content', langData[descKey]);
                
                let ogDesc = document.querySelector('meta[property="og:description"]');
                if (!ogDesc) {
                    ogDesc = document.createElement('meta');
                    ogDesc.setAttribute('property', 'og:description');
                    document.head.appendChild(ogDesc);
                }
                ogDesc.setAttribute('content', langData[descKey]);
            }
            
            // 3. OpenGraph Title & Locale
            if (langData[titleKey]) {
                let ogTitle = document.querySelector('meta[property="og:title"]');
                if (!ogTitle) {
                    ogTitle = document.createElement('meta');
                    ogTitle.setAttribute('property', 'og:title');
                    document.head.appendChild(ogTitle);
                }
                ogTitle.setAttribute('content', langData[titleKey]);
            }
            
            let ogLocale = document.querySelector('meta[property="og:locale"]');
            if (!ogLocale) {
                ogLocale = document.createElement('meta');
                ogLocale.setAttribute('property', 'og:locale');
                document.head.appendChild(ogLocale);
            }
            const localeMap = { en: 'en_US', fr: 'fr_FR', de: 'de_DE', it: 'it_IT', sv: 'sv_SE', nl: 'nl_NL', sq: 'sq_AL', mk: 'mk_MK' };
            ogLocale.setAttribute('content', localeMap[lang] || 'en_US');
            
        } catch (e) {
            console.error("Error updating SEO metadata:", e);
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
                    item.addEventListener('click', () => {
                        const lang = item.getAttribute('data-lang');
                        if (lang) {
                            setStoredLanguage(lang);
                        }
                    });
                } catch (err) {}
            });
        } catch (e) {
            console.error("Error setting up dropdown listeners:", e);
        }
    }
    
    // 5. Internal link management (preserve clean static URLs)
    function updateInternalLinks(lang) {
        // Preserves clean static URLs for search engines and direct subfolder routing
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
