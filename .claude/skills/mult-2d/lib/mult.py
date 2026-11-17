"""mult.py: библиотека плоской 2D-анимации для HyperFrames.

Персонажи, подписи-свитки, крупные слова, фон с пылью и птицами, сцены, субтитры, звуки.
Сцены описываются в Python, на выходе index.html + compositions/*.html, рендер через HyperFrames.

Пример:
    from mult import *
    p = Project("projects/my-mult", words="transcript.json", audio="assets/audio/vo.wav")
    p.scene("s1", 0, 6.5, body=sky() + ground() + char("hero", "man", h=600, x=700, bottom=1040),
            js='face("hero", "s", "u", 1.0); wave("hero", "R", -120, -160, 1.2, 3);')
    p.sfx("pop", [1.0, 2.4])
    p.build()
"""
import json, pathlib

LINE = "#2a1d14"
PAL = {
    "ink": "#1d1a17", "sand": "#e7c48a", "ground": "#d29b5c", "sky1": "#f7d9a3", "sky2": "#eba868",
    "accent": "#e8611a", "blue": "#2f5d9b", "gold": "#e3b341", "linen": "#f6efdc", "lip": "#7a3324",
    "papyrus": "#f3e2b8", "green": "#6f8a4e", "red": "#e23b2e", "white": "#fff8ea",
}
SKIN = {"a": "#c98a55", "b": "#b5763f", "c": "#d9a06b", "d": "#a96a3a", "e": "#f0c49a", "f": "#8a5530"}
HAIR = {"dark": "#2b211b", "brown": "#6b4423", "blond": "#d9b45a", "red": "#a8452a", "gray": "#9a9590"}
KINDS = ("man", "woman", "pharaoh", "queen", "worker", "girl")


# ---------- персонаж ----------

