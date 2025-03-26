import pygame, math
from . import pview, settings

def init():
    pview.set_mode(size0 = settings.resolution)
    pygame.display.set_caption(settings.gamename)


class camera:
    x0, y0 = 0, 0
    scale = 80
    target = 0, 0

def worldtoscreen(p):
    x, y = p
    px = pview.centerx0 + camera.scale * (x - camera.x0)
    py = pview.centery0 - camera.scale * (y - camera.y0)
    return pview.T(px, py)

def screentoworld(p):
    px, py = p
    x = camera.x0 + (px / pview.f - pview.centerx0) / camera.scale
    y = camera.y0 - (py / pview.f - pview.centery0) / camera.scale
    return x, y

def sizetoscreen(r):
    return pview.T(camera.scale * r)

def snapto(pos):
    camera.x0, camera.y0 = pos
    camera.target = pos

def think(dt):
    camera.x0, camera.y0 = math.softapproach((camera.x0, camera.y0), camera.target, 1.0 * dt, dymin = 1 / camera.scale)

def bounds():
    x0, y0 = screentoworld(pview.bottomleft)
    x1, y1 = screentoworld(pview.topright)
    return x0, y0, x1, y1

