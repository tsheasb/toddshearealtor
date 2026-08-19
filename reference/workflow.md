# SB Residency — Full Workflow

**Purpose:** The complete cycle from "Todd sits down on a Thursday" to "email lands in inboxes the following Tuesday," with who does what at each step. Read this alongside the build reference and hero template docs already in this project.

---

## The cadence — and the one rule that protects it

**Build day: a Thursday. Launch day: the following Tuesday, 9 AM Pacific — 5 days later.**

**Critical constraint:** Mailchimp's RSS campaign checks the feed every single Tuesday. It only stays silent on off-weeks because there's nothing *new* to find. That means new content can only be pushed to the repo roughly every other Thursday — if a new issue goes out every Thursday, the cadence quietly becomes weekly instead of biweekly, with no error or warning to flag it. This is a content-timing discipline, not something the code enforces automatically.

**Confirmed dates:**
- Issue 01 "Slim Pickings" — built Thursday, July 30, 2026. Live now. First send: Tuesday, August 4, 2026, 9 AM Pacific.
- Issue 02 build date: *(confirm — either Aug 6 or Aug 13, depending on which keeps the true biweekly rhythm going)*
- Every subsequent build day: 12 days after the previous build day (2-week cycle), always a Thursday, always launching the following Tuesday.

---

## Who does what

| Step | Owner | What happens |
|---|---|---|
| 1. Bring the inputs | **Todd** | Market to feature, 3 MLS numbers + listing URLs, any active listings, IG follows, what's caught your attention, go-ahead to proceed |
| 2. Build the issue | **Claude** | Pulls FLEX MLS stats, listing photos/agent attribution, writes copy in your voice, builds SEO package, builds hero image, previews the real rendered page |
| 3. Review & approve | **Todd** | Look at the preview, request changes, give final go-ahead |
| 4. Deploy to repo | **Claude Code** (as of 8/19/26 — replaces Kaya) | Same content-authoring Claude (in the Projects chat) hands off the finished post + assets, Claude Code places files, runs `build.py`, confirms clean build, commits, pushes to `main`, and also owns the Mailchimp template/campaign state directly via API |
| 5. Confirm live | **Todd** (spot check) | Open the live URL, eyeball hero/photos/links/footer |
| 6. Social posts | **Todd** | Video + carousel using the standing template (see Social section below) |
| 7. Email send | **Mailchimp, automatic** | Fires Tuesday 9 AM if new content is in the feed since last check. No action needed from anyone if steps 1–4 happened on schedule. |

---

## Per-issue checklist (what Todd brings each Thursday)

Same list as the standalone checklist doc already in this project — repeated here so the full cycle lives in one place:

- [ ] Market to feature (rotates through the nine service areas)
- [ ] Three Window Shopping MLS numbers **+ listing URLs** (for linking the address)
- [ ] Any active listings of Todd's own (for the optional "My Listings" section — skip if none)
- [ ] 1–2 Instagram follows
- [ ] What's caught your attention (Currently Obsessed With) + photo if available
- [ ] Go-ahead to build, then a second go-ahead to deploy

Claude handles without being asked: market stats via FLEX MLS, listing photos + agent/office attribution, SEO package, hero image, section blurbs, House Radio link, "not my listings" disclaimer, YoY/MoM framing (flagging anything that needs a gut-check).

---

## Deployment mechanics (as of 8/19/26 — Claude Code, no Kaya/Drive step)

1. Claude (Projects chat) finishes the issue content, packages the new post markdown + any new assets
2. Todd hands the bundle to Claude Code (or Claude Code pulls it directly if given access to the same output location)
3. Claude Code places files at the correct repo paths, runs `build.py`, confirms clean build, commits, pushes to `main`
4. Claude Code verifies the RSS feed's `<description>` field contains full post HTML (not just the teaser) before considering the push complete — see `CLAUDE.md` for why this matters
5. Mailchimp handles the send automatically the following Tuesday — no manual campaign creation or activation needed, that was a one-time setup step for issue 01.

---

## Social media — standing template

Same format every issue, content swapped in:

**Primary post — 30–45 second vertical video.** Todd on camera, same setup each time. One hook (the standout Nitty Gritty stat), a quick tease of one Window Shopping listing, "full issue's live, link in bio."

**Secondary post — carousel, fixed slide order:**
1. Hero card (issue name/number)
2. Key stat, big and bold
3–5. The three Window Shopping photos with price
6. CTA: "Full issue — link in bio"

**Stories, day-of only** — 2–3 slides, tag the IG follows featured, link sticker to the post.

*(Video script + carousel captions not yet drafted for issue 01 — Todd deferred this. Ask if wanted for future issues.)*

---

## What's still manual vs. what's automated

**Fully automated once armed (no action needed):**
- Mailchimp send, every Tuesday, checking for new content

**Requires a human/Kaya action each cycle:**
- Todd providing the issue inputs (this can't be automated away — it's Todd's judgment on market framing, listings, personal content)
- Claude building the issue (requires a live conversation each time)
- Todd approving before deployment
- Kaya deploying (automatic once Drive polling is confirmed working)
- Todd posting to social manually (Instagram direct-posting isn't connected yet — Buffer or Meta Graph API would be the next automation layer here if wanted)

**One-time setup, already done:**
- Domain authentication
- RSS campaign creation and first activation
- GitHub push access for Kaya
- build.py image support + CSS fixes + issue-list bug fix
