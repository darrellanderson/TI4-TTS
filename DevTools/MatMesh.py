#!/usr/bin/python

import math
import sys

# Agenda/Laws:
# CARD_W = 2 * 2
# CARD_H = 3 * 2
# ROWS = 2
# COLS = 5

# Agenda phase mat:
# CARD_W = 2
# CARD_H = 3
# ROWS = 1
# COLS = 1

# Secrets mat:
CARD_W = 2
CARD_H = 3
ROWS = 7
COLS = 8

# Support for the Throne mat:
# CARD_W = 2
# CARD_H = 3
# ROWS = 1
# COLS = 8

# Exploration mat:
# CARD_W = 2
# CARD_H = 3
# ROWS = 2
# COLS = 5

MAT_W = (CARD_W * COLS) + (0.5 * (COLS + 1))
MAT_H = (CARD_H * ROWS) + (0.5 * (ROWS + 1))
MAT_D = 0.4

CORNERS0 = [
    (-MAT_W / 2.0, 0, -MAT_H / 2.0),
    (-MAT_W / 2.0, 0, MAT_H / 2.0),
    (MAT_W / 2.0, 0, MAT_H / 2.0),
    (MAT_W / 2.0, 0, -MAT_H / 2.0),
]
CORNERS1 = [
    (-MAT_W / 2.0, MAT_D, -MAT_H / 2.0),
    (-MAT_W / 2.0, MAT_D, MAT_H / 2.0),
    (MAT_W / 2.0, MAT_D, MAT_H / 2.0),
    (MAT_W / 2.0, MAT_D, -MAT_H / 2.0),
]

sys.stdout.write('# Mat {:0.2f}x{:0.2f}x{:0.2f} / {:d}x{:d} @ {:0.2f}x{:0.2f}\n'.format(MAT_W, MAT_H, MAT_D, COLS, ROWS, CARD_W, CARD_H))
sys.stdout.write('\n')

# Corners.
for (x, y, z) in CORNERS0:
    sys.stdout.write('v {:.6f} {:.6f} {:.6f}\n'.format(x, y, z))
for (x, y, z) in CORNERS1:
    sys.stdout.write('v {:.6f} {:.6f} {:.6f}\n'.format(x, y, z))
sys.stdout.write('# 8 corners\n')
sys.stdout.write('\n')

# Vertex normal "up" and "down".
sys.stdout.write('vn 0.0 1.0 0.0\n')
sys.stdout.write('vn 0.0 -1.0 0.0\n')
sys.stdout.write('# 1 vertex normal\n')
sys.stdout.write('\n')

# Vertex texture for "blank" and for card.
u = 0.01
v = 0.01
sys.stdout.write('vt {:.6f} {:.6f}\n'.format(u, v))

# Agenda:
u0 = 274.0 / 2048.0
u1 = 494.0 / 2048.0
v0 = 1.0 - (48.0 / 1024.0)
v1 = 1.0 - (357.0 / 1024.0)

# Secret:
u0 = 0.29
u1 = 1
v0 = 0
v1 = 1

UVs = [
    (u0, v0),
    (u0, v1),
    (u1, v1),
    (u1, v0)
]
for (u, v) in UVs:
    sys.stdout.write('vt {:.6f} {:.6f}\n'.format(u, v))
sys.stdout.write('\n')

# Bottom.
sys.stdout.write('# Bottom\n')
sys.stdout.write('f 4/1/2 3/1/2 2/1/2 1/1/2\n')
sys.stdout.write('\n')

# Sides.
sys.stdout.write('# Sides\n')
sys.stdout.write('f 1/1/1 2/1/1 6/1/1 5/1/1\n')
sys.stdout.write('f 2/1/1 3/1/1 7/1/1 6/1/1\n')
sys.stdout.write('f 3/1/1 4/1/1 8/1/1 7/1/1\n')
sys.stdout.write('f 4/1/1 1/1/1 5/1/1 8/1/1\n')
sys.stdout.write('\n')

# Top.
v = 9
x0 = -MAT_W / 2.0
z0 = -MAT_H / 2.0
xGap = (MAT_W - (CARD_W * COLS)) / (COLS + 1.0)
zGap = (MAT_H - (CARD_H * ROWS)) / (ROWS + 1.0)

sys.stdout.write('# x={:.6f} z={:.6f}\n'.format(xGap, zGap))

for col in range(COLS + 1):
    x = x0 + (xGap + CARD_W) * col
    y = MAT_D

    # Full Z gap rectangles.
    corners = [
        (x, y, -MAT_H / 2.0),
        (x, y, MAT_H / 2.0),
        (x + xGap, y, MAT_H / 2.0),
        (x + xGap, y, -MAT_H / 2.0),
    ]
    for (x, y, z) in corners:
        sys.stdout.write('v {:.6f} {:.6f} {:.6f}\n'.format(x, y, z))
    sys.stdout.write('f {:d}/1/1 {:d}/1/1 {:d}/1/1 {:d}/1/1\n'.format(v, v+1, v+2, v+3))
    v += 4

    # Column with cards in it.
    if col < COLS:
        for row in range(ROWS + 1):
            x = x0 + (xGap + CARD_W) * col + xGap
            y = MAT_D
            z = z0 + (zGap + CARD_H) * row

            # Gap.
            corners = [
                (x, y, z),
                (x, y, z + zGap),
                (x + CARD_W, y, z + zGap),
                (x + CARD_W, y, z),
            ]
            for (x, y, z) in corners:
                sys.stdout.write('v {:.6f} {:.6f} {:.6f}\n'.format(x, y, z))
            sys.stdout.write('f {:d}/1/1 {:d}/1/1 {:d}/1/1 {:d}/1/1\n'.format(v, v+1, v+2, v+3))
            v += 4

            # Card
            if row < ROWS:
                x = x0 + (xGap + CARD_W) * col + xGap
                z = z0 + (zGap + CARD_H) * row + zGap
                sys.stdout.write('#CARD\n')
                corners = [
                    (x, y, z),
                    (x, y, z + CARD_H),
                    (x + CARD_W, y, z + CARD_H),
                    (x + CARD_W, y, z),
                ]
                for (x, y, z) in corners:
                    sys.stdout.write('v {:.6f} {:.6f} {:.6f}\n'.format(x, y, z))
                sys.stdout.write('f {:d}/2/1 {:d}/3/1 {:d}/4/1 {:d}/5/1\n'.format(v, v+1, v+2, v+3))
                v += 4

sys.stdout.flush()
