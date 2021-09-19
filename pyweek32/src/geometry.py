import math, bisect

def interp(x, xys):
	j = bisect.bisect(xys, (x,))
	if j == 0: return xys[0][1]
	if j >= len(xys): return xys[-1][1]
	return math.fadebetween(x, *xys[j-1], *xys[j])


def clearpoly(poly):
	poly1 = []
	seen = set()
	for p in poly:
		if p in seen:
			continue
		seen.add(p)
		poly1.append(p)
	return poly1

def traversepoly(poly):
	for j in range(len(poly)):
		yield poly[j], poly[(j + 1) % len(poly)]

def polycontains(poly, p):
	poly = clearpoly(poly)
	if len(poly) < 3:
		return False
	contains = False
	x, y = p
	for (x0, y0), (x1, y1) in traversepoly(poly):
		if y0 <= y < y1 or y0 >= y > y1:
			xc = math.fadebetween(y, y0, x0, y1, x1)
			if xc > x:
				contains = not contains
	return contains