def char(cid, kind="man", skin="a", h=420, x=0, bottom=860, flip=False, tool=None,
         outfit=None, pants="#3b3f4a", hair="dark"):
    """Плоский персонаж с контуром, стоит лицом к зрителю.

    kind: man | woman | pharaoh | queen | worker | girl
    skin: a..f, outfit: цвет одежды, pants: брюки (man), hair: dark|brown|blond|red|gray или #hex
    h: рост в px, x: центр по горизонтали, bottom: где стоят ноги (пол в сцене обычно 800-1050)
    tool: "hammer" в правой руке (worker)

    Группы для анимации (через JS-хелперы сцены):
      -upper (дыхание), -head (покачивание), -armL / -armR (плечо), -eyes (моргание), -legL / -legR (шаг)
      выражения: рот -m-n спокойный / -m-s улыбка / -m-o открытый / -m-f грустный, брови -b-n / -b-a злые / -b-u поднятые
    """
    assert kind in KINDS, kind
    s = SKIN.get(skin, skin)
    hc = HAIR.get(hair, hair)
    col = outfit or {"pharaoh": PAL["blue"], "queen": PAL["accent"], "worker": PAL["green"], "girl": PAL["gold"],
                     "man": PAL["blue"], "woman": PAL["accent"]}[kind]
    w = h / 2
    pid = f"{cid}-nem"
    O = 'class="o"'
    defs = (f'<defs><pattern id="{pid}" width="16" height="16" patternUnits="userSpaceOnUse">'
            f'<rect width="16" height="16" fill="{PAL["gold"]}"/><rect width="16" height="8" fill="{PAL["blue"]}"/></pattern></defs>')
    dress = kind in ("queen", "woman")
    if dress:
        dcol = PAL["linen"] if kind == "queen" else col
        lower = (f'<path {O} d="M62 236 L138 236 L154 392 L46 392 Z" fill="{dcol}"/>'
                 + (f'<path {O} d="M62 236 L138 236 L140 252 L60 252 Z" fill="{PAL["accent"]}"/>' if kind == "queen" else "")
                 + f'<g id="{cid}-legL"></g><g id="{cid}-legR"></g>')
    elif kind == "man":
        lower = (f'<g id="{cid}-legL"><rect {O} x="70" y="244" width="29" height="140" rx="10" fill="{pants}"/>'
                 f'<path {O} d="M60 386 Q62 372 84 372 Q100 372 99 390 Z" fill="#2a2522"/></g>'
                 f'<g id="{cid}-legR"><rect {O} x="101" y="244" width="29" height="140" rx="10" fill="{pants}"/>'
                 f'<path {O} d="M140 386 Q138 372 116 372 Q100 372 101 390 Z" fill="#2a2522"/></g>')
    else:
        belt = PAL["gold"] if kind == "pharaoh" else "#9b7b4b"
        lower = (f'<g id="{cid}-legL"><rect {O} x="72" y="292" width="25" height="94" rx="12" fill="{s}"/>'
                 f'<path {O} d="M62 384 Q64 372 84 372 Q100 372 98 390 Z" fill="{s}"/></g>'
                 f'<g id="{cid}-legR"><rect {O} x="103" y="292" width="25" height="94" rx="12" fill="{s}"/>'
                 f'<path {O} d="M138 384 Q136 372 116 372 Q100 372 102 390 Z" fill="{s}"/></g>'
                 f'<path {O} d="M60 246 L140 246 L156 326 L44 326 Z" fill="{PAL["linen"]}"/>'
                 + (f'<path {O} d="M90 258 L110 258 L114 326 L86 326 Z" fill="{PAL["gold"]}"/>' if kind == "pharaoh" else "")
                 + f'<rect {O} x="58" y="240" width="84" height="14" rx="5" fill="{belt}"/>')

    sleeve = kind in ("man", "woman")

    def arm(side, x0):
        hold = ""
        if tool == "hammer" and side == "R":
            hold = (f'<g transform="rotate(-100 {x0} 280)"><rect {O} x="{x0 - 5}" y="278" width="11" height="66" rx="4" fill="#8b5a2b"/>'
                    f'<rect {O} x="{x0 - 18}" y="336" width="37" height="24" rx="5" fill="#7c858e"/></g>')
        sl = f'<rect {O} x="{x0 - 13}" y="158" width="27" height="62" rx="12" fill="{col}"/>' if sleeve else \
             f'<rect {O} x="{x0 - 12}" y="220" width="25" height="9" rx="3" fill="{PAL["gold"]}"/>'
        return (f'<g id="{cid}-arm{side}">{hold}<rect {O} x="{x0 - 11}" y="160" width="23" height="114" rx="11.5" fill="{s}"/>'
                f'<circle {O} cx="{x0}" cy="280" r="14" fill="{s}"/>{sl}</g>')

    back = ""
    if kind == "pharaoh":
        hat = (f'<path {O} d="M52 100 Q54 40 100 38 Q146 40 148 100 L162 188 L134 188 L136 112 Q100 74 64 112 L66 188 L38 188 Z" fill="url(#{pid})"/>'
               f'<path {O} d="M60 90 Q100 62 140 90 L140 100 Q100 76 60 100 Z" fill="{PAL["gold"]}"/>'
               f'<path {O} d="M95 70 Q100 52 105 70 L103 82 L97 82 Z" fill="{PAL["accent"]}"/>'
               f'<path {O} d="M92 150 L108 150 L105 176 L95 176 Z" fill="{PAL["blue"]}"/>')
    elif kind == "queen":
        hat = (f'<path {O} d="M62 84 L50 10 L150 10 L138 84 Z" fill="{PAL["blue"]}"/>'
               f'<path {O} d="M58 66 L142 66 L140 80 L60 80 Z" fill="{PAL["gold"]}"/>'
               f'<path {O} d="M96 66 Q100 50 104 66 Z" fill="{PAL["accent"]}"/>')
    elif kind == "girl":
        hat = (f'<path {O} d="M56 98 Q58 54 100 52 Q142 54 144 98 Q100 78 56 98 Z" fill="{hc}"/>'
               f'<path {O} d="M136 92 Q164 120 150 172 Q140 178 136 168 Q146 128 128 100 Z" fill="{hc}"/>')
    elif kind == "worker":
        hat = f'<path {O} d="M56 98 Q58 52 100 50 Q142 52 144 98 Q100 84 56 98 Z" fill="#efe2c4"/>'
    elif kind == "man":
        hat = f'<path {O} d="M55 104 Q52 52 100 50 Q148 52 145 104 Q140 80 126 76 Q100 86 70 76 Q60 84 55 104 Z" fill="{hc}"/>'
    else:  # woman
        back = f'<path {O} d="M50 112 Q44 44 100 42 Q156 44 150 112 L156 176 Q100 186 44 176 Z" fill="{hc}"/>'
        hat = f'<path {O} d="M56 100 Q56 52 100 50 Q146 52 144 100 Q132 70 104 72 Q86 84 56 100 Z" fill="{hc}"/>'

    eye = lambda cx, d: (f'<ellipse cx="{cx}" cy="106" rx="11" ry="7.5" fill="#fffaf0" stroke="{LINE}" stroke-width="3"/>'
                         f'<circle cx="{cx + d}" cy="106" r="5" fill="{PAL["ink"]}"/>'
                         + (f'<path d="M{cx - 14 * (1 if d < 0 else -1)} 106 L{cx - 21 * (1 if d < 0 else -1)} 111" stroke="{LINE}" stroke-width="3.5" stroke-linecap="round"/>'
                            if kind in ("pharaoh", "queen", "worker", "girl") else ""))
    st = f'stroke="{LINE}" stroke-width="5" fill="none" stroke-linecap="round"'
    face = (f'<ellipse {O} cx="57" cy="110" rx="9" ry="12" fill="{s}"/><ellipse {O} cx="143" cy="110" rx="9" ry="12" fill="{s}"/>'
            f'<ellipse {O} cx="100" cy="106" rx="43" ry="47" fill="{s}"/>'
            f'<g id="{cid}-eyes">{eye(83, -1)}{eye(117, 1)}</g>'
            f'<path id="{cid}-b-n" d="M72 91 Q83 86 94 89 M106 89 Q117 86 128 91" {st}/>'
            f'<path id="{cid}-b-a" d="M72 86 L94 94 M106 94 L128 86" {st} opacity="0"/>'
            f'<path id="{cid}-b-u" d="M72 86 Q83 78 94 84 M106 84 Q117 78 128 86" {st} opacity="0"/>'
            f'<path d="M100 110 Q96 122 102 124" stroke="#00000040" stroke-width="3" fill="none" stroke-linecap="round"/>'
            f'<path id="{cid}-m-n" d="M91 134 Q100 139 109 134" stroke="{PAL["lip"]}" stroke-width="4" fill="none" stroke-linecap="round"/>'
            f'<path id="{cid}-m-s" d="M87 131 Q100 146 113 131 Z" fill="{PAL["lip"]}" stroke="{PAL["lip"]}" stroke-width="3" stroke-linejoin="round" opacity="0"/>'
            f'<ellipse id="{cid}-m-o" cx="100" cy="136" rx="7" ry="9" fill="{PAL["lip"]}" opacity="0"/>'
            f'<path id="{cid}-m-f" d="M90 139 Q100 131 110 139" stroke="{PAL["lip"]}" stroke-width="4" fill="none" stroke-linecap="round" opacity="0"/>')
    if sleeve:
        torso = (f'<rect {O} x="90" y="140" width="20" height="30" fill="{s}"/>'
                 f'<rect {O} x="58" y="158" width="84" height="{100 if kind == "man" else 92}" rx="24" fill="{col}"/>'
                 f'<path d="M86 160 L100 182 L114 160" stroke="{LINE}" stroke-width="4" fill="{s}"/>')
    else:
        torso = (f'<rect {O} x="90" y="140" width="20" height="30" fill="{s}"/>'
                 f'<rect {O} x="58" y="158" width="84" height="98" rx="26" fill="{s}"/>'
                 f'<path {O} d="M60 168 Q100 222 140 168 L140 184 Q100 240 60 184 Z" fill="{col}"/>'
                 f'<path d="M64 186 Q100 236 136 186" stroke="{PAL["gold"]}" stroke-width="7" fill="none"/>')
    upper = f'<g id="{cid}-upper">{back}{arm("L", 60)}{arm("R", 140)}{torso}<g id="{cid}-head">{face}{hat}</g></g>'
    flip_attr = ' transform="translate(200 0) scale(-1 1)"' if flip else ""
    svg = (f'<svg viewBox="0 -10 200 410" width="{w:.0f}" height="{h * 1.025:.0f}" overflow="visible">{defs}'
           f'<g{flip_attr}><ellipse cx="100" cy="392" rx="66" ry="10" fill="#00000030"/>{lower}{upper}</g></svg>')
    return f'<div id="{cid}" class="ch" style="left:{x - w / 2:.0f}px;top:{bottom - h:.0f}px;width:{w:.0f}px;height:{h:.0f}px">{svg}</div>'


