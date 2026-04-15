// GA4 Event Tracking for ForPetsWithLove.com
// Add this to your theme's footer.html or JavaScript file

// Initialize tracking after page load
document.addEventListener('DOMContentLoaded', function() {
    
    // 1. Amazon Affiliate Link Clicks
    const amazonLinks = document.querySelectorAll('a[href*="amazon.com"]');
    amazonLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const productCategory = determineProductCategory(link.href, link.textContent);
            
            if (typeof gtag !== 'undefined') {
                gtag('event', 'affiliate_click', {
                    'event_category': 'affiliate',
                    'event_label': 'amazon_' + productCategory,
                    'affiliate_platform': 'amazon',
                    'product_category': productCategory
                });
            }
        });
    });

    // 2. eBook CTA Clicks
    const ebookLinks = document.querySelectorAll('a[href*="books2read.com"], a[href*="amazon.com/dp/B0FDG9WPB2"]');
    ebookLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (typeof gtag !== 'undefined') {
                gtag('event', 'ebook_click', {
                    'event_category': 'ebook',
                    'event_label': 'universal_ebook_link',
                    'book_title': 'The Cat Scratching Solution',
                    'content_type': 'ebook'
                });
            }
        });
    });

    // 3. Internal Link Tracking (Related Articles)
    const relatedLinks = document.querySelectorAll('.related-articles a, section:has(h2) a[href^="/"], div:has(h2) a[href^="/"]');
    relatedLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (typeof gtag !== 'undefined') {
                gtag('event', 'internal_link', {
                    'event_category': 'navigation',
                    'event_label': link.textContent.trim().substring(0, 50),
                    'link_type': 'related_article',
                    'content_type': 'programmatic_seo'
                });
            }
        });
    });

    // 4. FAQ Interaction (if using details/summary or accordion)
    const faqItems = document.querySelectorAll('details summary, .faq-item h3, .faq-item button');
    faqItems.forEach(item => {
        item.addEventListener('click', function() {
            if (typeof gtag !== 'undefined') {
                gtag('event', 'faq_interaction', {
                    'event_category': 'engagement',
                    'event_label': item.textContent.trim().substring(0, 50),
                    'action': 'expand'
                });
            }
        });
    });

    // 5. People Also Ask Clicks
    const paaItems = document.querySelectorAll('.people-also-ask strong, .related-questions strong');
    paaItems.forEach(item => {
        item.addEventListener('click', function() {
            if (typeof gtag !== 'undefined') {
                gtag('event', 'people_also_ask', {
                    'event_category': 'engagement',
                    'event_label': item.textContent.trim().substring(0, 50)
                });
            }
        });
    });
});

// Helper: Determine product category from context
function determineProductCategory(url, text) {
    const combined = (text + ' ' + url).toLowerCase();
    
    if (combined.includes('dog food')) return 'dog_food';
    if (combined.includes('cat food')) return 'cat_food';
    if (combined.includes('dog bed')) return 'dog_bed';
    if (combined.includes('dog crate')) return 'dog_crate';
    if (combined.includes('cat litter')) return 'cat_litter';
    if (combined.includes('cat toy') || combined.includes('kitten')) return 'cat_toy';
    if (combined.includes('bird cage')) return 'bird_cage';
    if (combined.includes('reptile')) return 'reptile_supplies';
    if (combined.includes('hamster') || combined.includes('guinea pig')) return 'small_animal';
    if (combined.includes('fish') || combined.includes('aquarium')) return 'aquarium';

    // Fallback
    if (combined.includes('dog')) return 'dog_supplies';
    if (combined.includes('cat')) return 'cat_supplies';
    if (combined.includes('bird')) return 'bird_supplies';
    
    return 'pet_supplies';
}

// 6. Scroll Depth Tracking (optional)
let maxScroll = 0;
window.addEventListener('scroll', function() {
    const scrollable = document.documentElement.scrollHeight - window.innerHeight;
    const scrolled = (window.scrollY / scrollable) * 100;

    if (scrolled > maxScroll) {
        maxScroll = scrolled;

        // Track at 25%, 50%, 75%, 90%
        if (maxScroll >= 25 && maxScroll < 30) {
            trackScrollDepth(25);
        } else if (maxScroll >= 50 && maxScroll < 55) {
            trackScrollDepth(50);
        } else if (maxScroll >= 75 && maxScroll < 80) {
            trackScrollDepth(75);
        } else if (maxScroll >= 90 && maxScroll < 95) {
            trackScrollDepth(90);
        }
    }
});

function trackScrollDepth(depth) {
    if (typeof gtag !== 'undefined') {
        gtag('event', 'scroll_depth', {
            'event_category': 'engagement',
            'event_label': depth + '%',
            'percent_scrolled': depth
        });
    }
}
