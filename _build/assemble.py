#!/usr/bin/env python3
"""
Assemble full pages for ridgelineexcavationohio.com from body fragments.

Fragment source (in priority order):
  1. _build/bodies/<slug>.html   (authoritative raw fragment)
  2. static/<slug>.html          (first run: moved into _build/bodies/ if unassembled)

Output: static/<slug>.html (full HTML document), plus static/sitemap.xml, static/robots.txt
"""
import json
import re
import shutil
from datetime import date
from pathlib import Path

ROOT = Path("/home/agent/workspace/ridgeline-ohio")
STATIC = ROOT / "static"
BODIES = ROOT / "_build" / "bodies"
SITE = "https://ridgelineexcavationohio.com"
MARKER = "<!-- assembled:do-not-edit-fragment-below -->"

BIZ = {
    "@type": ["GeneralContractor", "HomeAndConstructionBusiness"],
    "@id": f"{SITE}/#business",
    "name": "Ridgeline Excavation LLC",
    "alternateName": "Ridgeline Excavation",
    "url": f"{SITE}/",
    "telephone": "+1-740-629-7020",
    "email": "ridgelinedig@gmail.com",
    "image": f"{SITE}/images/hero.jpg",
    "logo": f"{SITE}/images/logo-400.png",
    "description": (
        "Locally owned excavation and earthwork contractor serving the Mid-Ohio Valley: "
        "site preparation, land clearing, driveway installation, drainage, trail building, "
        "and tree removal in southeast Ohio and Wood, Tyler and Pleasants counties, West Virginia."
    ),
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "1495 Weppler Road",
        "addressLocality": "Lowell",
        "addressRegion": "OH",
        "postalCode": "45744",
        "addressCountry": "US",
    },
    "geo": {"@type": "GeoCoordinates", "latitude": 39.5646, "longitude": -81.5584},
    "foundingDate": "2025",
    "sameAs": [
        "https://www.facebook.com/profile.php?id=61583438379745",
        "https://www.instagram.com/rivervalleyexcavation/",
        "https://www.google.com/maps/place/River+Valley+Excavation/@39.5646497,-81.5583975,786m",
    ],
    "knowsAbout": [
        "site preparation", "land clearing", "excavation", "grading",
        "driveway installation", "driveway regrading", "gravel pads",
        "parking areas", "drainage", "French drains", "culverts",
        "concrete removal", "utility trenching", "water lines",
        "trail building", "tree removal", "stump removal", "brush clearing",
        "recreation ponds", "dirt bike tracks", "ATV trails", "site work",
    ],
    "hasOfferCatalog": {
        "@type": "OfferCatalog",
        "name": "Excavation and earthwork services",
        "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Site Preparation", "url": f"{SITE}/site-prep.html"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Land Clearing & Brush Removal", "url": f"{SITE}/land-clearing.html"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Tree, Stump & Lot Cleanup", "url": f"{SITE}/tree-removal.html"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Driveway Installation & Regrading", "url": f"{SITE}/driveway-installation.html"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Gravel Pads & Parking Areas", "url": f"{SITE}/gravel-pads.html"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Drainage: French Drains, Swales & Regrading", "url": f"{SITE}/drainage.html"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Utility Trenching", "url": f"{SITE}/trenching-and-utilities.html"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Culvert Installation & Concrete Removal", "url": f"{SITE}/culverts-and-concrete.html"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Trail Building & Clearing", "url": f"{SITE}/trail-building.html"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Recreation Pond Digging", "url": f"{SITE}/ponds.html"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Dirt Bike Tracks & ATV Trails", "url": f"{SITE}/atv-and-dirt-bike-tracks.html"}},
        ],
    },
}

