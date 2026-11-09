"""Hand-drawn SVG art for the NOP-chan game: scenery, character poses and the boss."""
import math
import random

INK = "#160f2e"
GOLD = "#ffcf5a"
PINK = "#ff6f9f"
PAPER = "#fff7e6"
RIM = "#ffb46b"

WIDTH = 1200
ROOF = 240


# ---------- character ----------

def _fk(origin, a1, l1, a2, l2):
    x, y = origin
    r1, r2 = math.radians(a1), math.radians(a2)
    knee = (x + l1 * math.sin(r1), y + l1 * math.cos(r1))
    end = (knee[0] + l2 * math.sin(r2), knee[1] + l2 * math.cos(r2))
    return knee, end


def _limb(points, width, color, rim=None):
    d = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in points)
    common = 'fill="none" stroke-linecap="round" stroke-linejoin="round"'
    out = (f'<path d="{d}" {common} stroke="{INK}" stroke-width="{width + 5}"/>'
           f'<path d="{d}" {common} stroke="{color}" stroke-width="{width}"/>')
    if rim:
        rx = [(x + width * .28, y) for x, y in points]
        rd = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in rx)
        out += f'<path d="{rd}" {common} stroke="{rim}" stroke-width="1.8" opacity=".85"/>'
    return out


def _shoe(ankle, shin):
    tilt = -shin * .85 if shin < 0 else -shin * .25
    return (f'<g transform="translate({ankle[0]:.1f} {ankle[1]:.1f}) rotate({tilt:.0f})">'
            f'<path d="M-6 -5C-3 -8 3 -7 8 -2C14 1 16 5 14 8L-7 8C-9 3 -8 -2 -6 -5Z" fill="#fff" stroke="{INK}" stroke-width="2.4" stroke-linejoin="round"/>'
            f'<path d="M-7 8L14 8L14 5L-7 5Z" fill="{PINK}" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>'
            f'<path d="M0 -6L5 -1" stroke="{GOLD}" stroke-width="2.2" stroke-linecap="round"/></g>')


TORSO = f"""<ellipse cx="-16" cy="-103" rx="15" ry="10" fill="#232749" stroke="{INK}" stroke-width="2.6"/>
<path d="M-15 -106C-24 -96 -26 -74 -23 -56C-22 -52 -21 -49 -20 -47L21 -47C24 -56 24 -72 21 -92C18 -102 12 -107 6 -108Z" fill="url(#hood)" stroke="{INK}" stroke-width="2.6" stroke-linejoin="round"/>
<path d="M21 -92C24 -72 24 -56 21 -47" fill="none" stroke="{RIM}" stroke-width="2.2" stroke-linecap="round"/>
<path d="M-20 -47C-26 -40 -28 -34 -30 -29L30 -29C28 -36 25 -42 21 -47Z" fill="#2b1d4f" stroke="{INK}" stroke-width="2.6" stroke-linejoin="round"/>
<path d="M-28 -32L29 -32" stroke="{PINK}" stroke-width="2.4"/>
<path d="M-12 -47L-15 -30M0 -47L0 -30M12 -47L15 -30" stroke="{INK}" stroke-width="1.4" opacity=".6"/>
<path d="M-23 -56L22 -56" stroke="#3a4074" stroke-width="3"/>
<path d="M4 -103L2 -88M12 -103L14 -90" fill="none" stroke="{PAPER}" stroke-width="2" stroke-linecap="round"/>
<circle cx="2" cy="-86" r="2" fill="{GOLD}"/><circle cx="14" cy="-88" r="2" fill="{GOLD}"/>"""


def _hair_tail(flip):
    if flip:
        d = ("M-16 -158C-44 -146 -54 -120 -54 -94C-54 -74 -62 -58 -76 -44C-64 -44 -52 -50 -44 -58"
             "C-44 -46 -48 -36 -56 -26C-40 -32 -28 -46 -22 -62C-16 -74 -10 -86 -8 -100Z")
    else:
        d = ("M-16 -158C-42 -146 -50 -120 -50 -94C-50 -72 -54 -54 -66 -38C-54 -40 -44 -46 -38 -56"
             "C-37 -44 -40 -32 -46 -20C-32 -28 -24 -44 -20 -60C-14 -74 -10 -86 -8 -100Z")
    return f'<path d="{d}" fill="url(#hairtail)" stroke="{INK}" stroke-width="2.6" stroke-linejoin="round"/>'


