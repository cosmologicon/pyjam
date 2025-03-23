import pygame
from . import pview, settings

def init():
    pview.set_mode(size0 = settings.resolution)
    pygame.display.set_caption(settings.gamename)





