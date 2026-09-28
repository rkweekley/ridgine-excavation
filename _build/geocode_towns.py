#!/usr/bin/env python3
"""Geocode service-area towns via OSM Nominatim (1 req/sec, custom UA)."""
import json
import time
import urllib.parse
import urllib.request

UA = "RidgelineExcavationSiteBuild/1.0 (contact: ryan@cyberalsolutions.com)"
TOWNS = [
    ("Marietta", "OH"), ("Parkersburg", "WV"), ("Belpre", "OH"),
    ("Beverly", "OH"), ("Lowell", "OH"), ("Waterford", "OH"),
    ("New Matamoras", "OH"), ("Caldwell", "OH"), ("Woodsfield", "OH"),
    ("McConnelsville", "OH"), ("Athens", "OH"), ("Vienna", "WV"),
    ("Williamstown", "WV"), ("Sistersville", "WV"), ("St. Marys", "WV"),
]

out = {}
for name, state in TOWNS:
    q = urllib.parse.urlencode({"q": f"{name}, {state}, USA", "format": "json", "limit": 1})
    req = urllib.request.Request(f"https://nominatim.openstreetmap.org/search?{q}", headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            data = json.load(r)
        if data:
            d = data[0]
            out[f"{name}, {state}"] = {
                "lat": round(float(d["lat"]), 4),
                "lon": round(float(d["lon"]), 4),
                "county": d.get("display_name", "").split(", ")[2] if len(d.get("display_name", "").split(", ")) > 2 else "",
                "display": d.get("display_name", ""),
            }
        else:
            out[f"{name}, {state}"] = None
    except Exception as e:  # noqa: BLE001
        out[f"{name}, {state}"] = {"error": str(e)}
    time.sleep(1.1)

with open("/home/agent/workspace/ridgeline-ohio/_build/towns.json", "w") as f:
    json.dump(out, f, indent=2)
for k, v in out.items():
    print(k, "->", v if not v else (v.get("lat"), v.get("lon"), v.get("county")))
