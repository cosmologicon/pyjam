import pygame, math
from . import pview, view, geometry, graphics


class You:
	def __init__(self, pos, r = 1, color = None):
		self.x, self.y = pos
		self.r = r
		self.speed = 6
		self.color = color or (100, 50, 50)
		self.A = 0
		self.Astepping = None
		self.twalk = 0
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
		you.A = math.tau - self.A + 2 * geometry.Ato(p1, p2)
		you.twalk = self.twalk
		return you
	def draw(self, surf = None):
		surf = surf or pview.screen
#		pos = view.screenpos((self.x, self.y))
#		r = view.screenscale(self.r)
#		pygame.draw.circle(surf, self.color, pos, r)
		scale = 0.06
		frame = int(round(self.twalk * self.speed * 1.8)) % 8
		A = -math.tau / 4 + self.A
		graphics.drawimgw(f"oldman-{frame}", (self.x, self.y), A, scale, surf)


class Room:
	def __init__(self, poly, color = None, mirrors = None):
		self.poly = [(a, b) for a, b in poly]
		self.color = color or (40, 40, 50)
		self.mirrors = (mirrors or [])[:]
	def getwall(self, jwall):
		return self.poly[jwall], self.poly[(jwall + 1) % len(self.poly)]
	def nwall(self):
		return len(self.poly)
	def addmirror(self, jwall, f, w):
		self.mirrors.append((jwall, f, w))
	def within(self, obj):
		return geometry.polywithin(self.poly, (obj.x, obj.y), obj.r)
	def wallpart(self, jwall, f, w):
		p1, p2 = self.getwall(jwall)
		d = math.distance(p1, p2)
		q1 = math.mix(p1, p2, f - w / (2 * d))
		q2 = math.mix(p1, p2, f + w / (2 * d))
		return q1, q2
	def Asetthrough(self, plook, jwall):
		ret = geometry.Aintervalset()
		for kwall, f, w in self.mirrors:
			if kwall == jwall:
				p1, p2 = self.wallpart(kwall, f, w)
				ret.add(geometry.Ainterval.through(plook, p1, p2))
		return ret
	def reflect(self, jwall, shader = None):
		p1, p2 = self.getwall(jwall)
		poly = geometry.polyreflect(p1, p2, self.poly)
		color = self.color
		if shader is not None:
			color = shader.shade(color)
		return Room(poly, color, self.mirrors)
	def draw(self, surf = None):
		surf = surf or pview.screen
		ps = [view.screenpos(p) for p in self.poly]
		pygame.draw.polygon(surf, self.color, ps)
		for jwall, f, w in self.mirrors:
			ps = [view.screenpos(p) for p in self.wallpart(jwall, f, w)]
			pygame.draw.line(surf, (200, 200, 255), *ps, view.screenscale(0.2))
			


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




