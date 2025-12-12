// =========================================
// 1. MOBILE MENU TOGGLE
// =========================================
const mobileToggle = document.querySelector('.mobile-toggle');
const nav = document.querySelector('.nav');
const navLinks = document.querySelectorAll('.nav-link');

mobileToggle.addEventListener('click', () => {
    nav.classList.toggle('active');
    // Change icon
    const icon = mobileToggle.querySelector('i');
    if (nav.classList.contains('active')) {
        icon.classList.remove('fa-bars');
        icon.classList.add('fa-times');
    } else {
        icon.classList.remove('fa-times');
        icon.classList.add('fa-bars');
    }
});

// Close menu when clicking a link
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        nav.classList.remove('active');
        const icon = mobileToggle.querySelector('i');
        icon.classList.remove('fa-times');
        icon.classList.add('fa-bars');
    });
});

// =========================================
// 2. HEADER SCROLL EFFECT
// =========================================
// =========================================
// 2. HEADER SCROLL EFFECT (Optimized)
// =========================================
const header = document.querySelector('.header');
let scrollTimeout;

window.addEventListener('scroll', () => {
    if (scrollTimeout) return;
    
    scrollTimeout = setTimeout(() => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
        scrollTimeout = null;
    }, 50); // Throttle to 50ms
});

// =========================================
// 3. TYPEWRITER EFFECT (only on index.html)
// =========================================
const textElement = document.querySelector('.typewriter');


// =========================================
// 4. SCROLL REVEAL ANIMATION
// =========================================
// Simple Intersection Observer for fade-in animations
const observerOptions = {
    threshold: 0.1
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('show');
            observer.unobserve(entry.target); // Only animate once
        }
    });
}, observerOptions);

// Add 'hidden' class to elements we want to animate
const hiddenElements = document.querySelectorAll('.section-title, .about-content, .skill-category, .project-card, .contact-wrapper');

// Animations are now handled via CSS classes in style.css for better performance

// =========================================
// 5. CONTACT FORM AJAX HANDLER
// =========================================
const contactForm = document.getElementById('contact-form');
const statusMessage = document.getElementById('status-message');

if (contactForm) {
    contactForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const submitBtn = contactForm.querySelector('.submit-btn');
        
        // Show loading state
        submitBtn.disabled = true;
        submitBtn.textContent = "Envoi en cours...";
        statusMessage.style.display = 'none';

        // NOTE: Replace these with your actual Service ID and Template ID
        const serviceID = 'service_mjqal0a';
        const templateID = 'template_72lv4fn';

        emailjs.sendForm(serviceID, templateID, this)
            .then(() => {
                // Success
                statusMessage.style.display = 'block';
                statusMessage.style.backgroundColor = '#d1fae5';
                statusMessage.style.color = '#065f46';
                statusMessage.innerHTML = '<i class="fas fa-check-circle"></i> Merci ! Votre message a été envoyé.';
                contactForm.reset();
            }, (err) => {
                // Error
                console.error('EmailJS Error:', err);
                statusMessage.style.display = 'block';
                statusMessage.style.backgroundColor = '#fee2e2';
                statusMessage.style.color = '#991b1b';
                statusMessage.innerHTML = '<i class="fas fa-exclamation-circle"></i> Une erreur est survenue. Vérifiez la configuration EmailJS.';
            })
            .finally(() => {
                submitBtn.disabled = false;
                submitBtn.textContent = "Envoyer le message";
                
                // Hide success message after 8 seconds
                setTimeout(() => {
                    if (statusMessage.style.backgroundColor === 'rgb(209, 250, 229)') { // if green
                         statusMessage.style.display = 'none';
                    }
                }, 8000);
            });
    });
}

// =========================================
// 6. INTERNATIONALIZATION (I18N)
// =========================================
// Translations are now loaded from translations.js
// const translations = { ... };

// Language Switcher Logic
const langSelector = document.querySelector('.language-selector');
const langDropdown = document.querySelector('.lang-dropdown');
const currentLangSpan = document.getElementById('current-lang');
const currentFlagImg = document.getElementById('current-flag');
const langOptions = document.querySelectorAll('.lang-option');

// Init Language
const savedLang = localStorage.getItem('preferredLang') || 'fr';
setLanguage(savedLang);

// Toggle Dropdown
if (langSelector && langDropdown) {
    langSelector.addEventListener('click', (e) => {
        e.stopPropagation();
        const isActive = langSelector.classList.contains('active');
        
        if (isActive) {
            langSelector.classList.remove('active');
            langDropdown.style.display = 'none';
            langDropdown.style.visibility = 'hidden';
            langDropdown.style.opacity = '0';
        } else {
            langSelector.classList.add('active');
            langDropdown.style.display = 'flex';
            setTimeout(() => {
                langDropdown.style.visibility = 'visible';
                langDropdown.style.opacity = '1';
                langDropdown.style.transform = 'translateY(0) scale(1)';
            }, 10);
        }
    });

    document.addEventListener('click', (e) => {
        if (!langSelector.contains(e.target)) {
            langSelector.classList.remove('active');
            langDropdown.style.display = 'none';
            langDropdown.style.visibility = 'hidden';
            langDropdown.style.opacity = '0';
        }
    });
    
    langDropdown.style.display = 'none';
}

async function setLanguage(lang) {
    try {
        const response = await fetch(`locales/${lang}.json`);
        if (!response.ok) throw new Error(`Could not load ${lang} translations`);
        const translations = await response.json();

        // Update UI
        // Update UI
        if (currentLangSpan) currentLangSpan.textContent = lang.toUpperCase();
        
        // Map language code to flag code (en -> gb)
        let flagCode = lang;
        if (lang === 'en') flagCode = 'gb';
        
        if (currentFlagImg) currentFlagImg.src = `https://flagcdn.com/w40/${flagCode}.png`;

        // Update Text
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            const keys = key.split('.');
            let text = translations;
            for (const k of keys) {
                if (text[k] === undefined) return;
                text = text[k];
            }
            el.innerHTML = text;
        });

        // Update Placeholders
        document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
            const key = el.getAttribute('data-i18n-placeholder');
            const keys = key.split('.');
            let text = translations;
            for (const k of keys) {
                if (text[k] === undefined) return;
                text = text[k];
            }
            el.placeholder = text;
        });

        // Save
        localStorage.setItem('preferredLang', lang);

    } catch (error) {
        console.error("Error loading translations:", error);
    }
}

// Option Click
langOptions.forEach(option => {
    option.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation(); 
        const lang = option.getAttribute('data-lang');
        setLanguage(lang);

        langSelector.classList.remove('active');
        langDropdown.style.display = 'none';
    });
});

// =========================================
// 7. DYNAMIC FOOTER LOADER
// =========================================
async function loadFooter() {
    const placeholder = document.getElementById('footer-placeholder');
    if (!placeholder) return;

    try {
        const response = await fetch('footer.html');
        if (!response.ok) throw new Error('Failed to load footer');
        
        const html = await response.text();
        placeholder.innerHTML = html;

        // Set Year
        const yearSpan = document.getElementById('year');
        if (yearSpan) {
            yearSpan.textContent = new Date().getFullYear();
        }

        // Re-apply translations if language is set
        const savedLang = localStorage.getItem('preferredLang') || 'fr';
        setLanguage(savedLang);

    } catch (error) {
        console.error('Error loading footer:', error);
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadFooter();
    // No need to call setLanguage here again as it's called inside loadFooter for footer,
    // and presumably called earlier for the page. 
    // Actually, looking at previous code, setLanguage was called freely.
    // I'll leave it as is to be safe.
});
