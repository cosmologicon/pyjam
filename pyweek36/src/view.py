# positive xG: to the right
# positive yG: up
# angles increase counter-clockwise: A = 0 right, A = tau/4 up

import pygame, math
from . import settings, pview
from .pview import T

xG0, yG0 = 0, 0
VscaleG = 80  # Technically V0scaleG, since this is in pview baseline coordinates.


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

def VconvertG(pG):
	xG, yG = pG
	xV0, yV0 = pview.center0
	return T(xV0 + VscaleG * (xG - xG0), yV0 - VscaleG * (yG - yG0))

def isvisible(obj):
	xG, yG = obj.pos
	distG = math.hypot(xG - xG0, yG - yG0)
	radiusG = pview.s0 / VscaleG
	return distG < radiusG + obj.r

