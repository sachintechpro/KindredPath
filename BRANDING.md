# KindredPath — Brand & UX Guide

## Purpose
KindredPath is a personal, family-facing information and reflection site. It is not a financial-services storefront and it does not promote a company, carrier, product, or adviser.

The voice is first person: **I am sharing what I have learned while trying to understand family financial decisions, protection, healthcare, retirement, caregiving, education and legacy.**

## Brand idea
**KindredPath** means the path a family travels together.

The visual identity should feel like a **well-kept family notebook**: warm, calm, trustworthy and human. It should not look like a fintech dashboard, insurance carrier site, SaaS product, or engineering portfolio.

## Visual language
- Background: warm parchment / paper, not pure white.
- Primary ink: deep forest charcoal.
- Accent: muted terracotta.
- Secondary accent: sage.
- Supporting accent: clay/gold.
- Cards: soft paper-white with thin warm borders.
- Corners: generous but not excessive.
- Shadows: subtle and natural.
- Photography: real family life, contextual, documentary-feeling; never generic corporate stock or AI-looking imagery.
- One meaningful image at a time on a page section. Avoid image grids and repeated photos.

## Typography
- Display: `DM Serif Display` for reflective, editorial headings.
- Body: `Manrope` for readable, modern text.
- Small labels: uppercase, restrained letter spacing.
- Avoid using the typography of the engineering portfolio.

## Core CSS tokens

```css
:root {
  --kp-ink: #1e2924;
  --kp-forest: #27463d;
  --kp-sage: #dce7df;
  --kp-terracotta: #c96f5b;
  --kp-clay: #c7a77a;
  --kp-paper: #f7f3eb;
  --kp-card: #fffdf9;
  --kp-muted: #69736d;
  --kp-line: #e4ded3;
  --kp-shadow: 0 18px 48px rgba(39,70,61,.09);
}
```

## Layout rules
1. No page should become a wall of cards.
2. On mobile, card collections become horizontal snap-scroll stories or compact stacked sections.
3. Long text is limited to approximately 2–3 lines in cards; the full explanation opens on the destination page.
4. Do not place several photographs beside one another.
5. Use motion for progressive disclosure, not decoration.
6. Respect `prefers-reduced-motion`.
7. Use lazy-loaded, responsive images with explicit dimensions.
8. Every calculator explains its assumptions immediately near the result.
9. Every product explanation distinguishes **what it can do**, **what it cannot do**, and **what questions I would ask**.
10. Official government or institutional sources are preferred for facts and current rules.

## Voice
Write in first person:
- “I built this because…”
- “I kept coming back to…”
- “What I learned…”
- “Here is how I think about it…”
- “I would ask…”
- “I would verify this with…”

Avoid:
- “Our company”
- “Best-in-class”
- “Revolutionary”
- sales funnels
- testimonials that are not real
- invented statistics
- product pitches
- marketing claims

## Source policy
KindredPath may explain products, but it does not endorse them.

For factual/current information, prefer:
- U.S. Census Bureau
- Consumer Financial Protection Bureau
- Medicare.gov / CMS
- Social Security Administration
- Internal Revenue Service
- U.S. Department of Labor
- U.S. Department of Education / Federal Student Aid
- other government, university, or recognized public institutions

Do not cite insurance carriers, banks, brokerages, financial-product vendors, lead-generation sites, or other marketing/business websites as authority.

## Photography
Photography is supporting context, not decoration.
- One hero/context image per major page.
- Avoid repeating the same photograph.
- Do not place three or more photos side-by-side.
- Keep image quality intentionally lightweight for mobile.
- Preserve photographer attribution when using external photography.

## Product education pattern
Each product/category should follow:
**What it is → Why a family might consider it → Potential benefits → Trade-offs / limitations → Questions I would ask → Official source**

## Future UX direction
KindredPath should feel more like a personal journal + public reference library than a commercial website.