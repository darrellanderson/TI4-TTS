#!/usr/bin/python

import sys

# Faction Selector is 16 x 10 x 0.2
# Setup Tile is 12 x 20 x 0.2

MAT_W = 4
MAT_H = 4
MAT_D = 1.5

MAT_W = 7.52
MAT_H = 9.22
MAT_D = 0.01

# SCPT draft mat
MAT_W = 36.82
MAT_H = 26.10
MAT_D = 0.4

# SCPT selection mat
MAT_W = 9.58
MAT_H = 6.90
MAT_D = 0.4

# DRAFT 2021 mat (7x6)
MAT_W = 32.28
MAT_H = 19.7

# DRAFT 2021 selection mat (3x3)
MAT_W = 14.12
MAT_H = 10.1


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

sys.stdout.write('# Mat {:0.2f}x{:0.2f}x{:0.2f}\n'.format(MAT_W, MAT_H, MAT_D))
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

# Vertex textures.
# sys.stdout.write('vt 0 0\n')
# sys.stdout.write('vt 1 0\n')
# sys.stdout.write('vt 1 1\n')
# sys.stdout.write('vt 0 1\n')
sys.stdout.write('vt 0 1\n')
sys.stdout.write('vt 0 0\n')
sys.stdout.write('vt 1 0\n')
sys.stdout.write('vt 1 1\n')
sys.stdout.write('# 2 vertex texture UVs\n')
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
sys.stdout.write('# Top\n')
sys.stdout.write('f 5/1/1 6/2/1 7/3/1 8/4/1\n')
sys.stdout.write('\n')
