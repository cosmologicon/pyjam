import pygame, os.path
from functools import lru_cache, cache
from . import view, pview

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
def rotorimg0(f):
    img0 = loadimg("wing")
    surf = img0.copy()
    surf.fill((0, 0, 0, 0))
    anchor = surf.get_rect().center
    dtheta = 360 / Nwing
    for jwing in range(Nwing):
        theta = -dtheta * (jwing + f)
        img = pygame.transform.rotozoom(img0, theta, 1)
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

def cacheres():
    for jf in range(16):
        rotorimg0(jf / 16)
    for jf in range(32):
        gearimg0(jf / 32)