AREA_SERVED = [
    {"@type": "City", "name": "Marietta", "address": {"@type": "PostalAddress", "addressLocality": "Marietta", "addressRegion": "OH", "addressCountry": "US"}},
    {"@type": "City", "name": "Lowell", "address": {"@type": "PostalAddress", "addressLocality": "Lowell", "addressRegion": "OH", "addressCountry": "US"}},
    {"@type": "City", "name": "Belpre", "address": {"@type": "PostalAddress", "addressLocality": "Belpre", "addressRegion": "OH", "addressCountry": "US"}},
    {"@type": "City", "name": "Beverly", "address": {"@type": "PostalAddress", "addressLocality": "Beverly", "addressRegion": "OH", "addressCountry": "US"}},
    {"@type": "City", "name": "Athens", "address": {"@type": "PostalAddress", "addressLocality": "Athens", "addressRegion": "OH", "addressCountry": "US"}},
    {"@type": "City", "name": "Nelsonville", "address": {"@type": "PostalAddress", "addressLocality": "Nelsonville", "addressRegion": "OH", "addressCountry": "US"}},
    {"@type": "City", "name": "Caldwell", "address": {"@type": "PostalAddress", "addressLocality": "Caldwell", "addressRegion": "OH", "addressCountry": "US"}},
    {"@type": "City", "name": "Woodsfield", "address": {"@type": "PostalAddress", "addressLocality": "Woodsfield", "addressRegion": "OH", "addressCountry": "US"}},
    {"@type": "City", "name": "McConnelsville", "address": {"@type": "PostalAddress", "addressLocality": "McConnelsville", "addressRegion": "OH", "addressCountry": "US"}},
    {"@type": "City", "name": "Cambridge", "address": {"@type": "PostalAddress", "addressLocality": "Cambridge", "addressRegion": "OH", "addressCountry": "US"}},
    {"@type": "City", "name": "New Concord", "address": {"@type": "PostalAddress", "addressLocality": "New Concord", "addressRegion": "OH", "addressCountry": "US"}},
    {"@type": "City", "name": "St. Clairsville", "address": {"@type": "PostalAddress", "addressLocality": "St. Clairsville", "addressRegion": "OH", "addressCountry": "US"}},
    {"@type": "City", "name": "Parkersburg", "address": {"@type": "PostalAddress", "addressLocality": "Parkersburg", "addressRegion": "WV", "addressCountry": "US"}},
    {"@type": "City", "name": "Vienna", "address": {"@type": "PostalAddress", "addressLocality": "Vienna", "addressRegion": "WV", "addressCountry": "US"}},
    {"@type": "City", "name": "Williamstown", "address": {"@type": "PostalAddress", "addressLocality": "Williamstown", "addressRegion": "WV", "addressCountry": "US"}},
    {"@type": "City", "name": "Mineral Wells", "address": {"@type": "PostalAddress", "addressLocality": "Mineral Wells", "addressRegion": "WV", "addressCountry": "US"}},
    {"@type": "AdministrativeArea", "name": "Washington County, Ohio"},
    {"@type": "AdministrativeArea", "name": "Athens County, Ohio"},
    {"@type": "AdministrativeArea", "name": "Guernsey County, Ohio"},
    {"@type": "AdministrativeArea", "name": "Noble County, Ohio"},
    {"@type": "AdministrativeArea", "name": "Monroe County, Ohio"},
    {"@type": "AdministrativeArea", "name": "Morgan County, Ohio"},
    {"@type": "AdministrativeArea", "name": "Belmont County, Ohio"},
    {"@type": "AdministrativeArea", "name": "Wood County, West Virginia"},
    {"@type": "AdministrativeArea", "name": "Tyler County, West Virginia"},
    {"@type": "AdministrativeArea", "name": "Pleasants County, West Virginia"},
]

