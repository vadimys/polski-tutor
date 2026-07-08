"""Telegram Mini App — панель прогресу (Похід / Місії / Прогрес), read-only.

Дані віддаються лише за валідним підписом Telegram (initData, HMAC bot_token) і
лише схваленому користувачу/адміну. Дії лишаються в надійних inline-флоу бота.
Патерн повторює zelika-studio-bot: інлайн HTML (без збірки) + JSON-API на :8080.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
import time
from datetime import date
from urllib.parse import parse_qsl

from aiohttp import web

from app.config import settings
from app.domain.models import MODULE_LABELS, Module
from app.services import access, clock, goals, missions
from app.services import state as user_state
from app.services.progress import READY_THRESHOLD
from app.services.quest import PASS, overall_pct

logger = logging.getLogger(__name__)

APP_PATH = "/app"
STATE_PATH = "/api/state"
_MAX_AGE = 86400  # initData дійсна добу (захист від replay)


def validate_init_data(init_data: str) -> int | None:
    """telegram user_id, якщо initData має валідний підпис і не протух; інакше None."""
    if not init_data or not settings.bot_token:
        return None
    try:
        parsed = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        return None
    recv_hash = parsed.pop("hash", "")
    if not recv_hash:
        return None
    data_check = "\n".join(f"{k}={parsed[k]}" for k in sorted(parsed))
    secret = hmac.new(b"WebAppData", settings.bot_token.encode(), hashlib.sha256).digest()
    calc = hmac.new(secret, data_check.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(calc, recv_hash):
        return None
    try:
        if time.time() - int(parsed.get("auth_date", "0")) > _MAX_AGE:
            return None
        return int(json.loads(parsed.get("user", "{}"))["id"])
    except (ValueError, KeyError, TypeError):
        return None


async def _auth_uid(request: web.Request) -> int | None:
    try:
        body = await request.json()
    except Exception:  # noqa: BLE001
        return None
    uid = validate_init_data(str(body.get("initData", "")))
    if uid is None or not await access.is_allowed(uid, settings.admin_id):
        return None
    return uid


def _days_left(inf) -> int | None:
    if not (inf.confirmed and inf.exam_date):
        return None
    try:
        return max(0, (date.fromisoformat(inf.exam_date) - clock.today_local()).days)
    except ValueError:
        return None


async def state_data(request: web.Request) -> web.Response:
    """POST /api/state → усе для панелі (прогрес + похід + місії). Лише з валідним підписом."""
    uid = await _auth_uid(request)
    if uid is None:
        return web.json_response({"error": "forbidden"}, status=403)

    st = await user_state.load(uid)
    inf = await access.info(uid)
    g = await goals.status(uid)
    ms = await missions.status(uid)
    readiness = st.readiness or {}
    weakest = min(Module, key=lambda m: readiness.get(m.value, 0))

    mods = []
    for m in Module:
        v = readiness.get(m.value, 0)
        mods.append({
            "key": m.value,
            "label": MODULE_LABELS[m],
            "pct": v,
            "passed": v >= PASS,
            "ready": v >= READY_THRESHOLD,
            "here": m is weakest and v < READY_THRESHOLD,
        })
    mods.sort(key=lambda x: x["pct"], reverse=True)

    return web.json_response({
        "level": g["level"], "xp": g["xp"], "to_next": g["to_next"],
        "streak": g["streak"], "freeze": g["freeze"],
        "goal": g["goal"], "today": g["today"], "goal_done": g["done"],
        "days_left": _days_left(inf),
        "quest_pct": overall_pct(readiness),
        "ready_threshold": READY_THRESHOLD,
        "boss_open": all(readiness.get(m.value, 0) >= PASS for m in Module),
        "modules": mods,
        "daily": ms["daily"], "weekly": ms["weekly"],
    })


async def app_page(_request: web.Request) -> web.Response:
    return web.Response(text=_HTML, content_type="text/html")


def add_routes(app: web.Application) -> None:
    """Домонтувати Mini App до наявного aiohttp (health) сервера."""
    app.router.add_get(APP_PATH, app_page)
    app.router.add_post(STATE_PATH, state_data)


_HTML = """<!doctype html><html lang="uk"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Polski B1</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<style>
  :root{--bg:var(--tg-theme-bg-color,#17212b);--card:var(--tg-theme-secondary-bg-color,#232e3c);
    --fg:var(--tg-theme-text-color,#fff);--hint:var(--tg-theme-hint-color,#8a9aa9);
    --btn:var(--tg-theme-button-color,#3390ec);--red:#dc143c;--green:#2ec07a;--gold:#f4b400}
  *{box-sizing:border-box}body{margin:0;font:15px/1.45 -apple-system,system-ui,Roboto,sans-serif;
    background:var(--bg);color:var(--fg);padding:12px 12px 28px}
  h2{font-size:18px;margin:2px 0 12px}.hint{color:var(--hint);font-size:13px}
  .card{background:var(--card);border-radius:16px;padding:14px;margin:10px 0}
  .row{display:flex;align-items:center;gap:10px}.sp{justify-content:space-between}
  .tabs{display:flex;gap:8px;position:sticky;top:0;background:var(--bg);padding:6px 0 10px;z-index:5}
  .tab{flex:1;text-align:center;padding:9px 6px;border-radius:12px;background:var(--card);
    color:var(--hint);font-weight:600;cursor:pointer;font-size:13px}
  .tab.on{background:var(--btn);color:#fff}
  .bar{height:9px;border-radius:6px;background:rgba(255,255,255,.12);overflow:hidden;flex:1}
  .fill{height:100%;border-radius:6px;background:var(--btn)}
  .fill.g{background:var(--green)}.fill.r{background:var(--red)}
  .ring{--p:0;width:96px;height:96px;border-radius:50%;flex:none;
    background:conic-gradient(var(--gold) calc(var(--p)*1%),rgba(255,255,255,.1) 0);
    display:grid;place-items:center}.ring>div{width:76px;height:76px;border-radius:50%;
    background:var(--card);display:grid;place-items:center;text-align:center;line-height:1.1}
  .big{font-size:22px;font-weight:700}.mut{color:var(--hint);font-size:12px}
  .st{margin:9px 0}.st .lab{margin-bottom:4px;display:flex;justify-content:space-between}
  .badge{display:inline-block;background:rgba(255,255,255,.08);border-radius:20px;
    padding:5px 11px;margin:3px 4px 0 0;font-size:13px}
  .done{opacity:.6;text-decoration:line-through}.pill{font-size:12px;padding:2px 8px;border-radius:20px}
  .pill.g{background:rgba(46,192,122,.2);color:var(--green)}.pill.o{background:rgba(244,180,0,.2);color:var(--gold)}
  .hidden{display:none}
</style></head><body>
<div class="tabs">
  <div class="tab on" data-t="quest">🗺 Похід</div>
  <div class="tab" data-t="miss">🎲 Місії</div>
  <div class="tab" data-t="prog">📊 Прогрес</div>
</div>
<div id="root"><div class="hint" style="text-align:center;padding:40px 0">Завантаження…</div></div>
<script>
const tg=window.Telegram?.WebApp; if(tg){tg.ready();tg.expand();}
const $=id=>document.getElementById(id);
function bar(p,cls){p=Math.max(0,Math.min(100,p));return `<div class="bar"><div class="fill ${cls||''}" style="width:${p}%"></div></div>`}
let D=null, TAB='quest';
function h(s){return (s||'').replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]))}

function quest(){
  let s=`<div class="card"><div class="row sp"><b>Похід до B1</b>`+
    (D.days_left!=null?`<span class="mut">до іспиту ${D.days_left} дн</span>`:``)+`</div>`+
    `<div style="margin:10px 0 4px" class="big">${D.quest_pct}%</div>`+
    `<div class="mut">пройдено шляху до готовності (${D.ready_threshold}%+ у кожному)</div>`+
    `<div style="margin-top:8px">${bar(D.quest_pct)}</div></div>`;
  s+=`<div class="card"><div class="mut" style="margin-bottom:6px">СТАНЦІЇ</div>`;
  for(const m of D.modules){
    const ic=m.ready?'✅':(m.here?'🚶':(m.pct>0?'🔓':'🔒'));
    const cls=m.ready?'g':(m.pct>0?'':'r');
    s+=`<div class="st"><div class="lab"><span>${ic} ${h(m.label)}${m.here?' <b style="color:var(--gold)">← ти тут</b>':''}</span><span class="mut">${m.pct}%</span></div>${bar(m.pct,cls)}</div>`;
  }
  s+=`</div><div class="card row sp"><span>${D.boss_open?'🏆':'🔒'} <b>Бос: повний мок</b></span>`+
    `<span class="pill ${D.boss_open?'g':'o'}">${D.boss_open?'відкрито':'усі ≥50%'}</span></div>`;
  return s;
}
function miss(){
  const mk=(m,unit,tgt)=>{const p=Math.round(100*m.progress/tgt);
    return `<div class="card"><div class="row sp ${m.done?'done':''}"><span>${h(m.desc)}</span><span class="pill o">+${m.xp} XP</span></div>`+
      `<div style="margin-top:8px" class="row"><span class="mut" style="width:54px">${m.progress}/${tgt}${unit}</span>${bar(p,m.done?'g':'')}</div></div>`};
  return `<div class="mut" style="margin:2px 4px 8px">Виконуй, щоб заробити бонусний XP.</div>`+
    `<div class="mut" style="margin:0 4px 4px">СЬОГОДНІ</div>`+mk(D.daily,'',D.daily.n)+
    `<div class="mut" style="margin:10px 4px 4px">ЦЕЙ ТИЖДЕНЬ</div>`+mk(D.weekly,' дн',D.weekly.days);
}
function prog(){
  const gp=Math.round(100*D.today/D.goal);
  let s=`<div class="card row" style="gap:16px"><div class="ring" style="--p:${gp}"><div><div class="big">${D.today}</div><div class="mut">/${D.goal} хв</div></div></div>`+
    `<div><div>🎯 <b>Ціль дня</b> ${D.goal_done?'✅':''}</div><div class="mut" style="margin-top:4px">🔥 Серія: <b>${D.streak}</b> дн${D.freeze?` · 🧊 ${D.freeze}`:''}</div></div></div>`;
  s+=`<div class="card"><div class="row sp"><span>⭐ <b>Рівень ${D.level}</b></span><span class="mut">${D.xp} XP · до наступного ${D.to_next}</span></div></div>`;
  s+=`<div class="card"><div class="mut" style="margin-bottom:6px">ГОТОВНІСТЬ ПО МОДУЛЯХ</div>`;
  for(const m of D.modules){const cls=m.ready?'g':(m.pct>=50?'':'r');
    s+=`<div class="st"><div class="lab"><span>${h(m.label)}</span><span class="mut">${m.pct}%</span></div>${bar(m.pct,cls)}</div>`}
  return s+`</div>`;
}
function render(){
  document.querySelectorAll('.tab').forEach(t=>t.classList.toggle('on',t.dataset.t===TAB));
  $('root').innerHTML = !D?'':(TAB==='quest'?quest():TAB==='miss'?miss():prog());
}
document.querySelectorAll('.tab').forEach(t=>t.onclick=()=>{TAB=t.dataset.t;render()});
fetch('/api/state',{method:'POST',headers:{'Content-Type':'application/json'},
  body:JSON.stringify({initData:tg?tg.initData:''})})
  .then(r=>r.ok?r.json():Promise.reject(r.status))
  .then(d=>{D=d;render()})
  .catch(e=>{$('root').innerHTML=`<div class="card">Не вдалося завантажити (${e}). Відкрий панель із бота.</div>`});
</script></body></html>"""
