import numpy, math, pygame
from . import state, view, pview
from .pview import T


def string():
	# Find the amount of droop in the string so that the total length is roughly equal to the
	# constant string length.
	# TODO: binary search for more efficiency.
	droop = 0
	while pathlength(droop) < state.stringlength:
		droop += 0.1
	ps = [view.worldtoscreen(p) for p in path(droop)]
	pygame.draw.lines(pview.screen, (0, 0, 0), False, ps, T(2))


# Sequence of points on the string path with the given droop factor.
def path(droop):
	hs = [j / 40 for j in range(41)]
	p0s = [math.mix(state.balloon.p, state.castle.p, h) for h in hs]
	return [(x, y - h * (1 - h) * droop) for h, (x, y) in zip(hs, p0s)]

def pathlength(droop):
	p = path(droop)
	return sum(math.distance(p[j], p[j+1]) for j in range(len(p) - 1))