# slug -> (breadcrumb label, title, meta description, schema kind, town/state or service name)
PAGES = [
    ("index", "Home",
     "Ridgeline Excavation | Site Prep & Land Clearing, OH & WV",
     "Excavation, site prep, land clearing, driveways and drainage across the Mid-Ohio Valley — Marietta, Parkersburg, Belpre and southeast Ohio. Free quotes: 740-629-7020.",
     "home", None),
    ("service-areas", "Service Areas",
     "Excavation Service Areas | Mid-Ohio Valley, OH & WV",
     "Ridgeline Excavation serves Marietta, Belpre, Beverly, Athens, Caldwell, Parkersburg, Vienna, Williamstown and the rest of the Mid-Ohio Valley. Call 740-629-7020.",
     "hub", None),
    ("faq", "FAQ",
     "Excavation FAQ | Access, Drainage & Permits | Ridgeline",
     "Answers on scheduling, site access, drainage, utilities and permits for excavation work in the Mid-Ohio Valley — what we do and what is your side of the project.",
     "faq", None),
    ("site-prep", "Site Preparation",
     "Site Preparation & Lot Grading | Mid-Ohio Valley",
     "Site prep for new homes and developments in southeast Ohio and WV — clearing, cut and fill, building pads and finish grading. Free quotes: 740-629-7020.",
     "service", "Site Preparation"),
    ("land-clearing", "Land Clearing",
     "Land Clearing & Brush Removal | SE Ohio & WV",
     "Lot clearing, brush and stump removal, acreage and fence-line clearing across the Mid-Ohio Valley — debris handled and hauled. Free quotes: 740-629-7020.",
     "service", "Land Clearing"),
    ("driveway-installation", "Driveways",
     "Driveway Installation & Grading | Ridgeline Excavation",
     "Gravel and asphalt driveway installation, grading, culvert installation and washout repair across the Mid-Ohio Valley. Free quotes: 740-629-7020.",
     "service", "Driveway Installation and Refurbishing"),
    ("drainage", "Drainage",
     "Drainage, French Drains & Culverts | Ridgeline",
     "Drainage work that fixes standing water, wet yards and washing driveways — French drains, swales, culverts and regrading. Mid-Ohio Valley. 740-629-7020.",
     "service", "Drainage"),
    ("trail-building", "Trails",
     "Trail Building & Clearing | Ridgeline Excavation",
     "Trail building and clearing on private land in southeast Ohio and WV — hiking, horse and ATV trails with grading, drainage and culvert crossings. Free quotes.",
     "service", "Trail Building and Clearing"),
    ("tree-removal", "Tree Removal",
     "Tree & Stump Removal, Lot Cleanup | Ridgeline",
     "Tree and hazard tree removal, stump removal, brush pile cleanup and lot cleanup across the Mid-Ohio Valley. Free quotes: 740-629-7020.",
     "service", "Tree Removal and Cleanup"),
    ("gravel-pads", "Gravel Pads",
     "Gravel Pads, Parking Areas & Equipment Pads | Ridgeline",
     "Gravel pad, parking area and equipment pad construction in the Mid-Ohio Valley — sub-base prep, stone, compaction and drainage away from the pad.",
     "service", "Gravel Pads and Parking Areas"),
    ("culverts-and-concrete", "Culverts & Concrete",
     "Culvert Installation & Concrete Removal | Ridgeline",
     "Culvert installation, cleanout and replacement plus concrete pad removal and haul-off across southeast Ohio and West Virginia. Free written estimates.",
     "service", "Culvert Installation and Concrete Removal"),
    ("trenching-and-utilities", "Trenching",
     "Utility Trenching & Water Line Digging | Ridgeline",
     "Utility trenching for water lines, power and drainage tile in the Mid-Ohio Valley — 811 locates handled before any dig. Call 740-629-7020.",
     "service", "Utility Trenching"),
    ("ponds", "Ponds",
     "Recreation Ponds & Farm Pond Digging | Ridgeline",
     "Recreation and farm pond digging in southeast Ohio — siting, clay sealing, bank shaping, spillways and cleanout of a silty pond. Free estimates.",
     "service", "Recreation Pond Digging"),
    ("atv-and-dirt-bike-tracks", "Tracks & Trails",
     "Dirt Bike Tracks & ATV Trail Systems | Ridgeline",
     "Backyard dirt bike practice tracks and ATV/UTV trail systems across the Mid-Ohio Valley — shaped to ride and built to drain. Free estimates.",
     "service", "Dirt Bike Tracks and ATV Trails"),
    ("excavation-marietta-oh", "Marietta, OH",
     "Excavation & Site Prep in Marietta, OH | Ridgeline",
     "Excavation, site prep and land clearing in Marietta, Ohio and Washington County — hillside and river-bottom lots, driveways and drainage. Call 740-629-7020.",
     "city", "Marietta"),
    ("excavation-parkersburg-wv", "Parkersburg, WV",
     "Excavation & Land Clearing in Parkersburg, WV",
     "Excavation, land clearing and site prep in Parkersburg, Vienna and Wood County, West Virginia — wet ground, hillside lots, driveways and drainage. 740-629-7020.",
     "city", "Parkersburg"),
    ("excavation-belpre-oh", "Belpre, OH",
     "Excavation & Land Clearing in Belpre, OH",
     "Excavation, site prep and land clearing in Belpre, Ohio along the Route 7 corridor — flood-plain ground, wooded ridge lots, driveways and drainage. 740-629-7020.",
     "city", "Belpre"),
    ("excavation-beverly-oh", "Beverly, OH",
     "Excavation & Land Clearing in Beverly, OH",
     "Excavation, land clearing and farm drainage in Beverly, Ohio and northwest Washington County — long gravel lanes, acreage clearing and ponds. Call 740-629-7020.",
     "city", "Beverly"),
    ("excavation-caldwell-oh", "Caldwell, OH",
     "Excavation & Land Clearing in Caldwell, OH",
     "Excavation, land clearing and field drainage in Caldwell, Ohio and Noble County — ponds, long gravel lanes, shale ground and building pads. Call 740-629-7020.",
     "city", "Caldwell"),
    ("excavation-athens-oh", "Athens, OH",
     "Excavation & Land Clearing in Athens, OH",
     "Excavation, land clearing and site prep in Athens, Ohio and Athens County — ridgetop building sites, steep slopes, switchback lanes and drainage. 740-629-7020.",
     "city", "Athens"),
    ("excavation-lowell-oh", "Lowell, OH",
     "Excavation & Land Clearing in Lowell, OH | Ridgeline",
     "Excavation, land clearing and gravel pads in Lowell, Ohio — our home base in northwest Washington County on the Muskingum River. Call 740-629-7020.",
     "city", "Lowell"),
    ("excavation-vienna-wv", "Vienna, WV",
     "Excavation & Land Clearing in Vienna, WV | Ridgeline",
     "Excavation, drainage and driveway work in Vienna, West Virginia and Wood County — tight in-town lots and outlying acreage. Call 740-629-7020.",
     "city", "Vienna"),
    ("excavation-williamstown-wv", "Williamstown, WV",
     "Excavation & Land Clearing in Williamstown, WV",
     "Excavation, land clearing and drainage in Williamstown, West Virginia — riverfront ground, steep wooded lots and acreage behind town. 740-629-7020.",
     "city", "Williamstown"),
    ("excavation-cambridge-oh", "Cambridge, OH",
     "Excavation & Land Clearing in Cambridge, OH",
     "Excavation, land clearing, driveways and culverts in Cambridge, Ohio and Guernsey County — clay and shale ground, farm lanes. Call 740-629-7020.",
     "city", "Cambridge"),
    ("excavation-woodsfield-oh", "Woodsfield, OH",
     "Excavation & Land Clearing in Woodsfield, OH",
     "Excavation, land clearing and ponds in Woodsfield, Ohio and Monroe County — long gravel lanes, pasture and steep hill ground. Call 740-629-7020.",
     "city", "Woodsfield"),
    ("excavation-st-clairsville-oh", "St. Clairsville, OH",
     "Excavation & Land Clearing in St. Clairsville, OH",
     "Excavation, site prep and drainage in St. Clairsville, Ohio and Belmont County — shale ground, hillside sites and commercial pads. 740-629-7020.",
     "city", "St. Clairsville"),
]

