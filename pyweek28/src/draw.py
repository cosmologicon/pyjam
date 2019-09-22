# Draw world objects (i.e. in the middle panel)

import pygame
from . import pview, state, view
from .pview import T

# TODO: that fancy "woven" effect for the cable.

# The central cable.
def cable():
	for f, shade in [(1, 50), (0.92, 60), (0.8, 70), (0.55, 80)]:
		xV0, yV0 = view.gametoview((-f * state.radius, state.top))
		xV1, yV1 = view.gametoview((f * state.radius, 0))
		yV0 = max(yV0, 0)
		yV1 = min(yV1, pview.h)
		rect = pygame.Rect(xV0, yV0, xV1 - xV0, yV1 - yV0)
		pview.screen.fill((shade, shade, shade), rect)

# TODO: procedurally generate station layouts so they look unique.
def station(yG):
	# TODO: abort early if the entire station is off screen.
	rectdata = [
		(1.2, 1.0, (40, 140, 140)),
		(1.5, 0.5, (50, 150, 150)),
		(2.0, 0.2, (60, 160, 160)),
	]
	for w, h, color in rectdata:
		xV0, yV0 = view.gametoview((-w, yG + h))
		xV1, yV1 = view.gametoview((w, yG - h))
		rect = pygame.Rect(xV0, yV0, xV1 - xV0, yV1 - yV0)
		if pview.rect.colliderect(rect):
			pview.screen.fill(color, rect)
		
	
