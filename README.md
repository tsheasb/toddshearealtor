# Todd Shea Real Estate — toddshearealtor.com

Static site. No build step to view it; one script generates SB Residency
issue pages and the RSS feed from markdown.

**If you are picking this up cold:** read this file top to bottom before
changing anything. Several values in the CSS look arbitrary and are not —
they were set by measurement and the reasoning is recorded here. Sections
marked **⚠ decided** capture choices made deliberately that would be easy
to undo by accident.

---

## Contents

```
index.html            Home
about.html            Todd
testimonials.html     Clients
residency.html        SB Residency hub
contact.html          Contact
posts/*.md            Issue source (what you edit)
posts/*.html          Generated — do not edit by hand
rss.xml               Generated — Mailchimp watches this
scripts/build.py      Generates posts, rss.xml, and the issue lists
scripts/check.py      Regression check — run after any change
css/site.css          Tokens, type, layout shell
css/components.css    Section and component styles
js/site.js            Nav, quote toggles, form capture
js/motion.js          Hero video + all scroll motion
assets/               Brand marks, photography, video, map
CNAME                 toddshearealtor.com
```

### Asset folders

| Folder | Contents |
|---|---|
| `assets/` | Shea brand marks (SVG), favicon PNGs, `area-map.svg` |
| `assets/bhhs/` | BHHS company logo + Equal Housing + REALTOR®, white on transparent |
| `assets/hero/` | Hero video (mp4 + webm), poster frames, older still images |
| `assets/life/` | Lifestyle photography for the home and Todd pages |
| `assets/todd/` | Portrait and coaching photo |
| `assets/work/` | Sold-property photography |
| `assets/ig/` | The eight Instagram tiles |

---

## Who this site is for, and what it is deliberately not

**⚠ decided.** Four competitor sites were reviewed at the start of this
build: Dusty Baker Group, Cristal Clarke, Kogevinas (montecitoproperties),
and The Hamilton Co. Every one of them leads with rank, sales volume, and
decades in business, and buries anything personal on a second page or in a
single sentence.

This site does the opposite on purpose:

- **The personal material leads.** Lifestyle photos sit directly under the
  hero, before any credential. The stats live on the Todd page, not the
  front door. If you find yourself moving numbers back to the homepage,
  you are rebuilding a competitor's site.
- **It is not a listings portal.** "This is not where you browse houses"
  is a positioning statement, not a placeholder. There is no MLS search,
  no property grid, no IDX feed. Sold properties appear as proof, not
  inventory.
- **The voice is short, confident, salty.** Per the brand sheet:
  "Another one closed." beats "Thrilled to announce!" Adjective stacking
  ("white-glove", "unmatched", "relentless") was deliberately edited out
  of the bio once already.

---

## Publishing an SB Residency issue

1. Copy the previous issue's `.md` in `posts/`, rename it
   `YYYY-MM-DD-short-slug.md`.
2. Edit the front matter and body.
3. Run `python3 scripts/build.py`
4. Commit and push.

The script writes the issue page, rebuilds `rss.xml`, and updates the issue
list on `residency.html` and the homepage. Mailchimp picks up the new feed
item on its next check.

Front matter:

```yaml
---
title: The Issue Title
date: 2026-08-05
number: 2
teaser: One line for the hub page and RSS description.
hero: /assets/posts/issue-02-hero.jpg
hero_alt: Description of the hero image
---
```

Body supports `## Headings`, `- bullets`, `**bold**`, `*italic*`, and
`[links](https://example.com)`. Everything else is plain paragraphs.

### The issue template (agreed, not yet built)

Every issue follows this shape:

1. Hero photo
2. Opening line
3. **The Nitty Gritty** — market stats
4. **Window Shopping** — three listings worth a look
5. **This Issue's Vibe** — follows, listening, reading; condensed
6. CTA
7. Sign-off with tagline + wordmark

**Cadence: every other week**, roughly 26 issues a year. (This was
originally written down as "bi-monthly", which was ambiguous — it means
biweekly.)

**⚠ Market data in an issue requires its own disclaimer** — see the BHHS
section below. Do not publish a Nitty Gritty section without it.

---

## Deploying to GitHub Pages

