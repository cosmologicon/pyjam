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
import math
from . import pview, settings
from .pview import T

# Camera offset. The position (X0, Y0, 0) is at the center of the screen.
X0, Y0 = None, None

def init():
	global X0, Y0
	pview.set_mode((1024, 480))
	X0, Y0 = 0, 0

def scale(z):
	return math.phi ** (z / 10)

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

def toscreen(gx, gy, gz = 0):
	x, y = to0plane(gx, gy, gz)
	return T(pview.centerx0 + 10 * x, pview.centery0 - 10 * y)

def screenoffset(dx, dy, z):
	s = scale(z) * 10
	return T(dx * s, -dy * s)

# The value of X0 at which the given x-coordinate in the z plane is at the same horizontal screen
# position of the given x0-coordinate in the 0 plane at X0 = 0.
def cameraat0(x, z, x0):
	return x - x0 / scale(z)
# When the camera is at X0, the value of x in the z-plane that's at the same horizontal screen
# position as x = x0 in the 0 plane.
def atcamera(X0, z, x0):
	return X0 + x0 / scale(z)

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
