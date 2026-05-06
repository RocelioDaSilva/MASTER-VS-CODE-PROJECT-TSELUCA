/* ============================================
   YourBusiness — Main JavaScript
   ============================================ */

(function () {
    'use strict';

    // === Mobile Navigation Toggle ===
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    if (hamburger && navLinks) {
        hamburger.addEventListener('click', function () {
            const isExpanded = this.getAttribute('aria-expanded') === 'true';
            this.setAttribute('aria-expanded', !isExpanded);
            navLinks.classList.toggle('active');
        });

        // Close menu when clicking a link
        navLinks.querySelectorAll('a').forEach(function (link) {
            link.addEventListener('click', function () {
                navLinks.classList.remove('active');
                hamburger.setAttribute('aria-expanded', 'false');
            });
        });

        // Close menu when clicking outside
        document.addEventListener('click', function (e) {
            if (!hamburger.contains(e.target) && !navLinks.contains(e.target)) {
                navLinks.classList.remove('active');
                hamburger.setAttribute('aria-expanded', 'false');
            }
        });

        // Close menu on Escape key
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && navLinks.classList.contains('active')) {
                navLinks.classList.remove('active');
                hamburger.setAttribute('aria-expanded', 'false');
                hamburger.focus();
            }
        });
    }

    // === Cookie Banner ===
    var cookieBanner = document.getElementById('cookieBanner');
    var cookieAccept = document.getElementById('cookieAccept');
    var cookieDecline = document.getElementById('cookieDecline');

    if (cookieBanner) {
        var cookieConsent = localStorage.getItem('cookieConsent');
        if (!cookieConsent) {
            // Show banner after a small delay for smooth appearance
            setTimeout(function () {
                cookieBanner.classList.add('visible');
                cookieBanner.setAttribute('aria-modal', 'true');
            }, 1000);
        }

        if (cookieAccept) {
            cookieAccept.addEventListener('click', function () {
                localStorage.setItem('cookieConsent', 'accepted');
                cookieBanner.classList.remove('visible');
                cookieBanner.removeAttribute('aria-modal');
            });
        }

        if (cookieDecline) {
            cookieDecline.addEventListener('click', function () {
                localStorage.setItem('cookieConsent', 'declined');
                cookieBanner.classList.remove('visible');
                cookieBanner.removeAttribute('aria-modal');
            });
        }
    }

    // === Contact Form Handling ===
    var contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function (e) {
            e.preventDefault();

            var formMessage = document.getElementById('formMessage');
            var isValid = true;

            // Validate required fields
            var requiredFields = contactForm.querySelectorAll('[required]');
            requiredFields.forEach(function (field) {
                var errorSpan = field.parentElement.querySelector('.field-error');
                if (!field.value.trim() && field.type !== 'checkbox') {
                    isValid = false;
                    field.style.borderColor = 'var(--color-accent, #ff0000)';
                    if (errorSpan) errorSpan.textContent = 'This field is required.';
                } else if (field.type === 'checkbox' && !field.checked) {
                    isValid = false;
                    if (errorSpan) errorSpan.textContent = 'You must agree to continue.';
                } else if (field.type === 'email' && field.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(field.value)) {
                    isValid = false;
                    field.style.borderColor = 'var(--color-accent, #ff0000)';
                    if (errorSpan) errorSpan.textContent = 'Please enter a valid email.';
                } else {
                    field.style.borderColor = '';
                    if (errorSpan) errorSpan.textContent = '';
                }
            });

            if (!isValid) {
                if (formMessage) {
                    formMessage.className = 'form-message error';
                    formMessage.textContent = 'Please fill in all required fields correctly.';
                }
                return;
            }

            // Simulate success (replace with actual endpoint when ready)
            var submitBtn = contactForm.querySelector('.submit-btn');
            if (submitBtn) {
                submitBtn.classList.add('loading');
                submitBtn.disabled = true;
                submitBtn.textContent = 'Sending...';
            }

            // Simulate network delay for realistic UX
            setTimeout(function () {
                if (formMessage) {
                    formMessage.className = 'form-message success';
                    formMessage.textContent = '✓ Thank you! Your message has been sent. We\'ll get back to you within 24 hours.';
                }

                contactForm.reset();

                if (submitBtn) {
                    submitBtn.classList.remove('loading');
                    submitBtn.disabled = false;
                    submitBtn.textContent = 'Send Message';
                }

                // Hide message after 8 seconds
                setTimeout(function () {
                    if (formMessage) formMessage.style.display = 'none';
                }, 8000);

                // Track in Google Analytics if available
                if (window.gtag) {
                    gtag('event', 'form_submission', {
                        event_category: 'contact_form'
                    });
                }
            }, 1500);
        });

        // Clear field errors on input
        contactForm.querySelectorAll('input, textarea, select').forEach(function (field) {
            field.addEventListener('input', function () {
                this.style.borderColor = '';
                var errorSpan = this.parentElement.querySelector('.field-error');
                if (errorSpan) errorSpan.textContent = '';
                var formMessage = document.getElementById('formMessage');
                if (formMessage && formMessage.classList.contains('error')) {
                    formMessage.style.display = 'none';
                }
            });
        });
    }

    // === URL Parameter Pre-fill (for services page links) ===
    var urlParams = new URLSearchParams(window.location.search);
    var serviceParam = urlParams.get('service');
    if (serviceParam) {
        var serviceSelect = document.getElementById('service');
        if (serviceSelect) {
            // Try to match the option value
            var options = serviceSelect.querySelectorAll('option');
            options.forEach(function (option) {
                if (option.value === serviceParam) {
                    option.selected = true;
                }
            });
        }
    }

    // === FAQ Accordion (enhanced with accessibility) ===
    var faqQuestions = document.querySelectorAll('.faq-question');
    faqQuestions.forEach(function (question, index) {
        // Add ARIA attributes
        question.setAttribute('role', 'button');
        question.setAttribute('tabindex', '0');
        question.setAttribute('aria-expanded', 'false');
        question.setAttribute('id', 'faq-q-' + index);

        var answer = question.nextElementSibling;
        if (answer && answer.classList.contains('faq-answer')) {
            answer.setAttribute('role', 'region');
            answer.setAttribute('aria-labelledby', 'faq-q-' + index);
            answer.setAttribute('aria-hidden', 'true');
        }

        function toggleFaq() {
            var item = question.closest('.faq-item');
            var isActive = item.classList.contains('active');
            item.classList.toggle('active');
            question.setAttribute('aria-expanded', !isActive);
            if (answer) {
                answer.setAttribute('aria-hidden', isActive);
            }
        }

        question.addEventListener('click', toggleFaq);

        // Keyboard support
        question.addEventListener('keydown', function (e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                toggleFaq();
            }
        });
    });

    // === Smooth Scroll for Anchor Links ===
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
            var targetId = this.getAttribute('href');
            if (targetId === '#') return;
            var target = document.querySelector(targetId);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // === Active Nav Link Highlighting ===
    var currentPage = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.nav-links a').forEach(function (link) {
        if (link.getAttribute('href') === currentPage) {
            link.setAttribute('aria-current', 'page');
        }
    });

    // === Back to Top Button ===
    var backToTop = document.querySelector('.back-to-top');
    if (backToTop) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 400) {
                backToTop.classList.add('visible');
            } else {
                backToTop.classList.remove('visible');
            }
        }, { passive: true });

        backToTop.addEventListener('click', function () {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // === Scroll Reveal Animations ===
    var animatedElements = document.querySelectorAll('.fade-in, .fade-in-left, .fade-in-right');
    if (animatedElements.length > 0 && 'IntersectionObserver' in window) {
        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

        animatedElements.forEach(function (el) {
            observer.observe(el);
        });
    }

    // === Phone Number Validation ===
    var phoneField = document.getElementById('phone');
    if (phoneField) {
        phoneField.addEventListener('input', function () {
            // Allow only digits, spaces, dashes, parentheses, plus
            this.value = this.value.replace(/[^\d\s\-\(\)\+]/g, '');
        });
    }

})();
