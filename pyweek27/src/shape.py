import pygame, math, inspect, json
from . import render, enco

C15, S15 = math.CS(math.radians(15))
C30, S30 = math.CS(math.radians(30))

def ptoline(p, n):
	pproj = math.dot(p, n)
	nx, ny = n
	proj = nx * pproj, ny * pproj
	return proj, math.distance(proj, p)

def scatter(ps):
	sps = [ps] + [tuple(render.R1(p) for p in ps)] + [tuple(render.R2(p) for p in ps)]
	sps = sps + [((x0, -y0), (x1, -y1)) for ((x0, y0), (x1, y1)) in sps]	
	sps = sps + [((-x0, y0), (-x1, y1)) for ((x0, y0), (x1, y1)) in sps]	
	return sps

def polygoncontains(poly, pos):
	x, y = pos
	ncross = 0
	for j in range(len(poly)):
		x0, y0 = poly[j]
		x1, y1 = poly[(j + 1) % len(poly)]
		if (y0 < y) != (y1 < y):
			if y0 < y1:
				(x0, y0), (x1, y1) = (x1, y1), (x0, y0)
			xa = math.fadebetween(y, y0, x0, y1, x1)
			if xa < x:
				ncross += 1
	return ncross % 2 == 1				


class Shape(enco.Component):
	def getspec(self):
		args = inspect.getargspec(self.__init__).args
		kw = { arg: getattr(self, arg) for arg in args if arg not in ["self"] }
		for arg in kw:
			if "color" in arg:
				kw[arg] = "#%02x%02x%02x%02x" % tuple(kw[arg])
		kw["type"] = self.__class__.__name__
		return json.loads(json.dumps(kw))

	def copy(self):
		spec = self.getspec()
		del spec["type"]
		return self.__class__(**spec)

	def constrainanchor(self, j, pos):
		self.anchors[j] = self.constrain(pos, j)
		if len(self.anchors) == 1:
			self.pos = self.anchors[0]
		else:
			raise ValueError

	def drawoutline0(self, Fspot):
		for p0, p1 in self.outlinesegs():
			ps = render.cull(p0, p1)
			if not ps:
				continue
			render.drawlinesF(Fspot, ps, self.color)
	def drawoutline(self, Fspot):
		for p0, p1 in self.outlinesegs():
			ps = render.cull(p0, p1)
			if not ps:
				continue
			for sps in scatter(ps):
				render.drawlinesF(Fspot, sps, self.color)

	def colorat(self, pos):
		return self.color if self.contains(pos) else None

	# Considered the same independent of position.
	def same(self, other):
		spec = self.getspec()
		otherspec = other.getspec()
		if set(spec) != set(otherspec):
			return False
		for k, v in spec.items():
			if k in ["pos"]:
				continue
			if v != otherspec[k]:
				return False
		return True

# polygon(f = 1)
class Polygonal(enco.Component):
	def outlinesegs(self):
		p = self.polygon()
		n = len(p)
		return [(p[j], p[(j+1)%n]) for j in range(n)]

	def contains(self, pos):
		return polygoncontains(self.polygon(), pos)

	def sectordraw(self, simgs):
#		for f, d in [(1, 0), (0.8, 0.5), (0.65, 1), (0.5, 1.5)]:
#		for f, d in [(1, 1.5), (0.8, 1), (0.65, 0.5), (0.5, 0)]:
		for f, d in [(1, 3), (0.8, 2), (0.65, 1), (0.5, 0)]:
			render.sectorpoly(simgs, self.polygon(f), render.dim(self.color, d))

	def cursorimg(self, s):
		img = pygame.Surface((s, 2 * s)).convert_alpha()
		img.fill((0, 0, 0, 0))
		self.sectordraw([img])
		oimg = pygame.Surface((2 * s, 2 * s)).convert_alpha()
		oimg.fill((0, 0, 0, 0))
		oimg.blit(pygame.transform.flip(img, True, False), (0, 0))
		oimg.blit(img, (s, 0))
		return oimg

