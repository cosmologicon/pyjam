# Unless otherwise noted, all positions and distances in this module are game (G) coodinates.
# Angle convention: Like a clock. 0 = up (-y). tau/4 = right (+x).

import math

def angletoward(pos):
	x, y = pos
	if (x, y) == (0, 0): return 0
	return math.atan2(x, -y)
	

def pgangle(A):
	return math.degrees(-A)


def vecadd(v0, v1):
	x0, y0 = v0
	x1, y1 = v1
	return x0 + x1, y0 + y1


