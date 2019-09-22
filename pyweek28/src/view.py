# View coordinates: Pygame position in pixels
#   (xV, yV) = (0, 0) is top left, (pview.w, pview.h) is bottom right.
# Game coordinates: position in the main view window in units of krelmars (km).
#   xG = 0 at the center of the elevator, with positive xG to the right.
#   yG = 0 at the surface, with positive yG going up.

import pygame
from . import settings, pview

def init():
	pview.set_mode(settings.resolution)
	pygame.display.set_caption(settings.gamename)



