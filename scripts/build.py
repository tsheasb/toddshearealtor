#!/usr/bin/env python3
"""
SB Residency build script.

Reads markdown files from posts/, writes:
  - posts/<slug>.html        one page per issue
  - rss.xml                  feed Mailchimp watches
  - updates the issue list on residency.html and index.html

Usage:  python3 scripts/build.py
"""

import os
import re
import html
import glob
from datetime import datetime, timezone
from email.utils import format_datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(ROOT, "posts")

SITE_URL = "https://toddshearealtor.com"
SITE_TITLE = "SB Residency — Todd Shea Real Estate"
SITE_DESC = ("Every other week: the Santa Barbara market, three listings worth a look, "
             "and whatever's holding my attention.")

# ---------------------------------------------------------------- parsing

def parse_front_matter(raw):
    """Split '---' front matter from body. Returns (meta dict, body str)."""
    if not raw.startswith("---"):
        return {}, raw
    parts = raw.split("---", 2)
    if len(parts) < 3:
        return {}, raw
    meta = {}
    for line in parts[1].strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, parts[2].strip()


def md_to_html(md):
    """Minimal markdown -> HTML. Handles h2, bold, links, lists, paragraphs."""
    out = []
    lines = md.split("\n")
    i = 0
    in_list = False

    def inline(t):
        t = html.escape(t, quote=False)
        t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
        t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
        t = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", t)
        return t

    while i < len(lines):
        line = lines[i].rstrip()

        if not line.strip():
            if in_list:
                out.append("</ul>")
                in_list = False
            i += 1
            continue

        if line.startswith("## "):
            if in_list:
                out.append("</ul>")
                in_list = False
            out.append(f"<h2>{inline(line[3:].strip())}</h2>")
        elif line.startswith("- "):
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{inline(line[2:].strip())}</li>")
        else:
            if in_list:
                out.append("</ul>")
                in_list = False
            out.append(f"<p>{inline(line.strip())}</p>")
        i += 1

    if in_list:
        out.append("</ul>")
    return "\n".join(out)


