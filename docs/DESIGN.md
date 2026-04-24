# Design System Document: The Sacred Silence
 
## 1. Overview & Creative North Star
This design system is built upon the Creative North Star of **"The Reverent Breath."** In a world of digital noise, this system functions as a digital sanctuary. It rejects the frantic "grid-block" aesthetic of standard apps in favor of high-end editorial layouts characterized by intentional asymmetry, overlapping elements, and vast, breathable negative space. 
 
The goal is to move beyond mere "minimalism" and achieve a sense of "reverence." We accomplish this by treating the screen not as a container for data, but as a series of physical layers—fine paper, translucent vellum, and soft stone. By using a sophisticated typography scale and a tonal-first approach to hierarchy, we guide the user toward a state of contemplative focus.
 
---
 
## 2. Colors: Tonal Depth & Soul
The palette is a curated collection of warm whites, gentle beiges, and muted earth tones. We avoid harsh blacks or vibrant primaries to maintain a spirit of peace.
 
### The "No-Line" Rule
To ensure a premium, custom feel, **1px solid borders are strictly prohibited for sectioning.** Boundaries must never be "drawn"; they must be "felt." Use background color shifts to define space. For example, a `surface-container-low` section sitting on a `surface` background creates a soft, sophisticated transition that feels natural rather than technical.
 
### Surface Hierarchy & Nesting
Treat the UI as a stack of fine materials.
- **Surface (`#fffcf7`):** The base layer—your "canvas."
- **Surface-Container-Low (`#fcf9f3`):** Use for large secondary sections or inset content.
- **Surface-Container-High (`#f0eee5`):** Reserved for interactive components or elevated cards.
- **Nesting:** When placing an element inside another, the inner container should typically move one step higher in the surface tier (e.g., a `surface-container-highest` card placed inside a `surface-container-low` section).
 
### Glass & Signature Textures
- **Glassmorphism:** For floating elements or top navigation bars, use semi-transparent `surface` colors with a `backdrop-blur` (12px–20px). This allows the colors of the content below to bleed through, creating a "frosted vellum" effect.
- **Tonal Gradients:** For primary Call-to-Actions (CTAs), use a subtle linear gradient from `primary` (`#695d4a`) to `primary-container` (`#f2e0c8`). This adds a "soul" and professional polish that flat color cannot replicate.
 
---
 
## 3. Typography: The Editorial Voice
The typography is the anchor of the experience. We pair the timeless authority of a serif with the modern clarity of a sans-serif.
 
- **The Serif (`notoSerif`):** Used for all `display` and `headline` levels. This font conveys tradition and weight. Use `display-lg` (3.5rem) with generous leading to create editorial-style headers that feel like a high-end magazine.
- **The Sans-Serif (`manrope`):** Used for `title`, `body`, and `label` levels. It is clean, humble, and highly legible. 
- **Intentional Asymmetry:** Don't feel obligated to center-align everything. Use left-aligned `headline-lg` text with a wide right margin to create a sense of movement and "breathing room."
 
---
 
## 4. Elevation & Depth: Tonal Layering
Traditional material design relies on shadows; this design system relies on **Tonal Layering.**
 
### The Layering Principle
Depth is achieved by stacking tiers. A `surface-container-lowest` card on a `surface-container-low` background creates a "recessed" feel, while a `surface-container-highest` element on a `surface` background creates a "lifted" feel. 
 
### Ambient Shadows
Shadows should be rare. When a "floating" effect is necessary (e.g., a floating action button or a modal):
- **Blur:** 24px to 40px.
- **Opacity:** 4%–6%.
- **Color:** Use a tinted version of `on-surface` (`#383831`) rather than pure grey to ensure the shadow feels like a natural part of the warm environment.
 
### The "Ghost Border" Fallback
If a border is required for accessibility (e.g., in high-contrast modes), use a **Ghost Border**: the `outline-variant` token (`#babab0`) at **15% opacity**. Never use 100% opaque lines.
 
---
 
## 5. Components: Soft & Intentional
 
### Buttons
- **Primary:** Rounded-xl (`1.5rem`) or Full (`9999px`). Use the `primary` to `primary-container` gradient. Text should be `label-md` in `on-primary`.
- **Secondary:** No background. Use a "Ghost Border" and `primary` text.
- **States:** On hover, increase the opacity of the gradient or slightly shift the surface tier. Avoid sudden color flashes.
 
### Cards & Lists
- **The No-Divider Rule:** Explicitly forbid 1px horizontal lines between list items. Use vertical white space (recommended: `2rem` between items) or a subtle background shift to `surface-container-low` on every other item to separate content.
- **Cards:** Use `lg` (`1rem`) or `xl` (`1.5rem`) corner radius. Use Tonal Layering instead of shadows.
 
### Input Fields
- **Style:** Understated. Use `surface-container-highest` for the background with no border. 
- **Focus:** When active, use a subtle `primary` glow (using a low-opacity shadow) rather than a thick border.
 
### Chips & Selection
- **Selection Chips:** Use `full` rounding. Unselected chips should be `surface-container-high`. Selected chips should transition to `primary` with `on-primary` text.
 
---
 
## 6. Do’s and Don’ts
 
### Do:
- **Embrace White Space:** If you think there is enough space, add 20% more. Space is a luxury in this app.
- **Use "Signature" Offsets:** Place a `headline-md` slightly overlapping the edge of a card to create a custom, high-end feel.
- **Prioritize Softness:** Every corner should be rounded (minimum `0.5rem`). Sharp corners feel aggressive; we are seeking peace.
 
### Don’t:
- **Don't use 1px Dividers:** They clutter the interface and break the "Quiet Path" philosophy.
- **Don't use Pure Black:** Even for text. Use `on-surface` (`#383831`) to keep the contrast soft and readable.
- **Don't use Vibrant Gradients:** Avoid "App Store" style bright blues or purples. Stay within the earth-tone family.
- **Don't Over-Animate:** Transitions should be slow (300ms–500ms) and use "Ease-out" to mimic a gentle breath.