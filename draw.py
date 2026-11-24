#!/usr/bin/env python3
"""Draw the front page for Monday 23 November 2026.

Local build tool only: it runs here, on this machine, to produce entry.png.
The grader never runs this file -- the entrypoint is main.ts (Node 22,
standard library only), which copies entry.png to the output directory.
Deterministic: no randomness, no network, no timestamps in the image;
the same source always writes the same PNG bytes.

Layout (1024 x 1024, newspaper front page):
  masthead -> 3 hero stories with drawn art -> 6 cards -> world map
  with numbered pins + "ALSO ON MONDAY" list of 16 more stories.

Sources (all first reported / confirmed Monday 23 November 2026):
  Reuters, CNN, BBC, AP, The Guardian, Le Monde, The Times, Eurostat.
  Story list and sources are in SOURCES.md next to this file.
"""

import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 242, 231)      # warm newsprint
INK = (20, 33, 61)           # deep navy ink
INK_SOFT = (58, 68, 92)
RED = (185, 28, 28)
GOLD = (184, 134, 11)
GOLD_LIGHT = (212, 175, 55)
TEAL = (13, 110, 110)
GREEN = (22, 101, 52)
CREAM_LINE = (210, 198, 170)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, xy, text, fnt, fill, width, leading=None):
    """Draw wrapped text; returns the y just below the last line."""
    x, y = xy
    leading = leading if leading is not None else int(fnt.size * 1.22)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def panel(draw, box, fill, outline=None, width=2):
    draw.rounded_rectangle(box, radius=6, fill=fill,
                           outline=outline, width=width)


# ---------------------------------------------------------------- stories
HEROES = [
    {
        "num": "1", "kicker": "MARKETS  •  CALIFORNIA",
        "head": "Huang is back — and Nvidia soars 31%",
        "deck": "Eleven days after resigning, Jensen Huang is reinstated as chief "
                "executive. Shares jump 31%, lifting the Nasdaq 6% and the S&P 500 5%.",
        "art": "nvidia",
    },
    {
        "num": "2", "kicker": "WAR AT SEA  •  LIBYA",
        "head": "Ukraine sinks Russian warship off Libya",
        "deck": "Zelensky confirms sea drones sank the corvette Merkury in Benghazi "
                "and hit the cargo ship Angara.",
        "art": "benghazi",
    },
    {
        "num": "3", "kicker": "CLIMATE  •  ANTALYA",
        "head": "COP31 collapses with no deal",
        "deck": "The longest climate talks ever end in failure: the EU rejects a pact "
                "that never mentions fossil fuels. 90 nations still sign a power pledge.",
        "art": "cop31",
    },
]

CARDS = [
    ("4", "KYIV UNDER FIRE",
     "Kyiv toll hits 15 as boy is pulled alive",
     "Rescuers free a 7-year-old after 14 hours in the rubble; a Russian "
     "drone spends 8 minutes in Polish airspace."),
    ("5", "SUDAN",
     "Drones hit homes and a UN building in Khartoum",
     "The UN condemns strikes on homes and its own compound; 3 staff "
     "hurt, children among the dead."),
    ("6", "INDONESIA",
     "Factory fire kills at least 24, dozens missing",
     "The toll from the Cikande sweets-factory fire reaches 24 as "
     "rescuers search the ruins."),
    ("7", "IRAN  •  WASHINGTON",
     "Trump piles on Iran sanctions; Vance in Washington",
     "New sanctions target the regime's 'last financial lifeline' as the "
     "vice-president presses Qatar for talks."),
    ("8", "TECH DEALS",
     "CrowdStrike buys Zscaler for $43.9 billion",
     "The all-stock cybersecurity mega-deal lands on the same day markets "
     "roar back."),
    ("9", "WEST BANK",
     "Settler attacks called 'Jewish terrorism'",
     "Opposition leader Eisenkot denounces the violence as Israel opens "
     "an inquiry into torched cars."),
]

ALSO = [
    "NHS begins a trial of AI in breast-cancer screening.",
    "Measles deaths in Pennsylvania rise to nine; 1,638 cases.",
    "Trump orders the Army to pause a toxic blast in Iowa.",
    "US admits deporting an American citizen to Mexico.",
    "Mexican soldiers attacked after a drug lord's arrest.",
    "Gaza strikes kill at least 3 on Monday, incl. an UNRWA worker.",
    "Thailand–Cambodia truce holds after Monday talks.",
    "Tyson Fury reveals a schizophrenia diagnosis.",
    "Malaysia to send thousands of Myanmar migrants home.",
    "UN: broken trade routes threaten food aid for 7.3m people.",
    "South Korea's education minister quits over AI cheating.",
    "Bolsonaro taken to intensive care with bowel trouble.",
    "Democrats take 258 House seats, biggest majority since 1992.",
    "NATO meets after Russian missiles land in Poland.",
    "Lebanese villagers return as Israeli troops pull back.",
    "Pakistan pilot set to fly to China's Tiangong station.",
]