# ---------- подписи и объекты ----------

def scroll(cid, title, sub="", x=0, y=0, size=48):
    """Подпись-свиток: свёрнутые края, тёмный контур. Шрифт подписи >= 30 px."""
    s = f'<div class="ss">{sub}</div>' if sub else ""
    return (f'<div id="{cid}" class="scroll" style="left:{x}px;top:{y}px"><i class="roll l"></i>'
            f'<div class="sb"><div class="st" style="font-size:{size}px">{title}</div>{s}</div><i class="roll r"></i></div>')


def word(cid, text, x=0, y=0, size=72, color="#fff8ea", center=False):
    """Крупное слово с толстой обводкой, выскакивает на ключевом слове озвучки."""
    pos = "left:0;right:0;text-align:center" if center else f"left:{x}px"
    return f'<div id="{cid}" class="word" style="{pos};top:{y}px;font-size:{size}px;color:{color}">{text}</div>'


def box(cid, x, y, w, h, color="#d6ad6c", radius=6, extra=""):
    """Прямоугольник с контуром: дома, стены, мебель, экраны. Для роста снизу: transform-origin задан."""
    return (f'<div id="{cid}" class="abs ln" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{color};'
            f'border-radius:{radius}px;transform-origin:50% 100%;{extra}"></div>')


