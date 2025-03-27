import pygame, math, random
from functools import lru_cache
from . import view, pview
from .pview import T

@lru_cache(100)
def alphanoise(s, alpha0, *f):
    surf = pygame.Surface((s + 1, s + 1)).convert_alpha()
    for x in range(s + 1):
        for y in range(s + 1):
            color = 0, 0, 0, math.imix(0, 255 * alpha0, math.fuzz(x % s, y % s, 7.6, *f))
            surf.set_at((x, y), color)
    return surf    

@lru_cache(100)
def alphatexture(w, salphas, *f):
    surf = pygame.Surface((w, w)).convert_alpha()
    surf.fill((0, 0, 0, 0))
    for s, alpha in salphas:
        x0 = int(w * math.fuzz(8.7, s, alpha, *f))
        y0 = int(w * math.fuzz(9.8, s, alpha, *f))
        noise = pygame.transform.smoothscale(alphanoise(s, alpha, *f), (w + 1, w + 1)).subsurface((0, 0, w, w))
        for dx in (-w, 0):
            for dy in (-w, 0):
                surf.blit(noise, (x0 + dx, y0 + dy), None, pygame.BLEND_RGBA_ADD)
    return surf

@lru_cache(10)
def texture(w, *f):
    salphas = tuple((s, 0.3 * math.Phi ** j) for j, s in enumerate([8, 13, 21, 34, 55, 89]))
    surf = pygame.Surface((w, w)).convert_alpha()
    surf.fill((40, 40, 70, 0))
    surf.blit(alphatexture(w, salphas, *f), (0, 0), None, pygame.BLEND_RGBA_ADD)
    return surf

# A set of x-coordinates that step by w such that the width-w tiles starting at those coordinates
# completely cover the range [xmin, xmax).
def tilerange(w, x0, xmin, xmax):
    jmin = int((xmin - x0) / w) - 1
    jmax = int((xmax - x0) / w) + 1
    return [x0 + j * w for j in range(jmin, jmax)]

def xytilerange(size, p0, rect):
    w, h = size
    x0, y0 = p0
    for x in tilerange(w, x0, rect.left, rect.right):
        for y in tilerange(h, y0, rect.top, rect.bottom):
            yield x, y

def draw():
    pview.fill((0, 0, 20))
    spec = (600, 0.2, 0.4), (700, 0.2, -0.4), (800, -0.4, 0.1)
    for j, (w, dx, dy) in enumerate(spec):
        otexture = texture(T(w), j)
        t = 0.001 * pygame.time.get_ticks()
        x0 = (-0.5 * (view.camera.x0 + dx * t) * view.camera.scale)
        y0 = (0.5 * (view.camera.y0 + dy * t) * view.camera.scale)
        for p in xytilerange(otexture.get_size(), T(x0, y0), pview.rect):
            pview.screen.blit(otexture, p)

def drawstars():
    t = 0.001 * pygame.time.get_ticks()
    for j in range(1000):
        n, f = divmod(t + math.fuzz(1, j), 1)
        x0 = pview.width0 * math.fuzz(1, n, j)
        y0 = pview.height0 * math.fuzz(2, n, j)
        x1 = x0 + 200
        y1 = y0 + 100
        p = math.mix((x0, y0), (x1, y1), f)
        pview.screen.set_at(T(p), (80, 80, 80, 255))



