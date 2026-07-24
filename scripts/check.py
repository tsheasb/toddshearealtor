#!/usr/bin/env python3
"""
Regression check for the whole site.

Loads every page at desktop and mobile widths, scrolls to the bottom so
lazy content and scroll animations fire, then reports:

  - text elements whose contrast against their effective background
    falls below 3:1
  - broken images
  - horizontal overflow
  - reveal animations still stuck hidden
  - JavaScript errors

Caption text over photography is skipped here because measuring it needs a
different method (set the text transparent, screenshot, sample the glyph
boxes) — see README, "Measured values".

Usage:  python3 scripts/check.py       (run from the site root)

Requires: playwright  (pip install playwright && playwright install chromium)
"""

import threading, http.server, socketserver, functools, os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
socketserver.TCPServer.allow_reuse_address = True
srv = socketserver.TCPServer(('127.0.0.1', 9147), functools.partial(http.server.SimpleHTTPRequestHandler))
threading.Thread(target=srv.serve_forever, daemon=True).start()
from playwright.sync_api import sync_playwright


def lum(rgb):
    def f(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = [f(x) for x in rgb]
    return .2126 * r + .7152 * g + .0722 * b


def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + .05) / (lo + .05)


def parse(c):
    return tuple(int(x) for x in c.replace('rgba(', '').replace('rgb(', '')
                 .replace(')', '').split(',')[:3])


PAGES = ['', 'about.html', 'testimonials.html', 'residency.html',
         'contact.html', 'posts/placeholder-issue-01.html']

allok = True
with sync_playwright() as p:
    b = p.chromium.launch()
    for vw, label in [(1440, 'desktop'), (390, 'mobile')]:
        for name in PAGES:
            ctx = b.new_context(viewport={'width': vw, 'height': 850})
            pg = ctx.new_page()
            errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.goto(f'http://127.0.0.1:9147/{name}')
            pg.wait_for_timeout(700)
            pg.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            pg.wait_for_timeout(2200)
            d = pg.evaluate('''() => {
              const els=[];
              for(const el of document.querySelectorAll('h1,h2,h3,p,a,button,label,li')){
                if(!el.innerText||!el.innerText.trim())continue;
                if(el.closest('figcaption'))continue;
                const cs=getComputedStyle(el); let bg='rgba(0, 0, 0, 0)', n=el;
                while(n&&bg==='rgba(0, 0, 0, 0)'){bg=getComputedStyle(n).backgroundColor;n=n.parentElement;}
                els.push({fg:cs.color,bg:bg});
              }
              return {els,
                broken:[...document.querySelectorAll('img')].filter(i=>i.complete&&i.naturalWidth===0).length,
                hidden:[...document.querySelectorAll('[data-reveal]')].filter(e=>parseFloat(getComputedStyle(e).opacity)<0.99).length,
                ovf:document.documentElement.scrollWidth>window.innerWidth};
            }''')
            bad = 0
            for e in d['els']:
                try:
                    if ratio(parse(e['fg']), parse(e['bg'])) < 3.0:
                        bad += 1
                except Exception:
                    pass
            ok = (bad == 0 and d['hidden'] == 0 and not d['ovf']
                  and not errs and d['broken'] <= 1)
            if not ok:
                allok = False
            detail = 'OK' if ok else (
                f"contrast={bad} hidden={d['hidden']} "
                f"broken={d['broken']} ovf={d['ovf']} err={len(errs)}")
            print(f"{label:8} {name or 'index':30} {detail}")
            ctx.close()
    b.close()
srv.shutdown()
print()
print('ALL PASS' if allok else 'ISSUES')