def sky(c1=None, c2=None):
    return f'<div class="sky" style="background:linear-gradient(180deg,{c1 or PAL["sky1"]},{c2 or PAL["sky2"]})"></div>'


def ground(color=None, top=800):
    return f'<div class="ground" style="top:{top}px;background:{color or PAL["ground"]}"></div>'


def sun(cid, x, y, r=75, color="#ffd36b"):
    return f'<div id="{cid}" class="abs ln" style="left:{x}px;top:{y}px;width:{2*r}px;height:{2*r}px;border-radius:50%;background:{color}"></div>'


def glyphs(cid, x, y, scale=1.0):
    """Египетский картуш с условными иероглифами (для исторических тем)."""
    return (f'<svg id="{cid}" class="glyph" viewBox="0 0 160 400" width="{160*scale:.0f}" height="{400*scale:.0f}" style="left:{x}px;top:{y}px">'
            f'<rect x="10" y="10" width="140" height="370" rx="70" fill="#f1d9a8" stroke="{LINE}" stroke-width="8"/>'
            f'<rect x="20" y="380" width="120" height="14" rx="4" fill="{LINE}"/>'
            f'<g id="{cid}-in" fill="{PAL["blue"]}" stroke="{LINE}" stroke-width="3">'
            f'<circle cx="80" cy="80" r="22"/><circle cx="80" cy="80" r="8" fill="#f1d9a8"/>'
            f'<path d="M42 140 l12 -10 l12 10 l12 -10 l12 10 l12 -10 l12 10 l-4 6 l-8 -7 l-12 10 l-12 -10 l-12 10 l-12 -10 l-12 10 l-8 -7 Z"/>'
            f'<rect x="72" y="170" width="16" height="70" rx="6"/><path d="M80 172 q24 -20 22 6 q-10 -8 -22 2 Z"/>'
            f'<ellipse cx="78" cy="292" rx="30" ry="20"/><path d="M104 286 l22 -10 l-8 18 Z"/><circle cx="66" cy="286" r="4" fill="#f1d9a8"/>'
            f'<rect x="56" y="318" width="48" height="10" rx="4"/></g></svg>')


