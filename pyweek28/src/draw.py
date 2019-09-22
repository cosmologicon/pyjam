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


# TODO(Christopher): there are much better looking options than this. Revisit this once we have an
# idea for the art style.

# For now, as a placeholder, stations are represented as a collection of cylinders, and we don't do
# any fancy occlusion, we just draw them in order from the back to the front.
def randomstationpiece():
	xW = random.uniform(-1, 1)
	yW = random.uniform(-1, 1)
	xW, yW = math.norm((xW, yW), 1.2)
	zW = random.uniform(-0.4, 0.4)
	h = random.uniform(0.01, 1) ** 0.5  # Bias toward shorter cylinders
	r = math.clamp(0.5 / h, 0.1, 2)
	color = random.randint(100, 200), random.randint(100, 200), random.randint(100, 200)
	return (xW, yW, zW), h, r, color
stationdata = [randomstationpiece() for _ in range(20)]

# TODO(Christopher): procedurally generate station layouts so they look unique.
def station(yG0, back):
	# TODO: abort early if the entire station is off screen.
	data = [(view.worldtogame(pW), h, w, color) for pW, h, w, color in stationdata]
	# Sort by depth
	data.sort(key = lambda entry: entry[0][1])
	for ((xG, yG), dG), h, r, color in data:
		if (back and dG > 0) or (not back and dG < 0):
			continue
		xV0, yV0 = view.gametoview((xG - r, yG0 + yG + h))
		xV1, yV1 = view.gametoview((xG + r, yG0 + yG - h))
		rect = pygame.Rect(xV0, yV0, xV1 - xV0, yV1 - yV0)
		if pview.rect.colliderect(rect):
			pview.screen.fill(color, rect)
		
	
