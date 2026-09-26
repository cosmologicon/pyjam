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

def vecsub(v0, v1):
	x0, y0 = v0
	x1, y1 = v1
	return x0 - x1, y0 - y1

def intersectsegcircle(pos0, pos1, center, r):
	t = math.clamp(math.dot(math.norm(vecsub(pos1, pos0)), vecsub(center, pos0)), 0, 1)
	pos = math.mix(pos0, pos1, t)
	return math.distance(pos, center) <= r

def intersectrectcircle(rect_pos, rect_size, circ_pos, circ_r):
	rect_x, rect_y = rect_pos
	rect_w, rect_h = rect_size
	circ_x, circ_y = circ_pos
	if rect_x <= circ_x < rect_x + rect_w and rect_y <= circ_y < rect_y + rect_h:
		return True
	ps = [(rect_x, rect_y), (rect_x + rect_w, rect_y), (rect_x + rect_w, rect_y + rect_h), (rect_x, rect_y + rect_h)]
	segs = [(ps[0], ps[1]), (ps[1], ps[2]), (ps[2], ps[3]), (ps[3], ps[0])]
	return any(intersectsegcircle(pos0, pos1, circ_pos, circ_r) for pos0, pos1 in segs)

