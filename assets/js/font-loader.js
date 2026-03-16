// Adobe Fonts Loader Optimization
(function() {
  'use strict';
  
  // Font loading configuration for Adobe Fonts Kit (app.kit.com)
  const fontConfig = {
    timeout: 3000,
    classes: true,
    events: true,
    fontinactive: function(family, fvd) {
      console.warn('Font failed to load:', family);
      document.body.classList.add('fonts-fallback');
    },
    fontactive: function(family, fvd) {
      document.body.classList.add('fonts-loaded');
      console.log('Font loaded successfully:', family);
    }
  };
  
  // Initialize font loading
  function initFontLoading() {
    if (typeof Typekit !== 'undefined') {
      try {
        Typekit.load(fontConfig);
      } catch(e) {
        console.error('Typekit loading error:', e);
      }
    } else {
      // Fallback if Typekit is not available
      document.body.classList.add('fonts-fallback');
    }
  }
  
  // DOM ready check
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initFontLoading);
  } else {
    initFontLoading();
  }
  
  // Performance monitoring
  if ('performance' in window) {
    window.addEventListener('load', function() {
      setTimeout(function() {
        const perfData = performance.getEntriesByType('navigation')[0];
        const fontLoadTime = perfData.loadEventEnd - perfData.loadEventStart;
        
        if (fontLoadTime > 1000) {
          console.warn('Slow font loading detected:', fontLoadTime + 'ms');
        }
      }, 0);
    });
  }
})();