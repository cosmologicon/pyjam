import pygame
from . import pview, settings

def init():
	pygame.display.init()
	pview.set_mode(size0 = settings.size0, height = settings.height,
		fullscreen = settings.fullscreen, forceres = settings.forceres)

