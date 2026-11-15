#!/usr/bin/env python3
"""Build the AACM site.

Each page's main content lives in src/pages/<name>.html. The first line is a
meta comment:   <!--meta {"title": "...", "description": "...", "nav": "about"} -->
This script wraps every page in the shared head, header and footer and writes
<name>.html at the repo root, ready to upload to any static host.

Placeholders you can use inside a page:
  <!--court:KEY-->   a portrait grid from src/data/leadership.json[KEY]

Run:  python3 build.py
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
PAGES = ROOT / "src" / "pages"
VERSION = "41"  # bump when CSS/JS change so browsers fetch the new files

PHONE_DISPLAY = "(224) 334-6661"
PHONE_TEL = "+12243346661"
EMAIL = "info@chicagoasanteman.org"
ADDRESS = "11070 S Western Ave, Chicago, IL 60643"
MAP_URL = "https://maps.app.goo.gl/mmgueGGtTuZAeEiD7"

LOGO = '<img src="assets/img/logo.png" alt="" width="36" height="44">'

# (key, label, href) or (group-key, label, [(key, label, href), ...])
NAV = [
    ("home", "Home", "index.html"),
    ("about", "About", [
        ("about", "About AACM", "about.html"),
        ("history", "Our History", "history.html"),
        ("asantes", "The Asantes", "the-asantes.html"),
        ("otumfuo", "Otumfuo Osei Tutu II", "otumfuo-osei-tutu-ii.html"),
    ]),
    ("leadership", "Leadership", [
        ("executive", "Executive Team", "executive-team.html"),
        ("elders", "Council of Elders", "council-of-elders.html"),
        ("royalty", "Enstooled Royalty (Ghana)", "enstooled-royalty.html"),
        ("former", "Past Asantefoɔ Executives", "former-executives.html"),
    ]),
    ("projects", "Programs", "projects.html"),
    ("inauguration", "Events", "inauguration.html"),
    ("media", "Gallery", "media.html"),
    ("contact", "Contact", "contact.html"),
]


def nav_html(active):
    out = []
    for key, label, target in NAV:
        if isinstance(target, list):
            in_group = any(k == active for k, _, _ in target)
            cur_attr = ' aria-current="page"'
            items = "\n".join(
                f'          <a href="{h}"{cur_attr if k == active else ""}>{l}</a>'
                for k, l, h in target)
            cls = ' class="is-active"' if in_group else ""
            out.append(f'      <div class="nav-group">\n        <button type="button"{cls}>{label}</button>\n'
                       f'        <div class="nav-menu">\n{items}\n        </div>\n      </div>')
        else:
            cur = ' aria-current="page"' if key == active else ""
            out.append(f'      <a href="{target}"{cur}>{label}</a>')
    out.append('      <a class="btn btn--gold" href="membership.html">Join Today</a>')
    return "\n".join(out)


# Licensed Canela: drop the web font files in assets/fonts/ (e.g. Canela-Regular.woff2,
# Canela-RegularItalic.woff2, Canela-Light.woff2) and the site switches to Canela on the
# next build. Until then headings fall back to Bodoni Moda.
CANELA_WEIGHTS = {"thin": 100, "light": 300, "regular": 400, "medium": 500, "bold": 700, "black": 900}


def canela_css():
    rules = []
    for f in sorted((ROOT / "assets/fonts").glob("Canela-*.woff2")):
        style = f.stem.split("-", 1)[1].lower()
        italic = style.endswith("italic")
        weight = CANELA_WEIGHTS.get(style.replace("italic", "") or "regular", 400)
        rules.append('@font-face { font-family: "Canela"; src: url("assets/fonts/%s") format("woff2"); font-weight: %d; font-style: %s; font-display: swap; }'
                     % (f.name, weight, "italic" if italic else "normal"))
    return ("  <style>" + " ".join(rules) + "</style>\n") if rules else ""


def head(meta):
    title = meta["title"] if meta.get("bare_title") else f'{meta["title"]} · Asanteman Chicago & Midwest'
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(meta.get('description', ''))}">
  <link rel="icon" href="assets/img/favicon.png" type="image/png">
  <link rel="manifest" href="manifest.webmanifest">
  <meta name="theme-color" content="#15100b">
  <link rel="apple-touch-icon" href="assets/img/icons/apple-touch-icon.png">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-title" content="Asanteman">
  <meta name="apple-mobile-web-app-status-bar-style" content="black">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400..600;1,6..96,400..600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
{canela_css()}  <link rel="stylesheet" href="assets/css/site.css?v={VERSION}">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="Asanteman Association of Chicago &amp; Midwest, home">
      {LOGO}
      <span><span class="brand-name">Asanteman</span><span class="brand-sub">Chicago &amp; Midwest</span></span>
    </a>
    <button class="nav-toggle" aria-label="Menu" aria-expanded="false" aria-controls="nav"><span></span></button>
    <nav class="nav" id="nav" aria-label="Main">
{nav_html(meta.get('nav'))}
    </nav>
  </div>
</header>

<main id="main">
"""


