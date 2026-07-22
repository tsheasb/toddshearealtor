# Todd Shea Real Estate — site

Static site. No build step required to view it; the only script generates
SB Residency issue pages and the RSS feed from markdown.

```
index.html            Home
about.html            Meet Todd
testimonials.html     Clients
residency.html        SB Residency hub
contact.html          Contact
posts/*.md            Issue source (what you edit)
posts/*.html          Generated — do not edit by hand
rss.xml               Generated — Mailchimp watches this
scripts/build.py      Generates posts, rss.xml, and the issue lists
css/ js/ assets/      Styles, behaviour, brand marks
CNAME                 toddshearealtor.com
```

---

## Publishing an SB Residency issue

1. Copy the previous issue's `.md` file in `posts/` and rename it
   `YYYY-MM-DD-short-slug.md`.
2. Edit the front matter and body.
3. Run `python3 scripts/build.py`
4. Commit and push.

The script writes the issue page, rebuilds `rss.xml`, and updates the issue
list on both `residency.html` and the homepage. Mailchimp picks up the new
feed item on its next check and sends the campaign.

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

---

## Deploying to GitHub Pages

1. Create a **public** repo.
2. Push these files to the root of the `main` branch.
3. Settings → Pages → Source: `main` / `root`.
4. Settings → Pages → Custom domain: `toddshearealtor.com` → Save.
   (`CNAME` is already in the repo.)
5. Tick **Enforce HTTPS** once the certificate provisions.

### DNS at Squarespace

Domains → toddshearealtor.com → DNS Settings. Leave everything else alone;
you are only using Squarespace as the registrar.

| Type | Host | Value |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | `YOUR-GITHUB-USERNAME.github.io` |

Propagation is usually 15 minutes to a few hours.

---

## The endpoint (Instagram + Follow Up Boss)

Both features need a small server-side handler. **GitHub Pages cannot do
this** — it only serves static files. Anything with a secret key must live
elsewhere. Recommended home: Kaya's existing VPS behind Traefik.

Set the two URLs at the top of `js/site.js`:

```js
var CONFIG = {
  captureEndpoint:   'https://api.toddshearealtor.com/lead',
  instagramEndpoint: 'https://api.toddshearealtor.com/instagram',
  ...
};
```

Until they are set, forms show "Form not connected yet" and the Instagram
grid keeps its placeholder tiles. Nothing breaks.

### `/lead` — Follow Up Boss

Receives `{ email, name?, phone?, interest?, message?, source, page }`.
Server-side, call FUB's `POST /v1/events` with your API key in a Basic auth
header. Return `200` with any JSON body.

**The FUB API key must never appear in `js/site.js`** — that file is public.

### `/instagram` — Graph API

Requirements: Instagram Business/Creator account (done), linked Facebook
Page (done), Meta app with the Instagram Graph API product, and a
long-lived access token.

The handler calls the Graph API for recent media and returns:

```json
{ "data": [ { "id": "...", "media_url": "...", "permalink": "...",
              "caption": "...", "media_type": "IMAGE" } ] }
```

Cache the response for 10–30 minutes so the site does not hit the rate
limit, and refresh the long-lived token on schedule — it expires every
60 days. A cron on the VPS handles this well.

---

## Mailchimp

Audience → Campaigns → **RSS-to-email**, feed URL
`https://toddshearealtor.com/rss.xml`, schedule set to match the every-other-week
cadence. Mailchimp sends automatically whenever a new item appears in the feed.

---

## Before launch

- [x] Phone number — (805) 453-7730
- [x] DRE licence number — `02028163`
- [x] Bio copy — Home hero and About page
- [x] Exact BHHS disclaimer text (independently owned and operated franchisee,
      Brand Guidelines Jul 2025, p7) in the footer of every page
- [x] Market-share claim removed — p13 prohibits franchisees from quoting
      company statistics

### BHHS compliance

- [x] **Company logo installed** — `assets/bhhs/bhhscp-secondary-white.png`
      (BHHSCP secondary lockup, white, on the Asphalt footer of every page).
      The primary vertical lockup is also in `assets/bhhs/` if a taller
      placement is ever needed.
- [x] **Equal Housing and REALTOR® badges installed**, converted to
      white-on-transparent from the supplied GIF and TIFF.
- [x] **2026 disclaimer** — uses the California Properties wording effective
      01-01-2026. Note this is the *HomeServices of America-owned* version
      ("an independently operated subsidiary of HomeServices of America, Inc."),
      not the independently-owned-and-operated franchisee wording in the global
      July 2025 guide. Source: "All Marketing LEGAL DISCLAIMERS", 01-01-2026.
- [ ] **Confirm the standalone site is permitted.** Global Brand Guidelines p15
      describes agents being given a page on the franchisee's site
      (`bhhsexample.com/todd-shea`) and does not explicitly authorise an
      agent-owned domain. `toddshearealtor.com` contains no form of the BHHS
      name, which satisfies the rule as written, but confirm with BHHS
      California Properties and GlobalBranding@HSFranchise.com before launch.
- [ ] **Web linking review** — to link this site from the BHHS global site,
      email GlobalBranding@HSFranchise.com with name, company name, and URL.
