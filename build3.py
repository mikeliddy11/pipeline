import json, re, html
from urllib.parse import quote_plus

R = [list(r) for r in json.load(open('leads.json'))]

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
def esc(x): return html.escape(str(x), quote=True)

def row(r):
    name, phone, city, niche, status, rating, reviews, demo = r
    flag = {'dead':'Site is dead','none':'No website','weak':'Weak site','ok':'Has a site'}[status]
    cls  = {'dead':'hot','none':'hot','weak':'warm','ok':'cool'}[status]
    meta = ' &middot; '.join([esc(city), esc(niche)])
    if rating and reviews:
        meta += ' &middot; %.1f from %d reviews' % (rating, reviews)
    d = ('<a class="demo" href="%s">Demo</a>' % demo) if demo else ''
    return ('<li class="%s" data-phone="%s">'
            '<a class="biz" href="%s" target="_blank" rel="noopener">'
            '<b>%s</b><span class="m">%s</span><span class="f">%s</span>'
            '<span class="status" aria-live="polite"></span></a>'
            '<a class="call" href="tel:+1%s">%s</a>'
            '<button class="log" type="button" data-name="%s" data-phone="%s">Log</button>%s</li>'
            % (cls, esc(phone), gm(name, city), esc(name), meta, esc(flag),
               tel(phone), phone, esc(name), esc(phone), d))

live = [r for r in R if r[0] not in SKIP]
hot  = sorted([r for r in live if r[4] in ('none','dead')], key=lambda r: -r[6])
warm = sorted([r for r in live if r[4]=='weak'], key=lambda r: -r[6])
cool = sorted([r for r in live if r[4]=='ok'], key=lambda r: r[0].lower())
skip = sorted([r for r in R if r[0] in SKIP], key=lambda r: r[0])

def block(t, rows, note):
    return ('<section><h2>%s <span class="n">%d</span></h2><p class="note">%s</p><ul>%s</ul></section>'
            % (t, len(rows), note, ''.join(row(r) for r in rows)))

body = (block('Call first', hot, 'No website or dead site. Tap the name for its Google listing, the number to call, Log when you hang up.')
      + block('Weak site', warm, 'Site exists but looks thin. Softer opener.')
      + block('Has a site', cool, 'Deprioritise. No broken-site angle.'))
if skip:
    body += ('<section><h2>Skip <span class="n">%d</span></h2><p class="note">%s</p><ul>%s</ul></section>'
             % (len(skip), esc(SKIP[skip[0][0]]), ''.join(row(r) for r in skip)))