HEAD = f"""<g id="head" transform="translate(7 -132)">
<path d="M-24 -14C-27 12 -13 31 7 39C16 36 28 22 31 4C33 -24 -22 -30 -24 -14Z" fill="url(#skin)" stroke="{INK}" stroke-width="2.6" stroke-linejoin="round"/>
<path d="M-20 -14C-16 -6 -6 -6 -2 -14C2 -6 10 -6 14 -14C18 -6 26 -6 31 -12L31 -30L-24 -30Z" fill="#eaa48f" opacity=".55"/>
<ellipse cx="-11" cy="20" rx="9" ry="5" fill="#ff7f9c" opacity=".55"/><ellipse cx="26" cy="19" rx="4.5" ry="4" fill="#ff7f9c" opacity=".55"/>
<path d="M-14 4C-12 -8 2 -10 8 -2C10 8 6 18 -3 18C-11 18 -15 12 -14 4Z" fill="#fff"/>
<ellipse cx="-2.5" cy="5" rx="8.5" ry="11.5" fill="url(#iris)" stroke="{INK}" stroke-width="1.3"/>
<ellipse cx="-1.5" cy="3.5" rx="4" ry="6.5" fill="{INK}"/>
<path d="M-8.5 11C-5 15 1 15 4 11C2 15.5 -6 15.5 -8.5 11Z" fill="#ffe08a"/>
<circle cx="-6" cy="-1" r="3.4" fill="#fff"/><circle cx="1.5" cy="9.5" r="1.7" fill="#fff"/>
<path d="M17 4C18 -6 27 -8 30 0C31 8 28 17 23 17C19 17 17 11 17 4Z" fill="#fff"/>
<ellipse cx="24" cy="5" rx="5" ry="10.5" fill="url(#iris)" stroke="{INK}" stroke-width="1.2"/>
<ellipse cx="24.5" cy="3.5" rx="2.4" ry="6" fill="{INK}"/>
<circle cx="22.5" cy="-1" r="2.6" fill="#fff"/>
<path d="M-18 4C-15 -11 3 -14 11 -3C4 -9 -8 -9 -18 4Z" fill="{INK}" stroke="{INK}" stroke-width="1.2" stroke-linejoin="round"/>
<path d="M-18 4L-22 1M-16 -1L-20 -4" stroke="{INK}" stroke-width="1.7" stroke-linecap="round"/>
<path d="M15 -2C20 -9 28 -9 32 -1C27 -5 21 -6 15 -2Z" fill="{INK}" stroke="{INK}" stroke-width="1.2" stroke-linejoin="round"/>
<path d="M-11 -14C-6 -18 2 -18 6 -15M17 -15C21 -18 27 -17 30 -14" fill="none" stroke="{INK}" stroke-width="1.7" stroke-linecap="round"/>
<path d="M19 18L21 20" stroke="#c77a68" stroke-width="1.8" stroke-linecap="round"/>
<path d="M8 25C12 33 20 33 23 25C18 27 13 27 8 25Z" fill="#b93a5e" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>
<path d="M12 29.5C15 27.5 18 27.5 20 29.5C17 31.5 14 31.5 12 29.5Z" fill="#ff93ad"/>
<path d="M-27 -8C-34 12 -32 34 -22 54C-18 34 -16 16 -16 -6Z" fill="url(#lockS)" stroke="{INK}" stroke-width="2.4" stroke-linejoin="round"/>
<path d="M36 6C42 -34 16 -58 -4 -56C-30 -54 -44 -30 -36 8C-33 -4 -28 -12 -22 -18C-20 -8 -16 0 -10 6C-9 -6 -6 -16 -1 -24C1 -12 6 -2 13 3C13 -8 16 -16 21 -24C24 -12 29 -2 36 6Z" fill="url(#hair)" stroke="{INK}" stroke-width="2.6" stroke-linejoin="round"/>
<path d="M-22 -18C-18 -30 -12 -38 -6 -42M-1 -24C0 -34 3 -42 7 -48M21 -24C21 -34 19 -42 16 -47" fill="none" stroke="#1d1645" stroke-width="1.6" stroke-linecap="round"/>
<path d="M-27 -29C-20 -40 -10 -44 0 -45L-4 -38L3 -42L0 -34L-8 -38L-11 -31L-16 -37L-21 -27Z" fill="#8f7fd6"/>
<path d="M12 -45C20 -43 27 -38 31 -30L27 -28L23 -35L19 -31L17 -38L11 -36Z" fill="#8f7fd6"/>
<path d="M33 -22C38 -12 39 -2 36 6" fill="none" stroke="{RIM}" stroke-width="2.4" stroke-linecap="round"/>
<path d="M-2 -55C-8 -72 8 -80 22 -74C10 -72 4 -66 8 -55Z" fill="#3b2f6b" stroke="{INK}" stroke-width="2.4" stroke-linejoin="round"/>
<path d="M-40 -2C-46 -40 -18 -62 2 -62C24 -62 46 -40 40 -4" fill="none" stroke="{INK}" stroke-width="7"/>
<path d="M-40 -2C-46 -40 -18 -62 2 -62C24 -62 46 -40 40 -4" fill="none" stroke="{GOLD}" stroke-width="2.6"/>
<rect x="-34" y="-12" width="17" height="30" rx="8" fill="#2c3160" stroke="{INK}" stroke-width="2.4"/>
<rect x="-30" y="-5" width="4.5" height="16" rx="2" fill="{GOLD}"/>
<rect x="9" y="-44" width="24" height="10" rx="3" fill="{GOLD}" stroke="{INK}" stroke-width="2" transform="rotate(20 21 -39)"/>
</g>"""