def load_posts():
    posts = []
    for path in glob.glob(os.path.join(POSTS_DIR, "*.md")):
        with open(path, encoding="utf-8") as f:
            meta, body = parse_front_matter(f.read())

        slug = os.path.splitext(os.path.basename(path))[0]
        slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", slug)

        try:
            date = datetime.strptime(meta.get("date", ""), "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except ValueError:
            date = datetime.now(timezone.utc)

        posts.append({
            "slug": slug,
            "title": meta.get("title", "Untitled"),
            "date": date,
            "number": int(meta.get("number", 0) or 0),
            "teaser": meta.get("teaser", ""),
            "hero": meta.get("hero", ""),
            "hero_alt": meta.get("hero_alt", ""),
            "body_html": md_to_html(body),
        })

    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


# ---------------------------------------------------------------- templates

SHELL_HEADER = """<header class="site-header">
  <div class="shell site-header__inner">
    <a class="site-header__logo" href="/" aria-label="Todd Shea Real Estate — home">
      <img src="/assets/shea-secondary-on-dark.svg" alt="Todd Shea Real Estate">
    </a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav class="nav" id="nav" aria-label="Main">
      <a href="/">Home</a>
      <a href="/about.html">Todd</a>
      <a href="/testimonials.html">Clients</a>
      <a href="/residency.html" aria-current="page">SB Residency</a>
      <a href="/contact.html">Contact</a>
    </nav>
  </div>
</header>"""

SHELL_FOOTER = """<footer class="site-footer">
  <div class="shell">
    <div class="site-footer__grid">
      <div class="site-footer__mark">
        <img src="/assets/shea-secondary-on-dark.svg" alt="Todd Shea Real Estate">
        <p class="muted" style="font-size:0.85rem">Santa Ynez Valley to Ventura.<br>Based in Santa Barbara.</p>
      </div>
      <div>
        <h4 class="muted">Site</h4>
        <ul class="footer-links">
          <li><a href="/about.html">Todd</a></li>
          <li><a href="/testimonials.html">Clients</a></li>
          <li><a href="/residency.html">SB Residency</a></li>
          <li><a href="/contact.html">Contact</a></li>
          <li><a href="/rss.xml">RSS</a></li>
        </ul>
      </div>
      <div>
        <h4 class="muted">Reach me</h4>
        <ul class="footer-links">
          <li><a href="tel:8054537730">(805) 453-7730</a></li>
          <li><a href="mailto:toddshea@bhhscal.com">toddshea@bhhscal.com</a></li>
          <li><a href="https://www.instagram.com/toddshearealtor/" target="_blank" rel="noopener">Instagram</a></li>
        </ul>
      </div>
    </div>
    <div class="legal">
      <div class="legal__identity">
        <p><strong>Todd Shea</strong> &middot; REALTOR<sup>&reg;</sup> &middot; DRE #02028163<br>
        Berkshire Hathaway HomeServices California Properties &middot; DRE #01317331<br>
        Montecito / Santa Barbara Office</p>
      </div>
      <p>&copy; 2026 Berkshire Hathaway HomeServices California Properties (BHHSCP) is a member of the
      franchise system of BHH Affiliates LLC. BHHS and the BHHS symbol are registered service marks of
      Columbia Insurance Company, a Berkshire Hathaway affiliate. BHH Affiliates LLC and BHHSCP do not
      guarantee accuracy of all data including measurements, conditions, and features of property.
      Information is obtained from various sources and will not be verified by broker or MLS. Buyer is
      advised to independently verify the accuracy of that information.</p>
      <p>This website is not the official website of Berkshire Hathaway HomeServices California Properties.
      Equal Housing Opportunity.</p>
      <div class="legal__badges">
        <span class="legal__badge-slot">[ BHHS California Properties lockup ]</span>
        <span class="legal__badge-slot">[ Equal Housing Opportunity ]</span>
        <span class="legal__badge-slot">[ REALTOR&reg; ]</span>
      </div>
      <p class="legal__note">Placeholder: drop the official BHHS lockup, Equal Housing, and REALTOR&reg;
      artwork into the slots above and delete this line. Confirm final placement with BHHS marketing
      before launch.</p>
    </div>
  </div>
</footer>"""


def render_post(post):
    hero = ""
    if post["hero"]:
        hero = (f'<div class="article__hero"><img src="{html.escape(post["hero"])}" '
                f'alt="{html.escape(post["hero_alt"])}"></div>')
    else:
        hero = '<div class="article__hero ph" data-ph="Issue hero — 1600×900"></div>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(post['title'])} — SB Residency</title>
<meta name="description" content="{html.escape(post['teaser'])}">
<link rel="icon" href="/assets/shea-mark-on-dark-128.png">
<link rel="alternate" type="application/rss+xml" title="SB Residency" href="/rss.xml">
<link rel="stylesheet" href="/css/site.css">
<link rel="stylesheet" href="/css/components.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>

{SHELL_HEADER}

<main id="main">
  <article class="section">
    <div class="shell">
      <div class="article">
        <div class="stripes"><span></span><span></span></div>
        <p class="article__meta">No. {post['number']:03d} · {post['date'].strftime('%B %-d, %Y')}</p>
        <h1 style="font-size:clamp(2rem,4.5vw,3.4rem);margin-bottom:2rem">{html.escape(post['title'])}</h1>
        {hero}
        {post['body_html']}
        <div class="article__signoff">
          <div class="stripes"><span></span><span></span></div>
          <p class="muted" style="font-size:0.9rem">Todd Shea · Santa Barbara<br>
          <a href="/residency.html" style="color:var(--gold)">All issues</a> ·
          <a href="/rss.xml" style="color:var(--gold)">RSS</a></p>
        </div>
      </div>
    </div>
  </article>
</main>

{SHELL_FOOTER}

<script src="/js/site.js"></script>
</body>
</html>
"""


def render_issue_list(posts, limit=None):
    items = posts[:limit] if limit else posts
    rows = []
    for p in items:
        rows.append(
            f'        <a class="issue" href="/posts/{p["slug"]}.html">\n'
            f'          <span class="issue__date">{p["date"].strftime("%b %-d, %Y")}</span>\n'
            f'          <span>\n'
            f'            <span class="issue__title">{html.escape(p["title"])}</span>\n'
            f'            <p class="issue__sub">{html.escape(p["teaser"])}</p>\n'
            f'          </span>\n'
            f'          <span class="issue__no">No. {p["number"]:03d}</span>\n'
            f'        </a>'
        )
    return "\n\n".join(rows)


def render_rss(posts):
    now = format_datetime(datetime.now(timezone.utc))
    items = []
    for p in posts:
        link = f"{SITE_URL}/posts/{p['slug']}.html"
        items.append(f"""    <item>
      <title>{html.escape(p['title'])}</title>
      <link>{link}</link>
      <guid isPermaLink="true">{link}</guid>
      <pubDate>{format_datetime(p['date'])}</pubDate>
      <description>{html.escape(p['teaser'])}</description>
      <content:encoded><![CDATA[{p['body_html']}]]></content:encoded>
    </item>""")

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
     xmlns:content="http://purl.org/rss/1.0/modules/content/"
     xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{SITE_TITLE}</title>
    <link>{SITE_URL}/residency.html</link>
    <atom:link href="{SITE_URL}/rss.xml" rel="self" type="application/rss+xml"/>
    <description>{SITE_DESC}</description>
    <language>en-us</language>
    <lastBuildDate>{now}</lastBuildDate>
{chr(10).join(items)}
  </channel>
</rss>
"""


def splice_issue_list(path, new_list):
    """Replace the contents of <div class="issue-list" data-issue-list> ... </div>."""
    if not os.path.exists(path):
        return False
    with open(path, encoding="utf-8") as f:
        content = f.read()

    pattern = re.compile(
        r'(<div class="issue-list" data-issue-list>)(.*?)(\n\s*</div>)',
        re.DOTALL
    )
    if not pattern.search(content):
        print(f"  ! issue-list container not found in {os.path.basename(path)}")
        return False

    updated = pattern.sub(lambda m: m.group(1) + "\n\n" + new_list + m.group(3), content)
    with open(path, "w", encoding="utf-8") as f:
        f.write(updated)
    return True


# ---------------------------------------------------------------- main

def main():
    posts = load_posts()
    if not posts:
        print("No posts found in posts/")
        return

    for p in posts:
        out = os.path.join(POSTS_DIR, f"{p['slug']}.html")
        with open(out, "w", encoding="utf-8") as f:
            f.write(render_post(p))
        print(f"  wrote posts/{p['slug']}.html")

    with open(os.path.join(ROOT, "rss.xml"), "w", encoding="utf-8") as f:
        f.write(render_rss(posts))
    print("  wrote rss.xml")

    if splice_issue_list(os.path.join(ROOT, "residency.html"), render_issue_list(posts)):
        print("  updated residency.html")
    if splice_issue_list(os.path.join(ROOT, "index.html"), render_issue_list(posts, limit=3)):
        print("  updated index.html")

    print(f"\nDone. {len(posts)} issue(s).")


if __name__ == "__main__":
    main()