CSS = """*{box-sizing:border-box}
:root{--paper:#FDFDFB;--ink:#11161C;--muted:#5C6672;--navy:#13294B;--line:#E7E5E0;--hot:#B3261E;--warm:#8A5A00;--green:#1B6B3A}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;-webkit-text-size-adjust:100%}
.wrap{max-width:760px;margin:0 auto;padding:0 14px 90px}
header{padding:22px 0 14px;border-bottom:1px solid var(--line)}
h1{font-size:19px;margin:0 0 6px;letter-spacing:-.01em}
.sub{margin:0;color:var(--muted);font-size:13.5px}
section{padding:24px 0 6px}
h2{font-size:13px;text-transform:uppercase;letter-spacing:.1em;margin:0;color:var(--muted)}
h2 .n{color:var(--ink);margin-left:6px}
.note{margin:6px 0 10px;font-size:12.5px;color:var(--muted)}
ul{list-style:none;margin:0;padding:0}
li{display:flex;align-items:center;gap:8px;padding:10px 0;border-bottom:1px solid var(--line)}
.biz{flex:1 1 auto;min-width:0;display:block;min-height:48px;padding:6px 0;text-decoration:none;color:inherit;cursor:pointer;-webkit-tap-highlight-color:rgba(19,41,75,.08)}
.biz b{display:inline;font-size:15.5px;font-weight:600;line-height:1.3;word-wrap:break-word;color:var(--ink);text-decoration:underline;text-decoration-color:rgba(92,102,114,.42);text-decoration-thickness:1px;text-underline-offset:3px}
.biz:hover b,.biz:focus-visible b{color:var(--navy);text-decoration-color:var(--navy);text-decoration-thickness:2px}
.biz:hover b::after,.biz:focus-visible b::after{content:" \u2197";color:var(--navy);font-weight:500}
.biz:focus-visible{outline:2px solid var(--navy);outline-offset:3px}
.m{display:block;font-size:12.5px;color:var(--muted);margin-top:3px}
.f{display:inline-block;font-size:11px;letter-spacing:.05em;text-transform:uppercase;margin-top:5px;color:var(--muted)}
li.hot .f{color:var(--hot)} li.warm .f{color:var(--warm)}
.status{display:block;font-size:12px;margin-top:4px;font-weight:600;color:var(--navy)}
.status:empty{display:none}
.status.voicemail,.status.no_answer,.status.busy{color:var(--warm)}
.status.wrong_number{color:var(--hot)}
.status.answered,.status.callback{color:var(--green)}
.call{flex:0 0 auto;background:var(--navy);color:#fff;text-decoration:none;font-size:14px;font-weight:500;padding:13px 12px;border-radius:2px;min-height:48px;display:flex;align-items:center;white-space:nowrap}
.log{flex:0 0 auto;background:#fff;border:1px solid var(--line);color:var(--muted);font:500 11px/1 inherit;letter-spacing:.06em;text-transform:uppercase;padding:0 9px;height:48px;min-width:48px;border-radius:2px;cursor:pointer}
.log:hover,.log:focus-visible{border-color:var(--navy);color:var(--navy);outline:none}
.demo{flex:0 0 auto;font-size:12px;color:var(--navy);text-decoration:none;border-bottom:1px solid var(--navy);padding:14px 2px;min-height:48px;display:flex;align-items:center}
.recent .r{display:flex;gap:8px;align-items:baseline;font-size:13px;padding:8px 0;border-bottom:1px solid var(--line)}
.recent .r b{font-size:13px;flex:1 1 auto;min-width:0}
.recent .r .o{font-size:11px;letter-spacing:.05em;text-transform:uppercase;font-weight:600}
.recent .r .d{color:var(--muted);font-size:12px;flex:0 0 auto}
.sheet{position:fixed;inset:0;background:rgba(17,22,28,.5);display:none;align-items:flex-end;z-index:50}
.sheet[data-open="1"]{display:flex}
.sheet-in{background:var(--paper);width:100%;max-width:760px;margin:0 auto;padding:18px 16px calc(20px + env(safe-area-inset-bottom));border-radius:10px 10px 0 0;max-height:90vh;overflow:auto}
.sheet h3{margin:0 0 2px;font-size:17px;line-height:1.25}
.sheet .p{margin:0 0 14px;color:var(--muted);font-size:13.5px}
.outcomes{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:6px}
.outcomes button{min-height:52px;border:1px solid var(--line);background:#fff;font:500 14px/1.2 inherit;color:var(--ink);border-radius:3px;cursor:pointer}
.outcomes button[aria-pressed="true"]{border-color:var(--navy);background:var(--navy);color:#fff}
label{display:block;font-size:11px;color:var(--muted);margin:12px 0 5px;letter-spacing:.06em;text-transform:uppercase}
input,textarea{width:100%;border:1px solid var(--line);background:#fff;padding:11px 12px;font:inherit;font-size:15px;border-radius:3px;color:var(--ink)}
textarea{min-height:64px;resize:vertical}
.sheet-actions{display:flex;gap:8px;margin-top:14px}
.save{flex:1;background:var(--navy);color:#fff;border:0;min-height:52px;font:600 15px inherit;border-radius:3px;cursor:pointer}
.save[disabled]{opacity:.55}
.cancel{flex:0 0 100px;background:#fff;border:1px solid var(--line);min-height:52px;font:500 14px inherit;border-radius:3px;cursor:pointer}
.msg{font-size:13px;margin-top:10px;min-height:16px;color:var(--green)}
.msg.err{color:var(--hot)}
@media (max-width:420px){.call{font-size:13px;padding:12px 10px}.log{padding:0 7px}}
@media (hover:none){.biz b::after{content:" \u2197";color:var(--muted);font-weight:500;font-size:13px}}"""

