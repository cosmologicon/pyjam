import random, pygame, math
from functools import lru_cache, cache
from . import view, pview, ptext, graphics
from .pview import T

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


def adjs(p):
    x, y = p
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
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


def random_weighted(dist, n0 = 0):
    values = []
    for level, weight in enumerate(dist, n0):
        values += [level] * weight
    return random.choice(values)


def gettable_at(p):
    n = int(math.interp(math.hypot(*p), 0, 0, 30, 5) + random.random())
    dist = {
        0: [1, 0, 0, 0],
        1: [1, 1, 0, 0],
        2: [2, 3, 1, 0],
        3: [2, 6, 6, 0],
        4: [0, 3, 6, 1],
        5: [0, 0, 1, 1],
    }[n]
    return random_weighted(dist, 1)

def strength_at(p):
    n = int(math.interp(math.hypot(x, y), 0, 0, 30, 4) + random.random())
    dist = {
        0: [1, 0, 0],
        1: [1, 1, 0],
        2: [1, 4, 0],
        3: [1, 4, 1],
        4: [1, 3, 3],
    }[n]
    return random_weighted(dist, 1)


while cset:
    p = random.choice(list(cset))
    gettables[p] = gettable_at(p)
    cset -= set(adjs(p))

tofill = set(gridset)
tofill.remove(ORIGIN)
tofill -= set(gettables)
tofill -= set(artifacts)

for artifact in artifacts[-4:]:
    tofill -= set(adjs(artifact))
    for p, w in zip(adjs(artifact), [E, E, E, N, STILL, S, W, W, W]):
        setwind(p, w, 3)


for x, y in tofill:
    f = math.interp(math.hypot(x, y), 1, 0, 2, 0.5)
    if random.random() < f:
        w = random.choice(ds)
        s = strength_at((x, y))
        setwind((x, y), w, s)
    else:
        setwind((x, y), STILL)

setwind((0, 1), E)

