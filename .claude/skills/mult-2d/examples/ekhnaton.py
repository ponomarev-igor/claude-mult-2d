"""Пример: первые 45 секунд истории про Эхнатона (7 сцен). Как писать сцены под озвучку.
Запуск из корня репозитория: python3 .claude/skills/mult-2d/examples/ekhnaton.py projects/ekhnaton
(в проекте должны быть transcript.json и assets/audio/vo.wav)
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "lib"))
from mult import *  # noqa

p = Project(sys.argv[1] if len(sys.argv) > 1 else "projects/ekhnaton", end=44.9)

# ---------- 1. Каменотёсы (0 - 8.05) ----------
wall = ('<div class="abs ln" style="left:440px;top:110px;width:1240px;height:700px;background:#dcb77a;'
        'background-image:linear-gradient(#c49a5c 4px,transparent 4px),linear-gradient(90deg,#c49a5c 4px,transparent 4px);'
        'background-size:180px 115px"></div>'
        '<div class="abs ln" style="left:420px;top:90px;width:1280px;height:40px;background:#b98a4e"></div>')
scaff = ('<div class="abs ln" style="left:600px;top:560px;width:860px;height:26px;background:#8b5a2b;border-radius:6px"></div>'
         '<div class="abs ln" style="left:640px;top:580px;width:24px;height:240px;background:#7a4c22"></div>'
         '<div class="abs ln" style="left:1390px;top:580px;width:24px;height:240px;background:#7a4c22"></div>')
chips = "".join(f'<div id="s1-chip{i}" class="abs" style="left:{1000 + (i % 3) * 16}px;top:{300 + (i // 3) * 14}px;width:14px;height:14px;background:#f3dcab;border:3px solid {LINE};border-radius:3px;opacity:0"></div>' for i in range(9))
body = ('<div class="sky"></div><div class="ground"></div>' + wall + glyphs("s1-cart", 975, 150, 0.85) + scaff + chips
        + char("s1-w1", "worker", "b", 400, 880, 568, tool="hammer") + char("s1-w2", "worker", "d", 400, 1300, 568, flip=True, tool="hammer")
        + char("s1-ph", "pharaoh", "a", 640, 250, 1040)
        + scroll("s1-c1", "ЕГИПЕТ", "XIV век до н. э.", 60, 40)
        + scroll("s1-c2", "АМОН", "главный бог страны", 1430, 40))
js = """
    pop("#s1-c1", 0.3); breathe("s1-ph", 0, 8); sway("s1-ph", 0, 8); blink("s1-ph", 1.9); blink("s1-ph", 6.2);
    face("s1-ph", "f", "a", 0.0); talk("s1-ph", 0.1, 4);
    arm("s1-ph", "R", -140, 0.7, 0.45);
    face("s1-w1", "f", "a", 2.0); face("s1-w2", "f", "a", 2.0);
    arm("s1-w1", "R", -140, 2.4); arm("s1-w2", "R", -140, 2.55);
    wave("s1-w1", "R", -140, -95, 3.1, 7, 0.17); wave("s1-w2", "R", -140, -95, 3.25, 7, 0.17);
    breathe("s1-w1", 0, 8, 0.3); breathe("s1-w2", 0, 8, 0.8);
    for (let i = 0; i < 9; i++) tl.fromTo(`#s1-chip${i}`, { opacity: 1, x: 0, y: 0, rotation: 0 }, { opacity: 0, x: (i % 3 - 1) * 80, y: 200 + (i % 4) * 30, rotation: 200, duration: 0.7, ease: "power2.in" }, S(3.3 + (i % 5) * 0.55));
    for (const g of [3.3, 3.85, 4.4, 4.95, 5.5, 6.05]) tl.to("#s1-cart", { x: 5, duration: 0.04, yoyo: true, repeat: 1 }, S(g));
    tl.fromTo("#s1-cart-in", { fill: "#2f5d9b" }, { fill: "#e8611a", duration: 0.25 }, S(4.58));
    tl.to("#s1-cart", { scale: 1.08, transformOrigin: "50% 50%", duration: 0.2, yoyo: true, repeat: 1 }, S(4.58));
    pop("#s1-c2", 5.5);
    blink("s1-w1", 2.6); blink("s1-w2", 5.0);
