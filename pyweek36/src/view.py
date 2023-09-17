import pygame
from . import settings, pview

def init():
	pview.set_mode(size0 = settings.size0, height = settings.height,
		fullscreen = settings.fullscreen, forceres = settings.forceres)
	pygame.display.set_caption(settings.gamename)

def toggle_fullscreen():
	settings.fullscreen = not settings.fullscreen
	pview.set_mode(fullscreen = settings.fullscreen)

def cycle_height():
	pview.cycle_height(settings.heights)
	settings.height = pview.height

