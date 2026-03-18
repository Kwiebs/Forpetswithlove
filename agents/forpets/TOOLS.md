# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics.

## What Goes Here

Things like:

- Content templates and formats
- Affiliate link patterns
- SEO keyword preferences
- Hugo frontmatter templates
- Content calendar schedules

## Affiliate Links

### Amazon Associates
- **US (.com):** forpetswith07-20
- **Spain (.es):** forpetswith0c-21
- **Italy (.it):** forpetswith08-21
- **Germany (.de):** forpetswith00-21
- **UK (.co.uk):** forpetswith09-21
- **France (.fr):** forpetswith04-21

### eBook Links
- **Universal:** https://books2read.com/u/47jzOq
- **Amazon:** https://www.amazon.com/dp/B0FDG9WPB2
- **Gumroad:** https://forpetswithlove.gumroad.com/l/vqioo

## Content Templates

### Blog Post Structure
```markdown
---
title: "{{title}}"
date: {{date}}
draft: false
categories: ["{{petType}}"]
tags: ["{{tag1}}", "{{tag2}}"]
---

## Introduction

## Main Content Sections

## Product Recommendations

## FAQ

## Conclusion
```

### Product Review Structure
```markdown
---
title: "{{productName}} Review: {{subtitle}}"
date: {{date}}
draft: false
categories: ["reviews", "{{petType}}"]
tags: ["review", "{{productType}}"]
---

## Overview

## Key Features

## Pros & Cons

## Who It's Best For

## Price & Value

## Conclusion
```

## Content Types

- **blog-post:** General advice and stories
- **product-review:** Detailed analysis of specific products
- **buying-guide:** Comparison shopping for product categories
- **how-to:** Step-by-step instructions
- **listicle:** Top X lists (e.g., "10 Best Dog Toys")

## Target Countries

- US (United States)
- ES (Spain)
- IT (Italy)
- DE (Germany)
- GB (United Kingdom)
- FR (France)

## Pet Types

- dogs
- cats
- birds
- fish
- reptiles
- small-animals
- all-pets

## Content Creation Workflow

1. **Generate Outline** - Create detailed outline with JSON format
2. **Write Content** - Based on outline, write full content
3. **Add Affiliate Links** - System inserts geo-targeted Amazon links
4. **Format for Hugo** - Add frontmatter and markdown
5. **Optional: eBook Promo** - Add call-to-action if includeEbook=true

## Prompt Templates

### Outline Generation
```
Create a detailed outline for a {{contentType}} about: {{topic}}

Target audience: Pet owners interested in {{petType}}
Word count target: {{wordCount}}

Include:
- Compelling title (SEO-optimized)
- Meta description (150-160 characters)
- 5-7 main sections with H2 headings
- Key points for each section
- 3-5 product recommendation opportunities

Format as JSON.
```

### Content Generation
```
Write a complete {{contentType}} based on this outline:

{{outline}}

Requirements:
- {{wordCount}} words approximately
- SEO-optimized with natural keyword usage
- Engaging, conversational tone
- Include personal anecdotes where appropriate
- Recommend specific pet products (mention product names generically)
- Use markdown format with ## for H2 and ### for H3
- Include introduction and conclusion
- Add FAQ section if appropriate

Do NOT include product links - those will be added automatically.
```

---

Add whatever helps you do your job. This is your cheat sheet.
