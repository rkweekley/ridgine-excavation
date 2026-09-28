import os
import time

import requests
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder="static")

# ---------------------------------------------------------------------------
# Mailgun relay config — secrets live in the container env (env file on the
# server), never in the browser or in this file.
# ---------------------------------------------------------------------------
MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY", "")
MAILGUN_DOMAIN = "mailgun.ridgelineexcavationohio.com"
MAILGUN_FROM = "Ridgeline Excavation <noreply@mailgun.ridgelineexcavationohio.com>"
# Relay destination for quote/contact form submissions (client's company inbox).
MAILGUN_TO = os.environ.get("MAILGUN_TO", "ridgelinedig@gmail.com")

# Simple in-memory rate limiter: 5 submissions per IP per 10 minutes.
RATE_LIMIT_MAX = 5
RATE_LIMIT_WINDOW = 600  # seconds
_submissions = {}  # ip -> [timestamps]


def _rate_limited(ip):
    now = time.time()
    stamps = [t for t in _submissions.get(ip, []) if now - t < RATE_LIMIT_WINDOW]
    if len(stamps) >= RATE_LIMIT_MAX:
        _submissions[ip] = stamps
        return True
    stamps.append(now)
    _submissions[ip] = stamps
    return False


# ---------------------------------------------------------------------------
# Static site
# ---------------------------------------------------------------------------
PAGES = [
    "service-areas",
    "faq",
    "site-prep",
    "land-clearing",
    "driveway-installation",
    "drainage",
    "trail-building",
    "tree-removal",
    "gravel-pads",
    "culverts-and-concrete",
    "trenching-and-utilities",
    "ponds",
    "atv-and-dirt-bike-tracks",
    "excavation-marietta-oh",
    "excavation-parkersburg-wv",
    "excavation-belpre-oh",
    "excavation-beverly-oh",
    "excavation-caldwell-oh",
    "excavation-athens-oh",
    "excavation-lowell-oh",
    "excavation-vienna-wv",
    "excavation-williamstown-wv",
    "excavation-cambridge-oh",
    "excavation-woodsfield-oh",
    "excavation-st-clairsville-oh",
]


def _html(filename, max_age=0):
    resp = send_from_directory("static", filename)
    resp.headers["Cache-Control"] = f"public, max-age={max_age}" if max_age else "no-cache"
    return resp


@app.route("/")
def index():
    return _html("index.html")


@app.route("/<slug>.html")
def inner_page(slug):
    if slug not in PAGES:
        return ("Not Found", 404)
    return _html(f"{slug}.html")


@app.route("/robots.txt")
def robots():
    return _html("robots.txt", max_age=3600)


@app.route("/sitemap.xml")
def sitemap():
    resp = _html("sitemap.xml", max_age=3600)
    resp.headers["Content-Type"] = "application/xml; charset=utf-8"
    return resp


@app.route("/favicon.ico")
def favicon():
    return send_from_directory("static/images", "logo-400.png", max_age=604800)


@app.route("/css/<path:path>")
def serve_css(path):
    return send_from_directory("static/css", path, max_age=604800)


@app.route("/js/<path:path>")
def serve_js(path):
    return send_from_directory("static/js", path, max_age=604800)


@app.route("/images/<path:path>")
def serve_images(path):
    return send_from_directory("static/images", path, max_age=2592000)


# ---------------------------------------------------------------------------
# Quote / contact form relay
# ---------------------------------------------------------------------------
@app.route("/api/contact", methods=["POST"])
def contact():
    data = request.get_json(silent=True) or {}

    # Honeypot: bots fill the hidden company_website field. Fake success, send nothing.
    if data.get("company_website"):
        return jsonify({"message": "Message sent! We'll get back to you soon."}), 200

    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    phone = (data.get("phone") or "").strip()
    service = (data.get("service") or "").strip()
    message = (data.get("message") or "").strip()

    if not name or len(name) > 200:
        return jsonify({"error": "Please provide your name."}), 400
    if not email or "@" not in email or len(email) > 200:
        return jsonify({"error": "Please provide a valid email address."}), 400
    if not message or len(message) > 5000:
        return jsonify({"error": "Please tell us about your project."}), 400

    if _rate_limited(request.remote_addr or "unknown"):
        return jsonify({"error": "Too many submissions. Call 740-629-7020 instead."}), 429

    subject = f"Quote request from {name}"
    body = (
        f"Name: {name}\n"
        f"Email: {email}\n"
        f"Phone: {phone or 'Not provided'}\n"
        f"Service needed: {service or 'Not specified'}\n\n"
        f"{message}\n\n"
        "-- Sent from ridgelineexcavationohio.com"
    )

    try:
        resp = requests.post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            data={
                "from": MAILGUN_FROM,
                "to": MAILGUN_TO,
                "h:Reply-To": email,
                "subject": subject,
                "text": body,
            },
            timeout=20,
        )
    except requests.RequestException as e:
        app.logger.error("Mailgun request failed: %s", e)
        return jsonify({"error": "Could not send right now. Call 740-629-7020."}), 502

    if resp.status_code != 200:
        app.logger.error("Mailgun rejected: %s", resp.text[:500])
        return jsonify({"error": "Could not send right now. Call 740-629-7020."}), 502

    return jsonify({"message": "Message sent! We'll get back to you soon."}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
