// Standalone search.js file for Hugo search functionality
document.addEventListener('DOMContentLoaded', function() {
  // Get the query parameter
  var urlParams = new URLSearchParams(window.location.search);
  var query = urlParams.get('q');
  
  if (query) {
    // Initialize search
    initSearch(query);
  }
});

function initSearch(query) {
  // Get the index URL from the data attribute
  var searchResultsDiv = document.getElementById('search-results');
  var indexURL = searchResultsDiv.dataset.indexUrl;
  
  if (!indexURL) {
    console.error("Search index URL not found in data attribute.");
    searchResultsDiv.innerHTML = '<p>Error: Search index URL configuration missing.</p>';
    return;
  }

  // Load the search index using the absolute URL
  fetchJSONFile(indexURL, function(data) {
    console.log("Search Index Loaded:", data); // Log fetched data
    // Configure Fuse.js
    var options = {
      shouldSort: true,
      location: 0,
      distance: 100,
      threshold: 0.5, // Made threshold less strict
      minMatchCharLength: 2,
      keys: [
        'title',
        'contents',
        'tags',
        'categories'
      ]
    };
    
    // Initialize Fuse with our data
    var fuse = new Fuse(data, options);
    
    // Perform the search
    var results = fuse.search(query);
    console.log("Fuse Results Count:", results.length); // Log results count
    
    // Display results
    displayResults(results, query);
  });
}

function fetchJSONFile(path, callback) {
  var httpRequest = new XMLHttpRequest();
  httpRequest.onreadystatechange = function() {
    if (httpRequest.readyState === 4) {
      if (httpRequest.status === 200) {
        var data = JSON.parse(httpRequest.responseText);
        if (callback) callback(data);
      } else {
        console.error('Error loading search index');
        document.getElementById('search-results').innerHTML = '<p>Error loading search index. Please try again later.</p>';
      }
    }
  };
  httpRequest.open('GET', path);
  httpRequest.send();
}

function displayResults(results, query) {
  var searchResults = document.getElementById('search-results');
  
  // Clear previous results
  searchResults.innerHTML = '<h3>Search Results for "' + query + '"</h3>';
  
  if (results.length === 0) {
    // No results
    searchResults.innerHTML += '<p>No results found for "' + query + '"</p>';
  } else {
    // Create a list for results
    var resultList = document.createElement('ul');
    resultList.className = 'search-results-list';
    
    // Add each result to the list
    results.forEach(function(result, i) {
      var item = document.createElement('li');
      
      var link = document.createElement('a');
      link.href = result.permalink;
      link.textContent = result.title;
      
      var snippet = document.createElement('p');
      snippet.textContent = result.contents ? result.contents.substring(0, 200) + '...' : '';
      
      item.appendChild(link);
      item.appendChild(snippet);
      
      if (result.tags) {
        var tags = document.createElement('p');
        tags.textContent = 'Tags: ' + result.tags;
        item.appendChild(tags);
      }
      
      resultList.appendChild(item);
    });
    
    searchResults.appendChild(resultList);
  }
}