"""
p.scene("s1", 0, 8.05, body, js, birds=0)

# ---------- 2. У него есть всё (8.05 - 17.35) ----------
temples = "".join(
    f'<div id="s2-t{i}" class="abs" style="left:{x}px;top:540px;width:240px;height:270px">'
    f'<div class="abs ln" style="left:0;top:40px;width:90px;height:230px;background:#d6ad6c;clip-path:none;border-radius:6px 6px 0 0"></div>'
    f'<div class="abs ln" style="left:150px;top:40px;width:90px;height:230px;background:#d6ad6c;border-radius:6px 6px 0 0"></div>'
    f'<div class="abs ln" style="left:84px;top:130px;width:72px;height:140px;background:#9c6a35"></div>'
    f'<div class="abs ln" style="left:-10px;top:24px;width:260px;height:26px;background:{PAL["accent"]};border-radius:6px"></div></div>'
    for i, x in enumerate([70, 1610]))
bags = "".join(f'<div id="s2-bag{i}" class="abs ln" style="left:{560 + i * 82}px;top:{760 - (i % 2) * 44}px;width:80px;height:80px;background:{PAL["gold"]};border-radius:40% 40% 18px 18px;opacity:0"></div>' for i in range(4))
body = ('<div class="sky"></div><div class="ground"></div>'
        + '<div id="s2-line" class="abs" style="left:330px;top:255px;width:1260px;height:0;border-top:10px dashed #2a1d14;transform-origin:0 50%"></div>'
        + temples + bags
        + char("s2-ph", "pharaoh", "a", 700, 960, 1050)
        + word("s2-w0", "ИМПЕРИЯ", 0, 70, 110, "#fff8ea", center=True)
        + word("s2-w1", "НУБИЯ", 120, 210, 80, PAL["gold"]) + word("s2-w2", "СИРИЯ", 1560, 210, 80, PAL["gold"])
        + word("s2-w3", "ДАНЬ", 560, 600, 76, "#fff8ea") + word("s2-w4", "ХРАМЫ", 1270, 430, 76, "#fff8ea"))
js = """
    breathe("s2-ph", 8.05, 17.3); sway("s2-ph", 8.05, 17.3); blink("s2-ph", 9.4); blink("s2-ph", 15.1);
    face("s2-ph", "s", "n", 9.0);
    arm("s2-ph", "L", 70, 9.2); arm("s2-ph", "R", -70, 9.2);
    pop("#s2-w0", 10.26); pop("#s2-w1", 11.02); pop("#s2-w2", 11.66);
    tl.fromTo("#s2-line", { scaleX: 0 }, { scaleX: 1, duration: 0.6, ease: "power2.out" }, S(11.1));
    pop("#s2-w3", 12.64);
    for (let i = 0; i < 4; i++) tl.fromTo(`#s2-bag${i}`, { opacity: 1, y: -560 }, { y: 0, duration: 0.45, ease: "bounce.out" }, S(12.7 + i * 0.18));
    pop("#s2-w4", 14.34);
    tl.fromTo("#s2-t0, #s2-t1", { y: 300, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: "back.out(1.4)", stagger: 0.15 }, S(14.4));
    for (const w of ["#s2-w0", "#s2-w1", "#s2-w2"]) tl.to(w, { scale: 1.06, duration: 0.5, yoyo: true, repeat: 5, ease: "sine.inOut" }, S(12.0));
    arm("s2-ph", "L", 10, 16.2); arm("s2-ph", "R", -10, 16.2);
