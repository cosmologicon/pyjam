# Draw world objects (i.e. in the middle panel)

import pygame, math, random
from . import pview, state, view
from .pview import T

# TODO(Christopher): Even though it's less realistic, I think it might look more dymanic if the
# starfield had a feeling of depth, i.e. not all the stars parallax the same amount when you move.
def randomstar():
	y = random.uniform(0, 10000)
	A = random.uniform(0, 1)
	return y, A
stardata = [randomstar() for _ in range(10000)]

# TODO: restrict to the central viewing area.
def stars():
	pview.fill((0, 0, 0))
	Nstar = 500  # TODO: change dynamically with resolution
	for y, A in stardata[:Nstar]:
		# TODO: dynamically change with camera zoom level
		pos = T(pview.centerx + 4000 * view.dA(A, view.A), 300 * (y - view.yG0) % pview.h)
		# TODO: different colors correlated with depth
		color = 255, 255, 255
		pview.screen.set_at(pos, color)

def atmosphere():
	# Atmosphere
	alpha = pview.I(math.fadebetween(view.yG0, 10, 255, 100, 0))
	if alpha: 
		pview.fill((100, 130, 220, alpha))

# TODO(Christopher): that fancy "woven" effect for the cable. (Christopher)

# The central cable.
def cable():
	for f, shade in [(1, 50), (0.92, 60), (0.8, 70), (0.55, 80)]:
		xV0, yV0 = view.gametoview((-f * state.radius, state.top))
		xV1, yV1 = view.gametoview((f * state.radius, 0))
		yV0 = max(yV0, 0)
		yV1 = min(yV1, pview.h)
		rect = pygame.Rect(xV0, yV0, xV1 - xV0, yV1 - yV0)
		pview.screen.fill((shade, shade, shade), rect)

# TODO(Christopher): procedurally generate station layouts so they look unique.
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
		
	
