import random, pygame, math
from . import view, pview, ptext

# +x = East, +y = North

ds = N, S, E, W = (0, 1), (0, -1), (1, 0), (-1, 0)
d2s = NE, NW, SE, SW = [math.vplus(d0, d1) for d0, d1 in [(N, E), (N, W), (S, E), (S, W)]]
STILL = (0, 0)
ORIGIN = (0, 0)

def rot(ps):
    return [(-y, x) for x, y in ps]
arrowds = { N: [(0, 0.4), (-0.2, -0.3), (0.2, -0.3)] }
arrowds[W] = rot(arrowds[N])
arrowds[S] = rot(arrowds[W])
arrowds[E] = rot(arrowds[S])
arrowds[STILL] = []
wnames = { N: "N", S: "S", E: "E", W: "W" }

R = 25
grid = [(x, y) for x in range(-R, R + 1) for y in range(-R, R + 1)]
gridset = set(grid)

wind = { p: STILL for p in gridset }
strength = { p: 0 for p in gridset }
gettables = {}

R0, R1 = 20, 24
artifacts = [math.vtimes(d, R0) for d in ds] + [math.vtimes(d, R1) for d in d2s]

def setwind(pos, w, s = 1):
    wind[pos] = w
    strength[pos] = 0 if w is STILL else s
setwind(ORIGIN, STILL)

if False:
    steps = { (0, 0): 0 }

    while tofill:
        p0 = random.choice(tofill)
        if not any(math.vplus(p0, d) in tofill for d in ds):
            dchoices = [(d, math.vplus(p0, d)) for d in ds]
            dchoices = [(d, p1) for d, p1 in dchoices if p1 in steps]
            d, p1 = max(dchoices, key = lambda dp1: steps[dp1[1]])
        else:
            d = random.choice(ds)
            p1 = math.vplus(p0, d)
            if p1 not in steps:
                continue
            if len(wind) > 1 + steps[p1] ** 2:
                continue
        if p1 in wind:
            steps[p0] = steps[p1] + 1
            wind[p0] = d
            tofill.remove(p0)

def adjs(p):
    x, y = p
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            yield x + dx, y + dy

cset = set(gridset)
cset.remove(ORIGIN)
for p in artifacts:
    cset -= set(adjs(p))
if True:
    for x in [-1, 1]:
        for y in [-1, 1]:
            gettables[(x, y)] = 1
            cset -= set(adjs((x, y)))

while cset:
    p = random.choice(list(cset))
    gettables[p] = int(math.interp(math.hypot(*p), 3, 1, 20, 4) + random.random())
    cset -= set(adjs(p))

tofill = set(gridset)
tofill.remove(ORIGIN)
tofill -= set(gettables)
tofill -= set(artifacts)

if False:
    for x, y in tofill:
        n = int(math.interp(math.hypot(x, y), 2, 40, 40, 4))
        w = random.choice(list(ds) + [STILL] * n)
        s = int(math.interp(math.hypot(x, y), 0, 1, R, 3) + random.random())
        setwind((x, y), w, s)

for x, y in tofill:
    f = math.interp(math.hypot(x, y), 1, 0, 2, 0.5)
    if random.random() < f:
        w = random.choice(ds)
        s = int(math.interp(math.hypot(x, y), 4, 1, 25, 3) + random.random())
        setwind((x, y), w, s)
    else:
        setwind((x, y), STILL)




def draw():
    x0, y0, x1, y1 = view.bounds()
    x0 = max(int(x0 - 0.5), -R)
    y0 = max(int(y0 - 0.5), -R)
    x1 = min(int(x1 + 0.5), R)
    y1 = min(int(y1 + 0.5), R)

    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            dxys = arrowds[wind[(x, y)]]
            if not dxys:
                continue
            ps = [view.worldtoscreen((x + dx, y + dy)) for dx, dy in dxys]
            color = {
                1: (200, 200, 255),
                2: (240, 240, 240),
                3: (255, 200, 200),
            }[strength[(x, y)]]
            pygame.draw.polygon(pview.screen, color, ps)
#            ptext.draw(wnames[wind[(x, y)]], center = view.worldtoscreen((x, y)),
#                color = (220, 220, 255), fontsize = view.sizetoscreen(0.3))




