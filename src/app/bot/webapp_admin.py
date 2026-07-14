"""Telegram Mini App — адмін-дашборд (read-only, ЛИШЕ для ADMIN_ID).

Веб-погляд на ті самі дані, що адмін-консоль показує текстом: огляд, воронка, люди,
AI-витрати, A/B, причини відмов, викладачі. Дані — за валідним підписом Telegram
(initData HMAC) і СТРОГО коли user_id == admin_id. Дії лишаються в inline-флоу бота.
Патерн і токен-система — як у webapp.py (панель учня): Telegram-theme vars → семантика.
"""

from __future__ import annotations

import logging

from aiohttp import web

from app.bot.webapp import validate_init_data
from app.config import settings
from app.services import admin_stats, aicost, churn, events, experiments

logger = logging.getLogger(__name__)

ADMIN_APP_PATH = "/admin"
ADMIN_API_PATH = "/api/admin"


async def _auth_admin(request: web.Request) -> bool:
    """True лише для валідного підпису Telegram І user_id == admin_id."""
    try:
        body = await request.json()
    except Exception:  # noqa: BLE001
        return False
    uid = validate_init_data(str(body.get("initData", "")))
    return uid is not None and uid == settings.admin_id


async def admin_data(request: web.Request) -> web.Response:
    if not await _auth_admin(request):
        return web.json_response({"error": "forbidden"}, status=403)
    tests = [
        {"key": k, "label": experiments.TESTS[k].get("label", k), "rows": await experiments.report(k)}
        for k in experiments.TESTS
    ]
    return web.json_response(
        {
            "overview": await admin_stats.overview(),
            "funnel": await admin_stats.funnel(),
            "features": [
                {"feat": f, "hits": h, "uniq": u} for f, h, u in (await events.feature_report())[:12]
            ],
            "aicost": await aicost.report(),
            "abtests": tests,
            "churn": await churn.reasons_report(),
            "teachers": await admin_stats.teachers(),
            "users": (await admin_stats.list_users(0))[0],
        }
    )


async def admin_page(_request: web.Request) -> web.Response:
    return web.Response(text=_HTML, content_type="text/html")


def admin_url() -> str:
    """URL адмін-дашборда з базового webapp_url (…/app → …/admin)."""
    base = settings.webapp_url
    if base.endswith("/app"):
        return base[: -len("/app")] + ADMIN_APP_PATH
    return base.rstrip("/") + ADMIN_APP_PATH


def add_routes(app: web.Application) -> None:
    app.router.add_get(ADMIN_APP_PATH, admin_page)
    app.router.add_post(ADMIN_API_PATH, admin_data)