def _dust(sid, n=14, color="#fff3d6"):
    out = []
    for i in range(n):
        x = (i * 397) % 1880 + 20; y = (i * 233) % 760 + 60; r = 4 + (i * 7) % 6
        out.append(f'<div id="{sid}-d{i}" class="abs dust" style="left:{x}px;top:{y}px;width:{r}px;height:{r}px;background:{color}"></div>')
    return "".join(out)


def _birds(sid, n=3):
    return "".join(
        f'<svg id="{sid}-bird{i}" class="abs" style="left:-120px;top:{150 + i * 60}px" width="70" height="30" viewBox="0 0 70 30">'
        f'<path id="{sid}-bw{i}" d="M2 18 Q18 2 35 18 Q52 2 68 18" stroke="{LINE}" stroke-width="5" fill="none" stroke-linecap="round"/></svg>'
        for i in range(n))


CSS = f"""
@font-face {{ font-family: "Inter Tight"; src: url("assets/fonts/InterTight-900-cyr.woff2") format("woff2"); font-weight: 900; unicode-range: U+0400-04FF; }}
@font-face {{ font-family: "Inter Tight"; src: url("assets/fonts/InterTight-900-lat.woff2") format("woff2"); font-weight: 900; unicode-range: U+0000-03FF, U+2000-206F; }}
@font-face {{ font-family: "Inter"; src: url("assets/fonts/Inter.ttf") format("truetype"); font-weight: 100 900; }}
#root {{ position: absolute; inset: 0; overflow: hidden; font-family: "Inter", sans-serif; }}
.stage {{ position: absolute; inset: 0; }}
.sky {{ position: absolute; inset: 0; background: linear-gradient(180deg, {PAL["sky1"]} 0%, {PAL["sky2"]} 100%); }}
.ground {{ position: absolute; left: -100px; right: -100px; top: 800px; bottom: -100px; background: {PAL["ground"]}; border-top: 6px solid {LINE}; }}
.ch {{ position: absolute; }}
.ch svg {{ display: block; overflow: visible; }}
.ch .o {{ stroke: {LINE}; stroke-width: 5; stroke-linejoin: round; }}
.abs {{ position: absolute; }}
.ln {{ border: 6px solid {LINE}; }}
.dust {{ border-radius: 50%; opacity: .7; }}
.glyph {{ position: absolute; overflow: visible; }}
.scroll {{ position: absolute; display: flex; align-items: stretch; white-space: nowrap; filter: drop-shadow(0 8px 0 #00000030); }}
.scroll .sb {{ background: {PAL["papyrus"]}; border-top: 6px solid {LINE}; border-bottom: 6px solid {LINE}; padding: 14px 26px 16px; }}
.scroll .roll {{ width: 30px; background: #ddc28c; border: 6px solid {LINE}; border-radius: 15px; margin: -10px 0; }}
.scroll .st {{ font-family: "Inter Tight"; font-weight: 900; letter-spacing: -0.01em; color: {LINE}; line-height: 1; }}
.scroll .ss {{ margin-top: 8px; font-size: 30px; font-weight: 700; color: #7a5a35; }}
.word {{ position: absolute; font-family: "Inter Tight"; font-weight: 900; letter-spacing: -0.02em; line-height: 1; white-space: nowrap; -webkit-text-stroke: 12px {LINE}; paint-order: stroke fill; }}
"""

