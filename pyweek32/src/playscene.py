import pygame, math, random
from . import view, pview, graphics, geometry
from .pview import T

class self:
	speed = 5
	length = 20
	numlinks = 48


def init():
	self.t = 0
	self.d = 0
	self.ps = [(0, (0, 0))]
	self.theta = 0  # 0 = north, tau/4 = east
	self.chompin = False
	self.tchomp = 0
	self.stars = [(random.uniform(-20, 20), random.uniform(-20, 20)) for _ in range(20)]

def think(dt, kpressed):
	self.t += dt
	
	if self.chompin and self.tchomp > 1 and kpressed[pygame.K_SPACE]:
		self.chompin = False
		self.tchomp = -1
	
	dkx = (1 if kpressed[pygame.K_RIGHT] else 0) - (1 if kpressed[pygame.K_LEFT] else 0)
	dky = (1 if kpressed[pygame.K_UP] else 0) - (1 if kpressed[pygame.K_DOWN] else 0)

	d0, (x0, y0) = self.ps[-1]
	self.d += dt * self.speed
	dy, dx = math.CS(self.theta, self.speed * dt)
			
	if self.chompin:
		self.tchomp += dt
		p0 = self.ps[0][1]
		self.p = math.mix((x0 + dx, y0 + dy), p0, math.clamp(self.tchomp * 0.5, 0, 1))
		x1, y1 = self.p
		self.theta = math.atan2(x1 - x0, y1 - y0)
	else:
		if True:
			omega = { -1: 0.3, 0: 0.6, 1: 1.2 }[dky] * self.speed
			self.theta += omega * dt * dkx % math.tau
		else:
			if dkx or dky:
				target = math.atan2(dkx, dky)
				self.theta = math.angleapproach(theta, target, 1.2 * self.speed * dt)
		self.p = x0 + dx, y0 + dy

	self.ps.append((self.d, self.p))
	while self.ps[0][0] < self.d - self.length:
		self.ps.pop(0)

	if self.chompin and self.tchomp < 5:
		ft = math.fadebetween(self.tchomp, 0, 1, 5, 0)
		ps = self.ps[:]
		for j in range(1, len(self.ps) - 1):
			d, p = ps[j]
			fd = math.fadebetween(abs(d - self.dchomp), 0, 1, 6, 0)
			if fd <= 0: continue
			_, (x0, y0) = ps[j-1]
			_, (x1, y1) = ps[j+1]
			pc = (x0 + x1) / 2, (y0 + y1) / 2
			p = math.softapproach(p, pc, 100 * dt * ft * fd, dymin = 0.001)
			self.ps[j] = d, p

	if not self.chompin:
		if canchomp():
			if self.tchomp >= 0:
				self.chompin = True
				self.dchomp = self.d
		else:
			if self.tchomp < 0:
				self.tchomp = 0

	view.x0, view.y0 = math.softapproach((view.x0, view.y0), self.p, 4 * dt, dymin=0.001)


def canchomp():
	for j, (d0, p0) in enumerate(self.ps):
		if d0 > self.d - self.length + 0.5:
			return False
		if j >= len(self.ps) - 1:
			return False
		d1, p1 = self.ps[j + 1]
		if math.distance(p0, p1) == 0:
			continue
		if math.distance(p0, self.p) > 1:
			continue
		(x0, y0), (x1, y1) = p0, p1
		if math.dot(math.CS(self.theta), math.norm((y1 - y0, x1 - x0))) > 0.2:
			return True


def draw():
#	if self.chompin:
#		pview.fill((40, 0, 0))
	graphics.drawstars()
	for k in range(self.numlinks):
		d = self.d - self.length * k / self.numlinks
		pos = view.screenpos(geometry.interp(d, self.ps))
		size = T(view.scale * (0.3 if k == 0 else 0.2 * 0.99 ** k))
		color = [(120, 255, 120), (255, 255, 0)][k % 2]
		color = math.imix(color, (120, 255, 120), k / 120)
		pygame.draw.circle(pview.screen, color, pos, size)
	ps = [p for d, p in self.ps]
	for pstar in self.stars:
		color = (100, 100, 200)
		if self.chompin and geometry.polycontains(ps, pstar):
			color = (255, 255, 255)
		pos = view.screenpos(pstar)
		size = T(view.scale * 0.3)
		pygame.draw.circle(pview.screen, color, pos, size)
		



