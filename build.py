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
VERSION = "52"  # bump when CSS/JS change so browsers fetch the new files

PHONE_DISPLAY = "(224) 334-6661"
PHONE_TEL = "+12243346661"
EMAIL = "info@chicagoasanteman.org"
ADDRESS = "11070 S Western Ave, Chicago, IL 60643"
MAP_URL = "https://maps.app.goo.gl/mmgueGGtTuZAeEiD7"

# Fill these in when AACM opens the accounts. Until then the Donate page says online
# giving is opening soon, and the newsletter forms open the visitor's email app.
DONATE_URL = ""          # e.g. a Zeffy / PayPal / Stripe donation link
MAILCHIMP_ACTION = ""    # the "action" URL from a Mailchimp embedded signup form
FACEBOOK_URL = "https://www.facebook.com/asantemanchicago"
YOUTUBE_URL = "https://www.youtube.com/@AsantemanChicago"

LOGO = '<img src="assets/img/logo.png" alt="" width="36" height="44">'

# (key, label, href) or (group-key, label, [(key, label, href), ...])
NAV = [
    ("about", "About us", [
        ("history", "History", "history.html"),
        ("asantes", "About the Asante Kingdom", "the-asantes.html"),
        ("executive", "Chiefs and queens", "executive-team.html"),
        ("elders", "Council of Elders", "council-of-elders.html"),
        ("manhyia", "Manhyia Palace", "manhyia-palace.html"),
        ("admin", "Administrative team", "executive-team.html#administrative"),
    ]),
    ("projects", "Our work", "projects.html"),
    ("involved-group", "Get involved", [
        ("involved", "Ways to get involved", "get-involved.html"),
        ("membership", "Membership & FAQ", "membership.html"),
        ("volunteer", "Volunteer", "volunteer.html"),
        ("sponsorship", "Development partnerships", "sponsorship.html"),
    ]),
    ("pubs", "Publications & Events", [
        ("media", "Media", "media.html"),
        ("events", "Events", "events.html"),
    ]),
    ("contact", "Contact us", "contact.html"),
]
# Pages that live inside a menu group without being a menu item themselves
GROUP_EXTRA = {"about": {"royalty", "former", "otumfuo", "about"}, "pubs": {"inauguration"}, "involved-group": {"membership-registration"}}


def nav_html(active):
    out = []
    for key, label, target in NAV:
        if isinstance(target, list):
            in_group = any(k == active for k, _, _ in target) or active in GROUP_EXTRA.get(key, ())
            cur_attr = ' aria-current="page"'
            items = "\n".join(
                f'          <a href="{h}"{cur_attr if k == active else ""}>{l.replace("&", "&amp;")}</a>'
                for k, l, h in target)
            cls = ' class="is-active"' if in_group else ""
            out.append(f'      <div class="nav-group">\n        <button type="button"{cls}>{label.replace("&", "&amp;")}</button>\n'
                       f'        <div class="nav-menu">\n{items}\n        </div>\n      </div>')
        else:
            cur = ' aria-current="page"' if key == active else ""
            out.append(f'      <a href="{target}"{cur}>{label.replace("&", "&amp;")}</a>')
    out.append('      <a class="btn btn--gold" href="membership-registration.html">Join Today</a>')
    return "\n".join(out)


# Licensed Canela: drop the web font files in assets/fonts/ (e.g. Canela-Regular.woff2,
# Canela-RegularItalic.woff2, Canela-Light.woff2) and the site switches to Canela on the
# next build. Until then headings fall back to Fraunces.
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
    body_attr = ' data-noexit' if meta.get("noexit") else ""
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
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..600;1,9..144,300..600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
{canela_css()}  <link rel="stylesheet" href="assets/css/site.css?v={VERSION}">
</head>
<body{body_attr}>
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
<a class="donate-tab" href="donate.html">Donate</a>

<main id="main">
"""


SOCIAL_SVG = {
    "facebook": '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path fill="currentColor" d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>',
    "youtube": '<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path fill="currentColor" d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>',
}


def social_html():
    return (f'<div class="social">'
            f'<a href="{FACEBOOK_URL}" rel="noopener" target="_blank" aria-label="AACM on Facebook">{SOCIAL_SVG["facebook"]}</a>'
            f'<a href="{YOUTUBE_URL}" rel="noopener" target="_blank" aria-label="AACM on YouTube">{SOCIAL_SVG["youtube"]}</a>'
            f'</div>')


def newsletter(idp="nl"):
    """Email signup. Posts to Mailchimp once MAILCHIMP_ACTION is set; until then it opens the visitor's email app."""
    if MAILCHIMP_ACTION:
        attrs = f'action="{MAILCHIMP_ACTION}" method="post" target="_blank" novalidate'
        note = "Thank you. Please confirm your subscription in the tab that just opened."
    else:
        attrs = f'data-mailto="{EMAIL}" data-subject="Newsletter subscription"'
        note = "Your email app should open with your request, ready to send."
    return (f'<form class="newsletter" {attrs}>'
            f'<label class="sr-only" for="{idp}-email">Email address</label>'
            f'<input type="email" id="{idp}-email" name="EMAIL" data-label="Email" placeholder="Your email address" required autocomplete="email">'
            f'<button class="btn btn--gold" type="submit">Subscribe</button>'
            f'<p class="form-status" role="status">{note}</p></form>')


