import pygame, math
from . import pview, settings, state
from .pview import T


# camera position
cx, cy = 0, 0
zoom = 120

# Right panel width
rw = 240
rrect = pygame.Rect(1280 - rw, 0, rw, 720)

# Minimum y-value that should ever be visible on screen
ymin = -1

def init():
	pview.set_mode(size0 = settings.size0, height = settings.height0,
		fullscreen = settings.fullscreen, forceres = settings.forceres)

def think(dt):
	global cx, cy
	target = state.you.x + 0.5, state.you.y + 1
	cx, cy = math.softapproach((cx, cy), target, 5 * dt, dymin = 1 / zoom)
	if state.w * zoom < rrect.left:
		cx = state.w / 2
	else:
		dx = rrect.left / zoom / 2
		cx = math.clamp(cx, dx, state.w - dx)
	cy = max(cy, state.yfloor + ymin + pview.centery0 / zoom)

def worldtoscreen(pos):
	x, y = pos
	x = rrect.left / 2 + zoom * (x - cx)
	y = pview.centery0 - zoom * (y - cy)
	return T(x, y)

def mapzoom():
	return rw / (state.w + 2)

def worldtomap(pos):
	x, y = pos
	x0 = 1280 - rw / 2
	y0 = 620
	mzoom = mapzoom()
	x = x0 + mzoom * (x - state.w / 2)
	y = y0 - mzoom * y
	return T(x, y)



