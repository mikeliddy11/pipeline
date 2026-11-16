import re, html, json
DEMOS = {
 'https://mikeliddy11.github.io/palm-atlantic-handyman/': 'Palm Atlantic',
 'https://media.base44.com/files/public/6adcd26cedd24c8c3f05e00a/376d87b4e_standalone.html': 'J and S Exterior',
 'https://media.base44.com/files/public/6adcd26cedd24c8c3f05e00a/c91fb1fea_standalone.html': 'Wave Electrical',
 'https://media.base44.com/files/public/6adcd26cedd24c8c3f05e00a/bdd14ae66_togy-v5-standalone.html': 'Togy',
}
R = [
("5T'S Mobile mechanic","(561) 763-6636","Royal Palm Beach","mobile","none",4.9,77,""),
("A & A Hauling Services, junk removal and demolition","(561) 797-3370","Lake Worth","junk","none",5.0,33,""),
("A G\u2019s Mobile Mechanic LLC","(561) 260-3309","Royal Palm Beach","mobile","none",5.0,97,""),
("AGC Auto Mechanics, LLC","(561) 714-7594","Royal Palm Beach","mobile","none",5.0,131,""),
("AR Power Electric","(561) 704-3545","Boynton Beach","electrician","ok",5.0,75,""),
("Above and Beyond Pest Control","(561) 725-9784","Lake Worth","pest","weak",4.8,482,""),
("Accurate Painting of the Palm Beaches","(561) 594-7379","West Palm Beach","painting","none",4.7,62,""),
("Action Garage Door Repair","(844) 242-1172","Royal Palm Beach","garage","none",5.0,88,""),
("Air Plus of South Florida, Inc.","(561) 371-0971","West Palm Beach","hvac","weak",4.9,366,""),
("All American Mobile Services LLC","(561) 430-0196","West Palm Beach","auto","dead",5.0,139,""),
("All Clear Auto Detailing & Window Tinting","(561) 255-9785","West Palm Beach","auto","none",4.9,59,""),
("All Things Moving Storage","(561) 632-8082","Lake Worth","junk","weak",4.9,50,""),
("All Town Plumbing Inc.","(561) 455-6532","Lake Worth","plumber","none",4.9,98,""),
("American Pressure Clean","(954) 562-5821","Greenacres","pressure washing","none",4.6,328,"https://is.gd/apclean2"),
("American Tree Services","(561) 373-6117","Greenacres","tree","none",4.4,15,""),
("Appliance Worx","(561) 808-3132","West Palm Beach","appliance","dead",5.0,198,""),
("Aqua Force Pressure Cleaning & Roof Cleaning","(954) 798-8333","West Palm Beach","pressure washing","weak",5.0,666,""),
("Bellosa's Pressure Washing LLC.","(561) 452-6218","Boynton Beach","pressure washing","none",5.0,32,""),
("Boston Electric LLC","(561) 570-7788","West Palm Beach","electrician","weak",4.9,225,""),
("Brian's Mobile Mechanic","(561) 574-4395","Royal Palm Beach","mobile","none",4.9,39,""),
("Brothers Mobile Mechanic","(561) 412-7439","Royal Palm Beach","mobile","none",4.8,72,""),
("Bud's Mobile Auto Repair","(561) 324-4096","Royal Palm Beach","mobile","none",4.7,34,""),
("Canoa Tree Service inc","(561) 301-8937","Greenacres","tree","none",4.9,84,""),
("CertaPro Painters of Boynton Beach, FL","(561) 318-0221","West Palm Beach","painting","ok",4.8,172,""),
("City Skyline Painting","(561) 727-8778","West Palm Beach","painting","ok",4.9,45,""),
("Clayton Merritt Services LLC","(561) 667-3831","Royal Palm Beach","handyman","none",4.8,32,""),
("Clean & Handy","(561) 375-4288","Royal Palm Beach","handyman","none",4.3,29,""),
("Coastal Copper Gutters Inc.","(561) 572-7865","Boynton Beach","roofing","ok",5.0,112,""),
("Coastal Roofing of South Florida","(561) 783-4185","Boynton Beach","roofing","ok",5.0,166,""),
("Conserva Irrigation of North Palm Beach","(561) 220-3146","Royal Palm Beach","lawn","weak",5.0,303,""),
("Cool Front Hvac, Inc","(561) 801-2206","West Palm Beach","hvac","none",5.0,398,""),
("Davies Plumbing Services","(561) 707-6884","Lake Worth","plumber","none",5.0,214,""),
("Dm Pressure Washing and property services","(561) 888-1900","Lake Worth","pressure washing","weak",5.0,77,""),
("Double A Electric LLC","(561) 377-5510","West Palm Beach","electrician","none",4.9,138,""),
("E Aguilar Landscaping INC","(561) 596-4437","Greenacres","tree","dead",5.0,47,""),
("Eddie's Pressure Cleaning LLC","(561) 480-6586","Lake Worth","pressure washing","none",5.0,17,""),
("Elite Cuts Landscaping","(561) 385-7967","Royal Palm Beach","lawn","none",4.9,22,""),
("Euphoric Cleaning Services","(561) 703-5663","Boynton Beach","cleaning","none",5.0,22,""),
("FHJ MOBILE AUTO REPAIR LLC","(954) 655-2704","Royal Palm Beach","mobile","none",4.9,61,""),
("Frankie Shinez Mobile Detailing","(631) 921-8947","West Palm Beach","auto","none",5.0,72,""),
("Garage Door Doctors - Boynton","(561) 257-5598","Royal Palm Beach","garage","none",5.0,82,""),
("Global Power & Ac Corp","(561) 286-7538","Boynton Beach","electrician","ok",5.0,735,""),
("Halpert Air","(561) 318-7537","Greenacres","hvac","none",4.8,41,""),
("Handy Danny Top Notch Services LLC","(561) 806-8111","Royal Palm Beach","handyman","none",5.0,49,""),
("Handyman All Around","(561) 270-5878","Royal Palm Beach","handyman","ok",4.9,81,""),
("Horizon Distributors","(561) 533-1481","Boynton Beach","landscaping","weak",4.4,44,""),
("Hunk\u2019s Junk Removal","(561) 508-1287","Lake Worth","junk","none",5.0,37,""),
("J & H Tree Service","(561) 856-4027","West Palm Beach","tree","weak",4.8,239,""),
("J&S Exterior Cleaning Solutions","(561) 358-9622","West Palm Beach","pressure washing","dead",5.0,300,""),
("J.W. Electric of the Palm Beaches, Inc.","(561) 633-9472","Boynton Beach","electrician","none",4.6,35,""),
("JC Innovative construction INC","(561) 729-7424","Greenacres","concrete","dead",4.9,64,""),
("JDL Electrical & Generator Services","(561) 637-8269","Boynton Beach","electrician","none",5.0,108,""),
("JP Volt Electric INC","(786) 451-1973","West Palm Beach","electrician","dead",0.0,0,""),
("Juliomovil Mechanic","(786) 532-0835","Royal Palm Beach","mobile","none",4.6,21,""),
("KDB Pressure Washing And Junk Removal LLC","(561) 720-5427","Lake Worth","junk","none",5.0,25,""),
("KJ Quick Fix LLC","(754) 269-0425","Royal Palm Beach","handyman","none",4.8,19,""),
("LRU LANDSCAPING","(561) 577-4960","Royal Palm Beach","lawn","none",4.9,108,""),
("Landscaping By Butcher's Nursery","(386) 255-0050","West Palm Beach","landscaping","weak",4.9,662,""),
("Lantana Dumpster LLC","(561) 444-8150","Lake Worth","junk","none",4.9,37,""),
("Legacy Plumbing Experts","(561) 909-9227","West Palm Beach","plumber","weak",4.6,196,""),
("Magic Clean Maids","(347) 620-0803","Boynton Beach","cleaning","dead",5.0,51,""),
("Mendez Brothers Lawn Services","(561) 584-3529","Royal Palm Beach","lawn","ok",5.0,48,""),
("Mickey's Plumbing","(561) 659-3770","West Palm Beach","plumber","weak",4.7,160,""),
("Migdael Mobile Mechanic","(561) 906-2211","Royal Palm Beach","mobile","none",4.7,44,""),
("Mobile TV & Appliance Repair","(561) 969-2636","West Palm Beach","appliance","dead",4.9,181,""),
("Mobile mechanic","(561) 543-6773","Royal Palm Beach","mobile","none",4.7,36,""),
("Monacco Garage Door services","(786) 530-6774","Royal Palm Beach","garage","none",5.0,56,""),
("Mower Mate, Inc.","(561) 793-4574","Royal Palm Beach","lawn","ok",4.6,67,""),
("Mr. Foreign Mobile Mechanic & Roadside Assistance","(561) 698-0238","Royal Palm Beach","mobile","none",5.0,31,""),
("Painting Green Inc","(561) 255-0379","West Palm Beach","painting","none",4.6,41,""),
("Palm Atlantic Handyman Services","(954) 607-0846","West Palm Beach","handyman","none",5.0,140,"https://mikeliddy11.github.io/palm-atlantic-handyman/"),
("Palm Beach Gardens Pool Cleaners","(561) 448-7116","West Palm Beach","pool","ok",4.9,46,""),
("Palm Beach Mobile Mechanic","(305) 561-4055","Royal Palm Beach","mobile","none",4.9,29,""),
("Palm Beach Pool Service, LLC","(561) 406-8271","West Palm Beach","pool","weak",5.0,45,""),
("Patterson Electrical Contracting LLC","(561) 946-8568","West Palm Beach","electrician","weak",5.0,224,""),
("Paul Stetson Tree Service and Pressure Cleaning","(561) 373-8764","West Palm Beach","tree","weak",4.9,182,""),
("Perfect Plumbing & Rooter","(561) 440-3569","Lake Worth","plumber","none",4.6,81,""),
("Pool Service Plus","(561) 635-7665","West Palm Beach","pool","ok",4.6,279,""),
("Premier Detailers","(561) 717-9961","West Palm Beach","auto","dead",4.6,55,""),
("Pressure Cleaning Pros","(561) 667-1688","Lake Worth","pressure washing","none",4.8,71,""),
("Pro Clean Pressure Washing 561 LLC","(561) 889-4272","West Palm Beach","pressure washing","dead",5.0,139,""),
("Prompt Painters","(561) 425-6663","West Palm Beach","painting","none",4.9,33,""),
("Pure Gloss Car Detailing","(561) 726-6059","West Palm Beach","auto","none",4.9,22,""),
("Pure Quality Mobile Detailing LLC","(561) 729-7290","Lake Worth","auto","none",5.0,60,""),
("R&R1 Pressure Cleaning and Painting","(561) 255-9339","Lake Worth","pressure washing","dead",4.8,136,""),
("RNC Handyman Services LLC","(561) 506-7480","Royal Palm Beach","handyman","ok",5.0,51,""),
("Ricca's Home Improvement LLC","(561) 531-4180","Royal Palm Beach","handyman","none",5.0,55,""),
("Royal Palm auto diagnostic and mobile mechanic","(305) 753-7058","Royal Palm Beach","mobile","none",4.6,46,""),
("Ryan Plumbing Inc","(561) 649-9101","Lake Worth","plumber","none",4.8,62,""),
("S&a Mobile Detailing","(561) 352-0435","West Palm Beach","auto","none",5.0,41,""),
("SeaBreeze Roofing & Sheet Metal Incorporated","(561) 292-3457","Boynton Beach","roofing","weak",4.7,514,""),
("Simple Lawn Care, Inc.","(561) 201-0873","Royal Palm Beach","lawn","none",4.1,16,""),
("Stand Strong Fencing of Boynton Beach","(561) 956-3384","Greenacres","fencing","weak",4.9,75,""),
("Style & Profile Mobile Detailing","(561) 662-4857","West Palm Beach","auto","none",4.9,27,""),
("Suncoast Electric and Air","(561) 406-4945","Boynton Beach","electrician","weak",4.9,482,""),
("Suncoast Home Solutions","(561) 475-4210","Boynton Beach","electrician","ok",4.8,114,""),
("Sunny Blue Pros Pool Service","(561) 342-5522","West Palm Beach","pool","ok",4.9,81,""),
("Supreme Suds Car Detailing","(561) 468-6197","West Palm Beach","auto","none",5.0,15,""),
("Tech In Place","(561) 479-9833","Boynton Beach","electrician","none",5.0,126,""),
("Telford Cooling, LLC.","(561) 203-0365","West Palm Beach","hvac","weak",4.9,341,""),
("The Blue Pool Guys","(561) 264-6667","West Palm Beach","pool","ok",4.8,101,""),
("The Garage Door Repair Docs LLC","(561) 200-9265","Royal Palm Beach","garage","none",5.0,30,""),
("Togy's Barber Studio","(603) 322-0714","West Palm Beach","barber","dead",5.0,161,"https://media.base44.com/files/public/6adcd26cedd24c8c3f05e00a/bdd14ae66_togy-v5-standalone.html"),
("Touched by Grace Pressure Cleaning","(561) 246-0354","West Palm Beach","pressure washing","dead",0.0,0,""),
("Triple Quality Painting, Inc.","(754) 245-0859","West Palm Beach","painting","none",4.9,129,""),
("Tropical Blue Pool & Spa Care","(561) 286-4411","West Palm Beach","pool","none",4.8,178,""),
("Turino Mobile Mechanic LLC","(561) 797-0908","Royal Palm Beach","mobile","none",4.2,111,""),
("Turner Pest Control","(561) 791-2400","Lake Worth","pest","weak",4.9,506,""),
("Us Latino Handyman Services","(561) 388-3382","Royal Palm Beach","handyman","none",4.9,35,""),
("Wave Electrical","(561) 307-9529","West Palm Beach","electrician","weak",4.9,317,"https://media.base44.com/files/public/6adcd26cedd24c8c3f05e00a/c91fb1fea_standalone.html"),
("West Palm Beach Garage Pros","(561) 803-0216","Royal Palm Beach","garage","none",5.0,26,""),
("West Palm Mobile Mechanic","(561) 562-9542","Royal Palm Beach","mobile","none",5.0,47,""),
("Wise House Pest Control","(561) 727-8239","West Palm Beach","pest","weak",5.0,647,""),
("ZND-Great Pest Solution & Termite Pest Control","(561) 532-5115","Lake Worth","pest","none",4.5,15,""),
]
assert len(R) == len({r[1] for r in R}), "duplicate phone numbers"

