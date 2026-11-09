#!/usr/bin/env python3
"""Render NOP-chan's contribution-graph game as one animated SVG. Standard library only.

    GH_TOKEN=... python3 generate.py --user Batchhh --out dist/nop-chan.svg
    python3 generate.py --data calendar.json --out nop-chan.svg
"""
import argparse
import datetime as dt
import json
import os
import random
import urllib.request
from pathlib import Path

import art
from art import GOLD, INK, PAPER, PINK, ROOF

HERE = Path(__file__).resolve().parent

QUERY = """query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{
totalContributions weeks{contributionDays{date contributionCount contributionLevel weekday}}}}}}"""

SCREEN = {"FIRST_QUARTILE": "#1d5a78", "SECOND_QUARTILE": "#2a93a8",
          "THIRD_QUARTILE": "#4fd6d6", "FOURTH_QUARTILE": "#c2fff3"}
BLOSSOM = {"FIRST_QUARTILE": "#99417f", "SECOND_QUARTILE": "#e0558f",
           "THIRD_QUARTILE": "#ff86ad", "FOURTH_QUARTILE": "#ffe6ee"}
DARK_WINDOW = "#1a1740"
HEIGHT = 446
GRID_X, GRID_Y, GRID_W = 36, ROOF + 22, 1128
START, STEP, BOSS_PAUSE, BOSS_HIT, CLEAR_HOLD = 1.0, 0.2, 3.1, 2.7, 4.6
BOSS_GAP = 148
RUN_LIMIT = 1112


def fetch(user, token):
    body = json.dumps({"query": QUERY, "variables": {"login": user}}).encode()
    request = urllib.request.Request("https://api.github.com/graphql", body, {
        "Authorization": f"Bearer {token}", "Content-Type": "application/json",
        "User-Agent": "nop-chan-generator"})
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
    if "errors" in payload:
        raise SystemExit(payload["errors"])
    return payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]


