/*
 * High-Converting Landing Page JavaScript
 * The Cat Scratching Solution eBook Landing Page
 * Conversion optimization and interactivity
 */

// ===== CONFIGURATION =====
const config = {
  // ConvertKit Integration (replace with your actual form IDs)
  convertkit: {
    forms: {
      'free-checklist': {
        id: '[YOUR_FORM_ID]', // Replace with actual ConvertKit form ID
        endpoint: 'https://api.convertkit.com/v3/forms/[YOUR_FORM_ID]/subscribe'
      },
      'chapter1-sample': {
        id: '[YOUR_FORM_ID_2]', // Replace with actual ConvertKit form ID
        endpoint: 'https://api.convertkit.com/v3/forms/[YOUR_FORM_ID_2]/subscribe'
      }
    }
  },
  
  // UTM Tracking
  utm: {
    source: 'utm_source',
    medium: 'utm_medium',
    campaign: 'utm_campaign',
    content: 'utm_content',
    term: 'utm_term'
  },
  
  // Analytics
  analytics: {
    ga4MeasurementId: 'G-GW45MT4LE0', // Using your existing GA4 ID
    enabled: true // Set to true when ready to track
  }
};

// ===== UTILITY FUNCTIONS =====
const utils = {
  // Format currency
  formatCurrency: (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  },
  
  // Generate UTM parameters
  generateUTM: (params) => {
    const url = new URL(window.location.href);
    Object.keys(params).forEach(key => {
      if (params[key]) {
        url.searchParams.set(key, params[key]);
      }
    });
    return url.toString();
  },
  
  // Email validation
  isValidEmail: (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  },
  
  // Show notification
  showNotification: (message, type = 'success') => {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
      notification.classList.add('show');
    }, 100);
    
    setTimeout(() => {
      notification.classList.remove('show');
      setTimeout(() => {
        document.body.removeChild(notification);
      }, 300);
    }, 3000);
  },
  
  // Smooth scroll to element
  scrollTo: (element, offset = 0) => {
    const targetPosition = element.offsetTop - offset;
    window.scrollTo({
      top: targetPosition,
      behavior: 'smooth'
    });
  }
};

// ===== CONVERTKIT INTEGRATION =====
class ConvertKitManager {
  constructor() {
    this.forms = config.convertkit.forms;
    this.init();
  }
  
  init() {
    this.bindFormEvents();
    this.setupIntersectionTracking();
  }
  
  bindFormEvents() {
    document.querySelectorAll('.convertkit-form').forEach(form => {
      form.addEventListener('submit', (e) => this.handleSubmit(e));
    });
  }
  
  async handleSubmit(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    const email = formData.get('email');
    const formType = form.dataset.ckForm;
    
    // Validate email
    if (!utils.isValidEmail(email)) {
      utils.showNotification('Please enter a valid email address', 'error');
      return;
    }
    
    // Show loading state
    this.setFormLoading(form, true);
    
    try {
      // Submit to ConvertKit
      await this.submitToConvertKit(formType, email);
      
      // Track conversion
      this.trackConversion(formType, email);
      
      // Show success
      this.showSuccess(form);
      
    } catch (error) {
      console.error('Form submission error:', error);
      utils.showNotification('Something went wrong. Please try again.', 'error');
    } finally {
      this.setFormLoading(form, false);
    }
  }
  