def _victory_arm():
    return (_limb([(8, -96), (40, -112), (48, -150)], 10, "#343b6e", RIM) +
            f'<path d="M44 -150L40 -170M52 -150L58 -169" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
            f'<path d="M44 -150L40 -170M52 -150L58 -169" stroke="#ffe3d2" stroke-width="4.4" stroke-linecap="round"/>'
            f'<circle cx="48" cy="-150" r="6.5" fill="#ffe3d2" stroke="{INK}" stroke-width="2.2"/>')


def _frame(near_leg, far_leg, near_arm, far_arm, flip, raised=False):
    hip_near, hip_far = (3, -52), (-3, -52)
    knee_n, foot_n = _fk(hip_near, near_leg[0], 27, near_leg[1], 25)
    knee_f, foot_f = _fk(hip_far, far_leg[0], 27, far_leg[1], 25)
    drop = -max(foot_n[1], foot_f[1]) - 8
    out = []
    elbow_f, hand_f = _fk((10, -96), far_arm[0], 17, far_arm[1], 17)
    out.append(_limb([(10, -96), elbow_f, hand_f], 9, "#1c2040"))
    out.append(_limb([hip_far, knee_f, foot_f], 10, "#14152e"))
    out.append(_shoe(foot_f, far_leg[1]))
    out.append(_limb([hip_near, knee_n, foot_n], 11, "#272a52", RIM))
    out.append(_shoe(foot_n, near_leg[1]))
    out.append(_hair_tail(flip))
    out.append(TORSO)
    elbow_n, hand_n = _fk((-3, -96), near_arm[0], 17, near_arm[1], 17)
    out.append(_limb([(-3, -96), elbow_n, hand_n], 10, "#343b6e", RIM))
    out.append(f'<circle cx="{hand_n[0]:.1f}" cy="{hand_n[1]:.1f}" r="5.5" fill="#ffe3d2" stroke="{INK}" stroke-width="2.2"/>')
    out.append('<use href="#head"/>')
    if raised:
        out.append(_victory_arm())
    return f'<g transform="translate(0 {drop:.1f})">{"".join(out)}</g>'


