# Issue bundle checklist (for the Projects chat)

Use this for every issue from Issue 08 on. The site layout, the feed, the build guards,
and the Mailchimp template are already set up in this repo. A bundle needs two things only:
**one post `.md` file and its images.**

## Do not include

- CSS, `build.py` or `check.py` changes, layout notes, or Mailchimp template instructions.
  The repo owns these. A past bundle repeated old instructions that no longer matched the
  live setup (for example, it named the wrong Mailchimp merge tag).
- Handoff or "reskin" documents, a preview HTML page, or a copy of the template lock.

## The post file

- **Name:** `YYYY-MM-DD-slug.md`. The slug becomes the page URL.
- **Date:** a Tuesday, 14 days after the previous issue. Issue 07 is 2026-10-27, so
  **Issue 08 is 2026-11-10**, then 2026-11-24, and so on.
- **Front matter**, all six fields required:
  - `title:` must start with `The SB Residency: ` (the build stops if it doesn't)
  - `date:` as above
  - `number:` the next whole number (the build stops on a missing or repeated number)
  - `teaser:` one plain-text sentence, under about 155 characters. It is the meta
    description, the inbox preview text, and the RSS summary, so no HTML.
  - `hero:` `/assets/posts/2026-issue-0N-<slug>-hero.jpg`
  - `hero_alt:` describes the photo plainly. Do not repeat the issue title.
- **Structure:** the standard sections and locked blurbs, in the standard order.
  The post ends with its own "Ready When You Are" section. The email template does not
  add a second one.
- **No em dashes or en dashes anywhere.** The build stops if it finds one.
- **Every listing that is not Todd's:** the flexmls share link, an agent and office
  credit, the MLS number, and the "none of the above are my listings" note. Use the
  short broker name, Berkshire Hathaway HomeServices.
- **Market stats:** name the area, the date window, the source, and the counting notes.

## Images

All images are self-hosted in `assets/posts/` and named `2026-issue-0N-<name>.jpg`.
Reference them in the post as `/assets/posts/2026-issue-0N-<name>.jpg`.

| Image | Rule |
|---|---|
| Hero | A **photo**, not a graphic. Landscape, **2400px wide**, JPEG quality 90. No text on it. Todd's own photo or one he has the rights to. Not a listing photo. |
| Body photos | JPEG, **landscape, at least 1600px wide**. They run edge to edge. |
| Portrait, square, or small photos (under 1600px wide) | Add `-inset` to the filename, for example `2026-issue-0N-cafe-inset.jpg`. They stay in the text column instead of being stretched. |
| House Radio cover | A copy named `2026-issue-0N-house-radio-cover.jpg` for each issue. It always stays in the column. |

The build stops if the post points at an image that is not in the bundle.

## What Claude Code does with a bundle

1. Pulls any changes from GitHub, builds, and runs the safeguards.
2. Checks every listing against FLEX MLS (price, beds, baths, agent, office).
3. Previews the pages and the feed, then commits locally.
4. **Waits for Todd's go-ahead before any push.**
5. After the push, confirms the live site and feed. The Mailchimp template needs no
   edit for a normal issue. A test email to Todd is optional.
