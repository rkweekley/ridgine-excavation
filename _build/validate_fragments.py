#!/usr/bin/env python3
"""Validate the page fragments against the build spec before assembly."""
import re
import sys
from pathlib import Path

ROOT = Path("/home/agent/workspace/ridgeline-ohio")
BODIES = ROOT / "_build" / "bodies"

SLUGS = [
    "index", "service-areas", "faq", "site-prep", "land-clearing",
    "driveway-installation", "drainage", "trail-building", "tree-removal",
    "excavation-marietta-oh", "excavation-parkersburg-wv", "excavation-belpre-oh",
    "excavation-beverly-oh", "excavation-caldwell-oh", "excavation-athens-oh",
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
VALID_LINKS = {f"/{s}.html" for s in SLUGS if s != "index"} | {"/", "/#contact", "/#services", "/#projects", "/#testimonials", "/#areas"}

BANNED = [
    (r"\b2003\b", "founding year of the unrelated Wyoming company"),
    (r"\best\.\s*\d{4}\b", "founding year"),
    (r"\$\s?\d", "price"),
    (r"\bper (hour|square foot|yard|acre)\b", "rate"),
    (r"agg?regateRating", "rating schema"),
    (r"★", "star rating"),
    (r"\b\d+(\.\d+)?\s*(out of|/)\s*5\b", "rating claim"),
    (r"info@(?!ridgelinedig)", "wrong email"),
    (r"ridgine|ridgline|ridgane|ridgeline-excavation", "typo/stale brand or domain"),
    (r"ridgelineexcavation\.com", "the Wyoming company's domain"),
    (r"\b\d{2,5}\s+[A-Z][a-z]+ (St|Street|Ave|Avenue|Rd|Road|Ln|Lane|Dr|Drive|Pike|Hwy)\b", "street address"),
    (r"\bheadquarters\b", "claims an HQ"),
    (r"family[- ]owned since", "unverified history"),
    (r"\bRyan\b", "stale owner name (current owner is TJ Flowers)"),
    (r"15\+ ?years|300\+ ?projects|decades of experience", "false experience claim (founded 2025)"),
    (r"testimonial|What Our Clients Say|t-author", "testimonial block"),
    (r"she said|said one customer", "quoted customer"),
]

problems = []
warnings = []
sentences = {}
for slug in SLUGS:
    f = BODIES / f"{slug}.html"
    if not f.exists():
        f = ROOT / "static" / f"{slug}.html"
    if not f.exists():
        problems.append(f"{slug}: MISSING fragment")
        continue
    h = f.read_text()
    text = re.sub(r"<[^>]+>", " ", h)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"\s+", " ", text)
    words = len(text.split())

    h1 = len(re.findall(r"<h1", h))
    if h1 != 1:
        problems.append(f"{slug}: {h1} h1 tags")
    if slug != "index":
        for cls in (["page-hero", "breadcrumb", "faq-block", "cta-band", "faq-item"] if slug == "faq"
                    else ["page-hero", "breadcrumb", "prose", "cta-band", "faq-item"]):
            if cls not in h:
                problems.append(f"{slug}: missing .{cls}")
    # service/town pages 350-800; hub pages (index, faq, service-areas) run longer by design
    lo, hi = (500, 1100) if slug in ("index", "faq", "service-areas") else (350, 900)
    if not (lo <= words <= hi):
        problems.append(f"{slug}: word count {words} outside {lo}-{hi}")
    for pat, why in BANNED:
        for m in re.finditer(pat, text, re.I):
            msg = f"{slug}: banned [{why}] -> ...{text[max(0, m.start()-60):m.end()+60]}..."
            problems.append(msg)
    # internal links
    for href in re.findall(r'href="(/[^"]*)"', h):
        if href.lstrip() not in VALID_LINKS:
            problems.append(f"{slug}: link target not in build -> {href}")
    # duplicate sentence detection across pages
    for s in re.split(r"(?<=[.!?])\s+", text):
        s = s.strip()
        if len(s.split()) >= 12:
            sentences.setdefault(s.lower(), []).append(slug)
    print(f"{slug:28s} words={words:4d} h1={h1} links={len(re.findall(r'href=\"/', h))}")

SHARED_FURNITURE = "call 740-629-7020 or send us your project details — we reply within one business day."
SHARED = ("see our full service areas or check our frequently asked questions",
          "call or text 740-629-7020")
dupes = {s: v for s, v in sentences.items() if not any(k in s for k in SHARED)
         if len(set(v)) > 1 and not s.startswith("call 740-629-7020 or send us your project details")}
for s, v in list(dupes.items())[:15]:
    problems.append(f"duplicate sentence across {sorted(set(v))}: {s[:90]}")

print("\n=== WARNINGS ===")
for w in warnings:
    print(" !", w)

print("\n=== PROBLEMS ===")
if problems:
    for p in problems:
        print(" -", p)
    sys.exit(1)
print("none")
