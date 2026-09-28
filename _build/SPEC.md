# Ridgeline Excavation — inner page copy spec

You are writing ONE fragment per assigned page: the `<main>` content only (no `<head>`,
no `<header>`, no `<footer>`, no `<script>`). It is assembled into a full page by a
generator that supplies the head, nav, footer, canonical, JSON-LD, CSS links.

Write the file(s) to the exact absolute path(s) given in your task.
Output ONLY valid HTML. No markdown fences, no commentary inside the file.

## Business facts (the ONLY claims you may make about the company)

- Name: **Ridgeline Excavation LLC**
- Phone: **740-629-7020** (link: `<a href="tel:7406297020">740-629-7020</a>`)
- Email: **ridgelinedig@gmail.com**
- Site: https://ridgelineexcavationohio.com
- Locally owned excavating / earthwork company. Residential, commercial and agricultural work.
- Services (exact names): Site Preparation, Land Clearing, Driveway Installation & Refurbishing,
  Drainage (swales, French drains, culverts), Trail Building & Clearing, Tree Removal & Cleanup.
- Service region: the **Mid-Ohio Valley** — southeast Ohio and the Wood/Tyler/Pleasants County
  area of West Virginia.
- Homepage already claims: 15+ years experience, 300+ projects completed, safety focused,
  24/7 emergency response. You may repeat those four, nothing stronger.
- Free quotes; response within one business day.

## HARD BANS (fabrication = the page is rejected)

- No founding year. In particular NEVER "est. 2003" — that belongs to an unrelated
  Ridgeline Excavation in Jackson, Wyoming.
- No prices, rates, hourly figures, or "$X per Y" anything.
- No street address (they are a service-area business), no office hours, no license or
  policy numbers, no insurance dollar amounts, no employee counts, no certifications,
  no awards, no "family owned since …", no equipment brand/model inventory.
- No review counts, star ratings, or named clients. No `aggregateRating`.
- No invented project addresses or client names.
- Do not claim a town is their "home base" or "headquarters" — say "we serve X".

## Area facts (public geography — fine to use, in your own words)

- Marietta (Washington County, OH) sits at the confluence of the Muskingum and Ohio Rivers.
- Washington County OH towns: Marietta, Belpre, Beverly, Lowell, Waterford, New Matamoras,
  Devola, Reno. Ohio River floodplain + steep hillside and ridge lots.
- West Virginia side: Parkersburg, Vienna, Williamstown (Wood County), Sistersville
  (Tyler County), St. Marys (Pleasants County).
- Noble County OH: Caldwell. Monroe County OH: Woodsfield. Morgan County OH: McConnelsville.
- Athens (Athens County, OH) — hilly, heavily wooded, lots of rural acreage and long gravel lanes.
- Regional conditions worth naming: clay-heavy soils that hold water, shale and sandstone
  rock, freeze-thaw cycles that heave driveways and clog drainage, spring runoff and
  river-bottom water tables, wooded ridge lots with stumps and brush, narrow access lanes
  to back acreage.

## Page structure (every page, in this order)

```html
<section class="page-hero">
  <div class="container">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="/">Home</a> <span aria-hidden="true">›</span> <span>PAGE NAME</span>
    </nav>
    <h1>…</h1>
    <p class="page-lede">…one or two sentences…</p>
    <div class="hero-cta">
      <a href="/#contact" class="btn btn-primary">Get a Free Quote</a>
      <a href="tel:7406297020" class="btn btn-outline">Call 740-629-7020</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container prose">
    …2–4 subsections, each <h2> + 1–3 <p> (or a <ul class="value-list">)…
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <div class="section-head">
      <p class="section-kicker">…</p>
      <h2 class="section-title">…</h2>
    </div>
    <div class="grid service-links">
      …3 <article class="card service-card"> with <h3> + <p> + <a class="card-link" href="…">…
    </div>
  </div>
</section>

<section class="section">
  <div class="container faq-block">
    <h2>…common questions…</h2>
    <div class="faq-item"><h3>Q…</h3><p>A…</p></div>   <!-- 3 or 4 of these -->
  </div>
</section>

<section class="cta-band">
  <div class="container">
    <h2>Ready to start your project?</h2>
    <p>Free quotes across the Mid-Ohio Valley. Call <a href="tel:7406297020">740-629-7020</a> or send us your project details — we reply within one business day.</p>
    <a href="/#contact" class="btn btn-primary">Request a Free Quote</a>
  </div>
</section>
```

## Internal links (required — use path-and-anchor only, no domain)

Available targets: `/`, `/#contact`, `/service-areas.html`, `/faq.html`,
`/site-prep.html`, `/land-clearing.html`, `/driveway-installation.html`, `/drainage.html`,
`/trail-building.html`, `/tree-removal.html`,
`/excavation-marietta-oh.html`, `/excavation-parkersburg-wv.html`, `/excavation-belpre-oh.html`,
`/excavation-beverly-oh.html`, `/excavation-caldwell-oh.html`, `/excavation-athens-oh.html`.

- Every page: 3 sibling-service links in the `service-links` grid (your task lists which).
- Every page: a "where we work" sentence or list linking 3 city pages (your task lists which).
- Servicing pages link to `/service-areas.html`; city pages link to `/faq.html`.

## Writing rules

- One `<h1>` per page, then `<h2>`/`<h3>` — never skip levels.
- 450–650 words of visible body copy. Concrete and plain: what gets done, in what order,
  what the customer sees, what affects cost (access, rock, drainage, haul distance) —
  without quoting numbers.
- No keyword stuffing: the primary phrase appears in the h1, the lede, and 2–3 more times
  naturally. No repeated identical sentences between pages.
- Each assigned page must read as if written for that topic alone — no boilerplate
  paragraphs copied between your own pages.
- Address the reader as "you"; refer to the company as "we".
- Alt text is not needed (the generator adds images).