def character():
    """Run cycle (four frames), an idle stance and a victory pose."""
    run = [
        ((42, 14), (-34, -82), (-48, 28), (44, 112)),
        ((12, -48), (4, -6), (-14, 56), (14, 88)),
        ((-34, -82), (42, 14), (44, 112), (-48, 28)),
        ((4, -6), (12, -48), (14, 88), (-14, 56)),
    ]
    frames = "".join(f'<g class="r{i}">{_frame(*pose, i % 2 == 0)}</g>' for i, pose in enumerate(run))
    idle = _frame((14, 6), (-12, -6), (30, 96), (24, 86), True)
    win = _frame((6, 0), (-8, -4), (24, 80), (-20, 40), True, raised=True)
    return (f'<g class="body">'
            f'<g class="run">{frames}</g><g class="idle">{idle}</g><g class="win"><g class="wj">{win}</g></g></g>')


# ---------- boss ----------

BOSS = f"""<g stroke="{INK}" stroke-width="3.5" stroke-linejoin="round" stroke-linecap="round">
<path fill="none" stroke-width="9" d="M-62 -40L-98 -56L-108 -4M-66 -24L-92 -24L-90 -3M62 -40L98 -56L108 -4M66 -24L92 -24L90 -3"/>
<path fill="none" stroke="#4b2a8a" stroke-width="4" d="M-62 -40L-98 -56L-108 -4M-66 -24L-92 -24L-90 -3M62 -40L98 -56L108 -4M66 -24L92 -24L90 -3"/>
<path fill="url(#horn)" d="M-34 -112C-66 -142 -58 -178 -32 -192C-40 -164 -24 -140 -12 -122Z"/>
<path fill="url(#horn)" d="M34 -112C66 -142 58 -178 32 -192C40 -164 24 -140 12 -122Z"/>
<path fill="url(#shell)" d="M-76 -30C-86 -98 -34 -128 0 -128C34 -128 86 -98 76 -30C54 -8 -54 -8 -76 -30Z"/>
<path fill="none" stroke="#ff5fa0" stroke-width="2.4" d="M38 -118C66 -104 80 -76 76 -36"/>
<path fill="none" stroke="#1a0f33" stroke-width="2.4" d="M0 -128V-82M-44 -112C-52 -98 -58 -86 -60 -70M44 -112C52 -98 58 -86 60 -70"/>
<circle cx="-34" cy="-68" r="34" fill="url(#eyeglow)" stroke="none"/><circle cx="34" cy="-68" r="34" fill="url(#eyeglow)" stroke="none"/>
<path fill="#120a26" d="M-58 -50C-36 -82 36 -82 58 -50C42 -8 -42 -8 -58 -50Z"/>
<path fill="url(#eye)" stroke-width="2.4" d="M-50 -82L-12 -64L-16 -52L-46 -64Z"/>
<path fill="url(#eye)" stroke-width="2.4" d="M50 -82L12 -64L16 -52L46 -64Z"/>
<path fill="{PAPER}" stroke-width="2.2" d="M-36 -40L-28 -24L-20 -38L-12 -22L-4 -36L4 -22L12 -38L20 -24L28 -38L36 -26L30 -40Z"/>
<text x="0" y="-92" text-anchor="middle" font-size="19" font-weight="800" fill="#ff8fbb" stroke="none">DEAD</text>
</g>
<g class="gl" stroke="none" opacity=".75"><rect x="-96" y="-104" width="50" height="6" fill="#49f2ff"/><rect x="40" y="-62" width="66" height="5" fill="#ff5fa0"/><rect x="-70" y="-26" width="36" height="5" fill="#49f2ff"/></g>"""


# ---------- scenery ----------

_cloud_ids = iter(range(1000))


def _cloud(circles, tiers):
    """Cel-paint a cloud: the same silhouette, shifted away from the sun and clipped to itself."""
    shape = lambda dx, dy: "".join(f'<circle cx="{x + dx:.0f}" cy="{y + dy:.0f}" r="{r:.0f}"/>' for x, y, r in circles)
    clip_id = f"cl{next(_cloud_ids)}"
    base_fill = tiers[0][0]
    layers = "".join(f'<g fill="{fill}">{shape(dx, dy)}</g>' for fill, dx, dy in tiers[1:])
    return (f'<clipPath id="{clip_id}">{shape(0, 0)}</clipPath><g fill="{base_fill}">{shape(0, 0)}</g>'
            f'<g clip-path="url(#{clip_id})">{layers}</g>')