HELPERS = """
    const pop = (sel, g, d) => tl.fromTo(sel, { opacity: 0, scale: 0.6, y: 20 }, { opacity: 1, scale: 1, y: 0, duration: d || 0.35, ease: "back.out(2)" }, S(g));
    const out = (sel, g) => tl.to(sel, { opacity: 0, y: -10, duration: 0.25, ease: "power2.in" }, S(g));
    const grow = (sel, g, stagger) => tl.fromTo(sel, { scaleY: 0 }, { scaleY: 1, duration: 0.45, ease: "back.out(1.7)", stagger: stagger || 0.25 }, S(g));
    const drop = (sel, g, i) => tl.fromTo(sel, { opacity: 1, y: -560 }, { y: 0, duration: 0.45, ease: "bounce.out" }, S(g + (i || 0) * 0.18));
    const pulse = (sel, g, n) => tl.to(sel, { scale: 1.06, duration: 0.5, yoyo: true, repeat: (n || 3) * 2 - 1, ease: "sine.inOut" }, S(g));
    const shake = (sel, g) => tl.to(sel, { x: 8, duration: 0.05, yoyo: true, repeat: 5 }, S(g));
    const breathe = (id, g0, g1, ph) => { const n = Math.max(1, Math.floor((g1 - g0) / 1.3)); tl.to(`#${id}-upper`, { y: -4, duration: 1.3, yoyo: true, repeat: n - 1, ease: "sine.inOut" }, S(g0 + (ph || 0))); };
    const sway = (id, g0, g1, ph) => { const n = Math.max(1, Math.floor((g1 - g0) / 1.6)); tl.fromTo(`#${id}-head`, { rotation: -2 }, { rotation: 2, svgOrigin: "100 150", duration: 1.6, yoyo: true, repeat: n - 1, ease: "sine.inOut", immediateRender: false }, S(g0 + (ph || 0))); };
    const idle = (id, g0, g1, ph) => { breathe(id, g0, g1, ph); sway(id, g0, g1, (ph || 0) + 0.4); for (let t = g0 + 1.2 + (ph || 0); t < g1 - 0.3; t += 2.9) blink(id, t); };
    const blink = (id, g) => tl.to(`#${id}-eyes`, { scaleY: 0.08, svgOrigin: "100 106", duration: 0.07, yoyo: true, repeat: 1, ease: "power1.in" }, S(g));
    const arm = (id, side, deg, g, d) => tl.to(`#${id}-arm${side}`, { rotation: deg, svgOrigin: side === "L" ? "60 170" : "140 170", duration: d || 0.4, ease: "back.out(1.6)" }, S(g));
    const wave = (id, side, a, b, g, n, d) => { tl.fromTo(`#${id}-arm${side}`, { rotation: a }, { rotation: b, svgOrigin: side === "L" ? "60 170" : "140 170", duration: d || 0.3, yoyo: true, repeat: n * 2 - 1, ease: "sine.inOut", immediateRender: false }, S(g)); };
    const talk = (id, g, n) => tl.to(`#${id}-m-n`, { scaleY: 2.4, svgOrigin: "100 136", duration: 0.12, yoyo: true, repeat: n * 2 - 1 }, S(g));
    const face = (id, m, b, g) => { for (const k of ["n", "s", "o", "f"]) tl.set(`#${id}-m-${k}`, { opacity: k === m ? 1 : 0 }, S(g)); for (const k of ["n", "a", "u"]) tl.set(`#${id}-b-${k}`, { opacity: k === b ? 1 : 0 }, S(g)); };
    const walk = (sel, ids, dx, g, d) => { const steps = Math.max(2, Math.round(d / 0.26)); tl.fromTo(sel, { x: 0 }, { x: dx, duration: d, ease: "sine.inOut" }, S(g));
      for (const id of ids) {
        tl.fromTo(`#${id}-legL`, { rotation: -14 }, { rotation: 14, svgOrigin: "84 296", duration: 0.26, yoyo: true, repeat: steps - 1, ease: "sine.inOut", immediateRender: false }, S(g));
        tl.fromTo(`#${id}-legR`, { rotation: 14 }, { rotation: -14, svgOrigin: "116 296", duration: 0.26, yoyo: true, repeat: steps - 1, ease: "sine.inOut", immediateRender: false }, S(g));
        tl.fromTo(`#${id}-armL`, { rotation: 12 }, { rotation: -12, svgOrigin: "60 170", duration: 0.26, yoyo: true, repeat: steps - 1, ease: "sine.inOut", immediateRender: false }, S(g));
        tl.fromTo(`#${id}-armR`, { rotation: 12 }, { rotation: -12, svgOrigin: "140 170", duration: 0.26, yoyo: true, repeat: steps - 1, ease: "sine.inOut", immediateRender: false }, S(g));
        tl.fromTo(`#${id}-upper`, { y: 0 }, { y: -9, duration: 0.13, yoyo: true, repeat: steps * 2 - 1, ease: "sine.inOut" }, S(g));
      } };
"""