- [ ] TCPA / consent wording for both forms.

#### Disclaimer add-ons that will be needed later

From the 2026 disclaimer sheet, these apply once real content goes up:

- **Any page showing market data** (SB Residency "Nitty Gritty"):
  "Properties may or may not be listed by the office/agent presenting this
  information. Information is deemed reliable but not guaranteed and is based
  on data from MLS as of (date)." Listing attribution rules also apply — each
  featured property needs its listing agent and brokerage named.
- **Sold-property content**: "Properties may or may not be represented by the
  office/agent presenting this information. Based on information obtained from
  the MLS as of (date)."
- **Any AI-generated or digitally enhanced imagery**: the disclaimer gains
  "Some images were digitally enhanced or AI-generated and are for illustration
  only; they may not reflect actual properties or conditions. For unaltered
  images, visit (website address)."

### Rules this site must keep following

- Company logo on the home page at minimum; clear space on all sides of at
  least the height of the "H" in Hathaway.
- The company logo may not be animated, tinted, resized disproportionately,
  used as wallpaper or watermark, or **combined with another graphic**. The
  Salt Seal and the BHHS logo must stay separate.
- Personal logos may not be larger than the company logo and must sit at least
  one X-height away from it.
- Write "Berkshire Hathaway HomeServices California Properties" in full at
  least once in copy. Never use "BHHS" alone in public-facing text, and never
  "Berkshire" or "HomeServices" on their own.
- No references to Warren Buffett or Berkshire Hathaway Inc., and no linking to
  pages that discuss them.
- No company statistics or market-share claims.
- Photography must look premium and authentic, not like stock. Avoid subjects
  looking straight at the camera. AI-generated imagery should be avoided for
  real properties, people, or places (p11).
- Approved hashtags: #goodtoknow, #goodtoask, #GTK, #BHHS, #BHHSrealestate,
  #ForeverAgent, #YourForeverAgent, #ForEveryone, #ForeverBrand,
  #RealEstatesForeverBrand.

### Content still outstanding

- [x] Three sold properties on the homepage — Palomino Ridge, Conejo Road,
      Ortega Hill, with the required MLS disclaimer (as of July 22, 2026).
      **Update that date whenever the properties change.**
- [ ] Listing attribution — if any featured property was listed by another
      brokerage, MLS rules require naming the listing agent and brokerage on
      the card. All three current properties were Todd's own listings.
- [ ] Three testimonials, first real SB Residency issue
- [ ] Photography — hero, portraits, work cards, client photos
- [ ] Stand up `/lead` and `/instagram`, then fill in `CONFIG`
- [ ] Enable HTTPS once GitHub's DNS check passes
- [ ] Connect the Mailchimp RSS campaign

### Where the compliance details live

The footer block is repeated in each `.html` file **and** in the
`SHELL_FOOTER` constant in `scripts/build.py`. Change both, or generated
issue pages will drift out of sync with the rest of the site.

---

## Brand

Per `shea-brand-guidelines.pdf` v1:

| Token | Hex | Use |
|---|---|---|
| Sunset Clay | `#D85A30` | Stripe 1, lead accent, eyebrows on light |
| Golden Hour | `#EF9F27` | Stripe 2, sub-line on dark |
| Bone | `#F4F1E8` | Ring + type on dark |
| Asphalt | `#161311` | Home turf background |
| Shorebreak | `#85B7EB` | Wave on dark |
| Deep Shorebreak | `#378ADD` | Wave on light |

Rules honoured in the CSS: flat only (no shadows, glows, or gradients);
stripes always Clay then Gold, never recoloured individually; the mark is
never rotated, skewed, or placed over photography without a solid panel;
type is Helvetica/Arial Bold, all caps, generous letter-spacing.

### Light-first layout

The brand sheet says Asphalt is home turf and the brand looks best on dark,
with Bone as the light-mode surface. This site runs the inverse: **Bone is the
base**, with Asphalt used for three deliberate contrast blocks (hero, Instagram
grid, footer) and a Deep Shorebreak panel for the off-market capture. Both
colours are used as the sheet specifies — the default is just flipped.

Section classes:

| Class | Surface |
|---|---|
| *(none)* | Bone — the base |
| `.section--tint` | `#EAE6DA`, a soft tint of Bone |
| `.section--dark` | Asphalt, Bone type |
| `.offmarket` | Deep Shorebreak panel |

### One derived colour — needs adding to the brand sheet

`--deep-text: #2968A7` is Deep Shorebreak darkened to 76% brightness. Brand
Deep Shorebreak only reaches 3.18:1 against Bone, which fails WCAG AA for
body-size text; the darkened tint reaches 5.12:1. It is used **only** for small
text and links on light surfaces, and for the off-market panel fill so Bone
type on it stays legible. Brand Deep Shorebreak is still used unchanged for
borders, rules, and large type.

Per the guidelines ("Don't introduce new colors without updating this sheet"),
this should either be added to the brand sheet as an approved text tint, or
replaced with an approved alternative. Flagged rather than assumed.

All text/background pairs on the site pass WCAG AA (4.5:1 normal, 3:1 large).