def tel(p): return re.sub(r'\D', '', p)
def row(r):
    name, phone, city, niche, status, rating, reviews, demo = r
    digits = tel(phone)
    stars = ('%.1f' % rating) if rating else ''
    meta = [city, niche]
    if stars: meta.append(stars + ' from ' + str(int(reviews)) + ' reviews' if reviews else stars + ' rating')
    flag = {'dead':'Site is dead','none':'No website','weak':'Weak site','ok':'Has a site'}[status]
    cls = {'dead':'hot','none':'hot','weak':'warm','ok':'cool'}[status]
    d = ('<a class="demo" href="%s">Demo</a>' % demo) if demo else ''
    return ('<li class="%s"><div class="l"><b>%s</b><span class="m">%s &middot; %s</span>'
            '<span class="f">%s</span></div><a class="call" href="tel:+1%s">%s</a>%s</li>'
            % (cls, html.escape(name), html.escape(' \u00b7 '.join(meta[:2])), html.escape(flag),
               html.escape(stars + '/' + str(int(reviews)) + ' Google' if stars and reviews else flag),
               digits, phone, d))

hot  = sorted([r for r in R if r[4] in ('none','dead')], key=lambda r: -r[6])
warm = sorted([r for r in R if r[4]=='weak'], key=lambda r: -r[6])
cool = sorted([r for r in R if r[4]=='ok'], key=lambda r: r[0].lower())