_HTML = """<!doctype html><html lang="uk"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Polski B1 · Admin</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<style>
  :root{--bg:var(--tg-theme-bg-color,#17212b);--card:var(--tg-theme-secondary-bg-color,#232e3c);
    --fg:var(--tg-theme-text-color,#fff);--hint:var(--tg-theme-hint-color,#8a9aa9);
    --btn:var(--tg-theme-button-color,#3390ec);--red:#dc143c;--green:#2ec07a;--gold:#f4b400}
  *{box-sizing:border-box}body{margin:0;font:15px/1.45 -apple-system,system-ui,Roboto,sans-serif;
    background:var(--bg);color:var(--fg);padding:12px 12px 28px}
  .hint{color:var(--hint);font-size:13px}.mut{color:var(--hint);font-size:12px}
  .card{background:var(--card);border-radius:16px;padding:14px;margin:10px 0}
  .row{display:flex;align-items:center;gap:10px}.sp{justify-content:space-between}
  .tabs{display:flex;gap:6px;flex-wrap:wrap;position:sticky;top:0;background:var(--bg);padding:6px 0 10px;z-index:5}
  .tab{flex:1;min-width:70px;text-align:center;padding:9px 4px;border-radius:12px;background:var(--card);
    color:var(--hint);font-weight:600;cursor:pointer;font-size:12px}
  .tab.on{background:var(--btn);color:#fff}
  .grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
  .kpi{background:var(--card);border-radius:14px;padding:12px}
  .kpi .n{font-size:22px;font-weight:700}.kpi .l{color:var(--hint);font-size:12px;margin-top:2px}
  .bar{height:9px;border-radius:6px;background:rgba(255,255,255,.12);overflow:hidden;flex:1}
  .fill{height:100%;border-radius:6px;background:var(--btn)}.fill.g{background:var(--green)}.fill.r{background:var(--red)}
  .st{margin:9px 0}.st .lab{margin-bottom:4px;display:flex;justify-content:space-between;gap:8px}
  .li{display:flex;justify-content:space-between;gap:8px;padding:7px 0;border-bottom:1px solid rgba(255,255,255,.07)}
  .li:last-child{border:0}.pill{font-size:11px;padding:2px 8px;border-radius:20px;background:rgba(255,255,255,.08)}
  .pill.g{background:rgba(46,192,122,.2);color:var(--green)}.pill.o{background:rgba(244,180,0,.2);color:var(--gold)}
  b.gold{color:var(--gold)}
</style></head><body>
<div class="tabs">
  <div class="tab on" data-t="ov">📊 Огляд</div>
  <div class="tab" data-t="fun">🔻 Воронка</div>
  <div class="tab" data-t="ppl">👥 Люди</div>
  <div class="tab" data-t="ai">💰 AI</div>
  <div class="tab" data-t="exp">🧪 A/B</div>
</div>
<div id="root"><div class="hint" style="text-align:center;padding:40px 0">Завантаження…</div></div>
<script>
const tg=window.Telegram?.WebApp; if(tg){tg.ready();tg.expand();}
const $=id=>document.getElementById(id);
const h=s=>(s||'').toString().replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
function bar(p,cls){p=Math.max(0,Math.min(100,p));return `<div class="bar"><div class="fill ${cls||''}" style="width:${p}%"></div></div>`}
let D=null, TAB='ov';

function kpi(n,l){return `<div class="kpi"><div class="n">${h(n)}</div><div class="l">${h(l)}</div></div>`}
function ov(){const o=D.overview;
  return `<div class="grid">`+
    kpi(o.total,'усього')+kpi(o.active7,'активні 7дн')+
    kpi(o.students,'учні')+kpi(o.teachers,'викладачі')+
    kpi(o.payers,'платні')+kpi(o.revenue+'⭐','виторг Stars')+
    kpi(o.avg_readiness+'%','сер. готовність')+kpi(o.conv_pct+'%','trial→оплата')+
    kpi(o.new7,'нових 7дн')+kpi(o.pending,'на розгляді')+`</div>`+
    `<div class="card row sp"><span>🎓 Результати іспиту</span><span class="mut">✅ ${o.passed} · ❌ ${o.failed} · ${o.pass_rate}% pass</span></div>`+
    `<div class="mut" style="text-align:center;margin-top:6px">станом на ${h(o.today)}</div>`;
}
function fun(){const f=D.funnel;const steps=[['🚀 Старт',f.total],['🟢 Доступ',f.approved],
    ['📝 Placement',f.placement],['🏋️ ≥1 вправа',f.did_ex],['💎 Оплата',f.paid]];
  const tot=Math.max(1,f.total);let s=`<div class="card">`;let prev=null;
  for(const [lab,n] of steps){const pct=Math.round(100*n/tot);
    const conv=prev!=null?` <span class="mut">(${Math.round(100*n/Math.max(1,prev))}% від вище)</span>`:'';
    s+=`<div class="st"><div class="lab"><span>${lab}${conv}</span><span class="mut">${n} · ${pct}%</span></div>${bar(pct)}</div>`;prev=n;}
  return s+`</div>`;
}
function ppl(){let s=`<div class="card"><div class="mut" style="margin-bottom:6px">ВИКЛАДАЧІ (${D.teachers.length})</div>`;
  for(const t of D.teachers.slice(0,15)) s+=`<div class="li"><span>${h(t.name)}</span><span class="mut">👥 ${t.n_students} · 💎 ${t.n_paying}</span></div>`;
  if(!D.teachers.length) s+='<div class="mut">немає</div>';
  s+=`</div><div class="card"><div class="mut" style="margin-bottom:6px">ОСТАННІ КОРИСТУВАЧІ</div>`;
  for(const u of D.users.slice(0,20)){const role=u.role==='teacher'?'👩‍🏫':(u.role==='admin'?'🛠':'🎓');
    s+=`<div class="li"><span>${role} ${h(u.name)}</span><span class="mut">${u.status==='approved'?'🟢':(u.status==='pending'?'🟡':'⚪')} 🏁${u.overall}% 🔥${u.streak}</span></div>`;}
  return s+`</div>`;
}
function ai(){let s=`<div class="card"><div class="mut" style="margin-bottom:6px">💰 AI-ВИТРАТИ ПО ФІЧАХ</div>`;
  let tot=0;for(const r of D.aicost){tot+=r.usd;
    s+=`<div class="li"><span>${h(r.label)}</span><span class="mut">${r.calls}× · ${r.in}→${r.out} · $${r.usd.toFixed(4)}</span></div>`;}
  if(!D.aicost.length) s+='<div class="mut">ще немає викликів</div>';
  s+=`<div class="row sp" style="margin-top:8px"><b>Разом</b><b class="gold">$${tot.toFixed(4)}</b></div></div>`;
  s+=`<div class="card"><div class="mut" style="margin-bottom:6px">📈 ФІЧІ (використання)</div>`;
  for(const f of D.features) s+=`<div class="li"><span>${h(f.feat)}</span><span class="mut">${f.hits}× · 👤${f.uniq}</span></div>`;
  if(!D.features.length) s+='<div class="mut">немає даних</div>';
  return s+`</div>`;
}
function exp(){let s='';
  for(const t of D.abtests){s+=`<div class="card"><div class="row sp"><b>🧪 ${h(t.label)}</b></div>`;
    const ready=t.rows.length&&t.rows.every(r=>r.exposed>=30);
    let best=null;for(const r of t.rows){if(!best||r.rate>best.rate)best=r;
      s+=`<div class="li"><span>${h(r.name)}</span><span class="mut">👁 ${r.exposed} · 💎 ${r.converted} · <b>${r.rate}%</b></span></div>`;}
    s+=`<div class="mut" style="margin-top:6px">${!t.rows.some(r=>r.exposed)?'ще немає показів':(ready?`✅ лідирує «${h(best.name)}»`:'⏳ попередньо (замало даних)')}</div></div>`;}
  s+=`<div class="card"><div class="mut" style="margin-bottom:6px">🙅 ПРИЧИНИ ВІДМОВ</div>`;
  const ent=Object.entries(D.churn||{}).sort((a,b)=>b[1]-a[1]);const ct=ent.reduce((s,[,v])=>s+v,0);
  const LAB={price:'💸 Дорого',notime:'⏳ Не встиг',unsure:'🤔 Не впевнений',noneed:'🙅 Не треба'};
  for(const [k,v] of ent) s+=`<div class="li"><span>${h(LAB[k]||k)}</span><span class="mut">${v} · ${Math.round(100*v/Math.max(1,ct))}%</span></div>`;
  if(!ent.length) s+='<div class="mut">немає даних</div>';
  return s+`</div>`;
}
const V={ov,fun,ppl,ai,exp};
function render(){document.querySelectorAll('.tab').forEach(t=>t.classList.toggle('on',t.dataset.t===TAB));
  $('root').innerHTML = D?V[TAB]():'';}
document.querySelectorAll('.tab').forEach(t=>t.onclick=()=>{TAB=t.dataset.t;render()});
fetch('/api/admin',{method:'POST',headers:{'Content-Type':'application/json'},
  body:JSON.stringify({initData:tg?tg.initData:''})})
  .then(r=>r.ok?r.json():Promise.reject(r.status))
  .then(d=>{D=d;render()})
  .catch(e=>{$('root').innerHTML=`<div class="card">Доступ лише для адміна (${e}).</div>`});
</script></body></html>"""
