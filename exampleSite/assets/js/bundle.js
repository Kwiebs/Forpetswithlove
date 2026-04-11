/**
 * ForPetsWithLove - Modern Theme JS Bundle
 * Handles: Dark mode, search, reading progress, back-to-top, mobile menu
 */

(function() {
  'use strict';

  /* === Theme Toggle === */
  const themeToggle = document.getElementById('themeToggle');
  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const html = document.documentElement;
      const current = html.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-theme', next);
      localStorage.setItem('theme', next);
      
      // Update icon
      const icon = themeToggle.querySelector('svg');
      if (next === 'dark') {
        icon.innerHTML = '<circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>';
      } else {
        icon.innerHTML = '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>';
      }
    });
  }

  /* === Search Modal === */
  const searchToggle = document.getElementById('searchToggle');
  const searchModal = document.getElementById('searchModal');
  const searchInput = document.getElementById('searchInput');
  
  if (searchToggle && searchModal) {
    searchToggle.addEventListener('click', () => {
      searchModal.classList.add('active');
      setTimeout(() => searchInput?.focus(), 100);
    });
    
    searchModal.addEventListener('click', (e) => {
      if (e.target === searchModal) {
        searchModal.classList.remove('active');
      }
    });
    
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && searchModal.classList.contains('active')) {
        searchModal.classList.remove('active');
      }
      // Cmd/Ctrl + K to open search
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        searchModal.classList.add('active');
        setTimeout(() => searchInput?.focus(), 100);
      }
    });
  }
  
  /* === FlexSearch / Fuse.js Integration === */
  let searchIndex = null;
  let searchData = [];
  
  async function initSearch() {
    const searchContainer = document.getElementById('searchResults');
    if (!searchContainer) return;
    
    try {
      // Load Fuse.js for client-side search
      const Fuse = await import('https://cdn.jsdelivr.net/npm/fuse.js@7.0.0/dist/fuse.mjs');
      
      // Fetch search index (generated at build time)
      const response = await fetch('/search/index.json');
      if (response.ok) {
        searchData = await response.json();
        
        searchIndex = new Fuse.default(searchData, {
          keys: [
            { name: 'title', weight: 2 },
            { name: 'description', weight: 1.5 },
            { name: 'tags', weight: 1 },
            { name: 'content', weight: 0.5 }
          ],
          threshold: 0.3,
          includeScore: true,
          minMatchCharLength: 2
        });
      }
    } catch (err) {
      console.warn('Search initialization failed:', err);
    }
  }
  
  if (searchInput) {
    let debounceTimer;
    searchInput.addEventListener('input', (e) => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => performSearch(e.target.value), 200);
    });
  }
  
  function performSearch(query) {
    const searchContainer = document.getElementById('searchResults');
    if (!searchContainer || !query.trim()) {
      searchContainer.innerHTML = '<p class="search-no-results">Type to search...</p>';
      return;
    }
    
    if (!searchIndex) {
      searchContainer.innerHTML = '<p class="search-no-results">Search not available</p>';
      return;
    }
    
    const results = searchIndex.search(query).slice(0, 10);
    
    if (results.length === 0) {
      searchContainer.innerHTML = `<p class="search-no-results">No results for "${query}"</p>`;
      return;
    }
    
    searchContainer.innerHTML = results.map(r => `
      <a href="${r.item.url}" class="search-result">
        <div class="search-result-title">${r.item.title}</div>
        <div class="search-result-excerpt">${r.item.description || ''}</div>
      </a>
    `).join('');
  }
  
  initSearch();

  /* === Reading Progress Bar === */
  const progressBar = document.getElementById('readingProgress');
  if (progressBar) {
    window.addEventListener('scroll', () => {
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      const progress = (window.scrollY / docHeight) * 100;
      progressBar.style.width = `${Math.min(progress, 100)}%`;
    }, { passive: true });
  }

  /* === Back to Top Button === */
  const backToTop = document.getElementById('backToTop');
  if (backToTop) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 400) {
        backToTop.classList.add('visible');
      } else {
        backToTop.classList.remove('visible');
      }
    }, { passive: true });
    
    backToTop.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* === Mobile Menu === */
  const menuToggle = document.getElementById('menuToggle');
  const mobileNav = document.getElementById('mobileNav');
  
  if (menuToggle && mobileNav) {
    menuToggle.addEventListener('click', () => {
      mobileNav.classList.toggle('active');
      document.body.style.overflow = mobileNav.classList.contains('active') ? 'hidden' : '';
    });
    
    const closeBtn = mobileNav.querySelector('.mobile-nav-close');
    if (closeBtn) {
      closeBtn.addEventListener('click', () => {
        mobileNav.classList.remove('active');
        document.body.style.overflow = '';
      });
    }
  }

  /* === Related Posts Lazy Load === */
  const relatedPosts = document.querySelector('.related-posts');
  if (relatedPosts) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('animate-in');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });
    
    relatedPosts.querySelectorAll('.card').forEach(card => {
      observer.observe(card);
    });
  }

  /* === Lazy Loading Images (Native + Fallback) === */
  document.querySelectorAll('img[loading="lazy"]').forEach(img => {
    img.addEventListener('error', () => {
      img.style.backgroundColor = 'var(--color-earth-200)';
      img.removeAttribute('src');
    });
  });

})();