"""
p.scene("s2", 8.05, 9.3, body, js, birds=3)

# ---------- 3. Новое имя (17.35 - 23.15) ----------
stars = "".join(f'<div id="s3-st{i}" class="abs" style="left:{(i*271)%1880}px;top:{(i*131)%560+20}px;width:6px;height:6px;border-radius:50%;background:#fff3d6"></div>' for i in range(22))
body = ('<div class="sky" style="background:linear-gradient(180deg,#2b2440,#4a3552)"></div>' + stars + '<div class="ground" style="background:#3a2a2a"></div>'
        + char("s3-ph", "pharaoh", "a", 760, 430, 1080)
        + '<div id="s3-old" class="word" style="left:820px;top:230px;font-size:110px;color:#fff8ea">АМЕНХОТЕП IV</div>'
        + f'<div id="s3-strike" class="abs" style="left:800px;top:288px;width:860px;height:18px;background:#e23b2e;border:5px solid {LINE};border-radius:9px;transform-origin:0 50%"></div>'
        + word("s3-new", "ЭХНАТОН", 820, 430, 170, PAL["accent"])
        + scroll("s3-c1", "АМЕН = АМОН", "старое имя посвящено богу", 840, 690))
js = """
    breathe("s3-ph", 17.35, 23.1); sway("s3-ph", 17.35, 23.1); blink("s3-ph", 18.3); blink("s3-ph", 21.9);
    for (let i = 0; i < 22; i++) tl.fromTo(`#s3-st${i}`, { opacity: 0.2 }, { opacity: 1, duration: 0.6 + (i % 4) * 0.25, yoyo: true, repeat: 5, ease: "sine.inOut" }, (i % 6) * 0.15);
    pop("#s3-old", 17.56);
    tl.fromTo("#s3-strike", { scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: "power3.out" }, S(18.84));
    face("s3-ph", "f", "a", 18.84);
    tl.to("#s3-old", { opacity: 0.45, duration: 0.3 }, S(19.0));
    pop("#s3-c1", 20.58);
    tl.fromTo("#s3-new", { opacity: 0, scale: 2.2 }, { opacity: 1, scale: 1, duration: 0.35, ease: "power4.out" }, S(21.6));
    tl.to("#s3-stage", { x: 10, duration: 0.05, yoyo: true, repeat: 5 }, S(21.95));
    face("s3-ph", "s", "u", 21.6); arm("s3-ph", "R", -45, 21.6);
"""
p.scene("s3", 17.35, 5.8, body, js, ambient=False)

# ---------- 4. Город с нуля (23.15 - 29.4) ----------
thebes = "".join(f'<div class="abs ln" style="left:{x}px;top:{800-hh}px;width:{ww}px;height:{hh}px;background:{c}"></div>'
                 for x, ww, hh, c in [(-10, 170, 340, "#c99b5e"), (150, 130, 250, "#d6ad6c"), (270, 180, 390, "#c3925a"), (440, 120, 220, "#d6ad6c")])
newcity = "".join(f'<div id="s4-b{i}" class="abs ln" style="left:{x}px;top:{800-hh}px;width:{ww}px;height:{hh}px;background:#f0d7a4;border-top:16px solid {PAL["accent"]};transform-origin:50% 100%"></div>'
                  for i, (x, ww, hh) in enumerate([(1200, 140, 220), (1350, 120, 300), (1480, 160, 250), (1650, 130, 340), (1790, 150, 200)]))
body = ('<div class="sky"></div><div class="ground"></div>' + thebes + newcity
        + f'<div id="s4-sun" class="abs" style="left:1640px;top:110px;width:150px;height:150px;border-radius:50%;background:#ffd36b;border:6px solid {LINE}"></div>'
        + '<div id="s4-pair" class="abs" style="left:0;top:0;width:1920px;height:1080px">'
        + char("s4-ph", "pharaoh", "a", 520, 600, 960) + char("s4-q", "queen", "c", 520, 840, 960) + '</div>'
        + scroll("s4-c1", "ФИВЫ", "столица предков", 60, 40)
        + scroll("s4-c2", "АХЕТАТОН", "город с нуля", 1340, 340)
        + word("s4-w1", "ПУСТЫНЯ", 1300, 640, 66, "#fff8ea"))
js = """
    pop("#s4-c1", 23.4); blink("s4-ph", 24.0); blink("s4-q", 27.9);
    face("s4-ph", "n", "n", 23.15); face("s4-q", "s", "n", 23.15);
    tl.fromTo("#s4-pair", { x: -260 }, { x: 260, duration: 2.6, ease: "sine.inOut" }, S(23.5));
    for (const id of ["s4-ph", "s4-q"]) {
      tl.fromTo(`#${id}-legL`, { rotation: -14 }, { rotation: 14, svgOrigin: "84 296", duration: 0.26, yoyo: true, repeat: 9, ease: "sine.inOut", immediateRender: false }, S(23.5));
      tl.fromTo(`#${id}-legR`, { rotation: 14 }, { rotation: -14, svgOrigin: "116 296", duration: 0.26, yoyo: true, repeat: 9, ease: "sine.inOut", immediateRender: false }, S(23.5));
      tl.fromTo(`#${id}-armL`, { rotation: 12 }, { rotation: -12, svgOrigin: "60 170", duration: 0.26, yoyo: true, repeat: 9, ease: "sine.inOut", immediateRender: false }, S(23.5));
      tl.fromTo(`#${id}-armR`, { rotation: 12 }, { rotation: -12, svgOrigin: "140 170", duration: 0.26, yoyo: true, repeat: 9, ease: "sine.inOut", immediateRender: false }, S(23.5));
      tl.fromTo(`#${id}-upper`, { y: 0 }, { y: -9, duration: 0.13, yoyo: true, repeat: 19, ease: "sine.inOut" }, S(23.5));
    }
    tl.fromTo("#s4-b0, #s4-b1, #s4-b2, #s4-b3, #s4-b4", { scaleY: 0 }, { scaleY: 1, duration: 0.45, ease: "back.out(1.7)", stagger: 0.28 }, S(25.34));
    face("s4-ph", "s", "u", 25.6);
    pop("#s4-c2", 26.12);
    pop("#s4-w1", 27.3); out("#s4-w1", 28.9);
    tl.to("#s4-sun", { scale: 1.08, duration: 0.8, yoyo: true, repeat: 7, ease: "sine.inOut" }, 0);
    breathe("s4-ph", 26.2, 29.3); breathe("s4-q", 26.2, 29.3, 0.4); sway("s4-q", 26.2, 29.3);
