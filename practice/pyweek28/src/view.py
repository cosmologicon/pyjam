# In world coordinates:
# x increases to the right
# y increases upward

# World coordinates are floats and the radius of the balloon is about 1.

from . import pview
from .pview import T


# Center of the screen in world units.
x0, y0 = 0, 0
zoom = 30  # Pixels per game unit in the default resolution. Actual zoom depends on resolution.

# TODO: dynamically zoom in or out depending on how powered up you are

def worldtoscreen(pworld):
	xworld, yworld = pworld
	xoffset = (xworld - x0) * zoom
	yoffset = (yworld - y0) * zoom
	return T(pview.centerx0 + xoffset, pview.centery0 - yoffset)