def build(calendar, faces, portrait):
    weeks = calendar["weeks"]
    total = calendar["totalContributions"]
    n = len(weeks)
    pitch = GRID_W / n
    size = pitch - 4
    centre = lambda c: GRID_X + c * pitch + size / 2
    days = [d for w in weeks for d in w["contributionDays"]]
    best_day = max(days, key=lambda d: d["contributionCount"])
    boss = next(i for i, w in enumerate(weeks) if best_day in w["contributionDays"])

    times = [START + i * STEP + (BOSS_PAUSE if i > boss else 0) for i in range(n)]
    hits = [t + (BOSS_HIT if i == boss else 0) for i, t in enumerate(times)]
    finish = times[-1] + 0.5
    loop = finish + CLEAR_HOLD
    pct = lambda t: f"{min(100.0, 100 * t / loop):.3f}".rstrip("0").rstrip(".") + "%"
    css = []

    def steps(name, frames):
        body = "".join(f"{pct(t)}{{{rule}}}" for t, rule in frames)
        css.append(f"@keyframes {name}{{{body}}}.{name}{{animation:{name} {loop:.3f}s step-end infinite}}")

    def smooth(name, frames):
        body = "".join(f"{pct(t)}{{{rule}}}" for t, rule in frames)
        css.append(f"@keyframes {name}{{{body}}}.{name}{{animation:{name} {loop:.3f}s linear infinite}}")

    rng = random.Random(0x1F2003D5)
    panes, glows, sheen, blossom, beams, petals, scores = [], [], [], [], [], [], []
    running = 0
    active = [i for i, w in enumerate(weeks) if any(d["contributionCount"] for d in w["contributionDays"])]
    for c, week in enumerate(weeks):
        x = GRID_X + c * pitch
        pink = []
        for d in week["contributionDays"]:
            y = GRID_Y + d["weekday"] * pitch
            level = d["contributionLevel"]
            coords = f'x="{x:.1f}" y="{y:.1f}"'
            panes.append(f'<use href="#w" {coords} fill="{SCREEN.get(level, DARK_WINDOW)}"/>')
            if level in BLOSSOM:
                sheen.append(f"M{x + 2:.1f} {y + size - 5:.1f}l{size * .5:.1f} {-(size - 7):.1f}h4l{-size * .5:.1f} {size - 7:.1f}Z")
            halo = f'cx="{x + size / 2:.1f}" cy="{y + size / 2:.1f}" r="{size * 1.15:.1f}"'
            if level in ("THIRD_QUARTILE", "FOURTH_QUARTILE"):
                glows.append(f'<circle {halo} fill="url(#gc)"/>')
            if level in BLOSSOM:
                pink.append(f'<use href="#w" {coords} fill="{BLOSSOM[level]}"/>')
                if level in ("THIRD_QUARTILE", "FOURTH_QUARTILE"):
                    pink.insert(0, f'<circle {halo} fill="url(#gp)"/>')
        hit = hits[c]
        count = sum(d["contributionCount"] for d in week["contributionDays"])
        if not count:
            continue
        running += count
        blossom.append(f'<g class="pk k{c}">{"".join(pink)}</g>')
        steps(f"k{c}", [(0, "opacity:0"), (hit, "opacity:1"), (loop, "opacity:1")])
        width = size + (16 if c == boss else 3)
        beams.append(f'<rect class="bm b{c}" x="{centre(c) - width / 2:.1f}" y="{ROOF - 6}" width="{width:.1f}" '
                     f'height="{7 * pitch + 28:.0f}" rx="4" fill="url(#beam)"/>')
        smooth(f"b{c}", [(0, "opacity:0"), (hit - 0.002, "opacity:0"), (hit, "opacity:1"),
                         (hit + 0.2, "opacity:0"), (loop, "opacity:0")])
        burst = 18 if c == boss else 3
        pieces = "".join(f'<use href="#p" x="{rng.uniform(-16, 16):.1f}" y="{rng.uniform(-8, 46):.1f}" '
                         f'fill="{rng.choice([PINK, "#ffd0e0", PAPER])}"/>' for _ in range(burst))
        petals.append(f'<g transform="translate({centre(c):.1f} {ROOF + 12})"><g class="pt f{c}">{pieces}</g></g>')
        drift = (86, 104) if c == boss else (24, 82)
        smooth(f"f{c}", [(0, "opacity:0"), (hit - 0.002, "opacity:0;transform:translate(0,0)"),
                         (hit, "opacity:1;transform:translate(0,0)"),
                         (hit + 1.2, f"opacity:0;transform:translate({drift[0]}px,{drift[1]}px)"),
                         (loop, "opacity:0")])
        klass = "sc sf" if c == active[-1] else "sc"
        scores.append(f'<text class="{klass} s{c}" x="356" y="52">{running:,}</text>')
        following = next((hits[j] for j in active if j > c), None)
        frames = [(0, "opacity:0"), (hit, "opacity:1")]
        frames.append((following, "opacity:0") if following else (loop, "opacity:1"))
        steps(f"s{c}", frames)
    first_hit = hits[active[0]] if active else 0
    steps("s0base", [(0, "opacity:1"), (first_hit, "opacity:0"), (loop, "opacity:0")])

    start_x = centre(0) - 60
    walk = [(0, start_x), (START * .35, start_x)]
    stop_x = centre(boss) - BOSS_GAP
    for i, t in enumerate(times):
        target = min(centre(i), stop_x) if i <= boss else min(centre(i), RUN_LIMIT)
        walk.append((t, target))
        if i == boss:
            walk.append((hits[i] + .15, target))
    last_x = walk[-1][1]
    walk += [(loop - 0.003, last_x), (loop, start_x)]
    smooth("wk", [(t, f"transform:translate({x:.1f}px,{ROOF + 1}px)") for t, x in walk])

    pause_a = next(times[i] for i in range(boss + 1) if centre(i) >= stop_x)
    pause_b = hits[boss] + .15
    steps("run", [(0, "opacity:0"), (START * .35, "opacity:1"), (pause_a, "opacity:0"), (pause_b, "opacity:1"),
                  (finish - .45, "opacity:0"), (loop, "opacity:0")])
    steps("idle", [(0, "opacity:1"), (START * .35, "opacity:0"), (pause_a, "opacity:1"), (pause_b, "opacity:0"),
                   (loop, "opacity:0")])
    steps("win", [(0, "opacity:0"), (finish - .45, "opacity:1"), (loop - .01, "opacity:1"), (loop, "opacity:0")])

    steps("bs", [(0, "opacity:1"), (hits[boss], "opacity:0"), (loop, "opacity:0")])
    cut = times[boss] + 0.05
    smooth("ct", [(0, "opacity:0;transform:translateX(-1500px)"),
                  (cut, "opacity:0;transform:translateX(-1500px)"),
                  (cut + 0.001, "opacity:1;transform:translateX(-1500px)"),
                  (cut + 0.24, "opacity:1;transform:translateX(0)"),
                  (cut + 2.15, "opacity:1;transform:translateX(18px)"),
                  (cut + 2.5, "opacity:1;transform:translateX(1500px)"),
                  (cut + 2.501, "opacity:0;transform:translateX(1500px)"),
                  (loop, "opacity:0;transform:translateX(1500px)")])
    smooth("cl", [(0, "opacity:0;transform:scale(2.4)"), (finish, "opacity:0;transform:scale(2.4)"),
                  (finish + 0.2, "opacity:1;transform:scale(1)"),
                  (loop - 0.2, "opacity:1;transform:scale(1)"), (loop, "opacity:0;transform:scale(1)")])

    months, previous, last_label = [], None, -9
    for c, week in enumerate(weeks):
        day = dt.date.fromisoformat(week["contributionDays"][0]["date"])
        if day.month != previous and c - last_label >= 3:
            months.append(f'<text class="mo" x="{GRID_X + c * pitch:.1f}" y="{HEIGHT - 11}">{day:%b}</text>')
            last_label = c
        previous = day.month

    when = dt.date.fromisoformat(best_day["date"])
    best_text = f'Best day: {best_day["contributionCount"]} contributions on {when:%b} {when.day}, {when.year}'
    backdrop = art.backdrop(rng, HEIGHT)
    fg_petals, fg_css = art.foreground_petals(rng, HEIGHT)

    style = f"""
{faces}
text{{font-family:'M',ui-monospace,Menlo,monospace}}
.ui{{font-family:'R',system-ui,sans-serif}}
.logo{{font-family:'D',system-ui,sans-serif}}
.mo{{font-family:'R',system-ui,sans-serif;font-size:14px;fill:#c6a9e8}}
.sc{{font-family:'R',system-ui,sans-serif;font-size:30px;fill:{GOLD};opacity:0}}
.sf{{opacity:1}}
.bm,.pt,.bs,.ct,.run,.idle{{opacity:0}}
.pk,.win{{opacity:1}}
.wk{{transform:translate({last_x:.1f}px,{ROOF + 1}px)}}
.dr1{{animation:d1 44s ease-in-out infinite alternate}}
.dr2{{animation:d2 60s ease-in-out infinite alternate}}
@keyframes d1{{from{{transform:translateX(-16px)}}to{{transform:translateX(20px)}}}}
@keyframes d2{{from{{transform:translateX(16px)}}to{{transform:translateX(-18px)}}}}
.r0,.r1,.r2,.r3{{opacity:0;animation:rf .44s step-end infinite}}
.r1{{animation-delay:-.33s}}.r2{{animation-delay:-.22s}}.r3{{animation-delay:-.11s}}
@keyframes rf{{0%{{opacity:1}}25%,100%{{opacity:0}}}}
.wj{{animation:wj .34s ease-in-out infinite alternate}}
@keyframes wj{{from{{transform:translateY(0)}}to{{transform:translateY(-16px)}}}}
.bw{{animation:bw .5s ease-in-out infinite alternate}}
@keyframes bw{{from{{transform:translateY(0)}}to{{transform:translateY(-7px)}}}}
.gl{{animation:gl 1.1s step-end infinite}}
@keyframes gl{{0%{{opacity:.8;transform:translateX(0)}}30%{{opacity:0}}55%{{opacity:.7;transform:translateX(8px)}}70%,100%{{opacity:0}}}}
{fg_css}
{"".join(css)}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}.r0{{opacity:1}}}}
"""

    label = f"Anime game at dusk: NOP-chan runs along a rooftop, turning {total:,} contributions into cherry-blossom windows. {best_text}."
    band = "M-40 62L1240 18L1240 372L-40 416Z"
    panel_x = centre(boss)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{HEIGHT}" viewBox="0 0 1200 {HEIGHT}" role="img" aria-label="{label}">