  async submitToConvertKit(formType, email) {
    const formConfig = this.forms[formType];
    
    if (!formConfig) {
      throw new Error(`Form configuration not found for: ${formType}`);
    }
    
    const payload = {
      email: email,
      fields: {
        source: 'ebook_landing_page',
        page: window.location.pathname,
        timestamp: new Date().toISOString(),
        user_agent: navigator.userAgent
      }
    };
    
    // Note: Replace the endpoint and add your API key
    const response = await fetch(formConfig.endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload)
    });
    
    if (!response.ok) {
      throw new Error('Failed to subscribe');
    }
    
    return response.json();
  }
  
  setFormLoading(form, isLoading) {
    const submitBtn = form.querySelector('button[type="submit"]');
    
    if (isLoading) {
      submitBtn.disabled = true;
      submitBtn.dataset.originalText = submitBtn.textContent;
      submitBtn.textContent = 'Submitting...';
    } else {
      submitBtn.disabled = false;
      if (submitBtn.dataset.originalText) {
        submitBtn.textContent = submitBtn.dataset.originalText;
      }
    }
  }
  
  showSuccess(form) {
    const submitBtn = form.querySelector('button[type="submit"]');
    const email = form.querySelector('input[type="email"]').value;
    
    submitBtn.disabled = true;
    submitBtn.textContent = '✓ Success! Check your email';
    
    // Track success event
    this.trackSuccess(form.dataset.ckForm);
    
    // Reset form after delay
    setTimeout(() => {
      form.reset();
      submitBtn.disabled = false;
      submitBtn.textContent = submitBtn.dataset.originalText || 'Submit';
    }, 5000);
  }
  
  trackConversion(formType, email) {
    // Google Analytics 4 event
    if (config.analytics.ga4MeasurementId) {
      gtag('event', 'generate_lead', {
        event_category: 'engagement',
        event_label: formType,
        value: 1,
        custom_parameter_email_hash: this.hashEmail(email)
      });
    }
    
    // Facebook Pixel
    if (typeof fbq !== 'undefined') {
      fbq('track', 'Lead', {
        content_name: 'Ebook Landing Page',
        content_category: 'Lead Magnet',
        value: 0.00,
        currency: 'USD'
      });
    }
  }
  
  trackSuccess(formType) {
    if (config.analytics.ga4MeasurementId) {
      gtag('event', 'form_submit_complete', {
        event_category: 'engagement',
        event_label: formType,
        value: 1
      });
    }
  }
  
  setupIntersectionTracking() {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const element = entry.target;
          const formType = element.dataset.ckForm;
          
          // Track form view
          if (config.analytics.ga4MeasurementId) {
            gtag('event', 'form_view', {
              event_category: 'engagement',
              event_label: formType,
              value: 1
            });
          }
          
          observer.unobserve(element);
        }
      });
    }, {
      threshold: 0.5
    });
    
    document.querySelectorAll('.convertkit-form').forEach(form => {
      observer.observe(form);
    });
  }
  
  hashEmail(email) {
    // Simple hash for privacy (replace with proper hashing if needed)
    let hash = 0;
    for (let i = 0; i < email.length; i++) {
      const char = email.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // Convert to 32bit integer
    }
    return Math.abs(hash).toString(36);
  }
}

// ===== CTA TRACKING =====
class CTATracker {
  constructor() {
    this.init();
  }
  
  init() {
    this.bindCTAClicks();
    this.setupScrollTracking();
    this.addStickyMobileCTA();
  }
  
  bindCTAClicks() {
    document.querySelectorAll('a[href*="books2read.com"]').forEach(cta => {
      cta.addEventListener('click', (e) => this.trackCTAClick(e));
    });
  }
  
  trackCTAClick(event) {
    const cta = event.target;
    const buttonText = cta.textContent.trim();
    const ctaLocation = this.getCTALocation(cta);
    
    // Add UTM parameters if not present
    if (!cta.href.includes('utm_')) {
      cta.href = utils.generateUTM({
        utm_source: 'ebook_landing',
        utm_medium: 'cta',
        utm_campaign: 'cat_scratching_solution',
        utm_content: buttonText.toLowerCase().replace(/\s+/g, '_'),
        utm_term: ctaLocation
      });
    }
    
    // Track analytics
    this.trackPurchaseIntent(buttonText, ctaLocation);
  }
  
  trackPurchaseIntent(buttonText, location) {
    if (config.analytics.ga4MeasurementId) {
      gtag('event', 'begin_checkout', {
        event_category: 'ecommerce',
        event_label: 'cat_scratching_ebook',
        value: 19.99, // Replace with actual price
        currency: 'USD',
        items: [{
          item_id: 'cat-scratching-solution',
          item_name: 'The Cat Scratching Solution',
          category: 'ebook',
          quantity: 1,
          price: 19.99
        }]
      });
    }
  }
  
  getCTALocation(element) {
    if (element.closest('.hero-section')) return 'hero';
    if (element.closest('.final-cta')) return 'footer';
    if (element.closest('.benefits-section')) return 'benefits';
    if (element.closest('.testimonials-section')) return 'testimonials';
    return 'unknown';
  }
  