def _bank(rng, x0, x1, base, height, tiers):
    circles = []
    x = x0
    while x < x1:
        t = (x - x0) / (x1 - x0)
        hump = math.sin(math.pi * t) ** .7
        r = rng.uniform(.34, .52) * height * (.45 + hump)
        circles.append((x, base - r * .55 - rng.uniform(0, height * .55) * hump, r))
        circles.append((x + rng.uniform(-14, 14), base - r * .25, r * .8))
        x += r * rng.uniform(.7, 1.05)
    return _cloud(circles, tiers), circles


def _skyline(rng, base, min_h, max_h, width_range, fill, lit=None):
    rects, windows, x = [], [], -10
    while x < WIDTH + 10:
        w = rng.randint(*width_range)
        h = rng.randint(min_h, max_h)
        rects.append(f"M{x} {base}V{base - h}h{w}V{base}Z")
        if lit:
            for wy in range(base - h + 7, base - 4, 9):
                for wx in range(x + 5, x + w - 5, 8):
                    if rng.random() < .32:
                        windows.append(f"M{wx} {wy}h4v5h-4Z")
        x += w + rng.randint(-3, 6)
    out = f'<path d="{"".join(rects)}" fill="{fill}"/>'
    if windows:
        out += f'<path d="{"".join(windows)}" fill="{lit}" opacity=".85"/>'
    return out


def _blossom_cluster(rng, cx, cy, spread, count):
    tones = ["#ffd9e6", "#ffb6cf", "#ff8fb8", "#f5709f"]
    out = []
    for i in range(count):
        a, dist = rng.uniform(0, math.tau), rng.uniform(0, spread) ** 1
        x, y = cx + math.cos(a) * dist, cy + math.sin(a) * dist * .75
        r = rng.uniform(4.6, 7.6)
        out.append(f'<use href="#fl" transform="translate({x:.0f} {y:.0f}) rotate({rng.randint(0, 72)}) scale({r / 6:.2f})" fill="{tones[min(3, int(i / count * 4))]}"/>')
    return "".join(reversed(out))


def _branch(rng, points, width):
    d = f"M{points[0][0]} {points[0][1]}" + "".join(f"L{x} {y}" for x, y in points[1:])
    return f'<path d="{d}" fill="none" stroke="#1f1233" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>'


def _pole(x, top, base):
    return (f'<g stroke="#1b1236" fill="none" stroke-linecap="round">'
            f'<path d="M{x} {base}V{top}" stroke-width="7"/>'
            f'<path d="M{x - 40} {top + 12}H{x + 40}M{x - 32} {top + 30}H{x + 32}" stroke-width="4.5"/>'
            f'</g><g fill="#1b1236"><rect x="{x - 14}" y="{top + 42}" width="28" height="34" rx="5"/>'
            f'<circle cx="{x - 34}" cy="{top + 7}" r="3.5"/><circle cx="{x + 34}" cy="{top + 7}" r="3.5"/></g>')


def _wire(x1, y1, x2, y2, sag, opacity=1):
    return (f'<path d="M{x1} {y1}Q{(x1 + x2) / 2} {max(y1, y2) + sag} {x2} {y2}" fill="none" '
            f'stroke="#1b1236" stroke-width="2" opacity="{opacity}"/>')