@lru_cache(100)
def old_windstrip0(w):
    w *= 4
    surf0 = pygame.Surface((w, w)).convert_alpha()
    surf0.fill((255, 255, 255, 0))
    x0, x1, x2 = pview.I(0.0 * w, 0.5 * w, 1.0 * w)
    y0, y1, dy = pview.I(0.1 * w, 0.35 * w, 0.3 * w)
    for sy in [-w, w-w//2, 0, w//2, w]:
        ps = [
            (x0, y1 + dy), (x1, y1), (x2, y1 + dy),
            (x2, y0 + dy), (x1, y0), (x0, y0 + dy),
        ]
        ps = [(x, y + sy) for x, y in ps]
        pygame.draw.polygon(surf0, (255, 255, 255, 255), ps)
    surf = pygame.Surface((w, 2 * w)).convert_alpha()
    surf.fill((255, 255, 255, 0))
    surf.blit(surf0, (0, 0))
    surf.blit(surf0, (0, w))
    w = int(w / 4)
    return pygame.transform.smoothscale(surf, (w, 2 * w))

@lru_cache(1000)
def old_windstrip(strength, w):
    if strength == 1:
        return graphics.mask(old_windstrip0(w), (140, 140, 255, 255))
    if strength == 2:
        surf0 = old_windstrip0(w)
        surf = pygame.Surface((2 * w, 2 * w)).convert_alpha()
        surf.fill((0, 0, 0, 0))
        d = int(w * 0.2)
        surf.blit(surf0, (d, 0), (0, 0, w - d, 2 * w))
        surf.blit(surf0, (w, 0), (d, 0, w - d, 2 * w))
        return pygame.transform.smoothscale(surf, (w, 2 * w))
    if strength == 3:
        surf0 = old_windstrip0(w)
        surf = pygame.Surface((3 * w, 2 * w)).convert_alpha()
        surf.fill((0, 0, 0, 0))
        d = int(w * 0.3)
        xc = int(w * 1.5)
        s = int(w * 0.5) + d
        a = int(w * 0.5) - d
        x1 = xc - d
        x0 = x1 - s
        x2 = xc + d
        surf.blit(surf0, (x0, 0), (0, 0, s, 2 * w))
        surf.blit(surf0, (x1, 0), (a, 0, 2 * d, 2 * w))
        surf.blit(surf0, (x2, 0), (a, 0, s, 2 * w))
        surf = pygame.transform.smoothscale(surf, (w, 2 * w))
        return graphics.mask(surf, (255, 160, 160, 255))

@cache
def windstrip0(strength):
    w = 800
    color = {
        1: (140, 140, 255, 255),
        2: (255, 255, 255, 255),
        3: (255, 160, 160, 255),
    }[strength]
    surf = pygame.Surface((w, 2 * w)).convert_alpha()
    surf.fill(color[:3] + (0,))
    arrowspec = {
        1: [(1, 0.6)],
        2: [(0.3, -0.3), (1, 0.6)],
        3: [(0.2, 0.5), (0.4, 0.2), (1, 1.5)],
    }[strength]
    rowps = [pview.I(w/2 * (1 - x), w/2 * y) for x, y in reversed(arrowspec)] + [pview.I(w/2, 0)] + [pview.I(w/2 * (1 + x), w/2 * y) for x, y in arrowspec]
    poly0ps = rowps + [pview.I(x, y + w/4) for x, y in reversed(rowps)]
    for jdy in range(-2, 6):
        dy = int(jdy * w / 2)
        polyps = [(x, y + dy) for x, y in poly0ps]
        pygame.draw.polygon(surf, color, polyps)
    return surf

@cache
def windstrip(strength, w):
    return pygame.transform.smoothscale(windstrip0(strength), (w, 2 * w))

        

@lru_cache(100)
def fadetile(w):
    if w != 100:
        return pygame.transform.smoothscale(fadetile(100), (w, w))
    surf = pygame.Surface((w, w)).convert_alpha()
    for x in range(w):
        for y in range(w):
            dx = ((w - 1) / 2 - x) / (w - 1) * 2 * 1.5
            dy = ((w - 1) / 2 - y) / (w - 1) * 2 * 1.2
            alpha = 0.2 * (1 - dx ** 4 - dy ** 4)
            color = 255, 255, 255, math.imix(0, 255, alpha)
            surf.set_at((x, y), color)
    return surf

@lru_cache(1000)
def windtile0(strength, w, f, d):
    if d == W:
        return pygame.transform.rotate(windtile0(strength, w, f, N), 90)
    if d == S:
        return pygame.transform.rotate(windtile0(strength, w, f, N), 180)
    if d == E:
        return pygame.transform.rotate(windtile0(strength, w, f, N), 270)
    surf = fadetile(w).copy()
    y = pview.I(w * f)
    surf.blit(windstrip(strength, w), (0, -y), None, pygame.BLEND_RGBA_MULT)
    return surf

def windtile(strength, w, f, d):
    f = int(f % 1 * 32) / 32
    return windtile0(strength, w, f, d)

def drawtile(x, y):
    if wind[(x, y)] == STILL: return
    f = pygame.time.get_ticks() * 0.001 * 0.5 * strength[(x, y)] + math.fuzz(123, x, y)
    tile = windtile(strength[(x, y)], view.sizetoscreen(1), f, wind[(x, y)])
    pview.screen.blit(tile, tile.get_rect(center = view.worldtoscreen((x, y))))

def drawarrow(x, y):
    dxys = arrowds[wind[(x, y)]]
    if not dxys:
        return
    ps = [view.worldtoscreen((x + dx, y + dy)) for dx, dy in dxys]
    color = {
        1: (200, 200, 255),
        2: (240, 240, 240),
        3: (255, 200, 200),
    }[strength[(x, y)]]
    pygame.draw.polygon(pview.screen, color, ps)

def draw():
    x0, y0, x1, y1 = view.bounds()
    x0 = max(int(x0 - 0.5), -R)
    y0 = max(int(y0 - 0.5), -R)
    x1 = min(int(x1 + 0.5), R)
    y1 = min(int(y1 + 0.5), R)

    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            if wind[(x, y)] == STILL: continue
#            drawarrow(x, y)
            drawtile(x, y)

#            ptext.draw(wnames[wind[(x, y)]], center = view.worldtoscreen((x, y)),
#                color = (220, 220, 255), fontsize = view.sizetoscreen(0.3))

def drawoverlay(d, f):
    w = T(800)
    alpha = math.imix(0, 255, math.dfade(f, 0, 1, 0.3))
    tile = graphics.mask(windtile(1, w, f, d), (255, 255, 255, alpha))
    pview.screen.blit(tile, tile.get_rect(center = pview.center))

def cacheres():
    fadetile(T(800))
    windstrip(1, T(800))

