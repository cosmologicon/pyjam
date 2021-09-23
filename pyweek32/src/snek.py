import pygame, math
from . import state, view, geometry, pview, settings, graphics
from .pview import T

class You:
	r = 0.3
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

	def lengthen(self):
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
		d0, (x0, y0), theta = self.ps[-1]

		if self.chompin:
			self.fspeed = math.approach(self.fspeed, 5, dt)
		else:
			self.fspeed = math.approach(self.fspeed, 1, 4 * dt)
		self.fspeed = 1

		step = dt * self.speed * self.fspeed
		self.d += step

				
		if self.chompin:
			self.tchomp += dt
			self.pos, self.theta = geometry.interp(self.d - self.length, self.ps)
#			p0 = self.ps[0][1]
#			dy, dx = math.CS(self.theta, step)
#			self.pos = math.mix((x0 + dx, y0 + dy), p0, math.clamp(self.tchomp * 0.5, 0, 1))
#			x1, y1 = self.pos
#			self.theta = math.atan2(x1 - x0, y1 - y0)
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
		a, k = 0, 0
		while a < self.length:
#			size = 0.5 if k == 0 else max(0.3 * 0.98 ** k, 0.2)
			size = 0.5 if k == 0 else 0.3
			a += size
			pos, theta = geometry.interp(self.d - a, self.ps)
#			color = [(120, 255, 120), (255, 255, 0)][k % 2]
#			color = math.imix(color, (120, 255, 120), k / 120)
#			pygame.draw.circle(pview.screen, color, pos, T(view.scale * size))
			segments.append((pos, theta))
			k += 1
			a += size
		for pos, angle in reversed(segments):
			graphics.drawimg(pos, "segment", self.r, angle - math.tau / 4)
		graphics.drawimg(self.pos, "head", self.r, self.theta - math.tau / 4)


