---
title: "Cat Care"
description: "All articles about Cat Care - Expert tips, guides, and reviews"
date: 2026-04-15
author: "Kweebs"
---

{{ define "main" }}
<section class="section">
  <div class="container">
    <header style="text-align: center; margin-bottom: 3rem;">
      <h1>Cat Care</h1>
      <p style="color: var(--text-secondary); max-width: 600px; margin: 1rem auto 0; font-size: 1.125rem;">
        Expert tips, guides, and reviews for Cat Care
      </p>
    </header>

    <div class="grid grid-3">
      {{ range where site.RegularPages "Section" "blog" }}
      {{ if in .Params.categories "cat-care" }}
      <article class="card">
        {{ with .Params.image }}
        <img src="{{ . | absURL }}" alt="{{ $.Title }}" class="card-image" loading="lazy" decoding="async">
        {{ end }}
        <div class="card-content">
          <h2 class="card-title" style="font-size: 1.25rem;">
            <a href="{{ .Permalink }}">{{ .Title }}</a>
          </h2>
          <p class="card-meta">
            <time datetime="{{ .Date.Format "2006-01-02" }}">{{ .Date.Format "Jan 2, 2006" }}</time>
          </p>
          {{ with .Description }}
          <p class="card-excerpt">{{ . }}</p>
          {{ end }}
          <a href="{{ .Permalink }}" class="btn btn-secondary" style="margin-top: 1rem; font-size: 0.875rem;">Read More</a>
        </div>
      </article>
      {{ end }}
      {{ end }}
    </div>
  </div>
</section>
{{ end }}