def foot():
    return f"""</main>

<footer class="site-footer">
  <div class="kente kente--thin" role="presentation"></div>
  <div class="wrap">
    <div>
      <a class="brand" href="index.html">
        {LOGO}
        <span><span class="brand-name">Asanteman</span><span class="brand-sub">Chicago &amp; Midwest</span></span>
      </a>
      <p class="motto">One People, One Heritage, One Mission.</p>
      <p>A tax-exempt 501(c)(3) non-profit organization.</p>
    </div>
    <div>
      <h4>Association</h4>
      <ul>
        <li><a href="about.html">About Us</a></li>
        <li><a href="membership.html">Membership</a></li>
        <li><a href="executive-team.html">Leadership</a></li>
        <li><a href="inauguration.html">Events</a></li>
        <li><a href="volunteer.html">Get Involved</a></li>
      </ul>
    </div>
    <div>
      <h4>Heritage</h4>
      <ul>
        <li><a href="history.html">Our History</a></li>
        <li><a href="the-asantes.html">The Asantes</a></li>
        <li><a href="otumfuo-osei-tutu-ii.html">Otumfuo Osei Tutu II</a></li>
        <li><a href="projects.html">Programs</a></li>
        <li><a href="media.html">Gallery</a></li>
      </ul>
    </div>
    <div>
      <h4>Visit &amp; Contact</h4>
      <ul>
        <li><a href="{MAP_URL}">11070 S Western Ave<br>Chicago, IL 60643</a></li>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li>
      </ul>
    </div>
  </div>
  <div class="legal">
    <div class="wrap">
      <span>© <span data-year>2026</span> Asanteman Association of Chicago &amp; Midwest. All rights reserved.</span>
      <span>Tax-exempt 501(c)(3)</span>
    </div>
  </div>
</footer>

<script src="assets/js/site.js?v={VERSION}"></script>
</body>
</html>
"""


LEADERSHIP = json.loads((ROOT / "src/data/leadership.json").read_text())


def photo_width(name):
    try:
        from PIL import Image
        with Image.open(ROOT / "assets/img/people" / name) as im:
            return im.size[0]
    except Exception:
        return 0


def court(key):
    cards = []
    for i, p in enumerate(LEADERSHIP[key]):
        name, title = html.escape(p["name"]), html.escape(p["title"])
        # the lead portrait is shown large only when the photo is sharp enough for it
        cls = "seat seat--hero" if i == 0 and key != "exec-stool" and photo_width(p["photo"]) >= 600 else "seat"
        cards.append(f"""        <div class="{cls}">
          <div class="seat-frame"><img src="assets/img/people/{p['photo']}" alt="{name}" loading="lazy" width="315" height="350"></div>
          <div class="stool-title">{title}</div>
          <h3>{name}</h3>
        </div>""")
    extra = " court--feature" if key == "exec-stool" else ""
    return f'<div class="court{extra} reveal">\n' + "\n".join(cards) + "\n      </div>"


DIVISIONS = [
    # key, display name, short role, one-line blurb, chief title match, queen-mother title match
    ("akwamu", "Akwamu", "The vanguard", "The division that goes first.", "akwamuhene", "akwamuhemaa"),
    ("adonten", "Adonten", "The main body", "The centre of the formation.", "adontenhene", "adontenhemaa"),
    ("nifa", "Nifa", "The right wing", "The right hand of the stool.", "nifahene", "nifahemaa"),
    ("benkum", "Benkum", "The left wing", "The left hand of the stool.", "benkumhene", "benkumhemaa"),
    ("kyidom", "Kyidom", "The rear guard", "The division that follows and protects.", "kyidomhene", "kyidomhemaa"),
    ("gyaase", "Gyaase", "The household", "The people closest to the stool.", "gyaasehene", "gyaasehemaa"),
]


def court_data():
    people = [p for k in ("exec-chiefs", "exec-queens", "exec-officers") for p in LEADERSHIP[k]]
    out = []
    for key, name, role, blurb, chief, queen in DIVISIONS:
        holders = []
        for sub in (chief, queen):
            if not sub:
                continue
            for p in people:
                if sub in p["title"].lower().replace(" ", ""):
                    holders.append({"name": p["name"], "title": p["title"], "photo": "assets/img/people/" + p["photo"]})
        if not holders:
            raise SystemExit("court_data: no holder found for " + name)
        out.append({"key": key, "name": name, "role": role, "blurb": blurb, "people": holders})
    return out


