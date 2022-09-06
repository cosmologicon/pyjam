import pygame
from . import pview
from . import settings

def init():
	pview.set_mode(settings.size0, fullscreen = settings.fullscreen)
	pygame.display.set_caption(settings.gamename)

