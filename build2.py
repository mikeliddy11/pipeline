import json, re, html
from urllib.parse import quote_plus
R = [list(r) for r in json.load(open('leads.json'))]
print('loaded', len(R))

# Corrections confirmed against live Google listings on 16 Nov
FIX = {
 'Coastal Roofing of South Florida': {'phone': '(561) 258-9064'},
 "Landscaping By Butcher's Nursery": {'city': 'Daytona Beach'},
 'The Garage Door Repair Docs LLC': {'city': 'Wellington'},
 'ZND-Great Pest Solution & Termite Pest Control': {'city': 'Palm Springs'},
}
SKIP = {'Brothers Mobile Mechanic': 'No Google listing matches this name and number. Do not dial.'}
for r in R:
    f = FIX.get(r[0])
    if f:
        if 'phone' in f: r[1] = f['phone']
        if 'city' in f: r[2] = f['city']

def tel(p): return re.sub(r'\D', '', p)
def gm(name, city):
    return 'https://www.google.com/maps/search/?api=1&query=' + quote_plus('%s %s FL' % (name, city))

def row(r):
    name, phone, city, niche, status, rating, reviews, demo = r
    flag = {'dead':'Site is dead','none':'No website','weak':'Weak site','ok':'Has a site'}[status]
    cls  = {'dead':'hot','none':'hot','weak':'warm','ok':'cool'}[status]
    stars = ('%.1f from %d reviews' % (rating, reviews)) if rating and reviews else ''
    meta = ' &middot; '.join([html.escape(city), html.escape(niche), stars]) if stars else ' &middot; '.join([html.escape(city), html.escape(niche)])
    d = ('<a class="demo" href="%s">Demo</a>' % demo) if demo else ''
    return ('<li class="%s"><a class="biz" href="%s" target="_blank" rel="noopener">'
            '<b>%s</b><span class="m">%s</span><span class="f">%s</span></a>'
            '<a class="call" href="tel:+1%s">%s</a>%s</li>'
            % (cls, gm(name, city), html.escape(name), meta, html.escape(flag), tel(phone), phone, d))

live = [r for r in R if r[0] not in SKIP]
hot  = sorted([r for r in live if r[4] in ('none','dead')], key=lambda r: -r[6])
warm = sorted([r for r in live if r[4]=='weak'], key=lambda r: -r[6])
cool = sorted([r for r in live if r[4]=='ok'], key=lambda r: r[0].lower())
skip = sorted([r for r in R if r[0] in SKIP], key=lambda r: r[0])

def block(t, rows, note):
    return '<section><h2>%s <span class="n">%d</span></h2><p class="note">%s</p><ul>%s</ul></section>' % (
        t, len(rows), note, ''.join(row(r) for r in rows))

body = (block('Call first', hot, 'No website or dead site. Tap the name to open its Google listing, tap the number to call.')
      + block('Weak site', warm, 'Site exists but looks thin. Softer opener.')
      + block('Has a site', cool, 'Deprioritise. No broken-site angle.'))
if skip:
    body += '<section><h2>Skip <span class="n">%d</span></h2><p class="note">%s</p><ul>%s</ul></section>' % (
        len(skip), html.escape(SKIP[skip[0][0]]), ''.join(row(r) for r in skip))

CSS = """*{box-sizing:border-box}
:root{--paper:#FDFDFB;--ink:#11161C;--muted:#5C6672;--navy:#13294B;--line:#E7E5E0;--hot:#B3261E;--warm:#8A5A00}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;-webkit-text-size-adjust:100%}
.wrap{max-width:760px;margin:0 auto;padding:0 14px 70px}
header{padding:22px 0 14px;border-bottom:1px solid var(--line)}
h1{font-size:19px;margin:0 0 6px;letter-spacing:-.01em}
.sub{margin:0;color:var(--muted);font-size:13.5px}
section{padding:26px 0 6px}
h2{font-size:13px;text-transform:uppercase;letter-spacing:.1em;margin:0;color:var(--muted)}
h2 .n{color:var(--ink);margin-left:6px}
.note{margin:6px 0 10px;font-size:12.5px;color:var(--muted)}
ul{list-style:none;margin:0;padding:0}
li{display:flex;align-items:center;gap:10px;padding:10px 0;border-bottom:1px solid var(--line)}
.biz{flex:1 1 auto;min-width:0;display:block;min-height:48px;padding:6px 0;text-decoration:none;color:inherit;cursor:pointer;-webkit-tap-highlight-color:rgba(19,41,75,.08)}
.biz b{display:inline;font-size:15.5px;font-weight:600;line-height:1.3;word-wrap:break-word;color:var(--ink);text-decoration:underline;text-decoration-color:rgba(92,102,114,.42);text-decoration-thickness:1px;text-underline-offset:3px}
.biz:hover b,.biz:focus-visible b{color:var(--navy);text-decoration-color:var(--navy);text-decoration-thickness:2px}
.biz:hover b::after,.biz:focus-visible b::after{content:" \2197";color:var(--navy);font-weight:500}
.biz:focus-visible{outline:2px solid var(--navy);outline-offset:3px}
@media (hover:none){.biz b::after{content:" \2197";color:var(--muted);font-weight:500;font-size:13px}}
.m{display:block;font-size:12.5px;color:var(--muted);margin-top:3px}
.f{display:inline-block;font-size:11px;letter-spacing:.05em;text-transform:uppercase;margin-top:5px;color:var(--muted)}
li.hot .f{color:var(--hot)} li.warm .f{color:var(--warm)}
.call{flex:0 0 auto;background:var(--navy);color:#fff;text-decoration:none;font-size:14px;font-weight:500;padding:13px 14px;border-radius:2px;min-height:48px;display:flex;align-items:center;white-space:nowrap}
.demo{flex:0 0 auto;font-size:12px;color:var(--navy);text-decoration:none;border-bottom:1px solid var(--navy);padding:14px 2px;min-height:48px;display:flex;align-items:center}
.g{font-size:11.5px;color:var(--muted);margin-top:2px;display:block}
@media (max-width:420px){.call{font-size:13px;padding:12px 11px}}"""

HEAD = ('<!DOCTYPE html>\n<html lang="en"><head><meta charset="utf-8">\n'
 '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
 '<meta name="robots" content="noindex, nofollow">\n'
 '<title>Lead list</title>\n<style>' + CSS + '</style></head><body><div class="wrap">\n'
 '<header><h1>Lead list, ' + str(len(live)) + ' to call</h1>\n'
 '<p class="sub">Numbers checked against live Google listings, 16 Nov. Tap a business name to open its Google listing. Tap the blue number to call.</p></header>\n')

open('index.html','w').write(HEAD + body + '\n</div></body></html>\n')
print('hot', len(hot), '| weak', len(warm), '| cool', len(cool), '| skip', len(skip))
print('google links:', open('index.html').read().count('google.com/maps/search'))
