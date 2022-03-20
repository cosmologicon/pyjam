import math

def rotpoly(poly):
	for i in range(len(poly)):
		yield poly[i], poly[(i + 1) % len(poly)]


def winding(poly, p):
	x0, y0 = p
	wind = 0
	for (x1, y1), (x2, y2) in rotpoly(poly):
		if (y1 <= y0) != (y2 <= y0):
			x = (x1 * (y2 - y0) - x2 * (y1 - y0)) / (y2 - y1)
			if x > x0:
				wind += 1
	return wind % 2 == 1

def psegdist(p1, p2, p):
	x1, y1 = p1
	x2, y2 = p2
	x, y = p
	v = x2 - x1, y2 - y1
	w = x - x1, y - y1
	a = math.dot(w, v) / math.length(v)
	if a <= 0:
		return math.distance(p1, p)
	if a >= math.length(v):
		return math.distance(p2, p)
	return math.sqrt(math.length(w) ** 2 - a ** 2)
	
def polywithin(poly, p, r = 0):
	if not winding(poly, p):
		return False
	return all(psegdist(p0, p1, p) > r for p0, p1 in rotpoly(poly))
		
	

