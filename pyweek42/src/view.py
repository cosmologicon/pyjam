import pygame
from . import settings, pview

def init():
	pview.set_mode(size0 = settings.size0, height = settings.height, fullscreen = settings.fullscreen, forceres = settings.forceres)
	pygame.display.set_caption(settings.gamename)






