---
layout: default
title: Search
permalink: /search/
---

# Search

Use the search box above to find tutorials, research themes, and other content on this site.

<div id="search-info" style="margin-top: 20px;">
  <p><em>Start typing to search through all content...</em></p>
  <p><small>Search includes:</small></p>
  <ul>
    <li>Tutorials and blog posts</li>
    <li>Research themes and papers</li>
    <li>Bio and personal information</li>
    <li>Tools and resources</li>
  </ul>
</div>

<script>
  // Focus search input when on search page
  document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
      searchInput.focus();
    }
  });
</script>
