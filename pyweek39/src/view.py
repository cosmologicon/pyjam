import pygame, math
from . import pview, settings, state

class camera:
    x0, y0 = 0, 0
    scale = 140
    zfactor = 1
    zoom = True
    cx0, cy0 = 0, 0
    target = 0, 0
    cscale = 140
    starget = 140
    vrect = None

def cacheres():
    from . import grid, graphics
    grid.cacheres()
    graphics.cacheres()


def init():
    pview.set_mode(size0 = settings.resolution)
    pygame.display.set_caption(settings.gamename)
    cacheres()
    think(0)

def think(dt):
    camera.starget = int(140 * 0.95 ** (state.maxfuel - 6))
    camera.cx0, camera.cy0 = math.softapproach((camera.cx0, camera.cy0), camera.target, 4.0 * dt, dymin = 1 / camera.cscale)
    camera.cscale = math.softapproachL(camera.cscale, camera.starget, 8 * dt, dymin = 0.001)
    camera.zfactor = math.softapproach(camera.zfactor, (1 if camera.zoom else 0), 6.0 * dt, dymin = 0.001)
    
    camera.x0, camera.y0 = math.mix((0, 0), (camera.cx0, camera.cy0), camera.zfactor)
    camera.scale = math.mixL(14, camera.cscale, camera.zfactor)

    camera.vrect = pview.rect.inflate(pview.T(camera.scale / 2, camera.scale / 2))


def worldtoscreen(p):
    x, y = p
    px = pview.centerx0 + camera.scale * (x - camera.x0)
    py = pview.centery0 - camera.scale * (y - camera.y0)
    return pview.T(px, py)

def onscreen(p):
    return camera.vrect.collidepoint(worldtoscreen(p))

def screentoworld(p):
    px, py = p
    x = camera.x0 + (px / pview.f - pview.centerx0) / camera.scale
    y = camera.y0 - (py / pview.f - pview.centery0) / camera.scale
    return x, y

def sizetoscreen(r):
    return pview.T(camera.scale * r)

def snapto(pos):
    camera.cx0, camera.cy0 = pos
    camera.target = pos
    think(0)

def zoomswap():
    camera.zoom = not camera.zoom


def bounds():
    x0, y0 = screentoworld(pview.bottomleft)
    x1, y1 = screentoworld(pview.topright)
    return x0, y0, x1, y1

