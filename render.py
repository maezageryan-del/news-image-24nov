#!/usr/bin/env python3
"""news-image-20261124 — draws the 24 November 2026 world-news broadsheet.

Deterministic: no network, no clock, no randomness. Reads stories.json
beside this file and writes entry.png (1024x1024, <= 1 MiB).
Run:  python3 render.py [out.png]
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
MARGIN = 28
RIGHT = W - MARGIN

PAPER = (247, 243, 234)
INK = (26, 26, 24)
RED = (178, 34, 34)
DARKRED = (140, 22, 22)
GREY = (110, 104, 92)
LIGHT = (232, 226, 212)
BLUE = (28, 68, 120)
GREEN = (28, 110, 60)
GOLD = (176, 132, 30)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF = "DejaVuSerif.ttf"
SERIF_B = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to a pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(draw, text, fnt, max_w, ellipsis="..."):
    """Truncate one line to a pixel width."""
    if draw.textlength(text, font=fnt) <= max_w:
        return text
    while text and draw.textlength(text + ellipsis, font=fnt) > max_w:
        text = text[:-1]
    return text + ellipsis


def load_stories():
    with open(os.path.join(HERE, "stories.json"), encoding="utf-8") as fh:
        return json.load(fh)


def draw_hatch(draw):
    """Fine paper texture: faint cross-hatch, deterministic."""
    step = 7
    for x in range(0, W + H, step):
        draw.line([(x, 0), (x - H, H)], fill=(236, 231, 218), width=1)
    for x in range(0, W + H, step):
        draw.line([(x, 0), (x + H, H)], fill=(238, 233, 221), width=1)
    for y in range(0, H, 64):
        draw.line([(0, y), (W, y)], fill=(240, 235, 224), width=1)


def draw_lead_art(draw, kind, x, y, w, h):
    """Layered drawn scene for a lead panel."""
    if kind == "nvidia":
        draw.rectangle([x, y, x + w, y + h], fill=(16, 42, 28))
        # chip
        cx, cy, cw, chh = x + 24, y + 18, 74, 54
        draw.rectangle([cx, cy, cx + cw, cy + chh], fill=(30, 80, 52),
                       outline=(120, 200, 150), width=2)
        draw.rectangle([cx + 16, cy + 12, cx + cw - 16, cy + chh - 12],
                       outline=(120, 200, 150), width=1)
        for i in range(5):
            px = cx + 8 + i * 15
            draw.line([(px, cy - 8), (px, cy)], fill=(120, 200, 150), width=2)
            draw.line([(px, cy + chh), (px, cy + chh + 8)],
                      fill=(120, 200, 150), width=2)
        draw.text((cx + 8, cy + chh - 26), "NVDA", font=font(SANS_B, 11),
                  fill=(190, 240, 210))
        # rising arrow chart (Nvidia in green, Nasdaq in amber)
        pts = [(x + 120, y + h - 18), (x + 160, y + h - 44),
               (x + 190, y + h - 34), (x + 230, y + h - 62),
               (x + 268, y + h - 84), (x + w - 14, y + 16)]
        pts2 = [(x + 120, y + h - 10), (x + 160, y + h - 26),
                (x + 195, y + h - 22), (x + 235, y + h - 40),
                (x + 270, y + h - 56), (x + w - 14, y + 34)]
        for gy in (y + 30, y + 58, y + 86):
            draw.line([(x + 112, gy), (x + w - 10, gy)],
                      fill=(40, 90, 60), width=1)
        draw.line(pts2, fill=(230, 180, 60), width=3, joint="curve")
        draw.line(pts, fill=(90, 230, 140), width=4, joint="curve")
        draw.polygon([(x + w - 26, y + 12), (x + w - 6, y + 14),
                      (x + w - 14, y + 30)], fill=(90, 230, 140))
        for gx in range(x + 112, x + w - 8, 26):
            draw.line([(gx, y + h - 12), (gx, y + h - 6)],
                      fill=(90, 230, 140), width=2)
        draw.text((x + 120, y + 12), "+31%", font=font(SERIF_B, 30),
                  fill=(140, 255, 180))
    elif kind == "korea":
        draw.rectangle([x, y, x + w, y + h], fill=(14, 30, 58))
        # radar arcs
        rcx, rcy = x + w - 78, y + h - 34
        for r in (26, 48, 70):
            draw.ellipse([rcx - r, rcy - r, rcx + r, rcy + r],
                         outline=(90, 160, 230), width=2)
        draw.line([(rcx, rcy), (rcx + 62, rcy - 52)], fill=(140, 210, 255),
                  width=3)
        draw.line([(rcx, rcy), (rcx - 8, rcy - 68)], fill=(90, 160, 230),
                  width=2)
        draw.line([(rcx, rcy), (rcx + 70, rcy + 8)], fill=(70, 130, 200),
                  width=2)
        # cloud
        draw.ellipse([x + 130, y + 8, x + 168, y + 22], fill=(70, 100, 150))
        draw.ellipse([x + 146, y + 4, x + 178, y + 20], fill=(70, 100, 150))
        # island
        draw.ellipse([x + 18, y + 40, x + 118, y + 84], fill=(58, 110, 70),
                     outline=(150, 220, 170), width=2)
        draw.ellipse([x + 128, y + 58, x + 152, y + 80], fill=(58, 110, 70),
                     outline=(150, 220, 170), width=1)
        # jets
        for jx, jy in ((x + 150, y + 26), (x + 190, y + 40)):
            draw.polygon([(jx, jy), (jx + 18, jy + 6), (jx, jy + 12),
                          (jx + 5, jy + 6)], fill=(220, 220, 220))
        # alert triangle
        tx, ty = x + 24, y + 10
        draw.polygon([(tx, ty + 22), (tx + 12, ty), (tx + 24, ty + 22)],
                     fill=(255, 200, 40), outline=(180, 40, 40), width=2)
        draw.text((tx + 9, ty + 6), "!", font=font(SANS_B, 12),
                  fill=(140, 20, 20))
        draw.text((x + 56, y + 12), "07:52 KST", font=font(SANS_B, 13),
                  fill=(255, 220, 120))
        draw.text((x + 18, y + h - 20), "ULLEUNG ISLAND",
                  font=font(SANS_B, 11), fill=(170, 210, 250))
    else:  # cyber
        draw.rectangle([x, y, x + w, y + h], fill=(32, 22, 52))
        # network nodes (denser mesh)
        nodes = [(x + 40, y + 30), (x + 90, y + 18), (x + 150, y + 34),
                 (x + 200, y + 20), (x + 250, y + 38), (x + 60, y + 78),
                 (x + 130, y + 88), (x + 210, y + 82), (x + 270, y + 74),
                 (x + 18, y + 56), (x + 290, y + 52), (x + 105, y + 58)]
        for a in range(len(nodes)):
            for b in range(a + 1, len(nodes)):
                if abs(nodes[a][0] - nodes[b][0]) < 90 and \
                        abs(nodes[a][1] - nodes[b][1]) < 60:
                    draw.line([nodes[a], nodes[b]], fill=(120, 110, 200),
                              width=1)
        for nx, ny in nodes:
            draw.ellipse([nx - 5, ny - 5, nx + 5, ny + 5],
                         fill=(170, 220, 255), outline=(220, 240, 255))
        # shield
        sx, sy = x + w // 2 - 34, y + 14
        shield = [(sx, sy), (sx + 68, sy), (sx + 68, sy + 34),
                  (sx + 34, sy + 66), (sx, sy + 34)]
        draw.polygon(shield, fill=(52, 130, 90),
                     outline=(140, 230, 180), width=2)
        draw.text((sx + 24, sy + 20), "$", font=font(SERIF_B, 26),
                  fill=(240, 255, 240))
        draw.text((x + 16, y + h - 22), "$43.9BN  ALL-STOCK",
                  font=font(SANS_B, 12), fill=(220, 210, 255))


def draw_map(draw, x, y, w, h):
    """Stylised world outline with pins (rough equirectangular)."""
    draw.rectangle([x, y, x + w, y + h], fill=(214, 228, 238),
                   outline=(150, 160, 170), width=1)

    def px(lon, lat):
        return (x + (lon + 170.0) / 360.0 * w,
                y + (75.0 - lat) / 130.0 * h)

    def poly(coords, fill):
        pts = [px(lon, lat) for lon, lat in coords]
        draw.polygon(pts, fill=fill, outline=(120, 110, 88))

    land = (216, 205, 180)
    poly([(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73),
          (-60, 60), (-55, 47), (-70, 42), (-75, 35), (-80, 26),
          (-90, 21), (-97, 16), (-105, 20), (-115, 28), (-125, 40),
          (-125, 49), (-150, 60), (-168, 66)], land)
    poly([(-80, 10), (-60, 8), (-50, 0), (-40, -5), (-35, -10),
          (-40, -20), (-48, -28), (-58, -35), (-65, -45), (-70, -52),
          (-73, -40), (-75, -20), (-80, -5), (-80, 10)], land)
    poly([(-10, 36), (-5, 44), (0, 50), (5, 55), (10, 58), (18, 56),
          (25, 60), (30, 70), (40, 68), (45, 60), (40, 50), (30, 45),
          (25, 40), (20, 40), (12, 44), (5, 43), (-2, 37), (-10, 36)], land)
    poly([(-10, 35), (0, 35), (10, 37), (20, 32), (32, 31), (35, 28),
          (40, 15), (48, 11), (51, 10), (45, 0), (40, -10), (35, -20),
          (30, -30), (20, -35), (15, -30), (12, -18), (10, -5), (8, 4),
          (-5, 5), (-15, 12), (-17, 20), (-15, 28), (-10, 35)], land)
    poly([(40, 70), (60, 70), (80, 73), (100, 76), (120, 73), (140, 72),
          (160, 70), (178, 66), (170, 60), (160, 55), (150, 50),
          (140, 45), (135, 40), (128, 35), (122, 30), (118, 25),
          (110, 20), (105, 10), (100, 8), (95, 15), (90, 22), (85, 20),
          (80, 15), (75, 8), (72, 20), (65, 25), (60, 25), (55, 26),
          (50, 30), (45, 30), (40, 35), (40, 45), (40, 55), (40, 70)],
         land)
    poly([(113, -22), (122, -14), (132, -12), (142, -11), (150, -22),
          (153, -27), (150, -37), (140, -38), (130, -32), (122, -34),
          (114, -30), (113, -22)], land)
    poly([(130, 31), (133, 34), (137, 35), (140, 38), (142, 42),
          (145, 44), (141, 45), (139, 40), (136, 36), (132, 33),
          (130, 31)], land)

    pins = [("SEOUL", 127, 37.5, 1, 0), ("TOKYO", 139.7, 35.7, 1, 0),
            ("DELHI", 77.2, 28.6, 1, 0), ("JAKARTA", 106.8, -6.2, 1, 0),
            ("BEIJING", 116.4, 39.9, -1, -1), ("GENEVA", 6.1, 46.2, -1, 0),
            ("WARSAW", 21, 52.2, 1, -1), ("GAZA", 34.5, 31.5, 1, 1),
            ("MEXICO CITY", -99.1, 19.4, 1, 0),
            ("NEW YORK", -74, 40.7, 1, 0),
            ("CANBERRA", 149.1, -35.3, -1, 0),
            ("MURMANSK", 33, 69, 1, -1)]
    fnt = font(SANS_B, 7)
    for label, lon, lat, dx, dy in pins:
        cx, cy = px(lon, lat)
        draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED,
                     outline=(255, 255, 255), width=1)
        lx = cx + 5 if dx > 0 else cx - 5 - draw.textlength(label, font=fnt)
        ly = cy - 4 if dy == 0 else (cy - 11 if dy < 0 else cy + 5)
        draw.text((lx, ly), label, font=fnt, fill=(90, 20, 20))


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "entry.png")
    data = load_stories()
    stories = data["stories"]
    leads = [s for s in stories if s["kind"] == "lead"]
    mediums = [s for s in stories if s["kind"] == "medium"]
    listed = [s for s in stories if s["kind"] == "list"]
    numbers = data["numbers_strip"]
    regions = data["regions"]

    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_hatch(draw)
    draw.rectangle([4, 4, W - 5, H - 5], outline=(60, 55, 45), width=2)

    # ---- Masthead ----
    draw.rectangle([MARGIN, 8, RIGHT, 10], fill=RED)
    draw.text((MARGIN, 14), "THE WORLD IN ONE PAGE",
              font=font(SERIF_B, 34), fill=INK)
    draw.text((RIGHT, 16), "TUESDAY 24 NOVEMBER 2026",
              font=font(SERIF_B, 18), fill=INK, anchor="ra")
    draw.text((RIGHT, 42), "36 STORIES  ·  EVERY ONE SOURCED",
              font=font(SANS_B, 11), fill=GREY, anchor="ra")
    draw.text((MARGIN, 62), "The day's world news, drawn in one page — Tuesday in Asia, Monday overnight in the West.",
              font=font(SANS, 10), fill=GREY)
    draw.line([(MARGIN, 76), (RIGHT, 76)], fill=INK, width=2)

    # ---- Red ticker ----
    draw.rectangle([MARGIN, 80, RIGHT, 102], fill=RED)
    ticker = ("HUANG RETURNS  ·  NVIDIA +31%  ·  KOREA SIRENS  ·  "
              "$43.9BN CYBER DEAL  ·  NATO AWACS TO POLAND  ·  GAZA STRIKES")
    draw.text((MARGIN + 8, 86), fit(draw, ticker, font(SANS_B, 12), RIGHT - MARGIN - 16),
              font=font(SANS_B, 12), fill=(255, 255, 255))

    # ---- Numbers strip (sourced numerals) ----
    y0, y1 = 106, 168
    cell_w = (RIGHT - MARGIN) / 6.0
    for i, num in enumerate(numbers):
        cx = MARGIN + cell_w * i
        if i:
            draw.line([(cx, y0 + 4), (cx, y1 - 4)], fill=(200, 192, 172), width=1)
        val = num["value"]
        draw.text((cx + cell_w / 2, y0 + 2), val, font=font(SERIF_B, 26),
                  fill=RED, anchor="ma")
        lab_lines = wrap(draw, num["label"], font(SANS_B, 7), cell_w - 12)
        ly = y0 + 34
        for ln in lab_lines[:2]:
            draw.text((cx + cell_w / 2, ly), ln, font=font(SANS_B, 7),
                      fill=INK, anchor="ma")
            ly += 10
        draw.text((cx + cell_w / 2, y1 - 12), "— " + num["source"],
                  font=font(SANS, 7), fill=GREY, anchor="ma")
    draw.line([(MARGIN, y1), (RIGHT, y1)], fill=(200, 192, 172), width=1)

    # ---- Region bar ----
    ry0, ry1 = 172, 190
    order = [("N AMERICA", (178, 34, 34)), ("EUROPE", (28, 68, 120)),
             ("ASIA", (28, 110, 60)), ("MIDDLE EAST", (176, 132, 30)),
             ("GLOBAL", (110, 90, 150)), ("OCEANIA", (40, 140, 150)),
             ("AFRICA", (200, 110, 60))]
    total = sum(regions.values())
    bx = MARGIN
    bar_w = RIGHT - MARGIN
    for name, col in order:
        key = name.replace(" ", "_").upper() if name != "N AMERICA" else "N America"
        # regions keys: "N America", "Europe", "Asia", "Middle East",
        # "Global", "Oceania", "Africa"
        key = {"N AMERICA": "N America", "EUROPE": "Europe",
               "ASIA": "Asia", "MIDDLE EAST": "Middle East",
               "GLOBAL": "Global", "OCEANIA": "Oceania",
               "AFRICA": "Africa"}[name]
        n = regions[key]
        seg = bar_w * n / total
        draw.rectangle([bx, ry0, bx + seg, ry1], fill=col)
        if seg >= 60:
            draw.text((bx + seg / 2, ry0 + 4), f"{name} {n}",
                      font=font(SANS_B, 9), fill=(255, 255, 255), anchor="ma")
        bx += seg
    legend = "  ".join(f"{name} {regions[{'N AMERICA': 'N America', 'EUROPE': 'Europe', 'ASIA': 'Asia', 'MIDDLE EAST': 'Middle East', 'GLOBAL': 'Global', 'OCEANIA': 'Oceania', 'AFRICA': 'Africa'}[name]]}"
                      for name, _ in order)
    draw.text((MARGIN, 192), "REGIONS: " + legend, font=font(SANS, 8), fill=GREY)

    # ---- Three lead panels ----
    lead_kinds = ["nvidia", "korea", "cyber"]
    col_w = 312
    col_x = [MARGIN, MARGIN + col_w + 16, MARGIN + 2 * (col_w + 16)]
    ly0 = 206
    art_h = 106
    for i, story in enumerate(leads):
        x = col_x[i]
        draw_lead_art(draw, lead_kinds[i], x, ly0, col_w, art_h)
        hy = ly0 + art_h + 8
        head_lines = wrap(draw, story["headline"], font(SERIF_B, 18), col_w)
        for ln in head_lines[:2]:
            draw.text((x, hy), ln, font=font(SERIF_B, 18), fill=INK)
            hy += 22
        deck_lines = wrap(draw, story["deck"], font(SANS, 10), col_w)
        dy = hy + 2
        for ln in deck_lines[:3]:
            draw.text((x, dy), ln, font=font(SANS, 10), fill=(60, 56, 48))
            dy += 13
        draw.text((x, ly0 + 208), f"{story['source']}  ·  {story['tag']}",
                  font=font(SANS_B, 9), fill=RED)
    draw.line([(MARGIN, 424), (RIGHT, 424)], fill=INK, width=1)

    # ---- Mediums: the day in ten ----
    my = 432
    draw.text((MARGIN, my), "THE DAY IN TEN", font=font(SANS_B, 12), fill=INK)
    draw.text((RIGHT, my), "all dated · all sourced", font=font(SANS, 10),
              fill=GREY, anchor="ra")
    row_h = 40
    med_y = my + 20
    med_cols = [MARGIN, MARGIN + 484]
    med_w = 472
    glyphs = ["NATO", "GAZA", "IRAN", "MODI", "TALKS", "NEPAL", "FIRE",
              "COURT", "UCL", "CHESS"]
    glyph_cols = [(28, 68, 120), (178, 34, 34), (120, 60, 20),
                  (28, 110, 60), (40, 140, 150), (176, 132, 30),
                  (200, 60, 30), (90, 60, 140), (20, 90, 40),
                  (140, 90, 20)]
    for i, story in enumerate(mediums):
        col = i % 2
        row = i // 2
        x = med_cols[col]
        y = med_y + row * row_h
        draw.rectangle([x, y + 2, x + 30, y + 32], fill=glyph_cols[i])
        draw.text((x + 15, y + 10), glyphs[i][:2], font=font(SANS_B, 10),
                  fill=(255, 255, 255), anchor="ma")
        tx = x + 38
        head = fit(draw, story["headline"], font(SANS_B, 11), med_w - 38 - 66)
        draw.text((tx, y + 1), head, font=font(SANS_B, 11), fill=INK)
        draw.text((x + med_w, y + 2), story["tag"], font=font(SANS_B, 8),
                  fill=RED, anchor="ra")
        deck = fit(draw, story["deck"], font(SANS, 9), med_w - 38 - 96)
        draw.text((tx, y + 17), deck, font=font(SANS, 9), fill=(60, 56, 48))
        draw.text((x + med_w, y + 17), story["source"], font=font(SANS, 8),
                  fill=GREY, anchor="ra")
        if row < 4:
            draw.line([(x, y + row_h - 2), (x + med_w, y + row_h - 2)],
                      fill=(220, 214, 198), width=1)

    # ---- Map ----
    map_y = med_y + 5 * row_h + 8
    draw.text((MARGIN, map_y), "WHERE IT HAPPENED",
              font=font(SANS_B, 12), fill=INK)
    draw.text((RIGHT, map_y), "12 pins — every lead and medium on the map",
              font=font(SANS, 10), fill=GREY, anchor="ra")
    draw_map(draw, MARGIN, map_y + 18, RIGHT - MARGIN, 96)

    # ---- Also list: 23 more stories ----
    list_y = map_y + 18 + 96 + 10
    draw.text((MARGIN, list_y), "ALSO — 23 MORE STORIES",
              font=font(SANS_B, 12), fill=INK)
    draw.text((RIGHT, list_y), "first reported today unless tagged",
              font=font(SANS, 10), fill=GREY, anchor="ra")
    ly = list_y + 18
    list_cols = [MARGIN, MARGIN + 484]
    for i, story in enumerate(listed):
        col = 0 if i < 12 else 1
        row = i if i < 12 else i - 12
        x = list_cols[col]
        y = ly + row * 11
        line = f"{story['headline']} — {story['source']} [{story['tag']}]"
        draw.text((x, y), fit(draw, line, font(SANS, 8), 472),
                  font=font(SANS, 8), fill=(40, 38, 34))

    # ---- Honesty boxes ----
    box_y = ly + 12 * 11 + 6
    box_h = 56
    bw = (RIGHT - MARGIN - 12) // 2
    draw.rectangle([MARGIN, box_y, MARGIN + bw, box_y + box_h],
                   outline=RED, width=2)
    draw.text((MARGIN + 8, box_y + 4), "DATE CHECK — NOT TODAY",
              font=font(SANS_B, 9), fill=RED)
    dc = ("COP31 collapse (Sun 22 Nov) · Alcaraz ATP Finals title (Sun 22) · "
          "Liverpool 4–0 Man Utd (Sun 22) · Merkury sinking (22–23 Nov) · "
          "Nikkei −5.06% (Fri 20 Nov)")
    dlines = wrap(draw, dc, font(SANS, 8), bw - 16)
    dy = box_y + 18
    for ln in dlines[:3]:
        draw.text((MARGIN + 8, dy), ln, font=font(SANS, 8), fill=INK)
        dy += 11
    x2 = MARGIN + bw + 12
    draw.rectangle([x2, box_y, x2 + bw, box_y + box_h],
                   outline=GREEN, width=2)
    draw.text((x2 + 8, box_y + 4), "CLAIMS CHECKED",
              font=font(SANS_B, 9), fill=GREEN)
    cc = ("Dell, Workday, Japan PMIs, Germany Ifo, US 5-yr auction: PREVIEWS, "
          "not results. Arsenal–Dortmund: TONIGHT, 20:00 GMT. Monday events "
          "tagged MONDAY. Every story sourced; nothing invented.")
    clines = wrap(draw, cc, font(SANS, 8), bw - 16)
    dy = box_y + 18
    for ln in clines[:3]:
        draw.text((x2 + 8, dy), ln, font=font(SANS, 8), fill=INK)
        dy += 11

    # ---- Footer ----
    fy = box_y + box_h + 6
    draw.text((MARGIN, fy),
              "Sources: Reuters · CNN · AP · Times of India · Asia Daily · Sportradar · IIASA · Cambridge · Sports Mole · Law360 · Finwire — full list in stories.json.",
              font=font(SANS, 8), fill=GREY)
    draw.text((MARGIN, fy + 11),
              "Drawn by hand in code — no photographs, no copied art. Tuesday 24 November 2026. @nimble-beacon-24.",
              font=font(SANS, 8), fill=GREY)

    img.save(out_path, format="PNG", optimize=False)
    print(f"wrote {out_path} {os.path.getsize(out_path)} bytes")


if __name__ == "__main__":
    main()
