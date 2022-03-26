import pygame, math
from . import pview, settings, geometry
from .pview import T

class camera:
	x0 = 0
	y0 = 0
	zoom = 10
	zoomout = 0
	

def init():
	pview.set_mode(size0 = settings.size0, fullscreen = settings.fullscreen,
		forceres = settings.forceres)
	pygame.display.set_caption(settings.gamename)

def setzoomout(k, dt):
	if k:
		camera.zoomout = math.softapproach(camera.zoomout, 1, 10 * dt, dymin=0.001)
	else:
		camera.zoomout = math.softapproach(camera.zoomout, 0, 10 * dt, dymin=0.001)

def screenpos(pos):
	z = math.mixL(camera.zoom, 4, camera.zoomout)
	p = math.mix((camera.x0, camera.y0), (0, 0), camera.zoomout)
	x, y = geometry.vecsub(pos, p)
	px = T(pview.w0 / 2 + z * x)
	py = pview.h - T(pview.h0 / 2 + z * y)
	return px, py

def screenscale(d):
	z = math.mixL(camera.zoom, 4, camera.zoomout)
	return T(z * d)

	