  setupScrollTracking() {
    const sections = [
      { name: 'hero', element: '.hero-section' },
      { name: 'benefits', element: '.benefits-section' },
      { name: 'learn', element: '.learn-section' },
      { name: 'target', element: '.target-section' },
      { name: 'testimonials', element: '.testimonials-section' },
      { name: 'preview', element: '.preview-section' },
      { name: 'faq', element: '.faq-section' }
    ];
    
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const section = sections.find(s => s.element === '.' + entry.target.className.split(' ')[0]);
          if (section && config.analytics.ga4MeasurementId) {
            gtag('event', 'scroll', {
              event_category: 'engagement',
              event_label: section.name,
              value: 1
            });
          }
          observer.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.5
    });
    
    sections.forEach(section => {
      const element = document.querySelector(section.element);
      if (element) {
        observer.observe(element);
      }
    });
  }
  
  addStickyMobileCTA() {
    // Only add on mobile devices
    if (window.innerWidth > 768) return;
    
    // Check if user hasn't converted yet
    if (localStorage.getItem('cta_converted')) return;
    
    const stickyCTA = document.createElement('div');
    stickyCTA.className = 'mobile-sticky-cta';
    stickyCTA.innerHTML = `
      <a href="https://books2read.com/u/47jzOq?utm_source=ebook_landing&utm_medium=sticky_cta&utm_campaign=cat_scratching_solution" 
         class="btn btn-primary btn-lg">
        Get The eBook Now
      </a>
    `;
    
    document.body.appendChild(stickyCTA);
    
    // Show after scrolling past hero
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
      const heroObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (!entry.isIntersecting) {
            stickyCTA.style.display = 'block';
            heroObserver.unobserve(entry.target);
          }
        });
      });
      heroObserver.observe(heroSection);
    }
  }
}

// ===== INTERACTIVITY MANAGERS =====
class FAQManager {
  constructor() {
    this.init();
  }
  
  init() {
    document.querySelectorAll('.faq-question').forEach(question => {
      question.addEventListener('click', () => this.toggleFAQ(question));
    });
  }
  
  toggleFAQ(question) {
    const answer = question.nextElementSibling;
    const icon = question.querySelector('.faq-icon');
    const isExpanded = question.getAttribute('aria-expanded') === 'true';
    
    // Toggle state
    question.setAttribute('aria-expanded', !isExpanded);
    answer.classList.toggle('hidden');
    icon.textContent = isExpanded ? '+' : '−';
    
    // Track FAQ interaction
    if (config.analytics.ga4MeasurementId) {
      gtag('event', 'faq_view', {
        event_category: 'engagement',
        event_label: question.textContent.trim(),
        value: 1
      });
    }
  }
}

class TableOfContentsManager {
  constructor() {
    this.init();
  }
  
  init() {
    const tocButton = document.querySelector('.collapsible-toc');
    if (tocButton) {
      tocButton.addEventListener('click', () => this.toggleTOC());
    }
  }
  
  toggleTOC() {
    const content = document.querySelector('.toc-content');
    const icon = document.querySelector('.toggle-icon');
    const isHidden = content.classList.contains('hidden');
    
    content.classList.toggle('hidden');
    icon.textContent = isHidden ? '▲' : '▼';
    
    // Track TOC interaction
    if (config.analytics.ga4MeasurementId) {
      gtag('event', 'table_of_contents_view', {
        event_category: 'engagement',
        value: 1
      });
    }
  }
}

// ===== PERFORMANCE OPTIMIZATION =====
class PerformanceOptimizer {
  constructor() {
    this.init();
  }
  
  init() {
    this.lazyLoadImages();
    this.preloadCriticalResources();
    this.setupServiceWorker();
  }
  
  lazyLoadImages() {
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.removeAttribute('data-src');
          imageObserver.unobserve(img);
        }
      });
    });
    
    images.forEach(img => imageObserver.observe(img));
  }
  
  preloadCriticalResources() {
    // Preload critical images
    const criticalImages = [
      '/images/cover-cat-scratches-furniture.jpg',
      '/images/author-jane-doe.jpg'
    ];
    
    criticalImages.forEach(src => {
      const link = document.createElement('link');
      link.rel = 'preload';
      link.as = 'image';
      link.href = src;
      document.head.appendChild(link);
    });
  }
  
  setupServiceWorker() {
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('/sw.js').catch(console.error);
    }
  }
}

// ===== ACCESSIBILITY ENHANCER =====
class AccessibilityEnhancer {
  constructor() {
    this.init();
  }
  
  init() {
    this.addSkipLinks();
    this.enhanceKeyboardNavigation();
    this.addAriaLabels();
    this.setupFocusManagement();
  }
  
  addSkipLinks() {
    const skipLink = document.createElement('a');
    skipLink.href = '#main-content';
    skipLink.textContent = 'Skip to main content';
    skipLink.className = 'skip-link sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 bg-blue-600 text-white px-4 py-2 rounded';
    
    document.body.insertBefore(skipLink, document.body.firstChild);
  }
  
