# chicagoasanteman.org redesign: working notes

## Direction: "Ahenfie" (the palace)
- Colours: ink-black and Asante gold, with kente green and maroon as accents, on ivory paper.
- Type: Fraunces (display serif) and Instrument Sans (body).
- Kente bands mark section breaks. The crest is the site logo. Adinkra symbols carry their meanings as section marks.
- Portraits sit in arch frames with a kente strip underneath, each person labelled with their stool title first.
- A few Twi touches: Akwaaba, Nkabom.

## Content kept from the live site
- Copy comes from the WordPress pages, unchanged.
- Placeholders dropped: theme stock photos, demo blog posts, the lorem-ipsum FAQ page, the "Start donating poor people" and "children need your help" banners, and the fake volunteer team.

## Open questions for AACM
1. **Logo.** Resolved: the crest from the live site is used as the logo and tab icon, as approved by the group.
2. **Phone number.** The home page and footer say (224) 334-6661, but the Contact page says +1 847-401-1145. Which is correct?
3. **Membership fee.** The live form said "$XXX"; the new one omits the amount. What is the fee?
4. **Social links.** Facebook, Twitter, YouTube and LinkedIn have no real URLs on the live site.
5. **Media albums.** The four "View Album" buttons on the live site go nowhere. Where do the photos live?
6. **Inauguration.** It was held May 23–24, 2026, which has passed. Should the page become a recap or gallery?
7. **Forms and hosting.** Where will the site be hosted, and which form service should replace the email-app approach? The newsletter signup from the live site isn't built yet.

## How the site is built
- Page content lives in `src/pages/*.html`; the shared header and footer, plus the nav, live in `build.py`.
- Leadership names, titles and photos live in `src/data/leadership.json`.
- Run `python3 build.py` to regenerate the `.html` files in the repo root. Upload the root folder to any static host. Edit `src/`, not the root files.
- After changing CSS or JS, bump `VERSION` in `build.py` so browsers fetch the new files.

## Pages (17, all built)
index, about, history, the-asantes, otumfuo-osei-tutu-ii, executive-team, council-of-elders, enstooled-royalty, former-executives, projects, inauguration, media, membership, membership-registration, volunteer, sponsorship, contact.

## Changes from the live site, to confirm
- **New addresses.** `sponsorship-application` is now `sponsorship.html`, and `membership-registration-form` is now `membership-registration.html`. If the old domain's URLs matter, add redirects at the host.
- **Spelling normalised** in titles: Bretuo (was "Biret uo"), Krontihene, Benkumhene (was "Bemkumhene"), Mmrantɛhene, Nsumankwahene, Sika I, and names in capitals. Please check these against AACM's own spelling.
- **Membership fee.** The "$XXX" is removed, so the form just says "the required membership fee". Put the real amount back once decided.
- **Media albums.** The four albums had no links and no names. I named them Gatherings, Ceremonies, Royalty and Youth & Culture as placeholders, and each links to Contact for now.
- **Inauguration venue** comes from the flyer: Hilton Chicago/Northbrook, 2855 Milwaukee Avenue, Northbrook, IL 60062. The date is May 23–24, 2026, which has passed.
- **Removed:** the lorem-ipsum FAQ page, the theme's demo blog, the shop/cart/donation pages, and the fake volunteer team. There are no Privacy or Terms pages yet, so the footer doesn't link to any.
- **Forms** open the visitor's email app with their answers, addressed to info@chicagoasanteman.org. They aren't saved anywhere until a form service is connected.

## Homepage features (Nov 2026 refinement)
- **Akan day-name finder:** enter a birth date, get the Twi day name and the traditional boy/girl names (Kwasi/Akosua through Kwame/Ama). Pure JavaScript, no data collected.
- **Court explorer:** six divisions (Akwamu, Adonten, Nifa, Benkum, Kyidom, Gyaase) matched to the executive on the site, with the chief and, where listed, the queen mother. It is built from `src/data/leadership.json`, so editing a title there changes the page. If a division has no matching title the build stops with an error.
- **Scroll-lit statement, counters, moments strip, frosted menu.**
- Adinkra captions were checked against published sources. Agyindawuru is now "Loyalty, vigilance".
- The one-line blurbs on the six divisions ("the vanguard", "the right wing", etc.) are standard descriptions of the Asante formation. Ask an elder to confirm before treating them as final.