SERVICES = [
    ("site-prep", "Site Preparation"), ("land-clearing", "Land Clearing"),
    ("tree-removal", "Tree & Stump Removal"), ("driveway-installation", "Driveways"),
    ("gravel-pads", "Gravel Pads & Parking"), ("drainage", "Drainage"),
    ("trenching-and-utilities", "Utility Trenching"), ("culverts-and-concrete", "Culverts & Concrete"),
    ("trail-building", "Trails"), ("ponds", "Recreation Ponds"),
    ("atv-and-dirt-bike-tracks", "Tracks & ATV Trails"),
]
CITIES = [
    ("excavation-marietta-oh", "Marietta, OH"), ("excavation-lowell-oh", "Lowell, OH"),
    ("excavation-belpre-oh", "Belpre, OH"), ("excavation-beverly-oh", "Beverly, OH"),
    ("excavation-athens-oh", "Athens, OH"), ("excavation-caldwell-oh", "Caldwell, OH"),
    ("excavation-woodsfield-oh", "Woodsfield, OH"), ("excavation-cambridge-oh", "Cambridge, OH"),
    ("excavation-st-clairsville-oh", "St. Clairsville, OH"), ("excavation-parkersburg-wv", "Parkersburg, WV"),
    ("excavation-vienna-wv", "Vienna, WV"), ("excavation-williamstown-wv", "Williamstown, WV"),
]

