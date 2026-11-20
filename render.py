#!/usr/bin/env python3
"""The World in One Day - Friday 20 November 2026.

A pure standard-library renderer: it draws a one-page broadsheet
that sums up the world news of 20 November 2026 and writes it as a
deterministic 1024x1024 PNG. No third-party modules, no network,
no clock, no randomness - the same bytes come out on every run.

The picture is drawn on an RGB pixel canvas with a small 5x7 bitmap
font defined below, then encoded as a PNG with zlib (stdlib).
"""
import struct
import zlib

W = 1024
H = 1024

PAPER = (247, 241, 227)
INK = (17, 17, 17)
RED = (193, 39, 45)
BLUE = (29, 78, 137)
TEAL = (14, 122, 109)
AMBER = (217, 142, 0)
GREY = (92, 92, 92)
LIGHT = (232, 222, 198)
WHITE = (255, 255, 255)
SKY = (184, 205, 226)
SMOKE = (120, 118, 112)

canvas = bytearray(W * H * 3)


def set_px(x, y, colour):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        canvas[i] = colour[0]
        canvas[i + 1] = colour[1]
        canvas[i + 2] = colour[2]


def fill_rect(x, y, w, h, colour):
    for yy in range(y, y + h):
        if 0 <= yy < H:
            base = (yy * W) * 3
            for xx in range(x, x + w):
                if 0 <= xx < W:
                    i = base + xx * 3
                    canvas[i] = colour[0]
                    canvas[i + 1] = colour[1]
                    canvas[i + 2] = colour[2]


def frame_rect(x, y, w, h, t, colour):
    fill_rect(x, y, w, t, colour)
    fill_rect(x, y + h - t, w, t, colour)
    fill_rect(x, y, t, h, colour)
    fill_rect(x + w - t, y, t, h, colour)


def hline(x, y, w, t, colour):
    fill_rect(x, y, w, t, colour)


def vline(x, y, h, t, colour):
    fill_rect(x, y, t, h, colour)


def circle(cx, cy, r, colour):
    for yy in range(cy - r, cy + r + 1):
        for xx in range(cx - r, cx + r + 1):
            if (xx - cx) * (xx - cx) + (yy - cy) * (yy - cy) <= r * r:
                set_px(xx, yy, colour)


def ring(cx, cy, r, t, colour):
    for yy in range(cy - r, cy + r + 1):
        for xx in range(cx - r, cx + r + 1):
            d2 = (xx - cx) * (xx - cx) + (yy - cy) * (yy - cy)
            if (r - t) * (r - t) <= d2 <= r * r:
                set_px(xx, yy, colour)


def triangle(x1, y1, x2, y2, x3, y3, colour):
    minx = max(0, min(x1, x2, x3))
    maxx = min(W - 1, max(x1, x2, x3))
    miny = max(0, min(y1, y2, y3))
    maxy = min(H - 1, max(y1, y2, y3))

    def edge(ax, ay, bx, by, px, py):
        return (px - ax) * (by - ay) - (py - ay) * (bx - ax)

    for yy in range(miny, maxy + 1):
        for xx in range(minx, maxx + 1):
            d1 = edge(x1, y1, x2, y2, xx, yy)
            d2 = edge(x2, y2, x3, y3, xx, yy)
            d3 = edge(x3, y3, x1, y1, xx, yy)
            if (d1 >= 0 and d2 >= 0 and d3 >= 0) or (d1 <= 0 and d2 <= 0 and d3 <= 0):
                set_px(xx, yy, colour)


