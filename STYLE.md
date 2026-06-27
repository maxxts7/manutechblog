# Post Style Specification

The house style for the long-form essays on this blog. This is the canonical
reference; when creating a new essay, copy the `<style>` block and structure
from one of the reference posts and keep the values below in sync.

**Reference implementations (all share this system):**
- `posts/the-loop-no-one-chose/index.html`
- `posts/open-in-principle-blind-in-practice/index.html`
- `posts/how-to-build-a-mirror-without-holding-it/index.html`

**Not governed by this spec:**
- `posts/cross-axis-capping/index.html` — a data-report layout with its own
  system (TL;DR box, callouts, stat blocks). Do not retrofit this spec onto it.
- `posts/typography-playground-d7b2839ccc1303c5/index.html` — private, unlisted
  sandbox for tuning the reading knobs. Its larger lead and adjustable weights
  are demo controls, not house style. It is the *source* you paste tokens from.

---

## 1. Fonts

Loaded from Google Fonts in `<head>`:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@400..900&family=Noto+Serif:ital,wght@0,400..700;1,400..700&display=swap" rel="stylesheet">
```

- **Headings / display:** Merriweather (`--font-head`)
- **Body / diagram labels:** Noto Serif (`--font-body`)

Diagram SVG text uses the **body** font, not a system sans-serif — labels are
meant to read as part of the prose.

---

## 2. Design tokens (`:root`)

```css
:root {
  /* palette */
  --text: #1a1a2e;
  --text-secondary: #64748b;
  --bg: #ffffff;
  --border: #e2e8f0;
  --blue: #3b82f6;
  --blue-dark: #1e40af;
  --blue-light: #dbeafe;
  --blue-muted: #60a5fa;
  --gray-50: #f8fafc;
  --gray-100: #f1f5f9;
  --gray-200: #e2e8f0;
  --gray-400: #94a3b8;
  --gray-700: #334155;
  --orange: #f59e0b;
  --orange-dark: #b45309;
  --orange-light: #fef3c7;

  /* reading knobs — single source of truth; re-tune in the typography playground */
  --font-head: 'Merriweather', Georgia, serif;
  --font-body: 'Noto Serif', Georgia, serif;
  --reading-width: 860px;
  --reading-size: 15.5px;
  --reading-lh: 1.55;
  --h1-size: 36.3px;
  --h2-size: 26.6px;
}
```

The **reading knobs** are the single source of truth for type. To re-tune,
adjust in the typography playground, then paste the resulting values here.
Blue is the accent throughout; orange is reserved for "prescribe / warning"
framing inside diagrams.

---

## 3. Layout

- `box-sizing: border-box` on everything.
- `body` — `--font-body`, `--reading-size`, `--reading-lh`, `--text` on `--bg`,
  antialiased, no margin.
- `::selection` — `--blue-light` background, `--blue-dark` text.
- `article` — `max-width: var(--reading-width)` (860px), centered,
  `padding: 3rem 1.5rem 4rem`.
- Top `nav` — a back-link above the article, same max-width and side padding.

Document order inside `<article>`:
`header → lead → hero → body (p / h2 / diagram / statement / gains) → readnext → footer`

---

## 4. Components

### Header
```html
<header>
  <p class="eyebrow">Essay</p>
  <h1>Title</h1>
  <p class="subtitle">One-line standfirst</p>
  <div class="author-line">
    <span class="author-name">Manu Xaviour Thaisseril Shaju</span>
    <span class="dot">&middot;</span>
    <span class="meta-date">June 2026</span>
  </div>
</header>
```
- `margin-bottom: 3.25rem`, `padding-bottom: 2rem`, `border-bottom: 1px solid var(--border)`.
- `.eyebrow` — 0.74rem, weight 700, `letter-spacing: 0.18em`, uppercase, `--blue`.
- `h1` — `--font-head`, `--h1-size`, weight 800, `line-height: 1.12`,
  `letter-spacing: -0.035em`, `text-wrap: balance`.
- `.subtitle` — 1.15rem, `--text-secondary`, weight 400, `max-width: 38ch`.
- `.author-name` 0.92rem/600 `--text`; `.dot` `--gray-200`; `.meta-date` 0.92rem `--gray-400`.

### Lead paragraph + drop cap
```html
<p class="lead">First paragraph…</p>
```
- **Lead text matches body size** — `font-size: var(--reading-size)`,
  `line-height: var(--reading-lh)`. The only distinction is the drop cap and
  `margin-bottom: 1.4rem`. (Do **not** re-introduce a larger lead size.)
- `.lead::first-letter` — floated drop cap, `--font-head`, 3.5rem,
  `line-height: 0.78`, weight 800, `--blue-dark`, `padding: 0.32rem 0.62rem 0 0`.

### Body type
- `p` — `margin: 0 0 0.95rem`, `text-wrap: pretty`.
- `strong` — weight 600. `em` — italic.
- `a` — `--blue`, no underline; underline on hover. External links use
  `rel="noopener" target="_blank"`.

### Section headings
```html
<h2>Section title</h2>
```
- `--font-head`, `--h2-size`, weight 700, `line-height: 1.25`,
  `letter-spacing: -0.02em`, `text-wrap: balance`.
- `margin: 2.25rem 0 1.3rem`, `padding-left: 0.85rem`,
  `border-left: 3px solid var(--blue)`.

### Hero figure
```html
<figure class="hero">
  <svg viewBox="…" role="img" aria-label="…">…</svg>
  <figcaption>…</figcaption>
