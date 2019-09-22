# View coordinates: Pygame position in pixels
#   (xV, yV) = (0, 0) is top left, (pview.w, pview.h) is bottom right.
# Game coordinates: position in the main view window in units of krelmars (km).
#   xG = 0 at the center of the elevator, with positive xG to the right.
#   yG = 0 at the surface, with positive yG going up.

import pygame
from . import settings, pview
from .pview import T

# Current center of the screen in game coordinates
xG0, yG0 = 0, 0
# Current size of a game unit in baseline pixels (still need to apply T to get to view coordinates)
zoom = 100


def init():
	pview.set_mode(settings.resolution)
	pygame.display.set_caption(settings.gamename)

def gametoview(pG):
	xG, yG = pG
	xV = T(pview.centerx0 + (xG - xG0) * zoom)
	yV = T(pview.centery0 - (yG - yG0) * zoom)
	return xV, yV

# TODO: implement viewtogame


