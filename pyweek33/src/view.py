import pygame
from . import pview, settings
from .pview import T

class camera:
	x0 = 0
	y0 = 0
	zoom = 14

def init():
	pview.set_mode(size0 = settings.size0, fullscreen = settings.fullscreen)
	pygame.display.set_caption(settings.gamename)

def screenpos(pos):
	x, y = pos
	px = T(pview.w0 / 2 + camera.zoom * x)
	py = pview.h - T(pview.h0 / 2 + camera.zoom * y)
	return px, py

def screenscale(d):
	return T(camera.zoom * d)

	