Repo: `github.com/tsheasb/toddshearealtor`, branch `main`, folder `/ (root)`.

1. Settings → Pages → Source: Deploy from a branch → `main` / `root`.
2. Custom domain: `toddshearealtor.com` (the `CNAME` file is in the repo).
3. Tick **Enforce HTTPS** once the certificate provisions.

`.nojekyll` is present and must stay — without it GitHub ignores files and
folders beginning with an underscore.

### DNS at Squarespace

Squarespace is the registrar only; the site is not built there. Domains →
toddshearealtor.com → DNS. **Leave the Google Workspace MX and TXT records
alone — that is the email.**

| Type | Host | Value |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | `tsheasb.github.io` |

---

## The `/lead` endpoint — not built yet

Both forms (off-market capture and the contact form) currently show
"Form not connected yet" and log the payload to the console. **No leads are
being captured.** This is the one functional gap on the site.

GitHub Pages serves static files only, so the Follow Up Boss API key cannot
live in `js/site.js` — that file is public. It needs a small server-side
handler. Agreed home: **Kaya's existing VPS** (Hostinger, Docker, Traefik),
since that infrastructure is already running and inspectable.

The handler receives `{ email, name?, phone?, interest?, message?, source, page }`
and calls FUB's `POST /v1/events` with the key in a Basic auth header.

Once it exists, set the URL at the top of `js/site.js`:

```js
var CONFIG = {
  captureEndpoint: 'https://api.toddshearealtor.com/lead',
  ...
};
```

The form already handles: honeypot field for bots, email validation,
disabled state while sending, success and failure messaging, and a fallback
that tells the visitor to email directly if the request fails.

---

## Instagram grid — static, not a live feed

**⚠ decided.** A live Graph API feed was considered and rejected for now:
it needs a long-lived token refreshed on a cron before its 60-day expiry,
which meant standing up server-side infrastructure for a decorative
section. The tiles are hand-picked instead, refreshed manually every few
months.

**To refresh:**

1. Screenshot eight posts from Instagram.
2. Crop square, save as `ig-1.jpg` … `ig-8.jpg` in `assets/ig/`, 800×800,
   quality ~82.
3. In `index.html`, update the eight `<a class="ig-cell">` blocks — each
   needs the post permalink in `href` and plain-language `alt` text.

**Eight is deliberate.** The grid is fixed at four columns on desktop and
two on phones, so eight always fills evenly. `auto-fit` was tried first and
produced a lopsided 5+3 on wide screens and a single column on mobile.

**⚠ Order matters.** The set is 4 photos + 4 marketing cards, alternating
perfectly — `P C P C / P C P C` on desktop and `P C` on every mobile row.
Keep that balance when swapping tiles; an uneven split forces two cards to
sit adjacent somewhere.

Current tiles: volleyball, Palomino Ridge *just listed*, Desert Willow golf,
Conejo Road *under contract*, Santa Ynez winery, Palomino Ridge *sold*,
steaks, Del Playa *sold*. Palomino Ridge appears twice on purpose — the
listing card and the sold card, same property.

**Watch the crop on marketing cards.** They carry text at the top and
bottom, so a centre square crop clips the price or the licence line. The
crops here were placed by finding the vertical anchor that retains 100% of
the high-detail rows, not by eye.

---

## Mailchimp

Audience → Campaigns → **RSS-to-email**, feed URL
`https://toddshearealtor.com/rss.xml`, schedule matching the every-other-week
cadence. Not yet connected.

---

## Brand

Per `shea-brand-guidelines.pdf` v1 (July 2026):

| Token | Hex | Use |
|---|---|---|
| Sunset Clay | `#D85A30` | Stripe 1, lead accent, eyebrows on light |
| Golden Hour | `#EF9F27` | Stripe 2, sub-line on dark, photo captions |
| Bone | `#F4F1E8` | Page base, type on dark |
| Asphalt | `#161311` | Contrast blocks, type on light |
| Shorebreak | `#85B7EB` | Wave in the mark, accents on dark |
| Deep Shorebreak | `#378ADD` | Wave on light, fills and rules |

