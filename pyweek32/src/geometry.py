import math, bisect

def vecsub(v0, v1):
	x0, y0 = v0
	x1, y1 = v1
	return x0 - x1, y0 - y1

def interp(x, xyzs):
	j = bisect.bisect(xyzs, (x,))
	if j == 0: return xyzs[0][1], xyzs[0][2]
	if j >= len(xyzs): return xyzs[-1][1], xyzs[-1][2]
	x0, y0, z0 = xyzs[j-1]
	x1, y1, z1 = xyzs[j]
	return math.fadebetween(x, x0, y0, x1, y1), math.anglefadebetween(x, x0, z0, x1, z1)


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

# Simple algorithm to get winding number about a point p. Works with convex polygons. Will fail if
# p is along any polygon side, or it shares an x or y coordinate with any point. 
def polywind(poly, p):
	if len(poly) < 3:
		return 0
	wind = 0
	x, y = p
	for (x0, y0), (x1, y1) in traversepoly(poly):
		yf = (y0 <= y < y1) - (y0 >= y > y1)
		if yf != 0:
			xf = math.sign(math.fadebetween(y, y0, x0, y1, x1) - x)
			wind += yf * xf
	assert wind % 2 == 0
	return int(wind // 2)


def collides(obj0, obj1):
	return math.distance(obj0.pos, obj1.pos) < obj0.r + obj1.r

def dtoline(p, p0, p1):
	d = vecsub(p, p0)
	d1 = vecsub(p1, p0)
	a = math.dot(d, math.norm(d1))
	if a <= 0: return math.distance(p, p0)
	if a >= math.length(d1): return math.distance(p, p1)
	return math.sqrt(math.length(d) ** 2 - a ** 2)