def backdrop(rng, height):
    """The static dusk sky, city and rooftop, plus the drifting cloud layers."""
    sun_x, sun_y = 905, ROOF - 16
    stars = "".join(f'<circle cx="{rng.randint(0, WIDTH)}" cy="{rng.randint(4, 92)}" r="{rng.choice([.9, 1.1, 1.6])}" opacity="{rng.uniform(.35, .95):.2f}"/>'
                    for _ in range(70))
    high_tiers = [("#ff9aa0", 0, 0), ("#c75a9a", -8, -13), ("#7f3f98", -18, -32), ("#4e3088", -28, -58)]
    mid_tiers = [("#ffe0a0", 0, 0), ("#ffa07a", -10, -16), ("#e0608f", -22, -38), ("#963f96", -34, -66)]
    low_tiers = [("#fff6d0", 0, 0), ("#ffc580", -8, -14), ("#f88a7a", -18, -34), ("#c4508a", -30, -60)]
    bank_a, _ = _bank(rng, 40, 520, 128, 112, high_tiers)
    bank_b, _ = _bank(rng, 640, 1240, 112, 96, high_tiers)
    bank_c, _ = _bank(rng, -30, 430, 214, 118, mid_tiers)
    bank_d, _ = _bank(rng, 480, 830, 208, 96, mid_tiers)
    bank_e, _ = _bank(rng, 980, 1260, 212, 104, low_tiers)
    rays = "".join(f'<path d="M{sun_x} {sun_y}L{sun_x + 900 * math.cos(a - .035):.0f} {sun_y + 900 * math.sin(a - .035):.0f}'
                   f'L{sun_x + 900 * math.cos(a + .035):.0f} {sun_y + 900 * math.sin(a + .035):.0f}Z"/>'
                   for a in [math.radians(d) for d in (196, 214, 234, 256, 284, 306, 330)])
    far = _skyline(rng, ROOF, 22, 74, (26, 58), "#8a3f8c")
    mid = _skyline(rng, ROOF, 12, 46, (34, 72), "#402060", "#ffd58a")
    wires = (_wire(-20, 74, 300, 88, 34) + _wire(-20, 92, 300, 106, 34) +
             _wire(300, 88, 1060, 72, 62) + _wire(300, 106, 1060, 90, 62) +
             _wire(268, 88, 1028, 72, 78, .85) +
             _wire(1060, 72, 1230, 62, 22) + _wire(1060, 90, 1230, 80, 22))
    bird = '<path d="M0 0Q6 -6 11 0Q16 -6 22 0Q16 -2 11 3Q6 -2 0 0Z"/>'
    birds = "".join(f'<g transform="translate({x} {y}) scale({s})" fill="#1b1236">{bird}</g>'
                    for x, y, s in [(640, 42, 1), (676, 30, .8), (704, 50, .7)])
    roof_clutter = (
        f'<g stroke="{INK}" stroke-width="2.6" stroke-linejoin="round">'
        f'<rect x="96" y="{ROOF - 42}" width="82" height="42" rx="3" fill="#2a1f55"/>'
        f'<rect x="104" y="{ROOF - 34}" width="44" height="26" rx="2" fill="#191238"/>'
        f'<path d="M108 {ROOF - 28}h36M108 {ROOF - 22}h36M108 {ROOF - 16}h36" stroke="#3b2f6b" stroke-width="2"/>'
        f'<circle cx="162" cy="{ROOF - 21}" r="9" fill="#191238"/>'
        f'<path d="M176 {ROOF - 40}L178 {ROOF - 4}" stroke="{RIM}" stroke-width="2"/>'
        f'</g><g stroke="#1b1236" stroke-width="3" fill="none" stroke-linecap="round">'
        f'<path d="M1130 {ROOF}V{ROOF - 86}M1110 {ROOF - 72}H1150M1116 {ROOF - 56}H1144M1120 {ROOF - 42}H1140"/></g>')
    rail_bars = "".join(f"M{x} {ROOF - 22}V{ROOF}" for x in range(0, WIDTH + 1, 24))
    rail = (f'<path d="{rail_bars}" stroke="#1d1440" stroke-width="2.4"/>'
            f'<path d="M0 {ROOF - 24}H{WIDTH}" stroke="#1d1440" stroke-width="4.5"/>'
            f'<path d="M0 {ROOF - 26}H{WIDTH}" stroke="{RIM}" stroke-width="1.4" opacity=".75"/>')
    right_branch = (_branch(rng, [(1210, 18), (1140, 34), (1078, 22), (1006, 34)], 6) +
                    _branch(rng, [(1140, 34), (1102, 60), (1056, 62)], 3.5) +
                    _blossom_cluster(rng, 1184, 26, 36, 26) + _blossom_cluster(rng, 1112, 34, 40, 30) +
                    _blossom_cluster(rng, 1062, 58, 26, 18) + _blossom_cluster(rng, 1030, 26, 32, 24))
    return (f'<rect width="{WIDTH}" height="{height}" fill="url(#sky)"/>'
            f'<g fill="#fff">{stars}</g>'
            f'<circle cx="{sun_x}" cy="{sun_y}" r="420" fill="url(#halo)"/>'
            f'<g fill="#fff3cf" opacity=".09">{rays}</g>'
            f'<g class="dr1">{bank_a}</g><g class="dr2">{bank_b}</g>'
            f'<circle cx="{sun_x}" cy="{sun_y}" r="74" fill="url(#sun)"/>'
            f'<g class="dr2">{bank_c}</g><g class="dr1">{bank_d}{bank_e}</g>'
            f'{far}{mid}'
            f'<circle cx="{sun_x}" cy="{ROOF}" r="240" fill="url(#halo2)"/>'
            f'{wires}{birds}{_pole(300, 58, ROOF)}{_pole(1060, 42, ROOF)}'
            f'{rail}{roof_clutter}{right_branch}')


