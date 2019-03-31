
# COORDINATE SYSTEMS:

# B-coordinates: baseline coordinates that run from (0, 0) in the upper-left to settings.size0 in
# the lower-right.

# F-coordinates: flake-specific coordinates that are 0 at the center of the flake. x increases to
# the right and y increases upward. The radius of the flake is 1.
# Transforming between B and F coordinates requires a flakespot (Fspot), which specifies the center
# and radius of the flake in B-coordinates.

from __future__ import division
import pygame, math
from . import settings, pview
from .pview import I, T

def init():
	pygame.display.init()
	pygame.display.set_caption(settings.gamename)
	pygame.font.init()
	pview.set_mode(settings.size0, forceres = settings.forceres, fullscreen = settings.fullscreen)


def FconvertB(Fspot, pB):
	(x0B, y0B), BrF = Fspot
	xB, yB = pB
	return (xB - x0B) / BrF, -(yB - y0B) / BrF

def BconvertF(Fspot, pF):
	(x0B, y0B), BrF = Fspot
	xF, yF = pF
	return x0B + BrF * xF, y0B - BrF * yF

def BrectoverFspot(Fspot):
	(x0B, y0B), BrF = Fspot
	rect = pygame.Rect(I(0, 0, 2 * BrF, 2 * BrF))
	rect.center = I(x0B, y0B)
	return rect

def Fspotapproach(Fspot0, Fspot1, dlogx):
	pos0, r0 = Fspot0
	pos1, r1 = Fspot1
	return math.softapproach(pos0, pos1, dlogx), math.softapproach(r0, r1, dlogx)

def Fspotvisible(Fspot):
	(x, y), r = Fspot
	rect = pygame.Rect((x - r, y - r, 2 * r, 2 * r))
	return rect.colliderect(pview.rect0)