# (number, label, lon, lat) for the map pins
PINS = [
    ("1", "California", -122.0, 37.4),
    ("2", "Benghazi", 20.1, 32.1),
    ("3", "Antalya", 30.7, 36.9),
    ("4", "Kyiv", 30.5, 50.5),
    ("5", "Khartoum", 32.5, 15.6),
    ("6", "Indonesia", 106.8, -6.2),
    ("7", "Washington", -77.0, 38.9),
    ("8", "West Bank", 35.2, 31.9),
]

# Display nudges (px) for pins that would overlap on a small world map.
PIN_NUDGE = {"2": (-16, 12), "3": (14, -12), "4": (0, -12),
             "5": (8, 10), "8": (18, 8)}

# Rough continent outlines in (lon, lat); drawn as one filled landmass.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 80),
     (-80, 73), (-76, 62), (-70, 58), (-65, 60), (-60, 52), (-55, 47),
     (-70, 42), (-75, 35), (-80, 32), (-81, 26), (-84, 30), (-90, 29),
     (-97, 26), (-105, 23), (-110, 24), (-115, 30), (-125, 40),
     (-125, 49), (-140, 60), (-155, 58), (-165, 60)],
    [(-58, 64), (-45, 60), (-40, 70), (-55, 76), (-65, 76), (-60, 70)],
    [(-80, 9), (-72, 12), (-62, 10), (-52, 5), (-50, 0), (-44, -3),
     (-35, -8), (-40, -20), (-48, -28), (-58, -35), (-65, -41),
     (-70, -50), (-74, -54), (-72, -40), (-72, -20), (-77, -12), (-80, -5)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31),
     (35, 28), (43, 12), (51, 11), (48, 0), (40, -10), (35, -18),
     (32, -29), (25, -34), (18, -35), (15, -27), (12, -18), (9, 4),
     (-8, 5), (-13, 8)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57),
     (10, 59), (18, 56), (21, 55), (28, 59), (30, 60), (24, 65),
     (18, 69), (12, 71), (5, 60), (5, 58), (-5, 50)],
    [(35, 36), (45, 40), (55, 42), (65, 45), (75, 55), (85, 60),
     (100, 65), (120, 70), (140, 72), (160, 70), (170, 66), (178, 65),
     (170, 60), (162, 60), (158, 52), (142, 50), (140, 40), (135, 35),
     (130, 33), (127, 35), (122, 38), (120, 32), (115, 23), (110, 20),
     (108, 12), (104, 9), (100, 7), (98, 10), (92, 16), (88, 22),
     (85, 20), (80, 15), (77, 8), (73, 20), (66, 25), (61, 25),
     (57, 27), (52, 29), (48, 30), (44, 29), (40, 32), (36, 36)],
    [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32),
     (137, -35), (140, -38), (147, -39), (150, -37), (153, -27),
     (150, -22), (146, -19), (142, -11), (137, -12), (132, -12),
     (126, -14), (122, -17), (118, -20)],
]

# ---------------------------------------------------------------- art
def art_nvidia(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(16, 68, 32))
    # circuit traces
    for yy in (y0 + 26, y0 + 52, y0 + 78):
        d.line([(x0 + 12, yy), (x1 - 90, yy)], fill=GOLD_LIGHT, width=3)
        d.ellipse([x1 - 96, yy - 5, x1 - 84, yy + 5], fill=GOLD_LIGHT)
    for xx in (x0 + 40, x0 + 90, x0 + 140):
        d.line([(xx, y0 + 12), (xx, y0 + 58)], fill=(60, 140, 80), width=3)
    # chip
    cx0, cy0, cx1, cy1 = x0 + 118, y0 + 58, x0 + 198, y0 + 118
    d.rectangle([cx0, cy0, cx1, cy1], fill=(8, 40, 20),
                outline=GOLD_LIGHT, width=3)
    d.text((cx0 + 18, cy0 + 14), "NVDA", font=SANS_B(24), fill=(255, 255, 255))
    d.text((cx0 + 14, cy0 + 40), "HUANG", font=SANS_B(13), fill=GOLD_LIGHT)
    # rising arrow, ending well left of the +31% badge at top right
    pts = [(x0 + 18, y1 - 22), (x0 + 62, y1 - 48), (x0 + 104, y1 - 38),
           (x0 + 150, y1 - 72), (x0 + 210, y1 - 88), (x1 - 130, y1 - 96)]
    d.line(pts, fill=(120, 255, 150), width=5)
    d.polygon([(x1 - 146, y1 - 96), (x1 - 124, y1 - 96), (x1 - 130, y1 - 76)],
              fill=(120, 255, 150))
    # +31% badge on a dark pill so nothing crosses the text
    d.rounded_rectangle([x1 - 118, y0 + 8, x1 - 10, y0 + 48], radius=8,
                        fill=(8, 40, 20), outline=GOLD_LIGHT, width=2)
    d.text((x1 - 108, y0 + 12), "+31%", font=SANS_B(30), fill=(120, 255, 150))