def block(title, rows, note):
    return '<section><h2>%s <span class="n">%d</span></h2><p class="note">%s</p><ul>%s</ul></section>' % (
        title, len(rows), note, ''.join(row(r) for r in rows))

body = (block('Call first', hot, 'No website, or their site is dead. Best angle.')
      + block('Weak site', warm, 'Site exists but looks thin. Softer opener only.')
      + block('Has a site', cool, 'Deprioritise. No broken-site angle.'))
HEAD = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Lead list</title>
<style>
:root{--paper:#FDFDFB;--ink:#11161C;--muted:#5C6672;--navy:#13294B;--line:#E7E5E0;--hot:#B3261E;--warm:#8A5A00}
*{box-sizing:border-box}
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
li{display:flex;align-items:center;gap:10px;padding:12px 0;border-bottom:1px solid var(--line)}
.l{flex:1 1 auto;min-width:0}
b{display:block;font-size:15.5px;font-weight:600;line-height:1.3;word-wrap:break-word}
.m{display:block;font-size:12.5px;color:var(--muted);margin-top:2px}
.f{display:inline-block;font-size:11px;letter-spacing:.05em;text-transform:uppercase;margin-top:5px;color:var(--muted)}
li.hot .f{color:var(--hot)} li.warm .f{color:var(--warm)}
.call{flex:0 0 auto;background:var(--navy);color:#fff;text-decoration:none;font-size:14px;font-weight:500;padding:13px 14px;border-radius:2px;min-height:48px;display:flex;align-items:center;white-space:nowrap}
.demo{flex:0 0 auto;font-size:12px;color:var(--navy);text-decoration:none;border-bottom:1px solid var(--navy);padding:14px 2px;min-height:48px;display:flex;align-items:center}
@media (max-width:420px){.call{font-size:13px;padding:12px 11px}}
</style></head><body><div class="wrap">
<header><h1>Lead list, """ + str(len(R)) + """ businesses</h1>
<p class="sub">Pulled 16 Nov. Tap a number to call. Sorted by review count inside each group. Re-check any claim live before you use it.</p></header>
"""
open('index.html','w').write(HEAD + body + "\n</div></body></html>\n")
print('rows:', len(R), '| hot:', len(hot), '| weak:', len(warm), '| has site:', len(cool))
json.dump([list(r) for r in R], open('leads.json','w'))
