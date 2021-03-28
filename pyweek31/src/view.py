import pygame
from . import pview
from . import settings

screen = None
def init():
	global screen
	pview.set_mode(size0 = settings.size0, height = settings.height, fullscreen = settings.fullscreen, forceres = settings.forceres)
	screen = pygame.display.get_surface()

def clear():
	screen.fill((25, 50, 25))