def art_benghazi(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(23, 58, 94))
    # sky band + sea bands
    d.rectangle([x0, y0, x1, y0 + 52], fill=(42, 78, 116))
    for i, yy in enumerate(range(y0 + 62, y1 - 6, 14)):
        d.line([(x0 + 8, yy), (x1 - 8, yy)], fill=(70, 120, 165), width=3)
    # smoke
    for (sx, sy, sr) in ((x0 + 120, y0 + 30, 26), (x0 + 150, y0 + 16, 32),
                         (x0 + 185, y0 + 34, 24)):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(90, 90, 96))
    # flames
    for (fx, fy, fs) in ((x0 + 128, y0 + 66, 26), (x0 + 158, y0 + 70, 20),
                         (x0 + 100, y0 + 72, 16)):
        d.polygon([(fx - fs, fy), (fx, fy - fs * 2), (fx + fs, fy)],
                  fill=(255, 140, 0))
        d.polygon([(fx - fs // 2, fy), (fx, fy - fs), (fx + fs // 2, fy)],
                  fill=(255, 220, 80))
    # warship hull, listing
    d.polygon([(x0 + 52, y0 + 96), (x0 + 250, y0 + 88), (x0 + 262, y0 + 108),
               (x0 + 60, y0 + 116)], fill=(18, 24, 34))
    d.rectangle([x0 + 96, y0 + 62, x0 + 150, y0 + 94], fill=(30, 38, 52))
    d.line([(x0 + 122, y0 + 62), (x0 + 122, y0 + 44)], fill=(30, 38, 52), width=4)
    # sea drones: small hulls with wakes
    for (dx, dy) in ((x0 + 30, y1 - 26), (x0 + 210, y1 - 18), (x0 + 268, y1 - 30)):
        d.ellipse([dx - 8, dy - 4, dx + 8, dy + 4], fill=(240, 240, 240))
        d.line([(dx - 22, dy + 2), (dx - 8, dy)], fill=(200, 220, 240), width=2)
    d.text((x0 + 12, y0 + 8), "BENGHAZI", font=SANS_B(13), fill=(255, 255, 255))


def art_cop31(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(146, 96, 44))
    # sun-baked ground + globe, left of centre so the stamp fits right
    d.ellipse([x0 + 62, y0 + 18, x0 + 182, y0 + 138], fill=(52, 130, 170))
    d.ellipse([x0 + 92, y0 + 44, x0 + 136, y0 + 76], fill=(70, 160, 90))
    d.ellipse([x0 + 122, y0 + 88, x0 + 160, y0 + 118], fill=(70, 160, 90))
    # crack across the globe
    d.line([(x0 + 76, y0 + 30), (x0 + 106, y0 + 66), (x0 + 94, y0 + 92),
            (x0 + 134, y0 + 128)], fill=(30, 40, 60), width=4)
    # empty chairs row
    for i in range(5):
        cx = x0 + 14 + i * 34
        d.rectangle([cx, y1 - 30, cx + 24, y1 - 14], fill=(90, 58, 26))
        d.line([(cx + 3, y1 - 30), (cx + 3, y1 - 46)], fill=(90, 58, 26), width=4)
    # NO DEAL stamp
    d.rounded_rectangle([x0 + 168, y0 + 96, x1 - 14, y0 + 130], radius=6,
                        outline=RED, width=4)
    d.text((x0 + 180, y0 + 102), "NO DEAL", font=SANS_B(22), fill=RED)


ART = {"nvidia": art_nvidia, "benghazi": art_benghazi, "cop31": art_cop31}


# ---------------------------------------------------------------- page
def draw_page():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead
    d.rectangle([0, 0, W, 116], fill=INK)
    d.rectangle([0, 116, W, 120], fill=GOLD)
    d.text((28, 12), "THE WORLD IN ONE PAGE", font=SERIF_B(46), fill=(255, 255, 255))
    d.text((28, 70), "MONDAY  23  NOVEMBER  2026", font=SANS_B(24), fill=GOLD_LIGHT)
    d.text((W - 28 - d.textlength("ONE DAY  •  ONE IMAGE", font=SANS_B(15)),
            78), "ONE DAY  •  ONE IMAGE", font=SANS_B(15), fill=(200, 205, 220))
    d.text((W - 28 - d.textlength("25 stories  •  3 heroes  •  6 cards", font=SANS(13)),
            20), "25 stories  •  3 heroes  •  6 cards", font=SANS(13),
           fill=(200, 205, 220))

    # --- heroes
    hx, hy, hw, hh, gap = 24, 134, 317, 318, 12
    for i, hero in enumerate(HEROES):
        x = hx + i * (hw + gap)
        panel(d, [x, hy, x + hw, hy + hh], fill=(255, 255, 255),
              outline=CREAM_LINE, width=2)
        d.rectangle([x, hy, x + hw, hy + 26], fill=RED)
        d.text((x + 10, hy + 4), hero["num"] + "  " + hero["kicker"],
               font=SANS_B(13), fill=(255, 255, 255))
        ART[hero["art"]](d, [x + 8, hy + 34, x + hw - 8, hy + 168])
        y = hy + 178
        y = para(d, (x + 12, y), hero["head"], SERIF_B(24), INK, hw - 24, leading=28)
        para(d, (x + 12, y + 6), hero["deck"], SANS(14), INK_SOFT, hw - 24, leading=18)

    # --- cards (3 x 2)
    cx, cy, cw, chh = 24, 466, 317, 112
    for i, (num, kick, head, deck) in enumerate(CARDS):
        x = cx + (i % 3) * (cw + gap)
        y = cy + (i // 3) * (chh + 12)
        panel(d, [x, y, x + cw, y + chh], fill=(255, 255, 255),
              outline=CREAM_LINE, width=2)
        d.rectangle([x, y, x + 8, y + chh], fill=TEAL)
        d.text((x + 18, y + 8), num + "  " + kick, font=SANS_B(12), fill=TEAL)
        yy = para(d, (x + 18, y + 28), head, SANS_B(16), INK, cw - 30, leading=19)
        para(d, (x + 18, yy + 3), deck, SANS(12), INK_SOFT, cw - 30, leading=15)

    # --- bottom: map (left) + also list (right)
    by = 716
    panel(d, [24, by, 494, 988], fill=(255, 255, 255), outline=CREAM_LINE, width=2)
    d.text((40, by + 10), "WHERE IT HAPPENED", font=SANS_B(17), fill=INK)
    d.text((40, by + 34), "Numbered pins mark the heroes and cards above.",
           font=SANS(12), fill=INK_SOFT)
    map_box = (40, by + 58, 478, 908)
    draw_map(d, map_box)
    d.text((40, 922), "1 California  •  2 Benghazi  •  3 Antalya  •  4 Kyiv",
           font=SANS(12), fill=INK_SOFT)
    d.text((40, 940), "5 Khartoum  •  6 Indonesia  •  7 Washington  •  8 West Bank",
           font=SANS(12), fill=INK_SOFT)
    d.text((40, 962), "Every pin is a place in Monday's news.",
           font=SANS_B(12), fill=INK)

    panel(d, [506, by, 1000, 988], fill=(255, 255, 255), outline=CREAM_LINE, width=2)
    d.text((522, by + 10), "ALSO ON MONDAY — 16 MORE STORIES", font=SANS_B(16), fill=INK)
    d.line([(522, by + 38), (984, by + 38)], fill=GOLD, width=3)
    y = by + 46
    for i, item in enumerate(ALSO, start=10):
        d.text((522, y), str(i) + ".", font=SANS_B(12), fill=RED)
        y = para(d, (556, y), item, SANS(12), INK, 984 - 556, leading=14)
        y += 1

    # --- footer
    d.text((24, 998), "Sources: Reuters, BBC, CNN, AP, The Guardian, Le Monde, The Times, Eurostat — "
           "all reported Monday 23 November 2026.", font=SANS(11), fill=INK_SOFT)
    return img


def draw_map(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(214, 233, 244))
    mw, mh = x1 - x0, y1 - y0

    def proj(lon, lat):
        return (x0 + (lon + 180.0) / 360.0 * mw,
                y0 + (75.0 - lat) / 130.0 * mh)

    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=(122, 158, 110))
    for (num, _label, lon, lat) in PINS:
        px, py = proj(lon, lat)
        # nudge the crowded Mediterranean pins apart, with a leader line
        # from the true spot to the displayed pin
        dx, dy = PIN_NUDGE.get(num, (0, 0))
        qx, qy = px + dx, py + dy
        if (dx, dy) != (0, 0):
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED)
            d.line([(px, py), (qx, qy)], fill=RED, width=2)
        d.ellipse([qx - 11, qy - 11, qx + 11, qy + 11], fill=RED,
                  outline=(255, 255, 255), width=2)
        tw = d.textlength(num, font=SANS_B(12))
        d.text((qx - tw / 2, qy - 8), num, font=SANS_B(12), fill=(255, 255, 255))


if __name__ == "__main__":
    image = draw_page()
    image.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")
