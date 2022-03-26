import pygame, math
from . import pview, view, geometry, graphics, ptext


class You:
	def __init__(self, pos, r = 1, color = None):
		self.x, self.y = pos
		self.r = r
		self.speed = 6
		self.color = color or (100, 50, 50)
		self.A = 0
		self.Astepping = None
		self.twalk = 0
		self.flipped = False
	def move(self, dx, dy, room):
		if dx or dy:
			A = geometry.Ato((0, 0), (dx, dy))
			dt = math.length((dx, dy))
			self.A = math.approachA(self.A, A, 5 * dt)
			self.twalk += dt
		else:
			self.twalk = 0
		p0 = self.x, self.y
		self.x += dx * self.speed
		self.y += dy * self.speed
		if not room.within(self):
			self.x, self.y = p0
	def reflect(self, p1, p2):
		pos = geometry.preflect(p1, p2, (self.x, self.y))
		you = You(pos, self.r)
		you.A = geometry.Areflect(p1, p2, self.A)
		you.twalk = self.twalk
		you.flipped = not self.flipped
		return you
	def draw(self, surf = None):
		surf = surf or pview.screen
#		pos = view.screenpos((self.x, self.y))
#		r = view.screenscale(self.r)
#		pygame.draw.circle(surf, self.color, pos, r)
		scale = 0.06 * self.r
		frame = int(round(self.twalk * self.speed * 1.8)) % 8
		A = -math.tau / 4 + self.A
		graphics.drawimgw(f"oldman-{frame}", (self.x, self.y), A, scale, self.flipped, surf)

class Plate:
	def __init__(self, jplate, pos, n, r = 1, color = None):
		self.jplate = jplate
		self.x, self.y = pos
		self.n = n
		self.r = r
		self.color = color or (100, 100, 100)
		self.A = 0
		self.flipped = False
	def reflect(self, p1, p2):
		pos = geometry.preflect(p1, p2, (self.x, self.y))
		plate = Plate(self.jplate, pos, self.n, self.r)
		plate.A = geometry.Areflect(p1, p2, self.A) + math.tau / 2
		plate.flipped = not self.flipped
		return plate
	def draw(self, surf = None):
		surf = surf or pview.screen
		scale = 0.01 * self.r
		graphics.drawimgw(f"plate-{self.n}", (self.x, self.y), self.A, scale, self.flipped, surf)


class Looker:
	def __init__(self, pos, r = 1):
		self.x, self.y = pos
		self.r = r
		self.color = 80, 80, 80
		self.A = 0
	def draw(self, surf = None):
		surf = surf or pview.screen
		scale = 0.03 * self.r
		flipped = False
		graphics.drawimgw("gargoyle", (self.x, self.y), self.A, scale, flipped, surf)




class Room:
	def __init__(self, poly, color = None, mirrors = None):
		self.poly = [(a, b) for a, b in poly]
		self.color = color or (40, 40, 50)
		self.mirrors = (mirrors or [])[:]
	def getwall(self, jwall):
		return self.poly[jwall], self.poly[(jwall + 1) % len(self.poly)]
	def walllength(self, jwall):
		return math.distance(*self.getwall(jwall))
	def nwall(self):
		return len(self.poly)
	def addmirror(self, jwall, f, w):
		self.mirrors.append((jwall, f, w))
	def mirrorwithin(self, p, d):
		dmin = d
		ret = None
		for jmirror in range(len(self.mirrors)):
			dmirror = self.mirrordistance(p, jmirror)
			if dmirror < dmin:
				dmin = dmirror
				ret = jmirror
		return ret
	def popmirror(self, jmirror):
		jwall, f, w = self.mirrors.pop(jmirror)
		return w
	def freesegments(self):
		for jwall in range(self.nwall()):
			fs = [(0, 1)]
			d = self.walllength(jwall)
			for kwall, f, w in self.mirrors:
				if kwall != jwall: continue
				f1, f2 = f - w / (2 * d), f + w / (2 * d)
				f0, f3 = fs.pop(-1)
				fs.append((f0, f1))
				fs.append((f2, f3))
			for f0, f1 in fs:
				yield jwall, d, f0, f1, 
	def spotwithin(self, p, w, d):
		dmin = d
		ret = None
		for jwall, dwall, f0, f1 in self.freesegments():
			g0 = f0 + w / (2 * dwall)
			g1 = f1 - w / (2 * dwall)
			if g0 > g1:
				continue
			p0, p1 = self.getwall(jwall)
			q0 = math.mix(p0, p1, g0)
			q1 = math.mix(p0, p1, g1)
			dist, fsub = geometry.psegdistf(q0, q1, p)
			if dist < d:
				f = math.mix(g0, g1, fsub)
				ret = jwall, f, w
				dmin = dist
		return ret, dmin
	def mirrordistance(self, p, jmirror):
		p1, p2 = self.wallpart(*self.mirrors[jmirror])
		return geometry.psegdist(p1, p2, p)
	def within(self, obj):
		return geometry.polywithin(self.poly, (obj.x, obj.y), obj.r)
	def wallpart(self, jwall, f, w):
		p1, p2 = self.getwall(jwall)
		d = math.distance(p1, p2)
		q1 = math.mix(p1, p2, f - w / (2 * d))
		q2 = math.mix(p1, p2, f + w / (2 * d))
		return q1, q2
	def Asetthrough(self, plook, jwall, lastjwall):
		ret = geometry.Aintervalset()
		for kwall, f, w in self.mirrors:
			if kwall == jwall:
				p1, p2 = self.wallpart(kwall, f, w)
				ret.add(geometry.Ainterval.through(plook, p1, p2))
		for kwall in range(self.nwall()):
			if kwall != jwall and kwall != lastjwall:
				p1, p2 = self.getwall(kwall)
				ret.subtract(geometry.Ainterval.through(plook, p1, p2))
		return ret
	def reflect(self, jwall, shader = None):
		p1, p2 = self.getwall(jwall)
		poly = geometry.polyreflect(p1, p2, self.poly)
		color = self.color
		if shader is not None:
			color = shader.shade(color)
		return Room(poly, color, self.mirrors)
	def draw(self, cmirror = None, surf = None):
		surf = surf or pview.screen
		ps = [view.screenpos(p) for p in self.poly]
		pygame.draw.polygon(surf, self.color, ps)
		for jmirror, (jwall, f, w) in enumerate(self.mirrors):
			ps = [view.screenpos(p) for p in self.wallpart(jwall, f, w)]
			color = (200, 200, 255)
			if jmirror == cmirror:
				color = math.imix(color, (255, 255, 255), 0.4)
			pygame.draw.line(surf, color, *ps, view.screenscale(0.2))



class Mirror:
	def __init__(self, room, jwall):
		self.p1 = p1
		self.p2 = p2
		self.color = (200, 200, 255)
	def shade(self, color):
		return math.imix(color, self.color, 0.1)
	def draw(self):
		p1 = view.screenpos(self.p1)
		p2 = view.screenpos(self.p2)
		w = view.screenscale(0.2)
		pygame.draw.line(pview.screen, self.color, p1, p2, w)




