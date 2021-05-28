#!/usr/bin/python

import math
import sys

N = 32
R = 150

def getPoints(n, r, y):
    result = []
    for i in range(0, n):
        phi = i * math.pi * 2 / n
        x = math.cos(phi) * r
        y = y
        z = math.sin(phi) * r
        result.append((x, y, z))
    return result

def getUV(points, r):
    result = []
    for point in points:
        (x, y, z) = point
        u = (x + r) / (2  * r)
        v = (z + r) / (2  * r)
        result.append((u, v))
    return result

def zigZag(n):
    result = []
    nextPos = 1
    nextNeg = n
    pos = True
    for _ in range(0, n - 2):
        if pos:
            result.append((nextPos, nextPos + 1, nextNeg))
            nextPos += 1
        else:
            result.append((nextNeg - 1, nextNeg, nextPos))
            nextNeg -= 1
        pos = not pos
    return result

points = getPoints(N, R, 0)
uv = getUV(points, R)
tris = zigZag(N)

sys.stdout.write('# Circle, with one point at y=-1 for bounds\n')
sys.stdout.write('\n')

for (x, y, z) in points:
    sys.stdout.write('v {:.6f} {:.6f} {:.6f}\n'.format(x, y, z))

sys.stdout.write('v 0 -1 0\n')
sys.stdout.write('v 1 -1 0\n')
sys.stdout.write('v 0 -1 1\n')

sys.stdout.write('# {:d} vertices\n'.format(N + 3))
sys.stdout.write('\n')

sys.stdout.write('vn 0.0 1.0 0.0\n')
sys.stdout.write('# 1 vertex normal\n')
sys.stdout.write('\n')

for (u, v) in uv:
    sys.stdout.write('vt {:.6f} {:.6f}\n'.format(u, v))
sys.stdout.write('# {:d} texture coords\n'.format(N))
sys.stdout.write('\n')

for (a, b, c) in tris:
    sys.stdout.write('f {:d}/{:d}/1 {:d}/{:d}/1 {:d}/{:d}/1\n'.format(c, c, b, b, a, a))
sys.stdout.write('f {:d} {:d} {:d}\n'.format(N + 1, N + 3, N + 2))
sys.stdout.write('# {:d} faces\n'.format(len(tris) + 1))
sys.stdout.write('\n')

sys.stdout.flush()
