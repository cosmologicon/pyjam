import pygame, math
from . import pview, settings, state
from .pview import T

# All possible values of zoom, to be used for precaching images.
allzooms = 144, 180, 224

# camera position
cx, cy = 0, 0
zoom = 224

# Right panel width
rw = 320
rrect = pygame.Rect(1280 - rw, 0, rw, 720)

# Minimum y-value that should ever be visible on screen
ymin = -1

def init():
	pview.set_mode(size0 = settings.size0, height = settings.height0,
		fullscreen = settings.fullscreen, forceres = settings.forceres)

def rwall():
	return rrect.left if state.panel else pview.w0
def vcenter():
	return rwall() / 2

def think(dt):
	global cx, cy
	targetx, targety = state.you.x + 0.5, state.you.y + 1
	cymin = state.yfloor + ymin + pview.centery0 / zoom
	cymax = state.h + 2 - pview.centery0 / zoom
	targety = math.clamp(targety, cymin, cymax)
	cx, cy = math.softapproach((cx, cy), (targetx, targety), 5 * dt, dymin = 1 / zoom)
	
	if state.w * zoom < rwall():
		cx = state.w / 2
	else:
		dx = vcenter() / zoom
		cx = math.clamp(cx, dx, state.w - dx)

def worldtoscreen(pos):
	x, y = pos
	x = vcenter() + zoom * (x - cx)
	y = pview.centery0 - zoom * (y - cy)
	return T(x, y)

def screen0toworld(pos):
	px, py = pos
	x = (px - vcenter()) / zoom + cx
	y = cy - (py - pview.centery0) / zoom
	return x, y


maptop = 220
def mapzoom():
	return min(rw / (state.w + 1), T(pview.h - maptop) / (state.h + 1))

def worldtomap(pos):
	x, y = pos
	x0 = 1280 - rw / 2
	y0 = pview.centery0 + maptop / 2
	mzoom = mapzoom()
	x = x0 + mzoom * (x - state.w / 2)
	y = y0 - mzoom * (y - state.h / 2)
	return T(x, y)


def backgroundspec():
	a = 0.3
	# Midpoint of the horizon
	x0, y0 = vcenter(), pview.centery0 + zoom * cy
	x0, y0 = math.mix((x0, y0), (vcenter(), pview.centery0), 1 - a)
	cxmin = state.w / 2 if state.w * zoom < rwall() else vcenter() / zoom
	wmin = 2 + rwall() + 2 * a * (state.w / 2 - cxmin) * zoom
	cymin = 0 + -1 + pview.centery0 / zoom
	ceiling = state.ychecks[-1] + 1 if state.ychecks else state.h
	cymax = ceiling + 2 - pview.centery0 / zoom
	ybottom = pview.centery0 + zoom * cymin
	hmin = 2 + ybottom + (cymax - cymin) * zoom * a
	return (x0, y0), (wmin, hmin)

def visiblerange():
	xmin, ymin = screen0toworld((0, pview.height0))
	xmax, ymax = screen0toworld((rwall(), 0))
	return (xmin - 1, xmax + 1), (ymin - 1, ymax + 1)