def line(x1, y1, x2, y2, t, colour):
    steps = max(abs(x2 - x1), abs(y2 - y1), 1)
    for s in range(steps + 1):
        xx = x1 + (x2 - x1) * s // steps
        yy = y1 + (y2 - y1) * s // steps
        fill_rect(xx - t // 2, yy - t // 2, t, t, colour)


# ---------------------------------------------------------------- font
# A 5x7 bitmap font. Each glyph is 7 rows of 5 pixels, '#' = ink.
FONT = {
    "A": (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "B": ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    "C": (".####", "#....", "#....", "#....", "#....", "#....", ".####"),
    "D": ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    "E": ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    "F": ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    "G": (".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."),
    "H": ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "I": (".###.", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "J": ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    "K": ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    "L": ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    "M": ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    "N": ("#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"),
    "O": (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "P": ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    "Q": (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    "R": ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    "S": (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    "T": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "U": ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "V": ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "W": ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    "X": ("#...#", ".#.#.", "..#..", "..#..", "..#..", ".#.#.", "#...#"),
    "Y": ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    "Z": ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    "0": (".###.", "#..##", "#.#.#", "##..#", "#...#", "#...#", ".###."),
    "1": ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "2": (".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"),
    "3": ("####.", "....#", "....#", ".###.", "....#", "....#", "####."),
    "4": ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    "5": ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    "6": (".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."),
    "7": ("#####", "....#", "...#.", "..#..", "..#..", "..#..", "..#.."),
    "8": (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    "9": (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
    " ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    ".": (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    ",": (".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."),
    ":": (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    ";": (".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."),
    "'": ("..#..", "..#..", "..#..", ".....", ".....", ".....", "....."),
    "-": (".....", ".....", ".....", "#####", ".....", ".....", "....."),
    "!": ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    "?": (".###.", "#...#", "....#", "..##.", "..#..", ".....", "..#.."),
    "$": ("..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."),
    "%": ("##..#", "##.#.", "....#", "...#.", "..#..", ".#...", "#..##"),
    "&": (".##..", "#..#.", "#.#..", ".#...", "#.#.#", "#..#.", ".##.#"),
    "/": ("....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."),
    "(": ("...##", "..#..", ".#...", ".#...", ".#...", "..#..", "...##"),
    ")": ("##...", "..#..", "...#.", "...#.", "...#.", "..#..", "##..."),
    "+": (".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."),
    "=": (".....", ".....", "#####", ".....", "#####", ".....", "....."),
    "*": (".....", "#.#.#", ".###.", "#####", ".###.", "#.#.#", "....."),
    '"': (".#.#.", ".#.#.", ".#.#.", ".....", ".....", ".....", "....."),
}


def char_w(scale):
    return 6 * scale


def text_w(text, scale):
    return len(text) * char_w(scale) - scale


def draw_text(x, y, text, scale, colour):
    cx = x
    for ch in text.upper():
        glyph = FONT.get(ch, FONT[" "])
        for row_i, row in enumerate(glyph):
            for col_i, bit in enumerate(row):
                if bit == "#":
                    fill_rect(cx + col_i * scale, y + row_i * scale, scale, scale, colour)
        cx += char_w(scale)
    return cx - scale


def draw_text_center(y, text, scale, colour, cx=512):
    w = text_w(text, scale)
    return draw_text(cx - w // 2, y, text, scale, colour)


def wrap(text, scale, max_w):
    words = text.upper().split()
    lines = []
    cur = ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_w(trial, scale) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_block(x, y, text, scale, colour, max_w, leading=None):
    if leading is None:
        leading = 9 * scale
    for ln in wrap(text, scale, max_w):
        draw_text(x, y, ln, scale, colour)
        y += leading
    return y



# ---------------------------------------------------------------- icons
def icon_summit(x, y):
    # three flags over a summit table
    fill_rect(x, y + 6, 62, 44, BLUE)
    fill_rect(x + 70, y + 6, 62, 44, RED)
    fill_rect(x + 140, y + 6, 62, 44, AMBER)
    for i in range(5):
        set_px(x + 10 + i * 3, y + 14, WHITE)
        fill_rect(x + 8 + i * 10, y + 14, 4, 4, WHITE)
    circle(x + 101, y + 28, 13, WHITE)
    circle(x + 101, y + 28, 8, RED)
    fill_rect(x + 146, y + 16, 50, 6, WHITE)
    fill_rect(x + 146, y + 30, 50, 6, WHITE)
    fill_rect(x, y + 58, 202, 10, INK)
    fill_rect(x + 18, y + 68, 166, 8, INK)
    circle(x + 32, y + 92, 12, INK)
    circle(x + 101, y + 92, 12, INK)
    circle(x + 170, y + 92, 12, INK)


def icon_scales(x, y):
    vline(x + 48, y, 78, 6, INK)
    hline(x + 6, y + 6, 90, 6, INK)
    circle(x + 51, y + 4, 7, INK)
    line(x + 14, y + 12, x + 2, y + 44, 3, INK)
    line(x + 14, y + 12, x + 26, y + 44, 3, INK)
    triangle(x + 2, y + 44, x + 26, y + 44, x + 14, y + 56, BLUE)
    line(x + 88, y + 12, x + 76, y + 44, 3, INK)
    line(x + 88, y + 12, x + 100, y + 44, 3, INK)
    triangle(x + 76, y + 44, x + 100, y + 44, x + 88, y + 56, BLUE)
    fill_rect(x + 22, y + 78, 58, 8, INK)


def icon_missile(x, y):
    line(x + 8, y + 62, x + 58, y + 12, 7, RED)
    triangle(x + 58, y + 12, x + 44, y + 14, x + 56, y + 26, INK)
    circle(x + 84, y + 22, 15, AMBER)
    circle(x + 84, y + 22, 8, RED)
    circle(x + 96, y + 48, 10, SMOKE)
    circle(x + 70, y + 52, 8, SMOKE)
    fill_rect(x, y + 74, 104, 8, INK)
    fill_rect(x + 10, y + 58, 16, 16, INK)
    fill_rect(x + 62, y + 58, 20, 16, INK)


def icon_chart(x, y):
    vline(x + 6, y + 4, 74, 5, INK)
    hline(x + 6, y + 74, 96, 5, INK)
    line(x + 14, y + 62, x + 40, y + 44, 5, TEAL)
    line(x + 40, y + 44, x + 62, y + 50, 5, TEAL)
    line(x + 62, y + 50, x + 94, y + 18, 5, TEAL)
    triangle(x + 94, y + 18, x + 80, y + 20, x + 92, y + 32, TEAL)
    fill_rect(x + 20, y + 84, 14, 10, BLUE)
    fill_rect(x + 44, y + 84, 14, 10, RED)


def icon_leaf(x, y):
    circle(x + 50, y + 42, 34, TEAL)
    triangle(x + 50, y + 6, x + 84, y + 42, x + 50, y + 78, TEAL)
    line(x + 50, y + 78, x + 50, y + 92, 5, INK)
    line(x + 50, y + 66, x + 68, y + 34, 3, WHITE)
    line(x + 50, y + 66, x + 36, y + 40, 3, WHITE)


# ---------------------------------------------------------------- page
def build_page():
    fill_rect(0, 0, W, H, PAPER)
    frame_rect(14, 14, W - 28, H - 28, 4, INK)

    # masthead
    draw_text_center(30, "THE WORLD IN ONE DAY", 3, INK)
    hline(34, 62, W - 68, 3, INK)
    draw_text_center(74, "20 NOVEMBER 2026", 9, INK)
    draw_text_center(146, "FRIDAY * THE DAY'S NEWS IN ONE PICTURE", 3, RED)
    hline(34, 176, W - 68, 5, INK)

    # ---- lead story: Shenzhen summit (left panel)
    lx, ly, lw = 34, 192, 600
    fill_rect(lx, ly, lw, 252, WHITE)
    frame_rect(lx, ly, lw, 252, 3, INK)
    fill_rect(lx, ly, lw, 30, RED)
    draw_text(lx + 14, ly + 7, "LEAD * SHENZHEN, CHINA", 2, WHITE)
    icon_summit(lx + 22, ly + 48)
    draw_block(lx + 240, ly + 46,
               "TRUMP, XI AND PUTIN HOLD FIRST TRILATERAL SUMMIT",
               3, INK, 330)
    draw_block(lx + 240, ly + 136,
               "PEACE DECLARATION: UN REFORM, ENERGY, NUCLEAR RISK. "
               "UKRAINE A PRIORITY.",
               2, GREY, 330)
    draw_block(lx + 22, ly + 196,
               "FIRST THREE-WAY MEETING OF THE THREE POWERS, "
               "AT APEC IN SHENZHEN.",
               2, INK, 556)

    # ---- second lead: ICJ (right panel)
    rx, ry, rw = 650, 192, 340
    fill_rect(rx, ry, rw, 252, LIGHT)
    frame_rect(rx, ry, rw, 252, 3, INK)
    fill_rect(rx, ry, rw, 30, BLUE)
    draw_text(rx + 14, ry + 7, "THE HAGUE * WORLD COURT", 2, WHITE)
    icon_scales(rx + 22, ry + 44)
    draw_block(rx + 136, ry + 44,
               "MYANMAR COMMITTED GENOCIDE", 3, INK, 180)
    draw_block(rx + 22, ry + 146,
               "ICJ, 9-6: GENOCIDE AGAINST THE ROHINGYA. "
               "REPARATIONS AND SAFE RETURN ORDERED.",
               2, INK, 296)

    # ---- row of three
    ty = 460
    th = 216
    tw = 304
    panels = [
        ("KYIV * OVERNIGHT", RED, icon_missile,
         "RUSSIA STRIKES KYIV",
         "BALLISTIC MISSILES, FIRES IN CITY. UK GIVES "
         "1,000 DRONES."),
        ("MARKETS * AI", TEAL, icon_chart,
         "ANTHROPIC IPO RECORD",
         "$81BN RAISED AT $83. VALUE $1.5 TRILLION, "
         "UP 17 PCT."),
        ("CLIMATE * COP31", AMBER, icon_leaf,
         "COP31 DROPS FOSSIL FUELS",
         "ANTALYA DRAFT REMOVES OIL, GAS, COAL, "
         "$120BN GOAL. OUTCRY."),
    ]
    for i, (kick, col, icon, head, body) in enumerate(panels):
        px = 34 + i * (tw + 14)
        fill_rect(px, ty, tw, th, WHITE)
        frame_rect(px, ty, tw, th, 3, INK)
        fill_rect(px, ty, tw, 28, col)
        draw_text(px + 12, ty + 6, kick, 2, WHITE)
        icon(px + 16, ty + 38)
        draw_block(px + 130, ty + 40, head, 3, INK, 160)
        draw_block(px + 16, ty + 144, body, 2, INK, 280)

    # ---- grid of six briefs (3 columns x 2 rows, fits the page)
    gy = 690
    gh = 108
    gw = 310
    briefs = [
        ("MIDDLE EAST", "HOUTHIS CLAIM STRIKES ON 4 SAUDI TARGETS; "
         "RIYADH LANDMARK HIT"),
        ("ASIA-PACIFIC", "PRABOWO MEETS XI: SEA TALKS; APEC DEALS "
         "PUT AT $86.8BN"),
        ("TAIWAN", "STOCKS PLUNGE 2,200 PTS; 2,700 CHINA-LINKED "
         "ACCOUNTS FLAGGED"),
        ("EUROPE", "SPAIN STRIKE HITS PORTS; PRAGUE MARCHES FOR "
         "FREE MEDIA"),
        ("DISASTER", "GEORGIA GAS BLAST KILLS 6; 5.6 QUAKE NEAR "
         "NEW CALEDONIA"),
        ("WORLD", "TOKYO: 13,000 PROTEST; ESTONIA MAY CLOSE "
         "RUSSIA BORDER"),
    ]
    for i, (kick, body) in enumerate(briefs):
        px = 34 + (i % 3) * (gw + 13)
        py = gy + (i // 3) * (gh + 10)
        fill_rect(px, py, gw, gh, WHITE)
        frame_rect(px, py, gw, gh, 2, INK)
        draw_text(px + 12, py + 10, kick, 2, RED)
        draw_block(px + 12, py + 34, body, 2, INK, 286)

    # ---- footer
    fy = 690 + 2 * (gh + 10) + 4
    hline(34, fy, W - 68, 3, INK)
    draw_block(34, fy + 10,
               "ALSO FRIDAY: DOLLAR NEAR 19-MONTH HIGH * SAMSUNG NAMES "
               "NEW MOBILE CHIEF * TRUMP PARDONS PETE ROSE * INDONESIA "
               "ASKS GOOGLE OVER 19,000 CHANNELS REMOVED",
               2, GREY, 956)
    draw_text_center(982, "SOURCES: REUTERS * AP * UN NEWS * LE MONDE * WIRES, 20 NOV 2026",
                     2, INK)


def write_png(path):
    raw = bytearray()
    row_bytes = W * 3
    for yy in range(H):
        raw.append(0)
        start = yy * row_bytes
        raw.extend(canvas[start:start + row_bytes])

    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        out += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        return out

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as fh:
        fh.write(png)
    return len(png)


if __name__ == "__main__":
    build_page()
    size = write_png("entry.png")
    print("entry.png", size, "bytes")