SHEET = """
<div class="sheet" id="sheet" data-open="0" role="dialog" aria-modal="true" aria-labelledby="s-name">
  <div class="sheet-in">
    <h3 id="s-name">Business</h3>
    <p class="p" id="s-phone"></p>
    <div class="outcomes" id="outcomes">
      <button type="button" data-outcome="answered">Answered</button>
      <button type="button" data-outcome="voicemail">Voicemail</button>
      <button type="button" data-outcome="no_answer">No answer</button>
      <button type="button" data-outcome="busy">Busy</button>
      <button type="button" data-outcome="callback">Call me back</button>
      <button type="button" data-outcome="wrong_number">Wrong number</button>
    </div>
    <label for="s-note">What was said</label>
    <textarea id="s-note" placeholder="Owner, objection, what they asked for"></textarea>
    <label for="s-next">Next action</label>
    <input id="s-next" type="text" placeholder="Send demo, call back, drop it">
    <label for="s-date">Follow up on</label>
    <input id="s-date" type="date">
    <div class="sheet-actions">
      <button class="save" id="s-save" type="button">Save call</button>
      <button class="cancel" id="s-cancel" type="button">Cancel</button>
    </div>
    <div class="msg" id="s-msg" aria-live="polite"></div>
  </div>
</div>
"""