@Shape()
@Polygonal()
class Shard(Shape):
	def __init__(self, pos, color, size):
		self.color = pygame.Color(color)
		self.size = size
		self.pos = self.constrain(pos, 0)
		self.anchors = [self.pos]

	def constrain(self, pos, j):
		if pos[1] < 0.0001:
			pos = pos[0], 0.0001
		if pos[0] < 0:
			pos = 0, pos[1]
		if math.dot(pos, (C30, -S30)) > 0:
			pos, _ = ptoline(pos, (S30, C30))
		a = math.length(pos)
		w, h = self.size
		if a > 1 - h:
			pos = math.norm(pos, 1 - h)
		return pos

	def polygon(self, f = 1):
		sx, sy = self.anchors[0]
		sw, sh = self.size
		S, C = math.norm((sx, sy), f)
		return [
			(sx + S * sh, sy + C * sh),
			(sx + C * sw, sy - S * sw),
			(sx - S * sh, sy - C * sh),
			(sx - C * sw, sy + S * sw),
		]

@Shape()
@Polygonal()
class Blade:
	def __init__(self, pos, color, size):
		self.color = pygame.Color(color)
		self.size = size
		self.pos = self.constrain(pos, 0)
		self.anchors = [self.pos]

	def constrain(self, pos, j):
		if pos[1] < 0.0001:
			pos = pos[0], 0.0001
		if pos[0] < 0:
			pos = 0, pos[1]
		if math.dot(pos, (C30, -S30)) > 0:
			pos, _ = ptoline(pos, (S30, C30))
		a = math.length(pos)
		w, h = self.size
		if a > 1 - h:
			pos = math.norm(pos, 1 - h)
		return pos

	def polygon(self, f = 1):
		sx, sy = self.anchors[0]
		sw, sh = self.size
		S, C = math.norm((sx, sy), f)
		return [
			(sx + S * sh, sy + C * sh),
			(sx + C * sw, sy - S * sw),
			(C * sw, -S * sw),
			(-C * sw, S * sw),
			(sx - C * sw, sy + S * sw),
		]

@Shape()
@Polygonal()
class Bar:
	def __init__(self, pos, color, width):
		self.color = pygame.Color(color)
		self.width = width
		self.pos = self.constrain(pos, 0)
		self.anchors = [self.pos]

	def constrain(self, pos, j):
		a = math.clamp(math.dot(pos, (S15, C15)), self.width, (1 - self.width / C15) * C15)
		return a * S15, a * C15

	def polygon(self, f = 1):
		s = math.length(self.anchors[0])
		w = self.width * f
		return [
			((s + w) * S15 - C15, (s + w) * C15 + S15),
			((s + w) * S15 + C15, (s + w) * C15 - S15),
			((s - w) * S15 + C15, (s - w) * C15 - S15),
			((s - w) * S15 - C15, (s - w) * C15 + S15),
		]

@Shape()
@Polygonal()
class Ring:
	def __init__(self, pos, color, width):
		self.color = pygame.Color(color)
		self.width = width
		self.pos = self.constrain(pos, 0)
		self.anchors = [self.pos]

	def constrain(self, pos, j):
		a = math.clamp(math.dot(pos, (S15, C15)), self.width, 1 - self.width)
		return a * S15, a * C15

	def polygon(self, f = 1):
		s = math.length(self.anchors[0])
		CSs = [math.CS(math.radians(theta)) for theta in range(-1, 35, 3)]
		w = self.width * f
		return [((s + w) * S, (s + w) * C) for C, S in CSs] + [((s - w) * S, (s - w) * C) for C, S in reversed(CSs)]

	def contains(self, pos):
		s = math.length(self.anchors[0])
		d = math.length(pos)
		return abs(s - d) < self.width

def fromspec(spec):
	cls = globals()[spec["type"]]
	del spec["type"]
	return cls(**spec)

