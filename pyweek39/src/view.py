import pygame
from . import pview, settings

def init():
    pview.set_mode(size0 = settings.resolution)
    pygame.display.set_caption(settings.gamename)


class camera:
    x0, y0 = 0, 0
    scale = 30

def worldtoscreen(p):
    x, y = p
    px = pview.centerx0 + camera.scale * x
    py = pview.centery0 - camera.scale * y
    return pview.T(px, py)