def foreground_petals(rng, height):
    out, css = [], []
    for i in range(12):
        start_x = rng.randint(-60, WIDTH)
        start_y = rng.randint(-40, 60)
        dx, dy = rng.randint(160, 340), rng.randint(height - 40, height + 40)
        duration, delay = rng.uniform(9, 16), rng.uniform(0, 12)
        out.append(f'<g class="fa{i}"><use href="#p" x="{start_x}" y="{start_y}" fill="{rng.choice([PINK, "#ffd0e0", PAPER])}" opacity=".95"/></g>')
        css.append(f"@keyframes fa{i}{{to{{transform:translate({dx}px,{dy}px) rotate(50deg)}}}}"
                   f".fa{i}{{transform-box:fill-box;animation:fa{i} {duration:.1f}s linear -{delay:.1f}s infinite}}")
    return "".join(out), "".join(css)


DEFS = f"""
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="{ROOF + 10}" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#17124a"/><stop offset=".3" stop-color="#3b2a86"/><stop offset=".55" stop-color="#9a3f92"/><stop offset=".78" stop-color="#f26a72"/><stop offset="1" stop-color="#ffc36b"/></linearGradient>
<radialGradient id="halo"><stop offset="0" stop-color="#fff0b8" stop-opacity=".75"/><stop offset=".4" stop-color="#ffb06b" stop-opacity=".28"/><stop offset="1" stop-color="#ff8a6b" stop-opacity="0"/></radialGradient>
<radialGradient id="halo2"><stop offset="0" stop-color="#ffd58a" stop-opacity=".5"/><stop offset="1" stop-color="#ffb06b" stop-opacity="0"/></radialGradient>
<radialGradient id="sun"><stop offset="0" stop-color="#fffbe6"/><stop offset=".8" stop-color="#fff0b8"/><stop offset="1" stop-color="#ffd58a"/></radialGradient>
<linearGradient id="iris" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2c1450"/><stop offset=".5" stop-color="#b83a85"/><stop offset=".85" stop-color="#ff9a5c"/><stop offset="1" stop-color="#ffe08a"/></linearGradient>
<linearGradient id="skin" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#f7c7b4"/><stop offset=".55" stop-color="#ffe6d6"/><stop offset="1" stop-color="#ffd3a8"/></linearGradient>
<linearGradient id="hair" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a3a88"/><stop offset=".55" stop-color="#352963"/><stop offset="1" stop-color="#5a2d78"/></linearGradient>
<linearGradient id="hairtail" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#32265f"/><stop offset=".5" stop-color="#3f2c74"/><stop offset=".95" stop-color="{PINK}"/></linearGradient>
<linearGradient id="lockS" x1="0" y1="0" x2="0" y2="1"><stop offset=".4" stop-color="#352963"/><stop offset="1" stop-color="{PINK}"/></linearGradient>
<linearGradient id="hood" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#1c2042"/><stop offset=".7" stop-color="#2c3160"/><stop offset="1" stop-color="#4a4378"/></linearGradient>
<linearGradient id="horn" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#2a1a55"/><stop offset=".6" stop-color="#7a2f88"/><stop offset="1" stop-color="{GOLD}"/></linearGradient>
<linearGradient id="shell" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6a3ab0"/><stop offset=".5" stop-color="#3a2276"/><stop offset="1" stop-color="#1a0f33"/></linearGradient>
<linearGradient id="eye" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff0a8"/><stop offset=".5" stop-color="#ff7a4a"/><stop offset="1" stop-color="#e5174d"/></linearGradient>
<radialGradient id="eyeglow"><stop offset="0" stop-color="#ff4d6d" stop-opacity=".75"/><stop offset="1" stop-color="#ff4d6d" stop-opacity="0"/></radialGradient>
<linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a1f5c"/><stop offset="1" stop-color="#120c2c"/></linearGradient>
<linearGradient id="wallsun" x1="0" y1="0" x2="1" y2="0"><stop offset=".5" stop-color="#ff9a6b" stop-opacity="0"/><stop offset=".76" stop-color="#ff9a6b" stop-opacity=".2"/><stop offset="1" stop-color="#ff9a6b" stop-opacity="0"/></linearGradient>
<linearGradient id="beam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fffbe6"/><stop offset=".6" stop-color="#ffd0e0"/><stop offset="1" stop-color="#ff8fb8" stop-opacity=".2"/></linearGradient>
<radialGradient id="gc"><stop offset="0" stop-color="#7cf5ee" stop-opacity=".5"/><stop offset="1" stop-color="#7cf5ee" stop-opacity="0"/></radialGradient>
<radialGradient id="gp"><stop offset="0" stop-color="#ffb3cf" stop-opacity=".65"/><stop offset="1" stop-color="#ffb3cf" stop-opacity="0"/></radialGradient>
<linearGradient id="band" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#3b1a78"/><stop offset=".45" stop-color="#d13a8a"/><stop offset=".8" stop-color="#ff8a5c"/><stop offset="1" stop-color="#ffd27a"/></linearGradient>
<linearGradient id="title" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fffbe6"/><stop offset=".55" stop-color="{GOLD}"/><stop offset="1" stop-color="#ff7a5c"/></linearGradient>
<linearGradient id="clear" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fffbe6"/><stop offset=".5" stop-color="#ffd8e6"/><stop offset="1" stop-color="{PINK}"/></linearGradient>
<pattern id="dots" width="11" height="11" patternUnits="userSpaceOnUse" patternTransform="rotate(30)"><circle cx="5.5" cy="5.5" r="2.1" fill="#160f2e" opacity=".3"/></pattern>
<path id="p" d="M0 -7C5.5 -7 8 -1.5 0 7C-8 -1.5 -5.5 -7 0 -7Z" stroke="{INK}" stroke-width=".8"/>
<g id="fl"><circle cx="0" cy="-3.6" r="3.2"/><circle cx="3.4" cy="-1.1" r="3.2"/><circle cx="2.1" cy="2.9" r="3.2"/><circle cx="-2.1" cy="2.9" r="3.2"/><circle cx="-3.4" cy="-1.1" r="3.2"/><circle r="1.5" fill="{GOLD}"/></g>
"""


def speed_lines(cx, cy, seed=7):
    rng = random.Random(seed)
    out = []
    for i in range(46):
        a = i / 46 * math.tau + rng.uniform(-.03, .03)
        near, far = rng.uniform(250, 420), 1300
        spread = rng.uniform(.006, .022)
        out.append(f"M{cx + near * math.cos(a):.0f} {cy + near * math.sin(a):.0f}"
                   f"L{cx + far * math.cos(a - spread):.0f} {cy + far * math.sin(a - spread):.0f}"
                   f"L{cx + far * math.cos(a + spread):.0f} {cy + far * math.sin(a + spread):.0f}Z")
    return "".join(out)