# ---------- Progressive web app: manifest + service worker ----------
MANIFEST = {
    "name": "Asanteman Association of Chicago & Midwest",
    "short_name": "Asanteman",
    "description": "Asante culture, leadership and community in Chicago and the Midwest.",
    "start_url": "./index.html?source=pwa",
    "scope": "./",
    "id": "./",
    "display": "standalone",
    "orientation": "portrait-primary",
    "background_color": "#15100b",
    "theme_color": "#15100b",
    "categories": ["lifestyle", "social", "education"],
    "icons": [
        {"src": "assets/img/icons/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
        {"src": "assets/img/icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
        {"src": "assets/img/icons/maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
    ],
    "shortcuts": [
        {"name": "Leadership", "url": "./executive-team.html", "icons": [{"src": "assets/img/icons/icon-192.png", "sizes": "192x192"}]},
        {"name": "Gallery", "url": "./media.html", "icons": [{"src": "assets/img/icons/icon-192.png", "sizes": "192x192"}]},
        {"name": "Join", "url": "./membership.html", "icons": [{"src": "assets/img/icons/icon-192.png", "sizes": "192x192"}]},
    ],
}

SW_TEMPLATE = r"""// Generated by build.py. Do not edit by hand.
const VERSION = '__VERSION__';
const CORE = 'aacm-core-' + VERSION;
const RUNTIME = 'aacm-runtime-v1';
const PRECACHE = __PRECACHE__;
const RUNTIME_LIMIT = 120;

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CORE).then((c) => c.addAll(PRECACHE)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k.startsWith('aacm-core-') && k !== CORE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

const trim = async (name, max) => {
  const c = await caches.open(name);
  const keys = await c.keys();
  for (let i = 0; i < keys.length - max; i++) await c.delete(keys[i]);
};

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);

  // Pages: network first so content stays fresh; saved copy or the offline page when there is no signal
  if (req.mode === 'navigate') {
    e.respondWith(
      fetch(req).then((res) => {
        const copy = res.clone();
        caches.open(RUNTIME).then((c) => c.put(req, copy)).then(() => trim(RUNTIME, RUNTIME_LIMIT));
        return res;
      }).catch(async () => (await caches.match(req, { ignoreSearch: true })) || caches.match('offline.html'))
    );
    return;
  }

  // Own files and Google Fonts: cache first, fill the cache as things are used
  const own = url.origin === self.location.origin;
  const fonts = url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com';
  if (!own && !fonts) return;
  e.respondWith(
    caches.match(req).then((hit) => hit || fetch(req).then((res) => {
      if (res.ok || res.type === 'opaque') {
        const copy = res.clone();
        caches.open(RUNTIME).then((c) => c.put(req, copy)).then(() => trim(RUNTIME, RUNTIME_LIMIT));
      }
      return res;
    }))
  );
});
"""


def write_pwa(pages):
    (ROOT / "manifest.webmanifest").write_text(json.dumps(MANIFEST, indent=2, ensure_ascii=False) + "\n")
    precache = ["./"] + pages + [
        "assets/css/site.css?v=" + VERSION, "assets/js/site.js?v=" + VERSION,
        "assets/img/logo.png", "assets/img/favicon.png", "assets/img/crest-mark.png", "assets/img/pattern-adinkra.png",
        "assets/img/icons/icon-192.png", "assets/img/icons/apple-touch-icon.png",
    ]
    sw = SW_TEMPLATE.replace("__VERSION__", VERSION).replace("__PRECACHE__", json.dumps(precache, indent=2))
    (ROOT / "sw.js").write_text(sw)


def build():
    built = []
    for src in sorted(PAGES.glob("*.html")):
        text = src.read_text()
        m = re.match(r"<!--meta (\{.*?\}) -->\n", text)
        if not m:
            raise SystemExit(f"{src.name}: first line must be a <!--meta {{...}} --> comment")
        meta = json.loads(m.group(1))
        body = text[m.end():]
        body = re.sub(r"<!--court:([\w-]+)-->", lambda mm: court(mm.group(1)), body)
        body = body.replace("<!--courtdata-->", '<script type="application/json" id="court-data">' + json.dumps(court_data(), ensure_ascii=False).replace("</", "<\\/") + "</script>")
        (ROOT / src.name).write_text(head(meta) + "\n" + body.rstrip() + "\n\n" + foot())
        built.append(src.name)
    write_pwa(built)
    print(f"Built {len(built)} pages: {', '.join(built)}")


if __name__ == "__main__":
    build()
