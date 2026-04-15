---
title: "Archive"
description: "Browse all articles from ForPetsWithLove.com - Complete archive of pet care tips, guides, and reviews"
date: 2026-04-15
author: "Kweebs"
---

{{ define "main" }}
<section class="section">
  <div class="container">
    <header style="text-align: center; margin-bottom: 3rem;">
      <h1>Complete Archive</h1>
      <p style="color: var(--text-secondary); max-width: 600px; margin: 1rem auto 0; font-size: 1.125rem;">
        Browse all {{ len (where site.RegularPages "Section" "blog") }} articles from our pet care library
      </p>
    </header>

    <!-- Category Filter -->
    <div style="margin-bottom: 2rem; display: flex; gap: 0.5rem; flex-wrap: wrap; justify-content: center;">
      <a href="{{ .Permalink }}" class="btn btn-primary" style="font-size: 0.875rem;">All Posts</a>
      {{ range $name, $taxonomy := site.Taxonomies.categories }}
      <a href="{{ "/categories/" | relURL }}{{ $name | urlize }}" class="btn btn-secondary" style="font-size: 0.875rem;">
        {{ $name | title }} ({{ len $taxonomy }})
      </a>
      {{ end }}
    </div>

    <!-- Posts by Year -->
    {{ $posts := where site.RegularPages "Section" "blog" }}
    {{ range $posts.GroupByDate "2006" }}
    <section style="margin-bottom: 3rem;">
      <h2 style="font-size: 1.5rem; margin-bottom: 1.5rem; border-bottom: 2px solid var(--color-teal-600); padding-bottom: 0.5rem;">
        {{ .Key }} ({{ len .Pages }} articles)
      </h2>
      <div class="grid grid-3">
        {{ range .Pages }}
        <article class="card" style="margin-bottom: 1rem;">
          {{ with .Params.image }}
          <img src="{{ . | absURL }}" alt="{{ $.Title }}" class="card-image" loading="lazy" decoding="async" style="max-height: 200px; object-fit: cover;">
          {{ end }}
          <div class="card-content">
            <h3 class="card-title" style="font-size: 1rem;">
              <a href="{{ .Permalink }}">{{ .Title }}</a>
            </h3>
            <p class="card-meta" style="font-size: 0.875rem;">
              <time datetime="{{ .Date.Format "2006-01-02" }}">{{ .Date.Format "January 2" }}</time>
              {{ with .Params.categories }} • {{ delimit . ", " }}{{ end }}
            </p>
          </div>
        </article>
        {{ end }}
      </div>
    </section>
    {{ end }}
  </div>
</section>
{{ end }}