Rules honoured in the CSS: flat only (no shadows, glows, gradients on brand
elements); stripes always Clay then Gold, never recoloured individually;
the mark is never rotated, skewed, or placed over photography without a
solid panel; type is Helvetica/Arial Bold, all caps, generous letter-spacing.

### Which mark goes where

- **Header** — `shea-secondary-on-light.svg`. The on-dark version fills the
  wordmark in Bone, which is invisible against the Bone header. This was a
  live bug once; do not "simplify" it back to one file.
- **Footer** — `shea-secondary-on-dark.svg`, because the footer is Asphalt.
- **Todd page mark section** — `shea-mark-on-dark.svg`, scaled
  proportionally inside `.split__media--mark`, never cropped to fill.

### Light-first layout

**⚠ decided.** The brand sheet says Asphalt is home turf and the brand
looks best on dark, with Bone as the light-mode surface. This site runs the
inverse: **Bone is the base**, with Asphalt reserved for deliberate
contrast blocks. Both colours are used as the sheet specifies — the default
is simply flipped. This was a considered choice, not an oversight.

| Class | Surface |
|---|---|
| *(none)* | Bone — the base |
| `.section--tint` | `#EAE6DA`, a soft tint of Bone |
| `.section--dark` | Asphalt, Bone type |
| `.offmarket` | Deep Shorebreak panel |

### One derived colour — still needs adding to the brand sheet

`--deep-text: #2968A7` is Deep Shorebreak darkened to 76% brightness. Brand
Deep Shorebreak reaches only 3.18:1 against Bone, which fails WCAG AA for
body-size text; the darkened tint reaches 5.12:1. Used **only** for small
text and links on light surfaces, and for the off-market panel fill so Bone
type on it stays legible. Brand Deep Shorebreak is unchanged for borders,
rules, and large type.

