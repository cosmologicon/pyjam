import math, bisect

def vecsub(v0, v1):
	x0, y0 = v0
	x1, y1 = v1
	return x0 - x1, y0 - y1

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


def collides(obj0, obj1):
	return math.distance(obj0.pos, obj1.pos) < obj0.r + obj1.r

def dtoline(p, p0, p1):
	d = vecsub(p, p0)
	d1 = vecsub(p1, p0)
	a = math.dot(d, math.norm(d1))
	if a <= 0: return math.distance(p, p0)
	if a >= math.length(d1): return math.distance(p, p1)
	return math.sqrt(math.length(d) ** 2 - a ** 2)


