import pygame, math
from . import pview, settings, state
from .pview import T


# camera position
cx, cy = 0, 0
zoom = 100

def init():
	pview.set_mode(size0 = settings.size0, height = settings.height0,
		fullscreen = settings.fullscreen, forceres = settings.forceres)



def think(dt):
	global cx, cy
	target = state.you.x, state.you.y
	cx, cy = math.softapproach((cx, cy), target, 3 * dt, dymin = 1 / zoom)

def worldtoscreen(pos):
	x, y = pos
	x = pview.centerx0 + zoom * (x - cx)
	y = pview.centery0 - zoom * (y - cy)
	return T(x, y)



