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
VERSION = "14"  # bump when CSS/JS change so browsers fetch the new files

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
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,300..700,0..100;1,9..144,300..700,0..100&family=Instrument+Sans:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/css/site.css?v={VERSION}">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<div class="topbar">
  <div class="wrap">
    <div class="tb-left">
      <a href="mailto:{EMAIL}">{EMAIL}</a>
      <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>
    </div>
    <div class="tb-right">{ADDRESS}</div>
  </div>
</div>

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


def court(key):
    cards = []
    for p in LEADERSHIP[key]:
        name, title = html.escape(p["name"]), html.escape(p["title"])
        cards.append(f"""        <div class="seat">
          <div class="seat-frame"><img src="assets/img/people/{p['photo']}" alt="{name}" loading="lazy" width="315" height="350"></div>
          <div class="stool-title">{title}</div>
          <h3>{name}</h3>
        </div>""")
    extra = " court--feature" if key == "exec-stool" else ""
    return f'<div class="court{extra} reveal">\n' + "\n".join(cards) + "\n      </div>"


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
        (ROOT / src.name).write_text(head(meta) + "\n" + body.rstrip() + "\n\n" + foot())
        built.append(src.name)
    print(f"Built {len(built)} pages: {', '.join(built)}")


if __name__ == "__main__":
    build()
