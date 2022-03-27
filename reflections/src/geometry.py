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


def psegdistf(p1, p2, p):
	v = vecsub(p2, p1)
	w = vecsub(p, p1)
	a = math.dot(w, v) / math.length(v)
	if a <= 0:
		return math.distance(p1, p), 0
	if a >= math.length(v):
		return math.distance(p2, p), 1
	return math.sqrt(math.length(w) ** 2 - a ** 2), a / math.length(v)


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

# https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
def segscrossat(p0, p1, p2, p3):
	s1x, s1y = vecsub(p1, p0)
	s2x, s2y = vecsub(p3, p2)
	d0x, d0y = vecsub(p0, p2)
	s = (-s1y * d0x + s1x * d0y) / (-s2x * s1y + s1x * s2y)
	t = (s2x * d0y - s2y * d0x) / (-s2x * s1y + s1x * s2y)
	assert 0 <= s <= 1 and 0 <= t <= 1
	return vecadd(p0, (t * s1x, t * s1y))


# https://stackoverflow.com/questions/1165647/how-to-determine-if-a-list-of-polygon-points-are-in-clockwise-order
def polycarea(poly):
	return sum((x2 - x1) * (y2 + y1) for (x1, y1), (x2, y2) in rotpoly(poly))
def polyclockwise(poly):
	return polycarea(poly) > 0

def withinrect(x, y, w, h):
	return 0 <= x <= w and 0 <= y <= h

# All points of intersection between the segment between (x1, y1) and (x2, y2), and the bundary of
# the rectangle (0, 0, w, h).
def crossrect(x1, y1, x2, y2, w, h):
	ps = []
	if (x1 < 0) != (x2 < 0):
		y = int(round(math.interp(0, x1, y1, x2, y2)))
		if 0 <= y <= h:
			ps.append((0, y))
	if (x1 > w) != (x2 > w):
		y = int(round(math.interp(w, x1, y1, x2, y2)))
		if 0 <= y <= h:
			ps.append((w, y))
	if (y1 < 0) != (y2 < 0):
		x = int(round(math.interp(0, y1, x1, y2, x2)))
		if 0 <= x <= w:
			ps.append((x, 0))
	if (y1 > h) != (y2 > h):
		x = int(round(math.interp(h, y1, x1, y2, x2)))
		if 0 <= x <= w:
			ps.append((x, h))
	ps.sort(key = lambda p: math.distance(p, (x1, y1)))
	return ps


# Return a polygon that's the intersection of the given polygon and the given rectangle.
def restrictpoly(poly, rect):
	if not polyclockwise(poly):
		poly = poly[::-1]
	w, h = rect
	ps = []
	allwithin = True
	for p1, p2 in rotpoly(poly):
		if withinrect(*p1, *rect):
			ps.append(p1)
		else:
			allwithin = False
		ps.extend(crossrect(*p1, *p2, *rect))
	if allwithin:
		return poly
	outline = [(0, 0), (0, h), (w, h), (w, 0)]
	if not ps:
		# Encloses entire rect
		if winding(poly, (w/2, h/2)):
			return outline
		else:
			return []
	# Every rectangle corner that's within the polygon must also be added, but it's really hard to
	# figure out the right order for it.
	for corner in outline:
		if winding(poly, corner):
			aps = [ps[:j] + [corner] + ps[j:] for j in range(len(ps))]
			ps = max(aps, key = polycarea)
	return ps



def viewfield(p0, p1, p2, r = 1000):
	yield p0
	for p in (p1, p2):
		d = math.norm(vecsub(p, p0), r)
		yield vecadd(p0, d)

# The segment of length r on the segment (p1, p2) that is closest to p.
def nearestsubseg(p, p1, p2, r):
	v = vecsub(p2, p1)
	d = math.length(v)
	if d < r:
		return None
	w = vecsub(p, p1)
	a = math.clamp(math.dot(w, v) / d, r / 2, d - r / 2)
	q1 = math.mix(p1, p2, (a - r / 2) / d)
	q2 = math.mix(p1, p2, (a + r / 2) / d)
	return q1, q2

def Ato(p0, p1):
	x, y = vecsub(p1, p0)
	return math.atan2(y, x)

def Areflect(p1, p2, A):
	return math.tau - A + 2 * Ato(p1, p2)