  enhanceKeyboardNavigation() {
    // Add tabindex to interactive elements
    document.querySelectorAll('.faq-question, .collapsible-toc').forEach(element => {
      element.setAttribute('tabindex', '0');
      
      element.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          element.click();
        }
      });
    });
  }
  
  addAriaLabels() {
    // Add ARIA labels to CTAs
    document.querySelectorAll('.btn-primary').forEach(btn => {
      if (!btn.getAttribute('aria-label')) {
        btn.setAttribute('aria-label', `Get The Cat Scratching Solution ebook`);
      }
    });
    
    // Add ARIA labels to forms
    document.querySelectorAll('.convertkit-form').forEach(form => {
      form.setAttribute('aria-label', 'Email signup form');
    });
  }
  
  setupFocusManagement() {
    // Track focus for analytics
    document.addEventListener('focusin', (e) => {
      if (config.analytics.ga4MeasurementId && e.target.classList.contains('form-field')) {
        gtag('event', 'form_field_focus', {
          event_category: 'engagement',
          event_label: e.target.name,
          value: 1
        });
      }
    });
  }
}

// ===== MAIN APPLICATION =====
class EbookLandingPage {
  constructor() {
    this.config = config;
    this.convertkit = null;
    this.ctaTracker = null;
    this.faqManager = null;
    this.tocManager = null;
    this.performanceOptimizer = null;
    this.accessibilityEnhancer = null;
    
    this.init();
  }
  
  init() {
    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.initializeComponents());
    } else {
      this.initializeComponents();
    }
  }
  
  initializeComponents() {
    try {
      this.convertkit = new ConvertKitManager();
      this.ctaTracker = new CTATracker();
      this.faqManager = new FAQManager();
      this.tocManager = new TableOfContentsManager();
      this.performanceOptimizer = new PerformanceOptimizer();
      this.accessibilityEnhancer = new AccessibilityEnhancer();
      
      // Initialize analytics
      this.initializeAnalytics();
      
      // Global error handling
      this.setupErrorHandling();
      
      console.log('Ebook Landing Page initialized successfully');
      
    } catch (error) {
      console.error('Error initializing landing page:', error);
    }
  }
  
  initializeAnalytics() {
    if (this.config.analytics.ga4MeasurementId && !this.config.analytics.enabled) {
      // Load Google Analytics 4
      const script = document.createElement('script');
      script.async = true;
      script.src = `https://www.googletagmanager.com/gtag/js?id=${this.config.analytics.ga4MeasurementId}`;
      document.head.appendChild(script);
      
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      window.gtag = gtag;
      gtag('js', new Date());
      gtag('config', this.config.analytics.ga4MeasurementId);
      
      this.config.analytics.enabled = true;
    }
  }
  
  setupErrorHandling() {
    window.addEventListener('error', (e) => {
      console.error('JavaScript error:', e.error);
      
      // Track errors in analytics
      if (this.config.analytics.enabled) {
        gtag('event', 'exception', {
          description: e.error.toString(),
          fatal: false
        });
      }
    });
    
    window.addEventListener('unhandledrejection', (e) => {
      console.error('Unhandled promise rejection:', e.reason);
    });
  }
}

// ===== CSS FOR NOTIFICATIONS =====
const style = document.createElement('style');
style.textContent = `
  .notification {
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 16px 24px;
    border-radius: 8px;
    color: white;
    font-weight: 600;
    z-index: 9999;
    transform: translateX(100%);
    transition: transform 0.3s ease-in-out;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }
  
  .notification.show {
    transform: translateX(0);
  }
  
  .notification-success {
    background-color: #059669;
  }
  
  .notification-error {
    background-color: #dc2626;
  }
  
  .skip-link {
    position: absolute;
    left: -10000px;
    width: 1px;
    height: 1px;
    overflow: hidden;
  }
  
  .skip-link:focus {
    position: static;
    width: auto;
    height: auto;
  }
  
  @media (prefers-reduced-motion: reduce) {
    .notification {
      transition: none;
    }
  }
`;
document.head.appendChild(style);

// ===== INITIALIZE APPLICATION =====
const ebookLandingPage = new EbookLandingPage();

// Export for testing purposes
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    EbookLandingPage,
    ConvertKitManager,
    CTATracker,
    utils,
    config
  };
}