"""
p.scene("s4", 23.15, 6.25, body, js, birds=2)

# ---------- 5. Солнечный диск (29.4 - 33.15) ----------
rays = "".join(f'<g transform="rotate({a} 0 0)"><rect x="-6" y="118" width="12" height="{150 + (i % 2) * 60}" rx="6" fill="#ffb84d" stroke="{LINE}" stroke-width="4"/>'
               f'<circle cx="0" cy="{274 + (i % 2) * 60}" r="16" fill="#ffb84d" stroke="{LINE}" stroke-width="4"/></g>' for i, a in enumerate(range(100, 261, 20)))
body = ('<div class="sky" style="background:linear-gradient(180deg,#f29e5a,#f7d9a3)"></div><div class="ground"></div>'
        + f'<svg id="s5-sun" class="abs" style="left:660px;top:-80px" width="600" height="600" viewBox="-300 -300 600 600" overflow="visible">'
          f'<g id="s5-rays">{rays}</g><circle r="124" fill="{PAL["accent"]}" stroke="{LINE}" stroke-width="7"/><circle r="92" fill="#ffcf5c"/></svg>'
        + char("s5-ph", "pharaoh", "a", 640, 960, 1060)
        + scroll("s5-c1", "АТОН", "единственный бог", 1370, 380))
js = """
    tl.fromTo("#s5-sun", { y: 380, opacity: 0.3 }, { y: 0, opacity: 1, duration: 1.4, ease: "power2.out" }, S(29.4));
    tl.fromTo("#s5-rays", { rotation: -10, svgOrigin: "0 0" }, { rotation: 10, svgOrigin: "0 0", duration: 3.75, ease: "none" }, S(29.4));
    face("s5-ph", "o", "u", 29.9);
    arm("s5-ph", "L", 150, 30.0, 0.5); arm("s5-ph", "R", -150, 30.0, 0.5);
    breathe("s5-ph", 29.4, 33.1); blink("s5-ph", 31.0);
    pop("#s5-c1", 31.36);
