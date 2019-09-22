# View coordinates: Pygame position in pixels
#   (xV, yV) = (0, 0) is top left, (pview.w, pview.h) is bottom right.
# Game coordinates: position in the main view window in units of krelmars (km).
#   xG = 0 at the center of the elevator, with positive xG to the right.
#   yG = 0 at the surface, with positive yG going up.
# A is the viewing angle, going from 0 to 1 and wrapping around.
# A = 0 means facing North, i.e. the camera is South of the elevator.
# A = 1/8 means facing Northeast, i.e. the camera is Southwest of the elevator.
# This can be a little counterintuitive, but if you step left, that moves you clockwise around the
# elevator, e.g. from South to Southwest.
# Note that xG refers to the viewing plane from the player's perspective. This means that an
# object's xG coordinate changes as you step around the elevator.

from __future__ import division
import pygame, math
from . import settings, pview
from .pview import T

# Current center of the screen in game coordinates
xG0, yG0 = 0, 0
# Current size of a game unit in baseline pixels (still need to apply T to get to view coordinates)
zoom = 100
# Current viewing angle
A = 0


def init():
	pview.set_mode(settings.resolution)
	pygame.display.set_caption(settings.gamename)

def gametoview(pG):
	xG, yG = pG
	xV = T(pview.centerx0 + (xG - xG0) * zoom)
	yV = T(pview.centery0 - (yG - yG0) * zoom)
	return xV, yV

# TODO: implement viewtogame


# viewing angles A are wrapped between 0 and 1. This returns the difference A0 - A1 (mod 1) such
# that the value is between -1/2 and +1/2.
def dA(A0, A1):
	return (A0 - A1 + 1/2) % 1 - 1/2

# approach function that takes the shortest distance wrapping around between 0 and 1.
# e.g. if you're at A0 = 7/8 and you want to approach A1 = 0, this will increase rather than decrease.
def Aapproach(A0, A1, Astep):
	return (A1 - math.softapproach(dA(A1, A0), 0, Astep, dymin = 0.001)) % 1
	

