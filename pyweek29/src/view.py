import pygame, math
from . import pview, settings, state
from .pview import T

# All possible values of zoom, to be used for precaching images.
allzooms = 120, 220

# camera position
cx, cy = 0, 0
zoom = 120

# Right panel width
rw = 360
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
	cymin = state.yfloor + ymin + pview.centery0 / zoom
	cymax = state.h + 2 - pview.centery0 / zoom
	cy = math.clamp(cy, cymin, cymax)

def worldtoscreen(pos):
	x, y = pos
	x = rrect.left / 2 + zoom * (x - cx)
	y = pview.centery0 - zoom * (y - cy)
	return T(x, y)

def screen0toworld(pos):
	px, py = pos
	x = (px - rrect.left / 2) / zoom + cx
	y = cy - (py - pview.centery0) / zoom
	return x, y

def mapzoom():
	return min(rw / (state.w + 2), pview.h0 / (state.h + 2))

def worldtomap(pos):
	x, y = pos
	x0 = 1280 - rw / 2
	y0 = pview.centery0
	mzoom = mapzoom()
	x = x0 + mzoom * (x - state.w / 2)
	y = y0 - mzoom * (y - state.h / 2)
	return T(x, y)


def backgroundspec():
	a = 0.3
	# Midpoint of the horizon
	x0, y0 = rrect.left / 2, pview.centery0 + zoom * cy
	x0, y0 = math.mix((x0, y0), (rrect.left / 2, pview.centery0), 1 - a)
	cxmin = state.w / 2 if state.w * zoom < rrect.left else rrect.left / zoom / 2
	wmin = 2 + rrect.left + 2 * a * (state.w / 2 - cxmin) * zoom
	cymin = state.yfloor + ymin + pview.centery0 / zoom
	cymax = state.h + 2 - pview.centery0 / zoom
	ybottom = pview.centery0 + zoom * cymin
	hmin = 2 + ybottom + (cymax - cymin) * zoom * a
	return (x0, y0), (wmin, hmin)

def visiblerange():
	xmin, ymin = screen0toworld((0, pview.height0))
	xmax, ymax = screen0toworld((rrect.left, 0))
	return (xmin - 1, xmax + 1), (ymin - 1, ymax + 1)


