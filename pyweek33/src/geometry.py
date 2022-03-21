import math

def vecadd(v1, v2):
	x1, y1 = v1
	x2, y2 = v2
	return x1 + x2, y1 + y2

# The vector v1 - v2
def vecsub(v1, v2):
	x1, y1 = v1
	x2, y2 = v2
	return x1 - x2, y1 - y2


def cross2(p0, p1):
	x0, y0 = p0
	x1, y1 = p1
	return x0 * y1 - x1 * y0

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
	v = vecsub(p2, p1)
	w = vecsub(p, p1)
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


# The point p reflected across the segment between p1 and p2
def preflect(p1, p2, p):
	x2, y2 = vecsub(p2, p1)
	x, y = vecsub(p, p1)
	A = x * x2 + y * y2
	B = x * y2 - y * x2
	D = x2 ** 2 + y2 ** 2
	xr = (x2 * A - y2 * B) / D
	yr = (y2 * A + x2 * B) / D
	x1, y1 = p1
	return xr + x1, yr + y1

def polyreflect(p1, p2, poly):
	return [preflect(p1, p2, p) for p in poly]


# Are p2 and p3 on different sides of the line through p0 and p1?
def diffsides(p0, p1, p2, p3):
	v = vecsub(p1, p0)
	w2 = vecsub(p2, p0)
	w3 = vecsub(p3, p0)
	return cross2(v, w2) * cross2(v, w3) < 0

# Does the segment from p0 to p1 intersect the segment from p2 to p3?
def segscross(p0, p1, p2, p3):
	return diffsides(p0, p1, p2, p3) and diffsides(p2, p3, p0, p1)


def viewfield(p0, p1, p2, r = 1000):
	yield p0
	for p in (p1, p2):
		d = math.norm(vecsub(p, p0), r)
		yield vecadd(p0, d)

if __name__ == "__main__":
	print(preflect((0, -10), (0, 10), (-6, 0)))

