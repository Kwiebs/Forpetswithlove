# ForPetsWithLove.com - Night Tasks Strategy

## Audit Findings

### ✅ Issues Found
1. **Menu links broken** - Header links to `/dogs/`, `/cats/`, `/birds/` etc. but these sections don't exist
2. **All content in `/blog/` section** - Need category-based filtering
3. **Newsletter forms** - Need Kit.com (ConvertKit) integration
4. **Missing working pages** - Need to verify ebook page, toxic foods page, quiz page

### Content Structure
```
/blog/ (30+ posts with categories)
  - Cat Care (30 posts)
  - Dog Care (22 posts)
  - Pet Care (17 posts)
  - Dog Health (13 posts)
  - Reptile Care (11 posts)
  - Small Pet Care (7 posts)
  - Fish Care (5 posts)
  - Bird Care (4 posts)
```

---

## Tasks for Tonight

### 1. Fix Menu Links → Category Pages
**Problem:** Menu links to `/dogs/`, `/cats/` etc. don't exist

**Solution:** Update header to link to category-filtered blog pages:
- `/blog/` with category filter (Hugo supports `/blog/categories/cat-care/`)
- Create taxonomy list templates for categories

**Files to update:**
- `layouts/partials/components/header.html`
- `layouts/_default/taxonomy.html` (if needed)

### 2. Create/Verify Core Pages
- [ ] Homepage - `/`
- [ ] Blog index - `/blog/`
- [ ] Ebook page - `/cat-scratching-solution-ebook/`
- [ ] Quiz page - `/quiz/`
- [ ] Toxic Foods - `/toxic-foods/`
- [ ] About - `/about/`
- [ ] Contact - `/contact/`

### 3. Newsletter Integration (Kit.com)
**When credentials provided:**
- Replace placeholder form action with Kit.com form embed
- Verify GDPR compliance checkbox
- Add success/error states

**Kit.com forms need:**
- Form ID
- Custom redirect URL after signup

### 4. SEO Programmatic Posts
**Tomorrow's task:**
- Create 50+ SEO-optimized blog posts
- Target long-tail keywords
- Each with proper meta, categories, tags

### 5. Technical SEO Audit Checklist
- [ ] Canonical URLs - all pages
- [ ] XML Sitemap - auto-generated
- [ ] Robots.txt - blocks /search/, /404
- [ ] OpenGraph + Twitter Cards - all pages
- [ ] JSON-LD Schema - Article, Organization, Breadcrumb
- [ ] Image alt text - all images
- [ ] Internal linking structure
- [ ] Page speed optimization
- [ ] Mobile responsiveness

---

## Implementation Plan

### Phase 1: Fix Broken Links (Now)
1. Update header menu to link to categories via URL params or taxonomy
2. Create category pages that filter blog posts

### Phase 2: Verify All Pages Work (Now)
1. Check all static pages render
2. Check external links
3. Check forms

### Phase 3: Newsletter Integration (Morning)
1. Add Kit.com credentials
2. Replace form placeholders
3. Test signup flow

### Phase 4: SEO Content Creation (Ongoing)
1. Create programmatic post templates
2. Generate posts targeting keywords
3. Add to sitemap

---

## Files to Modify
1. `layouts/partials/components/header.html` - Fix menu links
2. `layouts/partials/components/footer.html` - Fix newsletter form
3. `exampleSite/config.toml` - Add canonical, sitemap config
4. `layouts/_default/single.html` - Ensure proper meta
5. `layouts/index.html` - Verify all CTAs work