<style>{style}</style>
<defs>{art.DEFS}
<rect id="w" width="{size:.1f}" height="{size:.1f}" rx="2.5"/>
{art.HEAD}
<linearGradient id="phair" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#54429a"/><stop offset=".6" stop-color="#352963"/><stop offset="1" stop-color="#6a2f85"/></linearGradient>
<linearGradient id="phairback" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#231b4a"/><stop offset=".7" stop-color="#2b2058"/><stop offset="1" stop-color="#7a2f7f"/></linearGradient>
<linearGradient id="plock" gradientUnits="userSpaceOnUse" x1="0" y1="20" x2="0" y2="190"><stop offset="0" stop-color="#352963"/><stop offset=".5" stop-color="#3b2f6b"/><stop offset=".95" stop-color="{PINK}"/></linearGradient>
<linearGradient id="pface" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#f9ceba"/><stop offset=".5" stop-color="#ffe8da"/><stop offset="1" stop-color="#ffdcbb"/></linearGradient>
<linearGradient id="pneck" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e8a892"/><stop offset="1" stop-color="#ffd4bf"/></linearGradient>
<linearGradient id="phood" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#171a36"/><stop offset=".65" stop-color="#2c3160"/><stop offset="1" stop-color="#6a5280"/></linearGradient>
<linearGradient id="piris" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#27124a"/><stop offset=".45" stop-color="#a8337f"/><stop offset=".82" stop-color="#ff8a5c"/><stop offset="1" stop-color="#ffe08a"/></linearGradient>
<radialGradient id="pblush"><stop offset="0" stop-color="#ff7f9c" stop-opacity=".75"/><stop offset="1" stop-color="#ff7f9c" stop-opacity="0"/></radialGradient>
<clipPath id="frame"><rect width="1200" height="{HEIGHT}" rx="18"/></clipPath>
<clipPath id="bandclip"><path d="{band}"/></clipPath>
</defs>
<g clip-path="url(#frame)">
{backdrop}
<rect y="{ROOF}" width="1200" height="{HEIGHT - ROOF}" fill="url(#wall)"/>
<rect y="{ROOF}" width="1200" height="{HEIGHT - ROOF}" fill="url(#wallsun)"/>
<rect y="{ROOF}" width="1200" height="13" fill="#3a2a70"/>
<rect y="{ROOF}" width="1200" height="2.6" fill="#ffc98a"/>
<rect y="{ROOF + 13}" width="1200" height="3" fill="#0d0824"/>
{"".join(glows)}
{"".join(panes)}
{"".join(blossom)}
<path d="{"".join(sheen)}" fill="#fff" opacity=".13"/>
{"".join(months)}
<g transform="translate({panel_x:.1f} {ROOF + 1})"><g class="bs"><g class="bw">{art.BOSS}</g>
<g transform="translate(0 -206)"><rect x="-74" y="-27" width="148" height="30" rx="7" fill="{INK}" stroke="#ff5fa0" stroke-width="2.5"/><text class="ui" y="-5" text-anchor="middle" font-size="20" fill="#ffd0e0">SIGSEGV</text>
<rect x="-74" y="7" width="148" height="10" rx="3" fill="{INK}"/><rect x="-71" y="10" width="142" height="4" rx="2" fill="#ff4d6d"/></g></g></g>
{"".join(beams)}
{"".join(petals)}
<g class="wk"><g transform="scale(.92)">{art.character()}</g></g>
{fg_petals}
<g transform="rotate(-1 110 38)"><rect x="22" y="18" width="166" height="44" rx="9" fill="{GOLD}" stroke="{INK}" stroke-width="4"/><text class="ui" x="105" y="49" text-anchor="middle" font-size="27" fill="{INK}">NOP-chan</text></g>
<rect x="202" y="18" width="280" height="46" rx="10" fill="{INK}" fill-opacity=".82" stroke="{GOLD}" stroke-width="2.5"/>
<text class="ui" x="220" y="51" font-size="25" fill="#f4e6ff">Patched</text>
<text class="sc s0base" x="356" y="52">0</text>
{"".join(scores)}
<g class="cl" style="transform-origin:600px 330px;transform-box:view-box"><g transform="rotate(-3 600 330)">
<text class="logo" x="600" y="342" text-anchor="middle" font-size="92" fill="url(#clear)" stroke="{INK}" stroke-width="15" stroke-linejoin="round" paint-order="stroke">STAGE CLEAR!</text>
<rect x="282" y="360" width="636" height="48" rx="12" fill="{PAPER}" stroke="{INK}" stroke-width="4.5"/>
<text class="ui" x="600" y="394" text-anchor="middle" font-size="27" fill="{INK}">{total:,} contributions patched in the last year</text>
</g></g>
<g class="ct">
<path d="{band}" fill="url(#band)" stroke="{INK}" stroke-width="7"/>
<g clip-path="url(#bandclip)">
<rect y="0" width="1200" height="{HEIGHT}" fill="url(#dots)" opacity=".7"/>
<path d="{art.speed_lines(905, 215)}" fill="#fff" opacity=".55"/>
<g transform="translate(925 232) rotate(3) scale(.92)">{portrait}</g></g>
<g transform="rotate(-2 300 200)">
<text class="logo" x="52" y="232" font-size="156" fill="url(#title)" stroke="{INK}" stroke-width="18" stroke-linejoin="round" paint-order="stroke">NOP!!</text>
<rect x="56" y="266" width="596" height="46" rx="10" fill="{PAPER}" stroke="{INK}" stroke-width="4.5"/>
<text class="ui" x="74" y="299" font-size="25" fill="{INK}">{best_text}</text>
</g>
</g>
</g></svg>""", {"loop": loop, "boss_column": boss, "boss_start": times[boss], "boss_hit": hits[boss], "finish": finish,
                "best": best_text, "weeks": n, "total": total}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--user")
    parser.add_argument("--data", help="calendar JSON saved earlier, instead of calling the API")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    if args.data:
        calendar = json.loads(Path(args.data).read_text())
    else:
        calendar = fetch(args.user, os.environ["GH_TOKEN"])
    fonts = json.loads((HERE / "fonts.json").read_text())
    faces = "".join(f"@font-face{{font-family:'{name}';src:url(data:font/woff2;base64,{data}) format('woff2');}}"
                    for name, data in fonts.items())
    svg, info = build(calendar, faces, (HERE / "portrait.svgfrag").read_text())
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(svg)
    print(json.dumps({**info, "bytes": out.stat().st_size}))


if __name__ == "__main__":
    main()
