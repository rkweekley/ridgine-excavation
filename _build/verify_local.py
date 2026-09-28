#!/usr/bin/env python3
"""Local verification of the assembled site (disk-based, no Flask needed).

Simulates the Flask route table: '/' -> static/index.html, '/<slug>.html' -> static/<slug>.html,
'/css|js|images/<path>' -> static/<path>, plus /robots.txt, /sitemap.xml, /favicon.ico.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path("/home/agent/workspace/ridgeline-ohio")
STATIC = ROOT / "static"
SITE = "https://ridgelineexcavationohio.com"

PAGES = [
    "service-areas", "faq", "site-prep", "land-clearing", "driveway-installation",
    "drainage", "trail-building", "tree-removal", "excavation-marietta-oh",
    "excavation-parkersburg-wv", "excavation-belpre-oh", "excavation-beverly-oh",
    "excavation-caldwell-oh", "excavation-athens-oh",
    "gravel-pads",
    "culverts-and-concrete",
    "trenching-and-utilities",
    "ponds",
    "atv-and-dirt-bike-tracks",
    "excavation-lowell-oh",
    "excavation-vienna-wv",
    "excavation-williamstown-wv",
    "excavation-cambridge-oh",
    "excavation-woodsfield-oh",
    "excavation-st-clairsville-oh",
]
ALL = ["index"] + PAGES
fails = []


def resolve(path):
    """Map a URL path to a file on disk, mirroring app.py's routes."""
    p = path.split("?")[0]
    if p == "/":
        return STATIC / "index.html"
    if p == "/robots.txt":
        return STATIC / "robots.txt"
    if p == "/sitemap.xml":
        return STATIC / "sitemap.xml"
    if p == "/favicon.ico":
        return STATIC / "images" / "logo-400.png"
    if p.startswith("/css/") or p.startswith("/js/") or p.startswith("/images/"):
        return STATIC / p.lstrip("/")
    m = re.fullmatch(r"/([a-z0-9-]+)\.html", p)
    if m and m.group(1) in PAGES:
        return STATIC / f"{m.group(1)}.html"
    return None


# route table must match the files on disk exactly
on_disk = {f.stem for f in STATIC.glob("*.html")}
expected = set(ALL)
if on_disk != expected:
    fails.append(f"route/file mismatch: on_disk-only={on_disk - expected} table-only={expected - on_disk}")
print("route table vs files:", "OK" if on_disk == expected else "MISMATCH")

print("=== pages ===")
html_by_slug = {}
for slug in ALL:
    f = STATIC / f"{slug}.html"
    html = f.read_text()
    html_by_slug[slug] = html
    checks = {
        "doctype": html.startswith("<!DOCTYPE html>"),
        "canonical": f'rel="canonical" href="{SITE}/' in html,
        "og_title": 'property="og:title"' in html,
        "h1=1": len(re.findall(r"<h1", html)) == 1,
        "phone": "740-629-7020" in html,
        "gmail": "ridgelinedig@gmail.com" in html,
        "no_dead_email": "ridgine-excavation.com" not in html,
        "no_typo_brand": not re.search(r"Ridgane|Ridgine|Ridgline", html),
        "no_wy_domain": "ridgelineexcavation.com" not in html.replace("ridgelineexcavationohio.com", ""),
        "no_false_experience": not re.search(r"15\+ ?years|300\+ ?projects|est\.? ?20\d\d|decades of", html, re.I),
        "no_ryan": not re.search(r"\bRyan\b", html),
        "address": "1495 Weppler Road" in html[html.find("<footer"):],
        "jsonld": html.count("application/ld+json") >= 1,
        "nav": 'class="nav links"' in html or 'id="navLinks"' in html,
        "footer_nap": "740-629-7020" in html[html.find("<footer"):] if "<footer" in html else False,
        "one_main": html.count("<main>") == 1,
    }
    bad = [k for k, v in checks.items() if not v]
    title = re.search(r"<title>(.*?)</title>", html, re.S).group(1)
    desc = re.search(r'name="description" content="(.*?)"', html, re.S).group(1)
    tlen, dlen = len(title), len(desc)
    warn = []
    if tlen > 62:
        warn.append(f"title {tlen}c")
    if not (120 <= dlen <= 165):
        warn.append(f"desc {dlen}c")
    print(f"  {slug:28s} {'OK ' if not bad else 'FAIL ' + ','.join(bad)} | title {tlen}c desc {dlen}c {'; '.join(warn)}")
    if bad:
        fails.append(f"{slug}: {bad}")

print("=== JSON-LD ===")
for slug, html in html_by_slug.items():
    for i, block in enumerate(re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)):
        try:
            obj = json.loads(block)
            types = obj.get("@type")
            n = len(obj.get("mainEntity", []) or [])
            print(f"  {slug:28s} #{i} @type={types}" + (f" questions={n}" if n else ""))
        except Exception as e:  # noqa: BLE001
            print(f"  {slug:28s} #{i} PARSE ERROR: {e}")
            fails.append(f"{slug}: jsonld parse error")

print("=== internal links ===")
targets = set()
for slug, html in html_by_slug.items():
    for href in set(re.findall(r'href="(/[^"]*)"', html)):
        targets.add(href)
for t in sorted(targets):
    path = t.split("#")[0] or "/"
    f = resolve(path)
    ok = f is not None and f.exists()
    print(f"  {t:44s} {'OK' if ok else 'MISSING'}")
    if not ok:
        fails.append(f"dead link {t}")

print("=== assets ===")
for asset in ["/css/styles.css", "/js/main.js", "/images/hero.jpg", "/images/logo-nav.png",
              "/images/logo-hero.png", "/images/logo-400.png", "/images/projects/site-prep.jpg",
              "/images/projects/commercial.jpg", "/images/projects/drainage.jpg",
              "/images/projects/trail.jpg", "/robots.txt", "/sitemap.xml", "/favicon.ico"]:
    f = resolve(asset)
    ok = f is not None and f.exists() and f.stat().st_size > 20
    print(f"  {asset:44s} {'OK ' + str(f.stat().st_size) + 'b' if ok else 'MISSING'}")
    if not ok:
        fails.append(f"asset {asset}")

sm = (STATIC / "sitemap.xml").read_text()
locs = re.findall(r"<loc>(.*?)</loc>", sm)
exp = {f"{SITE}/" if s == "index" else f"{SITE}/{s}.html" for s in ALL}
print(f"=== sitemap: {len(locs)} urls; missing={exp - set(locs) or 'none'}; extra={set(locs) - exp or 'none'}")
if exp != set(locs):
    fails.append("sitemap mismatch")

print("\n=== RESULT ===")
if fails:
    for f in fails:
        print("  FAIL:", f)
    sys.exit(1)
print("  ALL CHECKS PASSED")