class Ainterval:
	def __init__(self, A0, A1):
		self.A0 = A0
		self.A1 = A0 + math.dA(A1 - A0)
		assert self.A1 >= self.A0
	@classmethod
	def through(cls, plook, p1, p2):
		A0 = Ato(plook, p1)
		A1 = Ato(plook, p2)
		if math.dA(A1 - A0) < 0:
			A0, A1 = A1, A0
		return cls(A0, A1)
	def __repr__(self):
		return f"[{round(self.A0, 4)}, {round(self.A1, 4)}]"
	def contains(self, A):
		return 0 <= math.dA(A - self.A0) <= self.A1 - self.A0
	def overlaps(self, other):
		if math.dA(other.A0 - self.A0) >= 0:
			return math.dA(self.A1 - other.A0) >= 0
		else:
			return math.dA(other.A1 - self.A0) >= 0
	def union(self, other):
		assert self.overlaps(other)
		A0min = self.A0 if math.dA(other.A0 - self.A0) >= 0 else other.A0
		A1max = self.A1 if math.dA(other.A1 - self.A1) < 0 else other.A1
		return Ainterval(A0min, A1max)
	def intersection(self, other):
		assert self.overlaps(other)
		A0max = other.A0 if math.dA(other.A0 - self.A0) >= 0 else self.A0
		A1min = other.A1 if math.dA(other.A1 - self.A1) < 0 else self.A1
		return Ainterval(A0max, A1min)
	def subtract(self, other):
		if not self.overlaps(other):
			return [self]
		startswithin = math.dA(other.A0 - self.A0) > 0
		endswithin = math.dA(self.A1 - other.A1) > 0
		ret = []
		if startswithin:
			ret.append(Ainterval(self.A0, other.A0))
		if endswithin:
			ret.append(Ainterval(other.A1, self.A1))
		return ret


class Aintervalset:
	def __init__(self):
		self.intervals = []
	def empty(self):
		return not self.intervals
	def contains(self, A):
		return any(a.contains(A) for a in self.intervals)
	def __repr__(self):
		return " ".join(repr(a) for a in self.intervals)
	def add(self, interval):
		overlaps = [a for a in self.intervals if interval.overlaps(a)]
		self.intervals = [a for a in self.intervals if not interval.overlaps(a)]
		for a in overlaps:
			interval = interval.union(a)
		self.intervals.append(interval)
	def subtract(self, interval):
		self.intervals = [b for a in self.intervals for b in a.subtract(interval)]
	def intersection(self, other):
		ret = Aintervalset()
		for a in self.intervals:
			for b in other.intervals:
				if a.overlaps(b):
					ret.add(a.intersection(b))
		return ret

if __name__ == "__main__":
	from . import maff
	print(preflect((0, -10), (0, 10), (-6, 0)))
	ai = Aintervalset()
	ai.add(Ainterval(3, -3))
	ai.add(Ainterval(-4.4, 2))
	ai.subtract(Ainterval(1.9, 3.1))
	print(ai)

	import random, pygame
	from . import pview, ptext
	pview.set_mode((900, 600))
	rect = pygame.Rect(300, 200, 300, 200)
	redo = True
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
			elif event.type == pygame.KEYDOWN:
				redo = True
		if redo:
			rpoint = lambda: (random.randint(-100, 400), random.randint(-100, 300))
			ps = [rpoint() for _ in range(random.choice((3, 4)))]
			rps = restrictpoly(ps, rect.size)
			print(ps)
			print(rps)
			print()
			redo = False
		pview.fill((0, 0, 0, 255))
		pygame.draw.rect(pview.screen, (0, 200, 0), rect)
		pygame.draw.polygon(pview.screen, (200, 0, 0), [(x+300,y+200) for x,y in ps])
		if len(rps) > 2:
			pygame.draw.polygon(pview.screen, (200, 200, 0), [(x+300,y+200) for x,y in rps])
		for j, (x, y) in enumerate(ps):
			ptext.draw(str(j), center = (x+310, y+200), fontsize=16, owidth=1, color=(255,100,100))
		for j, (x, y) in enumerate(rps):
			ptext.draw(str(j), center = (x+290, y+200), fontsize=16, owidth=1, color=(255,255,100))
		pygame.display.flip()

#	p1, p2, q2, q2 = (560, 726), (401, 726), (-6788, 18696), (-2004, 19951)
#	outline = [(0, 0), (0, 730), (w, h), (w, 0)]