"""
p.scene("s5", 29.4, 3.75, body, js)

# ---------- 6. Царица и дочери (33.15 - 39.75) ----------
frieze = (f'<div class="abs" style="left:0;top:0;width:1920px;height:800px;background:#e2c48f;'
          'background-image:linear-gradient(90deg,#d4b07a 3px,transparent 3px);background-size:240px 100%"></div>'
          f'<div class="abs" style="left:0;top:70px;width:1920px;height:28px;background:#2f5d9b;border-top:5px solid {LINE};border-bottom:5px solid {LINE}"></div>')
girls = "".join(char(f"s6-g{i}", "girl", "c" if i % 2 else "b", 330, 1070 + i * 140, 1010) for i in range(6))
body = (frieze + '<div class="ground" style="background:#c79a5c"></div>'
        + char("s6-ph", "pharaoh", "a", 680, 330, 1050) + char("s6-q", "queen", "c", 680, 720, 1050)
        + word("s6-eq", "=", 495, 380, 150, PAL["accent"])
        + girls
        + scroll("s6-c1", "НЕФЕРТИТИ", "царица", 820, 150)
        + word("s6-n", "6 ДОЧЕРЕЙ", 1180, 330, 96, "#fff8ea"))
js = """
    pop("#s6-c1", 33.28); breathe("s6-ph", 33.15, 39.7); breathe("s6-q", 33.15, 39.7, 0.5); sway("s6-q", 33.15, 39.7); sway("s6-ph", 33.15, 39.7, 0.8);
    face("s6-ph", "n", "n", 33.15); face("s6-q", "s", "n", 33.15);
    blink("s6-q", 34.2); blink("s6-ph", 35.0); blink("s6-q", 38.0);
    pop("#s6-eq", 35.72); face("s6-ph", "s", "n", 35.72);
    tl.to("#s6-c1", { opacity: 0, duration: 0.25 }, S(36.6));
    arm("s6-q", "L", 30, 37.0); arm("s6-ph", "R", -30, 37.0);
    for (let i = 0; i < 6; i++) { pop(`#s6-g${i}`, 37.3 + i * 0.22, 0.3); face(`s6-g${i}`, "s", "u", 37.3); }
    for (let i = 0; i < 6; i++) wave(`s6-g${i}`, "R", -120, -165, 38.9 + i * 0.05, 2, 0.2);
    pop("#s6-n", 38.64);
"""
p.scene("s6", 33.15, 6.6, body, js)

# ---------- 7. Имя стирают (39.75 - 44.9) ----------
body = ('<div class="sky" style="background:linear-gradient(180deg,#5a4a5e,#8a6a62)"></div><div class="ground" style="background:#7a5a3e"></div>'
        + wall.replace("#dcb77a", "#b8955e")
        + glyphs("s7-cart", 980, 150, 0.95)
        + word("s7-name", "ЭХНАТОН", 1180, 300, 70, "#fff8ea")
        + '<div class="abs ln" style="left:560px;top:700px;width:760px;height:26px;background:#8b5a2b;border-radius:6px"></div>'
        + chips.replace("s1-chip", "s7-chip").replace("left:1000", "left:990").replace("top:300", "top:330")
        + char("s7-w", "worker", "d", 480, 860, 708, tool="hammer")
        + word("s7-w2", "ИМЯ СТЁРЛИ", 0, 800, 120, "#e23b2e", center=True))
js = """
    breathe("s7-w", 39.75, 41.5); blink("s7-w", 40.6); face("s7-w", "f", "a", 39.75);
    arm("s7-w", "R", -140, 40.9, 0.4);
    wave("s7-w", "R", -140, -95, 41.8, 4, 0.2);
    for (const g of [41.8, 42.2, 42.6, 43.0]) tl.to("#s7-cart", { x: 6, duration: 0.05, yoyo: true, repeat: 1 }, S(g + 0.2));
    for (let i = 0; i < 9; i++) tl.fromTo(`#s7-chip${i}`, { opacity: 1, x: 0, y: 0, rotation: 0 }, { opacity: 0, x: (i % 3 - 1) * 80, y: 180 + (i % 4) * 30, rotation: 220, duration: 0.7, ease: "power2.in" }, S(41.95 + (i % 4) * 0.4));
    tl.to("#s7-cart-in", { opacity: 0.0, duration: 1.4, ease: "steps(5)" }, S(42.0));
    tl.to("#s7-name", { opacity: 0, filter: "blur(6px)", duration: 1.2, ease: "steps(4)" }, S(42.4));
    pop("#s7-w2", 43.92);
    tl.to("#s7-stage", { opacity: 0, duration: 0.4 }, S(44.5));
"""
p.scene("s7", 39.75, 5.15, body, js)


p.sfx("pop", [0.3, 5.5, 10.26, 11.02, 11.66, 12.64, 14.34, 20.58, 23.4, 26.12, 31.36, 33.28, 38.64])
p.sfx("click", [3.3, 3.85, 4.4, 4.95, 5.5, 6.05, 41.95, 42.35, 42.75, 43.15], vol=0.3)
p.sfx("whoosh", [8.0, 17.3, 23.1, 29.35, 33.1, 39.7], vol=0.15)
p.sfx("impact", [21.6, 43.92], vol=0.2, dur=0.95)
p.build()