# ---------- проект ----------

def load_words(path):
    """Слова с таймингами: HyperFrames transcript.json ([{text,start,end}]) или Whisper ({words:[{word,start,end}]})."""
    d = json.loads(pathlib.Path(path).read_text())
    items = d["words"] if isinstance(d, dict) else d
    return [{"w": (x.get("text") or x.get("word") or "").strip(), "start": float(x["start"]), "end": float(x["end"])} for x in items]


class Project:
    def __init__(self, root, words="transcript.json", audio="assets/audio/vo.wav", end=None, width=1920, height=1080):
        self.root = pathlib.Path(root)
        self.words = load_words(self.root / words)
        self.audio = audio
        self.end = round(end or (self.words[-1]["end"] + 0.6), 2)
        self.W, self.H = width, height
        self.scenes, self.sounds = [], []
        (self.root / "compositions").mkdir(parents=True, exist_ok=True)

    def t(self, text, nth=1):
        """Время начала слова (по началу совпадения, без регистра), nth-е вхождение."""
        k = 0
        for x in self.words:
            if x["w"].lower().strip(".,!?:;«»\"").startswith(text.lower()):
                k += 1
                if k == nth:
                    return round(x["start"], 2)
        raise KeyError(f"слово не найдено: {text}")

    def scene(self, sid, start, dur, body, js="", ambient=True, birds=0, push=True):
        """Одна сцена = одна sub-composition. В js время пишется в секундах ВСЕГО ролика, S() переводит в локальное."""
        amb = (_dust(sid) if ambient else "") + (_birds(sid, birds) if birds else "")
        aj = ""
        if ambient:
            aj += (f'    for (let i = 0; i < 14; i++) tl.fromTo(`#{sid}-d${{i}}`, {{ x: 0, y: 0 }}, {{ x: 60 + (i % 5) * 30, y: -40 - (i % 3) * 25, duration: {dur}, ease: "none" }}, 0);\n'
                   f'    for (let i = 0; i < 14; i++) tl.fromTo(`#{sid}-d${{i}}`, {{ opacity: 0.2 }}, {{ opacity: 0.8, duration: 0.9 + (i % 4) * 0.3, yoyo: true, repeat: Math.max(1, Math.floor({dur} / (1.8 + (i % 4) * 0.6))), ease: "sine.inOut" }}, (i % 5) * 0.2);\n')
        for i in range(birds):
            aj += (f'    tl.fromTo("#{sid}-bird{i}", {{ x: 0, y: 0 }}, {{ x: 2200, y: {-40 + i * 30}, duration: {dur * (0.9 + i * 0.15):.2f}, ease: "none" }}, {i * 0.6});\n'
                   f'    tl.fromTo("#{sid}-bw{i}", {{ scaleY: 1 }}, {{ scaleY: -0.4, transformOrigin: "50% 60%", duration: 0.22, yoyo: true, repeat: {int(dur / 0.22)}, ease: "sine.inOut" }}, {i * 0.6});\n')
        pj = (f'    tl.fromTo("#{sid}-stage", {{ scale: 1.0 }}, {{ scale: 1.04, duration: {dur}, ease: "none", transformOrigin: "50% 60%" }}, 0);\n' if push else "")
        html = f"""<template>
  <style>{CSS}</style>
  <div id="root" data-composition-id="{sid}" data-width="{self.W}" data-height="{self.H}">
    <div id="{sid}-stage" class="stage">
{body}
{amb}
    </div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    const S = (g) => +(g - {start}).toFixed(3);
{HELPERS}
{pj}{aj}{js}
    window.__timelines["{sid}"] = tl;
  </script>
</template>
"""
        (self.root / "compositions" / f"{sid}.html").write_text(html)
        self.scenes.append((sid, round(start, 3), round(dur, 3)))

    def sfx(self, name, times, vol=0.25, dur=0.52):
        """Звук из assets/audio/sfx-<name>.wav: pop, whoosh, click, impact. Громкость под голосом не выше 0.3."""
        for t in times:
            self.sounds.append((name, round(t, 2), vol, dur))

    def captions(self, max_words=6):
        phrases, cur = [], []
        for x in self.words:
            if x["start"] > self.end - 0.3:
                break
            cur.append(x)
            if x["w"][-1:] in ".,!?" or len(cur) >= max_words:
                phrases.append(cur); cur = []
        if cur:
            phrases.append(cur)
        caps = []
        for i, p in enumerate(phrases):
            st = p[0]["start"]; en = phrases[i + 1][0]["start"] if i + 1 < len(phrases) else self.end
            caps.append((f"cap{i}", round(st, 2), round(en - st, 2), " ".join(x["w"] for x in p)))
        return caps

    def build(self, subtitles=True):
        hosts = "\n".join(f'      <div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-start="{st}" data-duration="{du}" data-track-index="1" data-track-kind="graphics" data-width="{self.W}" data-height="{self.H}"></div>' for sid, st, du in self.scenes)
        caps = "\n".join(f'      <div id="{c}" class="clip cap" data-start="{s}" data-duration="{d}" data-track-index="5"><span>{t}</span></div>' for c, s, d, t in (self.captions() if subtitles else []))
        snd = "\n".join(f'      <audio id="sfx-{i:02d}" class="clip" data-start="{t}" data-duration="{min(d, max(0.1, self.end - t)):.2f}" data-track-index="{30 + i}" data-volume="{v}" src="assets/audio/sfx-{n}.wav"></audio>' for i, (n, t, v, d) in enumerate(self.sounds))
        index = f"""<!doctype html>
<html lang="ru">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={self.W}, height={self.H}" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      @font-face {{ font-family: "Inter"; src: url("assets/fonts/Inter.ttf") format("truetype"); font-weight: 100 900; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {self.W}px; height: {self.H}px; overflow: hidden; background: #111214; }}
      #root {{ position: relative; width: 100%; height: 100%; }}
      .cap {{ position: absolute; left: 0; right: 0; top: {int(self.H * 0.866)}px; text-align: center; z-index: 50; }}
      .cap span {{ display: inline-block; max-width: {int(self.W * 0.8)}px; color: #fff8ea; font-family: "Inter"; font-weight: 800; font-size: 46px; letter-spacing: 0.02em; word-spacing: 0.12em; line-height: 1.2; -webkit-text-stroke: 7px {LINE}; paint-order: stroke fill; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{self.end}" data-width="{self.W}" data-height="{self.H}">
{hosts}
{caps}
      <audio id="vo" class="clip" data-start="0" data-duration="{self.end}" data-track-index="10" data-volume="1" src="{self.audio}"></audio>
{snd}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
        (self.root / "index.html").write_text(index)
        print(f"готово: {len(self.scenes)} сцен, {self.end} с, звуков {len(self.sounds)} -> {self.root / 'index.html'}")
