# The game takes place in a three-dimensional space with a right-handed coordinate system:
#  increasing x -> to the right on the screen
#  increasing y -> upwards on the screen
#  increasing z -> out of the screen (closer to the viewer)
# Objects exist on a single plane (single z-value), although the player character can interact
# with objects on any plane. Objects with a higher z value may block from existence objects with a
# lower z value.

# An object's (x0, y0) value at a given time is its (x, y) value projected onto the z = 0 plane.
# Even if an object doesn't move in its own plane, its (x0, y0) changes as the camera moves.

# For the purposes of interactions, it's best to map things to the 0 plane before comparing them.

from __future__ import division, print_function
import math, pygame, bisect
from . import pview, settings
from .pview import T

# Camera offset. The position (X0, Y0, 0) is at the center of the screen.
# Y0 remains at 0 for the entire game.
X0, Y0 = None, None

def init():
	global X0, Y0
	# TODO: pview dump options
	pview.set_mode((1024, 480), height = settings.res, fullscreen = settings.fullscreen, forceres = settings.forceres)
	pygame.display.set_caption(settings.gamename)
	pygame.mouse.set_visible(False)
	X0, Y0 = 0, 0

def cycleresolution():
	js = [j for j, h in enumerate(settings.resolutions) if pview.h < h]
	j = min(js) if js else 0
	pview.set_mode(height = settings.resolutions[j])

def reset():
	global X0, Y0
	X0, Y0 = 0, 0

# Scale factor at the given z plane, with respect to the z = 0 plane.
def scale(z):
	return math.phi ** (z / 10)

def screenscale(r, z):
	return T(settings.gamescale * r * scale(z))

# Given an (x, y, z) position, return the position (x0, y0) such that (x, y, z) currently occupies
# the same screen position as (x0, y0, 0).
def to0(x, y, z):
	s = scale(z)
	return (x - X0) * s + X0, (y - Y0) * s + Y0
def from0(x0, y0, z):
	return to0(x0, y0, -z)

# Given an (x, y, z) position, return the position (x0, y0) such that the current screen position of
# (x, y, z) is the same as the screen position of (x0, y0, 0) when (X0, Y0) = (0, 0).
def to0plane(x, y, z):
	s = scale(z)
	return (x - X0) * s, (y - Y0) * s
def from0plane(x, y, z):
	s = scale(z)
	return X0 + x / s, Y0 + y / s
def from0planeatP0(x, y, z, P0):
	s = scale(-z)
	X0, Y0 = P0
	return X0 + x / s, Y0 + y / s

def toscreen(gx, gy, gz = 0):
	x, y = to0plane(gx, gy, gz)
	return T(pview.centerx0 + settings.gamescale * x, pview.centery0 - settings.gamescale * y)

def screenoffset(dx, dy, z):
	s = scale(z) * settings.gamescale
	return T(dx * s, -dy * s)

# The value of X0 at which the given x-coordinate in the z plane is at the same horizontal screen
# position of the given x0-coordinate in the 0 plane at X0 = 0.
def cameraat0(x, z, x0):
	return x - x0 / scale(z)
# When the camera is at X0, the value of x in the z-plane that's at the same horizontal screen
# position as x = x0 in the 0 plane.
def atcamera(X0, z, x0):
	return X0 + x0 / scale(z)

# Determine the x-value x2 such that (x2, z2) is at the player position when (x1, z1) is also at the
# player position.
def xmatchatplayer(x1, z1, z2):
	# playerx = (x1 - X) * scale(z1) = (x2 - X) * scale(z2)
	playerx = -30
	X = x1 - playerx / scale(z1)
	return playerx / scale(z2) + X

if __name__ == "__main__":
	from . import maff
	X0, Y0 = 0, 0
	print(to0(0, 0, 0))  # (0, 0)
	print(to0(0, 0, 5))  # (0, 0)
	print(to0(10, 0, 0))  # (10, 0)
	print(to0(10, 0, 5))  # (12.7, 0)
	X0 = 10
	print(to0(10, 0, 0))
	print(to0(10, 0, 5))

