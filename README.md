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

- [x] Phone number — (805) 453-7730, live in every footer and on Contact
- [x] BHHS legal disclosure text in the footer of every page
- [x] DRE licence number — `02028163`, live in every footer and in
      `scripts/build.py`
- [ ] Drop the official **BHHS California Properties lockup**, **Equal Housing
      Opportunity**, and **REALTOR®** artwork into the three slots in the
      footer legal block, then delete the italic placeholder note. Artwork
      comes from BHHS marketing — do not recreate it.
- [ ] Replace all placeholder copy (search for "Placeholder")
- [ ] Real photography for hero, portraits, work cards, client photos
- [ ] BHHS-approved TCPA consent wording on both forms
- [ ] Stand up `/lead` and `/instagram`, then fill in `CONFIG`
- [ ] Point DNS, enable HTTPS
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
| Sunset Clay | `#D85A30` | Stripe 1, lead accent |
| Golden Hour | `#EF9F27` | Stripe 2, sub-line on dark |
| Bone | `#F4F1E8` | Ring + type on dark |
| Asphalt | `#161311` | Home turf background |
| Shorebreak | `#85B7EB` | Wave on dark |
| Deep Shorebreak | `#378ADD` | Wave on light |

Rules honoured in the CSS: flat only (no shadows, glows, or gradients);
stripes always Clay then Gold, never recoloured individually; the mark is
never rotated, skewed, or placed over photography without a solid panel;
type is Helvetica/Arial Bold, all caps, generous letter-spacing.
