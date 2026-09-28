#!/usr/bin/env python3
"""Verify the deployed site over public HTTPS."""
import re
import sys
import urllib.request

SITE = "https://ridgelineexcavationohio.com"
PATHS = [
    "/", "/service-areas.html", "/faq.html", "/site-prep.html", "/land-clearing.html",
    "/driveway-installation.html", "/drainage.html", "/trail-building.html", "/tree-removal.html",
    "/gravel-pads.html", "/culverts-and-concrete.html", "/trenching-and-utilities.html",
    "/ponds.html", "/atv-and-dirt-bike-tracks.html",
    "/excavation-marietta-oh.html", "/excavation-parkersburg-wv.html", "/excavation-belpre-oh.html",
    "/excavation-beverly-oh.html", "/excavation-caldwell-oh.html", "/excavation-athens-oh.html",
    "/excavation-lowell-oh.html", "/excavation-vienna-wv.html", "/excavation-williamstown-wv.html",
    "/excavation-cambridge-oh.html", "/excavation-woodsfield-oh.html", "/excavation-st-clairsville-oh.html",
    "/sitemap.xml", "/robots.txt", "/css/styles.css", "/js/main.js", "/images/hero.jpg",
]
UA = "Mozilla/5.0 (compatible; site-verify/1.0)"
fails = []

for p in PATHS:
    url = SITE + p
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read().decode("utf-8", "ignore")
            code, size = r.status, len(body)
    except Exception as e:  # noqa: BLE001
        print(f"  {p:34s} ERROR {e}")
        fails.append(f"{p}: {e}")
        continue
    extra = ""
    if p.endswith(".html"):
        checks = {
            "canonical": f'rel="canonical" href="{SITE}/' in body,
            "gmail": "ridgelinedig@gmail.com" in body,
            "nodeadmail": "ridgine-excavation.com" not in body,
            "jsonld": 'application/ld+json' in body,
            "h1": len(re.findall(r"<h1", body)) == 1,
            "phone": "740-629-7020" in body,
        }
        bad = [k for k, v in checks.items() if not v]
        extra = "OK" if not bad else "FAIL:" + ",".join(bad)
        if bad:
            fails.append(f"{p}: {bad}")
    if code != 200:
        fails.append(f"{p}: http {code}")
    print(f"  {p:34s} {code} {size:7d}b {extra}")

print("\n=== sitemap content ===")
sm = urllib.request.urlopen(urllib.request.Request(SITE + "/sitemap.xml", headers={"User-Agent": UA}), timeout=30).read().decode()
locs = re.findall(r"<loc>(.*?)</loc>", sm)
print(f"  {len(locs)} urls")
for l in locs:
    print("   ", l)

print("\n=== deployed page titles ===")
for p in [x for x in PATHS if x.endswith(".html")]:
    body = urllib.request.urlopen(urllib.request.Request(SITE + p, headers={"User-Agent": UA}), timeout=30).read().decode()
    t = re.search(r"<title>(.*?)</title>", body, re.S).group(1)
    print(f"  {p:34s} {t}")

print("\n=== RESULT ===")
if fails:
    for f in fails:
        print("  FAIL:", f)
    sys.exit(1)
print("  DEPLOY VERIFIED")
