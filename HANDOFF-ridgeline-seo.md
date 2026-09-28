# Ridgeline Excavation LLC — local SEO fix: what was done, and what's left

Site: https://ridgelineexcavationohio.com (served from the Mac Mini, container `ridgine-excavation`, via Nginx Proxy Manager)
Company email of record: **ridgelinedig@gmail.com** · Phone: **740-629-7020**
Date: 2026-09-28

---

## 1. What was wrong (verified before the fix)

| Problem | Evidence |
|---|---|
| Dead contact email published site-wide | `info@ridgine-excavation.com` appeared 4× — that domain does not exist (no A, no MX record), so mail to it bounces. |
| No place names anywhere | 0 occurrences of Marietta, Parkersburg, Belpre, Athens, Caldwell in 495 words of copy. Only "Mid-Ohio Valley" (colloquial, not a Google geo entity). |
| One page total | No service pages, no town pages — no keyword surface to rank with. |
| No structured data | 0 JSON-LD blocks; no LocalBusiness/GeneralContractor node. |
| No crawl plumbing | `robots.txt` 404, `sitemap.xml` 404, no `rel=canonical`, no OG/Twitter tags. |
| Brand-name collision | 4 unrelated Ridgeline Excavations (Jackson WY, Clear Creek CO, Rathdrum ID, Bayfield CO) own the brand SERP. |
| Two live sites, two brands, two phone numbers | `digrivervalley.com` (the owner's earlier site) still sells the same company as **River Valley Excavation** on **740-761-4344**. Duplicate, conflicting entities split every signal Google would otherwise consolidate. |
| Google Business Profile is under the OLD brand | The Maps listing is "**River Valley Excavation**", Lowell OH (place coords 39.5646, -81.5584) — so the profile that owns "excavation near me" does not match the brand on the website. |
| False experience claims | The first build carried "15+ Years Experience", "300+ Projects Completed", "Est. 2003" (copy lifted from the Wyoming company). The business was founded in **2025**; those claims are gone site-wide. |
| Competitors running the playbook | digrivervalley.com has city pages for Marietta, Caldwell, Cambridge, Lowell, Belpre, Vienna, Athens…; sandersexcavating.com/marietta-oh; mariettaohioconcretecompany.com/excavating. |

The form relay itself was healthy: Mailgun domain `mailgun.ridgelineexcavationohio.com` is active and a real
submission ("Quote request from Amy Jackson") was delivered to the client inbox on 2026-09-25.

---

## 2. What was changed and deployed (live, verified over HTTPS)

- **Email fixed everywhere** → `ridgelinedig@gmail.com` (contact section, footer, all 15 pages). Server env
  `MAILGUN_TO` tidied to the same lowercase address.
- **15 pages now live** (was 1):
  - Services: `/site-prep.html`, `/land-clearing.html`, `/driveway-installation.html`, `/drainage.html`,
    `/trail-building.html`, `/tree-removal.html`
  - Towns: `/excavation-marietta-oh.html`, `/excavation-parkersburg-wv.html`, `/excavation-belpre-oh.html`,
    `/excavation-beverly-oh.html`, `/excavation-caldwell-oh.html`, `/excavation-athens-oh.html`
  - Hubs: `/service-areas.html` (towns + counties), `/faq.html` (12 Q&As)
  - Homepage rewritten for geo + service intent (river bottoms, clay, shale, hillside lots, access, drainage).
- **Structured data**: `GeneralContractor` + `HomeAndConstructionBusiness` with NAP, `areaServed`
  (cities + 8 counties), `hasOfferCatalog`; `Service` + `BreadcrumbList` on every inner page;
  `FAQPage` (12 questions) on the FAQ page. **No `aggregateRating`** — no verified reviews exist yet.
- **Crawl plumbing**: `robots.txt`, `sitemap.xml` (15 URLs), per-page canonical, OG/Twitter tags,
  geo meta, `?v=3` cache-buster on the stylesheet.
- **Internal linking**: nav, footer (services + service areas columns), town chips on the homepage,
  cross-links between service pages and town pages.
- **Fixed a real rendering bug**: `.cta-band a` was overriding `.btn-primary` on specificity, so the
  bottom CTA button label was lime text on a lime fill (invisible). Verified in the live DOM after the fix:
  `color rgb(10,10,10)` on `rgb(212,255,0)`.
- **Copy discipline**: no prices, no rates, no street address, no founding year, no invented history —
  in particular the "Est. 2003 / Commercial & Residential Earth Work" line in the old build (copied from the
  unrelated Wyoming company) is gone.

Verification run over public HTTPS: all 15 pages + sitemap + robots + CSS + JS + images return 200 with the
expected canonical/JSON-LD/NAP markers; internal link audit clean; JSON-LD parses on every page.
Form endpoint checks: invalid POST → 400 with the right message; honeypot POST → fake 200, no mail sent.

### Deployment mechanics (for future edits)
Working copy: `/home/agent/workspace/ridgeline-ohio` (fragment sources in `_build/bodies/`,
assembler `_build/assemble.py`, validators `_build/verify_local.py`, `_build/verify_live.py`).
Remote: `/Users/cyberal/docker/ridgine-excavation` on the Mac Mini
(`sshpass -e ssh cyberal@69.133.124.51`, password auth).
Rollback: previous source tree `ridgine-excavation.bak-20260928-1344`, previous image tagged
`ridgine-excavation:prev-20260928`.

---

## 3. What only the owner can do (needs the client's Google account)

This is the part that actually decides whether "excavation near me" works. The website can only
support it — the Local Pack is driven by the Business Profile.

1. **The profile already exists — under the wrong name.** The Google listing is "**River Valley Excavation**",
   Lowell OH (verify: google.com/maps/place/River+Valley+Excavation). Decide on the entity, then act:
   - **Preferred:** rename the profile to `Ridgeline Excavation LLC` (Google reviews name changes; it usually
     approves them, and sometimes asks for proof). One entity, one brand, keeps the profile's age and reviews.
   - **Alternative:** leave the profile as River Valley Excavation and treat "Ridgeline" as a DBA — worse,
     because the site, the reviews and the phone all advertise Ridgeline while the pack says River Valley.
   - Nothing can be done from here: it needs the client's Google account.
2. **Profile settings to use once the name is sorted**
   - Primary category: **Excavating contractor**
   - Secondary: Land clearing service · Site preparation contractor · Drainage service · Tree service · Paving contractor
   - Website: `https://ridgelineexcavationohio.com`
   - Phone: **confirm which line is live** — the site publishes 740-629-7020; the old site and (probably) the
     profile carry 740-761-4344. Google will match the profile to whatever the site prints, so they must agree.
   - Address: `1495 Weppler Road, Lowell, OH 45744` (published on the old site, so it is already public). A
     service-area business can hide the address from the profile, but the postcard/video verification needs it.
   - Service area: a 75-mile radius of Lowell — Washington, Athens, Guernsey, Noble, Monroe, Morgan, Belmont
     counties OH; Wood (+ Tyler, Pleasants) WV; Marietta, Lowell, Belpre, Beverly, Caldwell, Woodsfield,
     McConnelsville, Cambridge, New Concord, Nelsonville, St. Clairsville, Parkersburg, Vienna, Williamstown,
     Mineral Wells, Sistersville, St. Marys.
   - Services: add all eleven, using the exact names on the site.
   - Hours: 24/7 is advertised ("call or text 24/7"), evenings and weekends by appointment.
   - 10+ real job photos, business description ≈750 chars (reuse the homepage copy).
3. **Reviews** — the single biggest controllable Local Pack lever. Ask after every completed job; goal
   15–20 Google reviews in 90 days. Send a direct review link (from the GBP dashboard).
4. **Google Search Console** — verify `ridgelineexcavationohio.com` (DNS TXT via the domain's DNS host),
   submit `https://ridgelineexcavationohio.com/sitemap.xml`, then use "URL inspection → request indexing"
   on the homepage and the two main town pages.
5. **Other citations with identical NAP**: Bing Places, Apple Business Connect, Yelp, Facebook Page,
   local chamber, Ohio/WV contractor directories.
8. **Decide the fate of `digrivervalley.com`** — see open question 3 below.
9. **Kill the duplicate POC hostname**: `ridgine-excavation.cyberalsolutions.com` still resolves to the Mac
   with no matching TLS cert (fails to load). Either delete the DNS record or add a 301 to the real domain
   in NPM — a second copy of the same content is an SEO liability.

---

## 4. Honest expectations

- "Excavation near me" is a proximity query: the pack shows what's close to the searcher's phone. Even a
  perfect profile only wins in towns they are physically near. Chasing the bare head term is not the goal.
- The money queries are long-tail + town: "land clearing Marietta Ohio", "driveway grading Parkersburg",
  "septic pad excavation Washington County", "pond digging Caldwell". The new town and service pages are
  built for those.
- Realistic timeline: with the profile verified + reviews + the 26 pages indexed, pack visibility in their
  home towns is a 60–120 day proposition. Brand-name searches should come first (they currently lose even
  "Ridgeline Excavation" to the Wyoming company).

## 5. Open questions for Ryan / the client

1. ~~The three homepage testimonials~~ — **resolved 2026-09-28: they were not real, so they were deleted.** The
   whole "What Our Clients Say" block (3 fake 5-star quotes) is gone, its nav/anchor removed, and the unused
   `.testimonial/.stars/.t-author` CSS stripped. It is replaced by an honest "How We Work / What Happens After
   You Call" section (4 steps) plus a note that the Google review profile is being built and customers can ask
   to speak to past clients. Nothing on the site now claims a review or a rating, and no `aggregateRating`
   schema exists. **When real Google reviews exist, they should be embedded with their real attribution
   (and only then can review markup be considered).**
2. ~~The stat claims~~ — **resolved 2026-09-28.** They were false (the business was founded in 2025 and the
   claims were lifted from an unrelated Wyoming company). Replaced with claims that are supportable: 24/7 call
   or text, free written estimates, 811 locates handled, owner-operated by **TJ Flowers**, fully insured.
3. **`digrivervalley.com` — keep it or fold it in?** It is the same company under an old brand, still live and
   still selling. Options:
   - **301 the old site to `ridgelineexcavationohio.com`** (best for SEO: any existing authority and its
     town-page URLs consolidate onto the brand that the profile and reviews will use). Needs the domain's
     DNS/DNS host access.
   - Leave it live but strip the phone/email so it stops competing (weakest but free).
   - Leave it alone (worst: two entities, two numbers, confused customers).
   A straight 301 loses the "River Valley Excavation" keyword entirely, so if the client still gets work under
   that name, keep a single page on the new domain explaining the name change and 301 only the old *service
   and town* URLs to their new equivalents.
4. **Which phone number is live — 740-629-7020 or 740-761-4344?** The site prints 629-7020 site-wide and the
   form's mail goes to the Gmail; the old site prints 761-4344. One number must be the single NAP on the site,
   the profile and every citation. Tell me which and I will make the site and schema match.
5. **Real project photos.** The portfolio block now honestly reads "Typical Projects We Take On" and uses
   stock imagery. The owner has real photos on the old site (and, from the old gallery, real project
   names like a Reno shed pad). Send them and they replace the stock images — with the owner's OK to publish.
6. **Bonuses not yet wired** (say the word): analytics tag; a branded `info@ridgelineexcavationohio.com`
   forwarding to the Gmail (domain MX is live at the registrar); a text/SMS quote option; a real service-area
   map to replace the placeholder.
7. **GitHub Actions deploy is broken** — repo `rkweekley/ridgine-excavation` is private and both workflow
   runs failed on 2026-09-12. Deploys are done by rsync + `docker build` on the Mac. Fix CI, or keep manual?
8. **Send one real test submission** through the live form to the client inbox? It would land in their Gmail
   (labelled TEST), so I have held off without your OK.