Per the guidelines ("Don't introduce new colors without updating this
sheet"), this should be added as an approved text tint or replaced with an
approved alternative. Flagged rather than assumed.

---

## Measured values — do not adjust by eye

Several values were set by measuring the rendered page, not by judgement.
Changing them without re-measuring will break accessibility.

### Hero scrim

The hero sits over video averaging ~0.19 luminance. The scrim is a radial
pool anchored to the lower-left where the copy sits, plus a light bottom
gradient.

- **Why not a flat overlay:** a conventional dark scrim strong enough for
  the headline pushed the wharf and town to 0.03 luminance — it deleted the
  subject of the footage.
- **Measured:** the headline clears 4.5:1 at every viewport across four
  different moments in the video. Desktop is tightest at ~4.5.

### Life mosaic captions

Captions sit over photography with a gradient behind them.

- **Measured:** caption text ~15:1, the Golden Hour label ~6:1, against the
  brightest photo in the set.
- **A lighter gradient was tried** and dropped the gold label to 3.5:1,
  which fails AA for small text. The current stops are the lightest that
  still pass.
- **Measuring these correctly is fiddly.** Sampling the caption box
  includes the gradient element itself and returns nonsense (~1.2:1). The
  correct method is to set the text to `transparent`, screenshot, then
  sample the exact glyph boxes.


### Life mosaic shape

**⚠ Every slot is portrait on purpose.** All four source photos are 3:4.
An earlier version used a 16:7 wide banner for the fourth slot, which kept
only **34% of the image height** and cropped Todd and Melissa off at the
chest. The layout is now two tall anchors (golf, Melissa) flanking a
stacked pair (surf, kitchen). If you add a wide slot back, check what
percentage of the source height survives before committing to it.

### Everything else

All text/background pairs across all pages pass WCAG AA (4.5:1 normal,
3:1 large). The regression pattern used throughout this build: load every
page at 1440px and 390px, scroll to the bottom, walk every text element,
compute contrast against its effective background, and flag anything under
3:1 along with broken images, horizontal overflow, stuck reveal animations,
and JS errors.

---

## Scroll motion

`js/motion.js`. All effects are opt-in via data attributes:

| Attribute | Effect |
|---|---|
| `data-reveal` | Fades and rises as the element enters view |
| `data-reveal-delay="120"` | Staggers a group (ms) |
| `data-count="116"` | Counts up on first view |
| `data-count-suffix=" yrs"` | Appended to the counted value |
| `data-parallax="0.18"` | Drifts at a fraction of scroll speed |
| `data-words` | Splits an H1 into words that rise in sequence |
| `data-scroll-scale` | Image scales 1.06 → 1.00 while crossing the viewport |
| `data-scroll-rotate` | Gentle −7° → +7° rotation (the Salt Seal only) |

The `.stripes` brand device draws itself left-to-right wherever it appears,
automatically.

**Safe by default.** Elements are visible in CSS; the hidden pre-reveal
state only applies once JS sets `data-motion="on"` on `<html>`. If JS fails
or is blocked, the page reads normally — this is tested, not assumed. The
script exits immediately for `prefers-reduced-motion` and stops mid-session
if the visitor enables it. A scroll listener force-completes any animation
if someone reaches the bottom faster than the observers fire.

**⚠ Restraint is the point.** Motion is at section level, not per-word or
per-letter beyond the H1s. A site that is obviously showing off works
against "another one closed."

### Hero video

`assets/hero/hero.mp4` (H.264, 2.2 MB) and `hero.webm` (VP9, 1.6 MB), with
`hero-poster.jpg` behind them. The video is **skipped** — poster shown
instead — for reduced-motion users, `saveData`, 2G connections, and screens
under 720px. All four paths are tested.

The video replaced a still photograph that read as "gloomy". Measured, the
video is much warmer (+34.6 red-over-blue vs +13.6) and also darker
(0.19 vs 0.42 luminance), which is why the scrim was retuned when it went in.

---

## BHHS compliance

Source documents: the global Brand Guidelines (July 2025) and
"All Marketing LEGAL DISCLAIMERS" effective 01-01-2026.

### Done

- Company logo (`bhhscp-secondary-white.png`) in the footer of every page.
- Equal Housing and REALTOR® badges, converted to white-on-transparent.
- **The 2026 California Properties disclaimer.** Note this is the
  *HomeServices of America-owned* wording ("an independently operated
  subsidiary of HomeServices of America, Inc."), **not** the
  independently-owned-and-operated franchisee wording in the global guide.
  The wrong version was installed first and corrected.
- **Market-share claim removed.** The bio originally said BHHS California
  Properties is "Santa Barbara's #1 real estate company by market share".
  Global guidelines p13 prohibits franchisees from quoting company
  statistics. Do not reinstate it.

### Outstanding

- [ ] **Confirm a standalone agent site is permitted.** Global guidelines
      p15 describes agents being given a page *on the franchisee's site*
      (`bhhsexample.com/todd-shea`) and does not explicitly authorise an
      agent-owned domain. `toddshearealtor.com` contains no form of the
      BHHS name, which satisfies the rule as literally written — but
      confirm with BHHS California Properties and
      GlobalBranding@HSFranchise.com.
- [ ] **Web linking review** — to link this site from the BHHS global site,
      email GlobalBranding@HSFranchise.com with name, company, and URL.
- [ ] **TCPA / consent wording** for both forms. Placeholder text is in
      place on the contact form and must be replaced before launch.

### Disclaimer add-ons that will be needed

- **Sold properties** (already on the homepage, already applied):
  "Properties may or may not be represented by the office/agent presenting
  this information. Based on information obtained from the MLS as of
  [date]." **The date is hardcoded — update it when the properties change.**
- **Any page showing market data** (the SB Residency "Nitty Gritty"):
  "Properties may or may not be listed by the office/agent presenting this
  information. Information is deemed reliable but not guaranteed and is
  based on data from MLS as of [date]." Listing attribution rules also
  apply — each featured property needs its listing agent and brokerage named.
- **Any AI-generated or digitally enhanced imagery**: the disclaimer gains
  a sentence identifying it and pointing to unaltered images.

### Rules this site must keep following

- Company logo on the home page at minimum; clear space on all sides of at
  least the height of the "H" in Hathaway.
- The company logo may not be animated, tinted, resized disproportionately,
  used as wallpaper or watermark, or **combined with another graphic**. The
  Salt Seal and the BHHS logo stay separate.
- Personal logos may not be larger than the company logo.
- Write "Berkshire Hathaway HomeServices California Properties" in full at
  least once. Never "BHHS" alone in public-facing text, and never
  "Berkshire" or "HomeServices" on their own.
- No references to Warren Buffett or Berkshire Hathaway Inc.
- No company statistics or market-share claims.
- Photography must look premium and authentic, not stock. AI-generated
  imagery should be avoided for real properties, people, or places.

### Where the compliance details live

The footer block is repeated in each `.html` file **and** in the
`SHELL_FOOTER` constant in `scripts/build.py`. Change both, or generated
issue pages drift out of sync.

---

## Content decisions worth preserving

**⚠ The areas map is a list, not a projection.** `assets/area-map.svg` is
generated as a vertical column — one row per town, pins on a shared axis,
labels parallel, grouped under Santa Ynez Valley / South Coast / Ventura
County. A geographically accurate horizontal version was built first and
failed: the coastal towns sit within ~20 miles of each other, so Santa
Barbara, Montecito, Summerland and Carpinteria overlapped no matter how the
labels were staggered. The vertical form makes collisions impossible by
construction. The group headings also handle the county problem below.

**⚠ Some images bypass the standard slot ratio.** `.split__media` is 4:5,
but the waving-at-the-door photo is 0.649 aspect and was losing 313px —
his legs — to that crop. It uses `.split__media--tall`, which matches the
source exactly. If a photo looks clipped, compare its aspect to the slot
before reaching for a different crop anchor.

**⚠ Service area language.** Todd works Los Olivos, Buellton, Santa Ynez,
Goleta, Santa Barbara, Montecito, Summerland, Carpinteria, Ojai and
Ventura. Ventura and Ojai are Ventura County, so "Santa Barbara County"
would be inaccurate. The decision: say **"Santa Barbara"** in the hero
(it's the emotional line, not a service-area statement), and list the towns
**once** in the "Ten towns, one coastline" section with the map. There were
previously twelve mentions in three different phrasings across six files;
that was deliberately consolidated. Don't scatter it again.

**Testimonials.** Six real Google reviews, verbatim, names as they appear
publicly. **None of the six mention Zia Group**, Todd's former brokerage —
that was the selection criterion, since naming a competitor on a BHHS site
is a problem. There are 38 Google reviews and 21 Zillow reviews, all
five-star, but the page deliberately avoids a hardcoded count so it doesn't
need updating. Client photos are not used — the layout shows a five-star
mark instead, because inventing or sourcing client photos wasn't an option.

**Family photography.** Todd's children appear in some source photos but
were deliberately kept off the site. Melissa appears; the kids do not.
A volleyball team photo was also declined, and the coaching photo used is
cropped to remove a seated player — consent was confirmed for the
remaining subject.

**The Salt Seal narrative** uses "100+ closings" (evergreen), while the
Credentials block uses the specific "116". Intentional.

**Anniversary note.** Todd and Melissa's 20th is 1 December 2026. Copy
currently reads "twenty-plus". After that date "twenty years" becomes
accurate again if preferred.

---

## Still outstanding

- [ ] `/lead` endpoint — forms capture nothing until this exists
- [ ] Mailchimp RSS campaign
- [ ] First real SB Residency issue (a placeholder issue is in `posts/`)
- [ ] TCPA consent wording from BHHS
- [ ] BHHS confirmation on the standalone domain
- [ ] Enforce HTTPS in GitHub Pages settings once the cert provisions

---

## Working method

Every change in this build was verified before delivery, not assumed:

- Load every page at desktop and mobile widths
- Scroll to the bottom so all lazy content and animations fire
- Check: contrast on every text element, broken images, horizontal
  overflow, stuck animations, JS errors
- For anything over photography or video, measure contrast at the actual
  glyph positions across multiple frames

`scripts/check.py` automates the first four. Run it from the site root
after any change:

```
python3 scripts/check.py
```

It needs playwright (`pip install playwright && playwright install chromium`)
and should print `ALL PASS`. Caption-over-photo contrast is not covered by
it — that needs the transparent-text method described above.

This caught several real bugs — a sideways golf photo (EXIF orientation 6),
invisible header type, `.lede` and `.muted` still using dark-theme colours
after the light flip, and an invisible hero headline. Worth keeping up.