JS = """
(function(){
  var API='https://jarvis-3f05e00a.base44.app/functions/callLog';
  var TOKEN='mike-calls-7Qx4h2Vb9Lz';
  var LABEL={answered:'Answered',voicemail:'Voicemail',no_answer:'No answer',busy:'Busy',callback:'Call back',wrong_number:'Wrong number'};
  var sheet=document.getElementById('sheet');
  var elName=document.getElementById('s-name'), elPhone=document.getElementById('s-phone');
  var elNote=document.getElementById('s-note'), elNext=document.getElementById('s-next'), elDate=document.getElementById('s-date');
  var elMsg=document.getElementById('s-msg'), btnSave=document.getElementById('s-save');
  var outcomes=document.getElementById('outcomes');
  var current=null, choice='';

  function post(payload){
    return fetch(API,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)})
      .then(function(r){return r.json();});
  }
  function digits(p){return String(p||'').replace(/\\D/g,'').slice(-10);}
  function shortDate(iso){
    if(!iso) return '';
    var d=new Date(iso);
    if(isNaN(d)) return '';
    return d.toLocaleDateString('en-US',{month:'short',day:'numeric'});
  }
  function paint(phone, call){
    var nodes=document.querySelectorAll('li[data-phone]');
    for(var i=0;i<nodes.length;i++){
      if(digits(nodes[i].getAttribute('data-phone'))!==digits(phone)) continue;
      var s=nodes[i].querySelector('.status');
      if(!s) continue;
      if(!call){ s.textContent=''; s.className='status'; continue; }
      s.className='status '+call.outcome;
      s.textContent=(LABEL[call.outcome]||call.outcome)+' '+shortDate(call.called_at);
    }
  }
  function openSheet(name, phone){
    current={name:name,phone:phone}; choice='';
    elName.textContent=name; elPhone.textContent=phone;
    elNote.value=''; elNext.value=''; elDate.value='';
    elMsg.textContent=''; elMsg.className='msg'; btnSave.disabled=false;
    var b=outcomes.querySelectorAll('button');
    for(var i=0;i<b.length;i++) b[i].setAttribute('aria-pressed','false');
    sheet.setAttribute('data-open','1');
    elNote.blur();
  }
  function closeSheet(){ sheet.setAttribute('data-open','0'); current=null; }

  outcomes.addEventListener('click',function(e){
    var t=e.target.closest('button[data-outcome]');
    if(!t) return;
    choice=t.getAttribute('data-outcome');
    var b=outcomes.querySelectorAll('button');
    for(var i=0;i<b.length;i++) b[i].setAttribute('aria-pressed', b[i]===t?'true':'false');
  });
  document.addEventListener('click',function(e){
    var t=e.target.closest('.log');
    if(t){ openSheet(t.getAttribute('data-name'), t.getAttribute('data-phone')); }
  });
  document.getElementById('s-cancel').addEventListener('click',closeSheet);
  sheet.addEventListener('click',function(e){ if(e.target===sheet) closeSheet(); });
  document.addEventListener('keydown',function(e){ if(e.key==='Escape') closeSheet(); });

  btnSave.addEventListener('click',function(){
    if(!current) return;
    if(!choice){ elMsg.className='msg err'; elMsg.textContent='Pick what happened first.'; return; }
    var payload={action:'save',token:TOKEN,lead_name:current.name,phone:current.phone,outcome:choice,
      notes:elNote.value,next_action:elNext.value,follow_up_date:elDate.value,called_at:new Date().toISOString()};
    btnSave.disabled=true; elMsg.className='msg'; elMsg.textContent='Saving...';
    post(payload).then(function(r){
      if(r && r.ok){
        paint(current.phone, r.call);
        drawRecent();
        elMsg.className='msg';
        elMsg.textContent='Saved. Lead record updated.';
        setTimeout(closeSheet,700);
      } else {
        btnSave.disabled=false;
        elMsg.className='msg err';
        elMsg.textContent='Not saved: '+((r&&r.error)||'unknown error');
      }
    }).catch(function(){
      btnSave.disabled=false; elMsg.className='msg err'; elMsg.textContent='No connection. Try again.';
    });
  });

  var recentBox=document.getElementById('recent'), recentList=document.getElementById('recent-list'), recentN=document.getElementById('recent-n');
  function drawRecent(){
    post({action:'list'}).then(function(r){
      if(!r||!r.ok) return;
      var latest=r.latest||{};
      for(var k in latest){ if(latest.hasOwnProperty(k)) paint(k, latest[k]); }
      var calls=r.calls||[];
      if(!calls.length){ recentBox.hidden=true; return; }
      recentBox.hidden=false; recentN.textContent=calls.length;
      var out='';
      for(var i=0;i<Math.min(calls.length,8);i++){
        var c=calls[i];
        out+='<div class="r"><b>'+c.lead_name+'</b><span class="o '+c.outcome+'">'+(LABEL[c.outcome]||c.outcome)+'</span><span class="d">'+shortDate(c.called_at)+'</span></div>';
      }
      recentList.innerHTML=out;
    }).catch(function(){});
  }
  drawRecent();
})();
"""

doc = ('<!DOCTYPE html>\n<html lang="en"><head><meta charset="utf-8">\n'
 '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
 '<meta name="robots" content="noindex, nofollow">\n'
 '<title>Leads and call log</title>\n<style>' + CSS + '</style></head><body><div class="wrap">\n'
 '<header><h1>Leads and call log, ' + str(len(live)) + ' to call</h1>\n'
 '<p class="sub">Numbers checked against live Google listings, 16 Nov. Tap a name for its Google listing, the number to call, Log when you hang up.</p></header>\n'
 '<section class="recent" id="recent" hidden><h2>Recent calls <span class="n" id="recent-n"></span></h2><div id="recent-list"></div></section>\n'
 + body + '\n</div>' + SHEET + '\n<script>' + JS + '</script>\n</body></html>\n')

open('index.html', 'w').write(doc)
open('app.js', 'w').write(JS)
print('hot', len(hot), '| weak', len(warm), '| cool', len(cool), '| skip', len(skip))
print('google', doc.count('google.com/maps/search'), '| log buttons', doc.count('class="log"'), '| tel', doc.count('href="tel:+1'))
