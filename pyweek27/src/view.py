import pygame
from . import settings, pview

def init():
	pygame.display.init()
	pygame.display.set_caption(settings.gamename)
	pygame.font.init()
	pview.set_mode(settings.size0, forceres = settings.forceres)



