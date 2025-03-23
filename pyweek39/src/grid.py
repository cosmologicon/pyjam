import random, pygame
from . import view, pview, ptext

# +x = East, +y = North

ds = N, S, E, W = (0, 1), (0, -1), (1, 0), (-1, 0)
STILL = (0, 0)

def rot(ps):
    return [(-y, x) for x, y in ps]
arrowds = { N: [(0, 0.4), (-0.2, -0.3), (0.2, -0.3)] }
arrowds[W] = rot(arrowds[N])
arrowds[S] = rot(arrowds[W])
arrowds[E] = rot(arrowds[S])
arrowds[STILL] = []
wnames = { N: "N", S: "S", E: "E", W: "W" }

R = 10

wind = {}

for x in range(-R, R + 1):
    for y in range(-R, R + 1):
        if (x, y) == (0, 0):
            wind[(x, y)] = STILL
        else:
            wind[(x, y)] = random.choice(ds)

def draw():
    for x in range(-R, R + 1):
        for y in range(-R, R + 1):
            dxys = arrowds[wind[(x, y)]]
            if not dxys:
                continue
            ps = [view.worldtoscreen((x + dx, y + dy)) for dx, dy in dxys]
            pygame.draw.polygon(pview.screen, (255, 255, 255), ps)
            ptext.draw(wnames[wind[(x, y)]], center = view.worldtoscreen((x, y)),
                color = "black", fontsize = view.sizetoscreen(0.2))