def foot(show_news=True):
    news = f"""  <div class="wrap footer-news">
    <div>
      <h4>Newsletter</h4>
      <p class="fn-lede">News, events and stories from the Asanteman Association of Chicago &amp; Midwest.</p>
    </div>
    {newsletter("foot")}
  </div>
""" if show_news else ""
    return f"""</main>

<footer class="site-footer">
  <div class="kente kente--thin" role="presentation"></div>
{news}  <div class="wrap footer-cols">
    <div>
      <a class="brand" href="index.html">
        {LOGO}
        <span><span class="brand-name">Asanteman</span><span class="brand-sub">Chicago &amp; Midwest</span></span>
      </a>
      <p class="motto">One People, One Heritage, One Mission.</p>
      <p>A tax-exempt 501(c)(3) non-profit organization.</p>
      {social_html()}
    </div>
    <div>
      <h4>About us</h4>
      <ul>
        <li><a href="history.html">History</a></li>
        <li><a href="the-asantes.html">About the Asante Kingdom</a></li>
        <li><a href="executive-team.html">Chiefs and queens</a></li>
        <li><a href="council-of-elders.html">Council of Elders</a></li>
        <li><a href="manhyia-palace.html">Manhyia Palace</a></li>
        <li><a href="executive-team.html#administrative">Administrative team</a></li>
      </ul>
    </div>
    <div>
      <h4>Take part</h4>
      <ul>
        <li><a href="projects.html">Our work</a></li>
        <li><a href="get-involved.html">Get involved</a></li>
        <li><a href="membership.html">Membership &amp; FAQ</a></li>
        <li><a href="events.html">Events</a></li>
        <li><a href="media.html">Media</a></li>
        <li><a href="donate.html">Donate</a></li>
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

<dialog class="exit-pop" id="exit-pop" aria-labelledby="exit-title">
  <button type="button" class="exit-close" aria-label="Close">×</button>
  <img src="assets/img/crest-mark.png" alt="" width="44" height="52">
  <div class="eyebrow">Before you go</div>
  <h2 id="exit-title">Stay close to the court.</h2>
  <p>Events, news and stories from the Asanteman Association of Chicago &amp; Midwest, sent to your inbox.</p>
  {newsletter("exit")}
  <button type="button" class="exit-skip">No thanks</button>
</dialog>

<script src="assets/js/site.js?v={VERSION}"></script>
</body>
</html>
"""


# ---------- events (src/data/events.json) ----------
EVENTS = json.loads((ROOT / "src/data/events.json").read_text())
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def event_card(e, past=False):
    d = e.get("date", "")
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", d)
    day, mon = (str(int(m.group(3))), MONTHS[int(m.group(2)) - 1]) if m else ("", "")
    badge = f'<div class="ev-date"><b>{day}</b><span>{mon}</span></div>' if m else ""
    href = e.get("href")
    cta = f'<a class="link-arrow" href="{html.escape(href)}">{html.escape(e.get("cta", "Details"))}</a>' if href else ""
    when = html.escape(e.get("when", ""))
    place = html.escape(e.get("place", ""))
    meta = " · ".join(x for x in (when, place) if x)
    return (f'<article class="ev{" ev--past" if past else ""}">{badge}<div class="ev-body">'
            f'<h3>{html.escape(e["title"])}</h3>'
            f'{"<p class=ev-meta>" + meta + "</p>" if meta else ""}'
            f'{"<p>" + html.escape(e["blurb"]) + "</p>" if e.get("blurb") else ""}{cta}</div></article>')


def events_block(kind):
    up = EVENTS.get("upcoming", [])
    if up:
        return '<div class="evs">' + "".join(event_card(e) for e in up) + "</div>"
    return ('<div class="ev-empty"><p><b>New dates are on the way.</b> Subscribe to hear first, or write to '
            f'<a href="mailto:{EMAIL}">{EMAIL}</a>.</p>{newsletter("ev-" + kind)}</div>')


def donate_block():
    if DONATE_URL:
        return f'<p><a class="btn btn--gold" href="{DONATE_URL}" rel="noopener">Give now</a></p>'
    return ('<div class="notice"><b>Online giving opens soon.</b> Until then, to give or to ask how a gift is used, '
            f'write to <a href="mailto:{EMAIL}">{EMAIL}</a> or call <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>.</div>')


def events_recent():
    return '<div class="evs">' + "".join(event_card(e, True) for e in EVENTS.get("recent", [])) + "</div>"


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
        body = body.replace("<!--newsletter-->", newsletter("pg")).replace("<!--social-->", social_html())
        body = body.replace("<!--events:home-->", events_block("home")).replace("<!--events:page-->", events_block("page")).replace("<!--events:recent-->", events_recent())
        body = body.replace("<!--donate-->", donate_block())
        body = re.sub(r"<!--court:([\w-]+)-->", lambda mm: court(mm.group(1)), body)
        body = body.replace("<!--courtdata-->", '<script type="application/json" id="court-data">' + json.dumps(court_data(), ensure_ascii=False).replace("</", "<\\/") + "</script>")
        (ROOT / src.name).write_text(head(meta) + "\n" + body.rstrip() + "\n\n" + foot(not meta.get("own_news")))
        built.append(src.name)
    write_pwa(built)
    print(f"Built {len(built)} pages: {', '.join(built)}")


if __name__ == "__main__":
    build()