NAV = """<header class="site-header" id="top">
  <nav class="nav container" aria-label="Main navigation">
    <a class="brand" href="/">
      <img class="brand-logo" src="/images/logo-nav.png" alt="Ridgeline Excavation LLC logo" width="44" height="44">
      <span class="brand-text">Ridgeline<strong>Excavation</strong></span>
    </a>
    <button class="nav-toggle" id="navToggle" aria-label="Open menu" aria-expanded="false">
      <span class="bar"></span><span class="bar"></span><span class="bar"></span>
    </button>
    <ul class="nav-links" id="navLinks">
      <li><a href="/#services">Services</a></li>
      <li><a href="/service-areas.html">Service Areas</a></li>
      <li><a href="/faq.html">FAQ</a></li>
      <li><a href="/#projects">Projects</a></li>
      <li><a href="/#contact" class="btn btn-primary btn-sm">Get a Quote</a></li>
    </ul>
  </nav>
</header>
"""


def footer():
    svc = "\n".join(f'        <li><a href="/{s}.html">{n}</a></li>' for s, n in SERVICES)
    cty = "\n".join(f'        <li><a href="/{s}.html">{n}</a></li>' for s, n in CITIES)
    return f"""<footer class="footer">
  <div class="container footer-grid">
    <div class="footer-brand">
      <div class="footer-logo-row">
        <img class="footer-logo" src="/images/logo-nav.png" alt="Ridgeline Excavation LLC logo" width="44" height="44">
        <p class="footer-title">Ridgeline Excavation&nbsp;LLC</p>
      </div>
      <p>Owner-operated excavation, site work, land clearing, drainage and driveways out of Lowell, Ohio — serving a 75-mile radius of the Mid-Ohio Valley across southeast Ohio and Wood County, West Virginia.</p>
    </div>
    <div class="footer-links">
      <p class="footer-head">Services</p>
      <ul>
{svc}
      </ul>
    </div>
    <div class="footer-links">
      <p class="footer-head">Service Areas</p>
      <ul>
{cty}
        <li><a href="/service-areas.html">All service areas</a></li>
      </ul>
    </div>
    <div class="footer-contact">
      <p class="footer-head">Contact</p>
      <ul>
        <li><a href="tel:7406297020">740-629-7020</a> — call or text 24/7</li>
        <li><a href="mailto:ridgelinedig@gmail.com">ridgelinedig@gmail.com</a></li>
        <li>1495 Weppler Road, Lowell, OH 45744</li>
        <li>Serving a 75-mile radius of the Mid-Ohio Valley, OH &amp; WV</li>
        <li><a href="/faq.html">FAQ</a> · <a href="/service-areas.html">Service areas</a></li>
        <li class="footer-social">
          <a href="https://www.facebook.com/profile.php?id=61583438379745" rel="me noopener" target="_blank">Facebook</a> ·
          <a href="https://www.instagram.com/rivervalleyexcavation/" rel="me noopener" target="_blank">Instagram</a> ·
          <a href="https://www.google.com/maps/place/River+Valley+Excavation/@39.5646497,-81.5583975,786m" rel="me noopener" target="_blank">Google</a>
        </li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom container">
    <p>© <span id="year">2026</span> Ridgeline Excavation LLC. All rights reserved.</p>
  </div>
</footer>
"""


