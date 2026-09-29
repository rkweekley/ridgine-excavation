# Ridgeline Excavation LLC — local SEO fix: what was done, and what's left

Site: https://ridgelineexcavationohio.com (served from the Mac Mini, container `ridgine-excavation`, via Nginx Proxy Manager)
Company email of record: **ridgelinedig@gmail.com** · Phone: **740-629-7020** (confirmed live by Ryan 2026-09-28; the old line 740-761-4344 is retired)
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
| `digrivervalley.com` was SOLD to another person | It was the previous site for this business (trading as **River Valley Excavation**, 740-761-4344) and is now a third party's property. We do not control it, must not 301 it, and must NOT reuse its identity assets (street address, social profiles, Maps listing). Only its BUSINESS FACTS are usable: services offered, service area, operating practices. |
| Google Business Profile — ownership unclear | The Maps listing "**River Valley Excavation**" (Lowell OH) came off the old site. Since the site was sold, that profile may belong to the previous owner rather than the client. CONFIRM OWNERSHIP before touching it: if it is not the client's, they need a fresh profile of their own. |
| False experience claims | The first build carried "15+ Years Experience", "300+ Projects Completed", "Est. 2003" (copy lifted from the Wyoming company). Those claims are gone site-wide, and no founding year is claimed anywhere. |
| Competitors running the playbook | The old site carried city pages for Marietta, Caldwell, Cambridge, Lowell, Belpre, Vienna, Athens…; also sandersexcavating.com/marietta-oh and mariettaohioconcretecompany.com/excavating. The sold domain may now compete in the same area under the old brand. |

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
Deploy source of truth: the public repo `rkweekley/ridgine-excavation` — push to `main` and
GitHub Actions does the rest. The workflow builds a multi-arch image (linux/amd64 + linux/arm64,
required for the Apple Silicon Mac), pushes `ghcr.io/rkweekley/ridgine-excavation:latest`, then SSHs
to the Mac, pulls it and recreates the `ridgine-excavation` container on the `mac` network with the
host-side env file. It health-gates through Nginx Proxy Manager and FAILS the job if the site does
not answer 200 (the old workflow printed a green line over a dead site).
Repo secrets: `MAC_MINI_HOST`, `DEPLOY_USER_PROD`, `DEPLOY_SSH_KEY_PROD`.
Runtime secrets (Mailgun key) stay on the Mac at `/Users/cyberal/docker/ridgine-excavation/ridgine.env`
— never in git or the image.
Rollback: re-run any green workflow run from the Actions tab, or `docker run` the previous image tag.

---

## 3. What only the owner can do (needs the client's Google account)

This is the part that actually decides whether "excavation near me" works. The website can only
support it — the Local Pack is driven by the Business Profile.

1. **First establish who owns the "River Valley Excavation" profile.** It came from the old site, which has
   been sold — so it may belong to the previous owner. Check with the client, then:
   - **Client owns it:** rename it to `Ridgeline Excavation LLC` (Google reviews name changes) and update the
     phone to 740-629-7020. One entity, keeps its age and any reviews.
   - **Client does not own it:** create a NEW profile for Ridgeline at the client's own address and leave the
     old one alone. Never claim or edit a profile that is not the client's — it will just be reverted.
   - Nothing can be done from here: it needs the client's Google account.
2. **Profile settings to use once the name is sorted**
   - Primary category: **Excavating contractor**
   - Secondary: Land clearing service · Site preparation contractor · Drainage service · Tree service · Paving contractor
   - Website: `https://ridgelineexcavationohio.com`
   - Phone: **740-629-7020** — confirmed live 2026-09-28. The site prints it on all 26 pages, in the `tel:`
     links and in the schema, so the profile MUST match it. If the profile still shows 740-761-4344, change it
     first: the pack shows the profile's number and it will not match the website until it is fixed.
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
3. ~~What to do with `digrivervalley.com`~~ — **resolved 2026-09-28: it was sold to another person.**
   Nothing to do, and nothing to take from it except business facts. Do NOT 301 it, do not ask for its
   content, and do not reuse its address, social pages or Maps listing. Everything of that nature was
   REMOVED from this site on 2026-09-28:
   - schema `streetAddress`, `postalCode`, `geo`, `foundingDate` and `sameAs` (the FB/IG/Maps links)
   - the street address and the Facebook / Instagram / Google links in the footer
   The site now publishes town-level NAP only ("Lowell, Ohio", 740-629-7020, ridgelinedig@gmail.com).
   `verify_local.py` fails the build if any of that borrowed identity creeps back in.
   Worth telling the client: the buyer may now be operating in the same area under the old brand and number,
   which makes their own profile and reviews (question 1) more important, not less.
4. ~~Which phone number is live~~ — **resolved 2026-09-28: 740-629-7020.** No site change was needed — all
   26 pages, the `tel:` links and the JSON-LD already use it. The retired 740-761-4344 is the number printed
   on the SOLD site, so it is not ours to correct; if the client's own profile or citations show it, fix those.
5. **Confirm the client's own details before publishing any of them** (all of this came off the sold site and
   is currently kept at town level until confirmed):
   - a street address they actually want published (none is currently shown)
   - their own Facebook / Instagram page URLs (none are currently linked — `sameAs` is absent from the schema)
   - that the operational claims still hold for TJ's business: 75-mile radius, the county and town list,
     24/7 call or text, fully insured, 811 locates handled, cash/check/card/financing, photo-documented jobs
   - whether they want the "owner-operated by TJ Flowers" line kept on the homepage (currently there)
6. **Real project photos.** The portfolio block reads "Typical Projects We Take On" and uses stock imagery.
   Do NOT lift photos from the sold site — they belong to the buyer. Ask the client for their own.
7. **Bonuses not yet wired** (say the word): analytics tag; a branded `info@ridgelineexcavationohio.com`
   forwarding to the Gmail (domain MX is live at the registrar); a text/SMS quote option; a real service-area
   map to replace the placeholder.
8. **GitHub Actions deploys are live** — CI is green; deploys are `git push` to `main` on
   `rkweekley/ridgine-excavation` (see §Deployment mechanics).