</figure>
```
- `width: fit-content`, centered, `margin: 2.25rem auto 2.5rem`,
  `padding: 1.5rem 1.6rem 1.25rem`, `--gray-50` bg, `1px solid var(--gray-200)`,
  `border-radius: 14px`, centered text.
- `svg` — block, `width: 230px`, `max-width: 100%`, auto height.
- `figcaption` — `max-width: 28ch`, 0.8rem/1.5, `--text-secondary`.

### Inline diagram
```html
<figure class="diagram">
  <svg viewBox="…" role="img" aria-label="…">…</svg>
  <figcaption><strong>Lead-in.</strong> Caption text, with <em>emphasis</em>.</figcaption>
</figure>
```
- Full-bleed within the column: `margin: 2.75rem -1.5rem`,
  `padding: 1.75rem 1.6rem 1.5rem`, `--gray-50` bg, `1px solid var(--gray-200)`,
  `border-radius: 14px`.
- `svg` — block, full width, auto height.
- **`svg text` — `font-family: var(--font-body)`** (matches the prose).
- `figcaption` — `max-width: 56ch`, centered, 0.8rem/1.55, `--text-secondary`;
  `strong` is `--gray-700`/600, `em` italic.
- SVG must carry `role="img"` and a descriptive `aria-label`.

### Display statement (pull-quote)
```html
<p class="statement">A single load-bearing line.</p>
```
- `--font-head`, centered, `max-width: 33ch`, 1.35rem, **weight 500** (slightly
  bold), `line-height: 1.32`, `letter-spacing: -0.02em`, `text-wrap: balance`,
  `margin: 3.25rem auto`, `padding-top: 2.1rem`.
- `::before` — a centered 44×3px `--blue` rule above the line.

### Gains list
```html
<ul class="gains">
  <li><strong>Point heading.</strong> Supporting sentence…</li>
</ul>
```
- `list-style: none`, `margin: 1.75rem 0 2rem`.
- `li` — `margin-bottom: 1.5rem`, `padding-left: 1.35rem`,
  `border-left: 2px solid var(--blue-light)`; last child no bottom margin.
- `li strong` — `display: block`, 1.05rem, `letter-spacing: -0.01em`.

### Read-next card
```html
<a class="readnext" href="/posts/<slug>/">
  <p class="rn-label">Read next &rarr;</p>
  <p class="rn-title">Next Title</p>
  <p class="rn-desc">One-sentence hook.</p>
</a>
```
- Block link card: `margin-top: 3.5rem`, `padding: 1.4rem 1.65rem`,
  `1px solid var(--gray-200)`, `border-radius: 12px`, `--gray-50` bg,
  inherits text color.
- Hover — `border-color: var(--blue)`, `box-shadow: 0 2px 12px rgba(59,130,246,0.08)`.
- `.rn-label` 0.7rem/700, `letter-spacing: 0.14em`, uppercase, `--blue`.
- `.rn-title` 1.18rem/700, `letter-spacing: -0.02em`, `--text`.
- `.rn-desc` 0.9rem, `--text-secondary`, `line-height: 1.5`.

### Footer
```html
<footer>
  <p class="byline">Manu Xaviour Thaisseril Shaju &middot; June 2026</p>
  <a class="back" href="/">&larr; All writing</a>
</footer>
```
- `margin-top: 4rem`, `padding-top: 1.75rem`, `border-top: 1px solid var(--border)`,
  flex with space-between, wraps with `gap: 0.75rem`.
- `.byline` 0.85rem `--gray-400`; `.back` 0.85rem `--text-secondary`,
  `--blue` on hover.

---

## 5. Responsive

```css
@media (max-width: 700px) {
  header h1 { font-size: calc(var(--h1-size) * 0.8); }
  .lead::first-letter { font-size: 3rem; }
  .statement { font-size: 1.15rem; }
}
```
The lead body text does **not** shrink (it already equals body size); only the
drop cap does.

---

## 6. Head / metadata checklist

Each post `<head>` carries:
- `<title>`, `<meta name="description">`, `<link rel="canonical">`.
- Open Graph: `og:type=article`, `og:site_name`, `og:title`, `og:description`,
  `og:url`, `og:image` (+ `:width` 1200, `:height` 630, `:alt`).
- Twitter: `summary_large_image` card with title/description/image.
- Absolute URLs use the live base `https://manutechblog.netlify.app`.
- A `1200×630` `og.png` lives beside each post's `index.html`.

---

## 7. Recent decisions (changelog)

- **Lead = body size.** Opening paragraph reads at `--reading-size`; only the
  drop cap and bottom margin distinguish it. (Previously 1.16rem / 1.08rem.)
- **Statement weight 500.** Pull-quotes are slightly bold (was 700, briefly 400).
- **Diagram font = body.** `.diagram svg text` uses `var(--font-body)` instead
  of a system sans-serif stack.
