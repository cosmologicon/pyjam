# positive xG: to the right
# positive yG: up
# angles increase clockwise: A = 0 up, A = tau/4 right

import pygame
from . import settings, pview
from .pview import T

xG0, yG0 = 0, 0
VscaleG = 100  # Technically V0scaleG, since this is in pview baseline coordinates.


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

