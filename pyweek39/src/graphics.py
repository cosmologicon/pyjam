import pygame, os.path, math
from functools import lru_cache, cache
from . import view, pview, settings

@cache
def loadimg(imgname):
    filename = os.path.join("img", f"{imgname}.png")
    return pygame.image.load(filename).convert_alpha()

def mask(surf, color):
    msurf = surf.copy()
    msurf.fill(color)
    msurf.blit(surf, (0, 0), None, pygame.BLEND_RGBA_MULT)
    return msurf


Nwing = 5

@cache
def bladeimg0(theta):
    return pygame.transform.rotozoom(loadimg("wing"), theta, 1)

@cache
def rotorimg0(f):
    img0 = loadimg("wing")
    surf = img0.copy()
    surf.fill((0, 0, 0, 0))
    anchor = surf.get_rect().center
    dtheta = 360 / Nwing
    for jwing in range(Nwing):
        theta = int(-dtheta * (jwing + f)) % 360
        img = bladeimg0(theta)
        surf.blit(img, img.get_rect(center = anchor))
    return surf

@lru_cache(200)
def rotorimg(w, f, flip = False):
    if flip:
        return pygame.transform.flip(rotorimg(w, f), True, False)
    img = pygame.transform.smoothscale(rotorimg0(f), (w, w))
    return img

@cache
def gearimg0(f):
    img0 = loadimg("gear")
    surf = img0.copy()
    surf.fill((0, 0, 0, 0))
    anchor = surf.get_rect().center
    dtheta = 360 / 4
    img = pygame.transform.rotozoom(img0, dtheta * f, 1)
    surf.blit(img, img.get_rect(center = anchor))
    return surf

@lru_cache(200)
def gearimg(w, f):
    img = pygame.transform.smoothscale(gearimg0(f), (w, w))
    return img

@lru_cache(20)
def domeimg(w, color=None):
    if color is not None:
        return mask(domeimg(w), color)
    return pygame.transform.smoothscale(loadimg("dome"), (w, w))

@lru_cache(20)
def bodyimg(w):
    return pygame.transform.smoothscale(loadimg("body"), (w, w))


@lru_cache(20)
def homeimg(w):
    return pygame.transform.smoothscale(mask(loadimg("home"), (100, 100, 100, 255)), (w, w))

@lru_cache(1000)
def waveimg(w, alpha):
    return mask(pygame.transform.smoothscale(loadimg("wave"), (w, w)), (255, 255, 255, alpha))


def drawimgat(img, p):
    anchor = view.worldtoscreen(p)
    pview.screen.blit(img, img.get_rect(center = anchor))

def drawrotor(p, f, flip = False):
    w = view.sizetoscreen(0.7)
    f = int(f % 1 * 32) / 32
    drawimgat(rotorimg(w, f, flip), p)

def drawgear(p, f):
    w = view.sizetoscreen(0.5)
    f = int(f % 1 * 32) / 32
    drawimgat(gearimg(w, f), p)

def drawbody(p):
    w = view.sizetoscreen(0.85)
    drawimgat(bodyimg(w), p)

def drawdome(p, color, size = 0.4):
    w = view.sizetoscreen(size)
    drawimgat(domeimg(w, color), p)

def drawhome0(p, w0):
    t = pygame.time.get_ticks() * 0.001 + 1234.56
    for af in (0.1, 0.1123):
        f = t * af % 1
        alpha = math.imix(10, 0, f)
        w = pview.I(w0 * math.mix(1, 1.8, f))
        drawimgat(waveimg(w, alpha), p)
    drawimgat(homeimg(w0), p)

def drawhome(p):
    drawhome0(p, view.sizetoscreen(1.4))


def drawlightning(f0):
    if not settings.lightning:
        return
    t = 0.001 * pygame.time.get_ticks()
    if math.fuzz(int(t)) < f0:
        f = t % 1
        if 0 < f < 0.1 or 0.2 < f < 0.3:
            pview.fill((255, 255, 255, 4))

def cacheres():
    for jf in range(32):
        f = jf / 32
        dtheta = 360 / Nwing
        for jwing in range(Nwing):
            theta = int(-dtheta * (jwing + f)) % 360
            bladeimg0(theta)
            yield
        rotorimg0(f)
        yield
    bladeimg0.cache_clear()
    for jf in range(32):
        gearimg0(jf / 32)
        yield

todo = cacheres()
def killtime(dt):
    global todo
    tend = pygame.time.get_ticks() + 1000 * dt
    while todo is not None and pygame.time.get_ticks() <= tend:
        try:
            next(todo)
        except StopIteration:
            todo = None
    return todo is not None

