import pygame, math
from . import state, view, geometry, pview, settings, graphics
from .pview import T

class You:
	r = 0.01
	def __init__(self, pos):
		self.t = 0
		self.d = 0
		self.pos = pos
		self.theta = 0  # 0 = north, tau/4 = east
		self.ps = [(self.d, self.pos, self.theta)]
		self.chompin = False
		self.tchomp = 0
		self.speed = 4
		self.dspeed = 0.4
		self.fspeed = 1
		self.length = 10
		self.dlength = 5
		self.alive = True
		self.wound = []
		self.aaah = 0
		self.aaahtarget = 0
		self.menu = False

	def lengthen(self):
		state.effects.append(ShedSkin(self))
		self.length += self.dlength
		self.speed += self.dspeed

	def blockps(self):
		ps = [(self.pos, 4)]
		p0 = self.pos
		for d, p, theta in self.ps:
			if d < self.d - self.length:
				break
			if math.distance(self.pos, p) > 0.5:
				ps.append((p, 1))
				p0 = p
		return ps


	def canchomp(self):
		for j, (d0, p0, theta0) in enumerate(self.ps):
			if d0 > self.d - self.length + 0.5:
				return False
			if j >= len(self.ps) - 1:
				return False
			d1, p1, theta1 = self.ps[j + 1]
			if math.distance(p0, p1) == 0:
				continue
			if math.distance(p0, self.pos) > 1:
				continue
			(x0, y0), (x1, y1) = p0, p1
			if math.dot(math.CS(self.theta), math.norm((y1 - y0, x1 - x0))) > 0.2:
				return True
		
	
	def chomp(self):
		self.chompin = True
		self.dchomp = self.d
		self.chomppoly = [p for d, p, theta in self.ps]
		state.setactive(self.chomppoly)
		xs, ys = zip(*self.chomppoly)
		xmin, xmax = min(xs), max(xs)
		ymin, ymax = min(ys), max(ys)
		self.vtarget = (xmax + xmin) / 2, (ymax + ymin) / 2
		self.starget = min(1280 / (4 + xmax - xmin), 720 / (4 + ymax - ymin))

	def unchomp(self):
		if self.chompin and self.tchomp > 1:
			state.activate()
			self.chompin = False
			self.tchomp = -1
			self.wound = []

	def think(self, dt, dkx, dky):
		self.t += dt
		d0, (x0, y0), theta = self.ps[-1]

		if self.chompin:
			self.fspeed = math.approach(self.fspeed, 5, dt)
		else:
			self.fspeed = math.approach(self.fspeed, 1, 4 * dt)
		self.fspeed = 1

		self.aaahtarget = 1 if self.canchomp() and self.tchomp == 0 else 0
		if self.chompin:
			self.aaahtarget = 0.5
		self.aaah = math.approach(self.aaah, self.aaahtarget, 2 * dt)

		step = dt * self.speed * self.fspeed
		self.d += step

				
		if self.chompin:
			self.tchomp += dt
			self.pos, _ = geometry.interp(self.d - self.length, self.ps)
			x0, y0 = self.pos
			(x1, y1), _ = geometry.interp(self.d - self.length + 1, self.ps)
			self.theta = math.atan2(x1 - x0, y1 - y0)
		else:
			if settings.directcontrol:
				if dkx or dky:
					target = math.atan2(dkx, dky)
					self.theta = math.angleapproach(self.theta, target, 0.9 * self.speed * dt)
			else:
				omega = { -1: 1.2, 0: 0.6, 1: 0.3 }[dky] * self.speed
				self.theta += omega * dt * dkx % math.tau
			dy, dx = math.CS(self.theta, step)
			self.pos = x0 + dx, y0 + dy

		self.ps.append((self.d, self.pos, self.theta))
		while len(self.ps) > 1 and self.ps[1][0] <= self.d - self.length:
			self.ps.pop(0)

		if self.chompin and self.tchomp < 5:
			ft = math.fadebetween(self.tchomp, 0, 1, 5, 0)
			ps = self.ps[:]
			for j in range(1, len(self.ps) - 1):
				d, p, theta = ps[j]
				fd = math.fadebetween(abs(d - self.dchomp), 0, 1, 6, 0)
				if fd <= 0: continue
				_, (x0, y0), theta0 = ps[j-1]
				_, (x1, y1), theta1 = ps[j+1]
				pc = (x0 + x1) / 2, (y0 + y1) / 2
				p = math.softapproach(p, pc, 500 * dt * ft * fd, dymin = 0.001)
				theta = math.atan2(x1 - x0, y1 - y0)
				self.ps[j] = d, p, theta

		if not self.chompin:
			if self.canchomp():
				if settings.autochomp and self.tchomp == 0:
					self.chomp()
			else:
				if self.tchomp < 0:
					self.tchomp = min(self.tchomp + dt, 0)


	def draw(self):
		segments = []
		a, k, size = -0.25, 0, 0.25
		while a < self.length:
#			size = 0.5 if k == 0 else max(0.3 * 0.98 ** k, 0.2)
			a += size
			pos, theta = geometry.interp(self.d - a, self.ps)
			size = max(size * 0.997, 0.15)
			segments.append((pos, theta, size))
			k += 1
			a += size
		imgname = "segment-menu" if self.menu else "segment"
		for pos, angle, size in reversed(segments):
			graphics.drawimg(pos, imgname, size, angle - math.tau / 4)
		theta = self.theta - math.tau / 4
		pos = math.CS(-self.theta, 0.3, center = self.pos)
		A = math.fadebetween(self.aaah, 1, 0, 0, 0.2)
		if self.chompin:
			A = 0
		theta += math.mix(-A, A, math.cycle(0.5 * self.t) ** 2)
		graphics.drawimg(pos, "head-bottom", 0.3, theta + 0.3 * self.aaah)
		graphics.drawimg(pos, "head-top", 0.3, theta - 0.9 * self.aaah)


class ShedSkin:
	def __init__(self, you):
		self.you = you
		self.t = 0
		self.a = 0
		self.amax = you.length
		self.L = 20

	def think(self, dt):
		self.t += dt
		self.a += 20 * dt
		self.alive = self.a - self.L < self.you.length
		
	def draw(self):
		segments = []
		a, k, size = 0, 0, 0.5
		while a < self.you.length:
			a += size
			size *= 0.99
			if self.a - self.L < a < self.a:
				f = math.fadebetween(a, self.a, 0, self.a - self.L, 1)
				pos, theta = geometry.interp(self.you.d - a, self.you.ps)
				segments.append((pos, theta, size, f))
			k += 1
			a += size
		for pos, angle, size, f in reversed(segments):
			s = math.mix(1, 2.5, f ** 0.5) * size
			alpha = math.mix(0.4, 0, f)
			graphics.drawimg(pos, "segment", s, angle - math.tau / 4, alpha)
		


