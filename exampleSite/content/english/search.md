---
title: "Search"
description: "Search ForPetsWithLove.com for pet care articles, guides, and tips."
date: 2026-01-01
layout: search
---

# Search Our Pet Care Library

Find articles on dog training, cat behavior, pet health, and more.

<form id="search-form" action="/search/" method="get" style="max-width: 600px; margin: 2rem auto;">
  <div style="display: flex; gap: 0.5rem;">
    <input 
      type="search" 
      name="q" 
      id="search-input"
      placeholder="Search for pet care tips..."
      required
      style="
        flex: 1;
        padding: 0.875rem 1.25rem;
        font-size: 1rem;
        border: 2px solid var(--color-earth-200);
        border-radius: 0.5rem;
        outline: none;
        transition: border-color 150ms;
      "
      onfocus="this.style.borderColor='var(--color-teal-500)'"
      onblur="this.style.borderColor='var(--color-earth-200)'"
    >
    <button 
      type="submit" 
      style="
        padding: 0.875rem 1.5rem;
        font-size: 1rem;
        font-weight: 600;
        color: white;
        background: var(--color-teal-600);
        border: none;
        border-radius: 0.5rem;
        cursor: pointer;
        transition: background 150ms;
      "
      onmouseover="this.style.background='var(--color-teal-700)'"
      onmouseout="this.style.background='var(--color-teal-600)'"
    >
      Search
    </button>
  </div>
</form>

<div id="search-results" style="max-width: 800px; margin: 2rem auto;">
  <!-- Results will appear here -->
</div>

<div id="search-stats" style="text-align: center; color: var(--text-secondary); margin-top: 1rem;">
  <noscript>Please enable JavaScript to use search.</noscript>
</div>

<script>
// Search functionality
document.addEventListener('DOMContentLoaded', function() {
  const searchForm = document.getElementById('search-form');
  const searchInput = document.getElementById('search-input');
  const resultsDiv = document.getElementById('search-results');
  
  const urlParams = new URLSearchParams(window.location.search);
  const query = urlParams.get('q');
  
  if (query) {
    searchInput.value = query;
    performSearch(query);
  }
  
  searchForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const q = searchInput.value.trim();
    if (q) {
      window.location.href = '/search/?q=' + encodeURIComponent(q);
    }
  });
  
  async function performSearch(query) {
    try {
      const response = await fetch('/index.json');
      const data = await response.json();
      
      const results = data.data.filter(item => {
        const searchText = (item.title + ' ' + item.description + ' ' + item.content).toLowerCase();
        return searchText.includes(query.toLowerCase());
      });
      
      displayResults(results, query);
    } catch (error) {
      resultsDiv.innerHTML = '<p style="color: red;">Search temporarily unavailable. Please try again.</p>';
    }
  }
  
  function displayResults(results, query) {
    if (results.length === 0) {
      resultsDiv.innerHTML = '<p style="text-align: center; padding: 2rem;">No results found for "' + query + '". Try different keywords.</p>';
      return;
    }
    
    let html = '<div style="display: flex; flex-direction: column; gap: 1.5rem;">';
    
    results.forEach(item => {
      // Highlight matching text
      const title = item.title.replace(new RegExp('(' + query + ')', 'gi'), '<mark>$1</mark>');
      const desc = item.description.replace(new RegExp('(' + query + ')', 'gi'), '<mark>$1</mark>');
      
      html += `
        <article style="padding: 1.5rem; background: var(--color-earth-100); border-radius: 0.5rem; border-left: 4px solid var(--color-teal-500);">
          <h3 style="margin: 0 0 0.5rem 0;"><a href="${item.url}" style="color: var(--color-teal-700); text-decoration: none;">${title}</a></h3>
          <p style="margin: 0; color: var(--text-secondary); font-size: 0.9375rem;">${desc}</p>
          ${item.categories && item.categories.length ? '<p style="margin: 0.5rem 0 0 0; font-size: 0.8125rem; color: var(--color-teal-600);">' + item.categories.join(', ') + '</p>' : ''}
        </article>
      `;
    });
    
    html += '</div>';
    resultsDiv.innerHTML = html;
    
    document.getElementById('search-stats').innerHTML = 'Found ' + results.length + ' result' + (results.length !== 1 ? 's' : '') + ' for "' + query + '"';
  }
});
</script>

<style>
mark {
  background: var(--color-earth-300);
  padding: 0 0.25rem;
  border-radius: 2px;
}
</style>