def jsonld_scripts(kind, slug, service_name, fragment_html):
    out = []
    if kind == "home":
        biz = dict(BIZ)
        biz["areaServed"] = AREA_SERVED
        out.append({"@context": "https://schema.org", **biz})
        out.append({
            "@context": "https://schema.org",
            "@type": "WebSite",
            "url": f"{SITE}/",
            "name": "Ridgeline Excavation LLC",
            "publisher": {"@id": f"{SITE}/#business"},
        })
    elif kind == "faq":
        qa = re.findall(r'<div class="faq-item">\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>\s*</div>', fragment_html, re.S)
        strip = lambda s: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()
        out.append({
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}}
                for q, a in qa
            ],
        })
    else:
        svc = {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": service_name,
            "serviceType": service_name,
            "url": f"{SITE}/{slug}.html",
            "provider": {"@id": f"{SITE}/#business", "name": "Ridgeline Excavation LLC", "telephone": "+1-740-629-7020", "url": f"{SITE}/"},
            "areaServed": AREA_SERVED,
        }
        if kind == "city":
            svc["availableChannel"] = {"@type": "ServiceChannel", "serviceUrl": f"{SITE}/#contact", "servicePhone": "+1-740-629-7020"}
        out.append(svc)
    label = next(p[1] for p in PAGES if p[0] == slug)
    out.append({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": (
            [{"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
             {"@type": "ListItem", "position": 2, "name": label, "item": f"{SITE}/{slug}.html"}]
            if slug != "index" else
            [{"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"}]
        ),
    })
    return "\n".join(
        '<script type="application/ld+json">\n' + json.dumps(s, indent=2, ensure_ascii=False) + "\n</script>"
        for s in out
    )


def head(slug, title, desc):
    url = f"{SITE}/" if slug == "index" else f"{SITE}/{slug}.html"
    return f"""<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="geo.region" content="US-OH">
<meta name="geo.placename" content="Marietta, Ohio">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Ridgeline Excavation LLC">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/images/hero.jpg">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE}/images/hero.jpg">
<meta name="theme-color" content="#050505">
<link rel="icon" href="/images/logo-400.png">
<link rel="apple-touch-icon" href="/images/logo-400.png">
<link rel="stylesheet" href="/css/styles.css?v=4">"""


def get_fragment(slug):
    frag = BODIES / f"{slug}.html"
    if frag.exists():
        return frag.read_text()
    live = STATIC / f"{slug}.html"
    if not live.exists():
        raise SystemExit(f"missing fragment for {slug}")
    text = live.read_text()
    if MARKER in text:
        raise SystemExit(f"{slug}: assembled page found but no fragment in _build/bodies")
    BODIES.mkdir(parents=True, exist_ok=True)
    shutil.copy(live, frag)
    return frag.read_text()


def main():
    today = date.today().isoformat()
    index_frag = None
    urls = []
    for slug, label, title, desc, kind, service_name in PAGES:
        frag = get_fragment(slug)
        page = f"""<!DOCTYPE html>
<html lang="en">
<head>
{head(slug, title, desc)}
{jsonld_scripts(kind, slug, service_name, frag)}
</head>
<body>
{NAV}
<main>
{frag.strip()}
</main>
{footer()}
<script src="/js/main.js"></script>
</body>
</html>
"""
        (STATIC / f"{slug}.html").write_text(page)
        urls.append((f"{SITE}/" if slug == "index" else f"{SITE}/{slug}.html", today))
        h1 = len(re.findall(r"<h1", frag))
        print(f"  wrote {slug}.html  h1={h1}  words≈{len(re.sub(r'<[^>]+>', ' ', frag).split())}")

    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, lastmod in urls:
        sm.append("  <url>")
        sm.append(f"    <loc>{u}</loc>")
        sm.append(f"    <lastmod>{lastmod}</lastmod>")
        sm.append("  </url>")
    sm.append("</urlset>")
    (STATIC / "sitemap.xml").write_text("\n".join(sm) + "\n")
    (STATIC / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\n"
        f"Sitemap: {SITE}/sitemap.xml\n"
    )
    print(f"  wrote sitemap.xml ({len(urls)} urls) and robots.txt")


if __name__ == "__main__":
    main()
