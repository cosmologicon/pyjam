import random, math, pygame
from . import pview, view, geometry, settings
from .pview import T


class Obj:
	def __init__(self, pos):
		self.pos = pos
		self.t = 0
		self.alive = True

	def think(self, dt):
		self.t += dt

	def getcolor(self):
		return self.color

	def draw(self):
		color = self.getcolor()
		pos = view.screenpos(self.pos)
		size = T(view.scale * self.r)
		pygame.draw.circle(pview.screen, color, pos, size)

	def collide(self):
		pass

	def collect(self):
		pass

class Star(Obj):
	color = 128, 128, 128
	r = 0.3

	def getcolor(self):
		if you.ischompin(self.pos):
			return math.imix(self.color, (255, 255, 255), 0.6)
		else:
			return self.color

	def collide(self):
		if not self.alive: return
		you.length = max(you.length - 5, 10)
		self.alive = False

	def collect(self):
		if not self.alive: return
		self.alive = False
		self.act()
	
	def act(self):
		pass

class GrowStar(Star):
	color = 100, 100, 200
	def act(self):
		you.length += 1.5

class DieStar(Star):
	color = 200, 100, 100
	def act(self):
		you.length = 0
		you.alive = False

class Mine(Obj):
	color = 60, 60, 60
	r = 0.6

	def collide(self):
		if not self.alive: return
		you.length = max(you.length - 5, 10)
		self.alive = False

class Wall:
	color = 140, 20, 20
	r = 0.05
	def __init__(self, pos0, pos1):
		self.pos0 = pos0
		self.pos1 = pos1

	def draw(self):
		pos0 = view.screenpos(self.pos0)
		pos1 = view.screenpos(self.pos1)
		pygame.draw.line(pview.screen, self.color, pos0, pos1, T(2 * view.scale * self.r))

	def collides(self, you):
		return geometry.dtoline(you.pos, self.pos0, self.pos1) < you.r + self.r

	def collide(self):
		you.length = 0
		you.alive = False
	


class You:
	r = 0.3
	def __init__(self):
		self.t = 0
		self.d = 0
		self.pos = (0, 0)
		self.ps = [(self.d, self.pos)]
		self.theta = 0  # 0 = north, tau/4 = east
		self.chompin = False
		self.tchomp = 0
		self.speed = 5
		self.fspeed = 1
		self.length = 10
		self.alive = True

	def canchomp(self):
		for j, (d0, p0) in enumerate(self.ps):
			if d0 > self.d - self.length + 0.5:
				return False
			if j >= len(self.ps) - 1:
				return False
			d1, p1 = self.ps[j + 1]
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
		self.chomppoly = [p for d, p in self.ps]
		self.ischompincache = {}
		xs, ys = zip(*self.chomppoly)
		xmin, xmax = min(xs), max(xs)
		ymin, ymax = min(ys), max(ys)
		self.vtarget = (xmax + xmin) / 2, (ymax + ymin) / 2
		self.starget = min(1280 / (4 + xmax - xmin), 720 / (4 + ymax - ymin))

	def ischompin(self, pos):
		if not self.chompin: return False
		if pos not in self.ischompincache:
			self.ischompincache[pos] = geometry.polycontains(self.chomppoly, pos)
		return self.ischompincache[pos]
	
	def unchomp(self):
		if self.chompin and self.tchomp > 1:
			for obj in objs:
				if self.ischompin(obj.pos):
					obj.collect()
			self.chompin = False
			self.tchomp = -1

	def think(self, dt, dkx, dky):
		d0, (x0, y0) = self.ps[-1]

		if self.chompin:
			self.fspeed = math.approach(self.fspeed, 5, dt)
		else:
			self.fspeed = math.approach(self.fspeed, 1, 4 * dt)

		step = dt * self.speed * self.fspeed
		self.d += step

				
		if self.chompin:
			self.tchomp += dt
			p0 = self.ps[0][1]
			dy, dx = math.CS(self.theta, step)
			self.pos = math.mix((x0 + dx, y0 + dy), p0, math.clamp(self.tchomp * 0.5, 0, 1))
			x1, y1 = self.pos
			self.theta = math.atan2(x1 - x0, y1 - y0)
		else:
			if settings.directcontrol:
				if dkx or dky:
					target = math.atan2(dkx, dky)
					self.theta = math.angleapproach(self.theta, target, 0.9 * self.speed * dt)
			else:
				omega = { -1: 0.3, 0: 0.6, 1: 1.2 }[dky] * self.speed
				self.theta += omega * dt * dkx % math.tau
			dy, dx = math.CS(self.theta, step)
			self.pos = x0 + dx, y0 + dy

		self.ps.append((self.d, self.pos))
		while len(self.ps) > 1 and self.ps[1][0] <= self.d - self.length:
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
				p = math.softapproach(p, pc, 500 * dt * ft * fd, dymin = 0.001)
				self.ps[j] = d, p

		if not self.chompin:
			if self.canchomp():
				if self.tchomp == 0:
					self.chomp()
			else:
				if self.tchomp < 0:
					self.tchomp = min(self.tchomp + dt, 0)


	def draw(self):
		a, k = 0, 0
		while a < self.length:
			size = 0.5 if k == 0 else max(0.3 * 0.98 ** k, 0.2)
			if k > 0: a += size
			pos = view.screenpos(geometry.interp(self.d - a, self.ps))
			color = [(120, 255, 120), (255, 255, 0)][k % 2]
			color = math.imix(color, (120, 255, 120), k / 120)
			pygame.draw.circle(pview.screen, color, pos, T(view.scale * size))
			k += 1
			a += size



objs = []
walls = []
def init():
	global R, you
	R = 20
	you = You()
	del objs[:]
	d = R - 2
	taken = set()
	def randompos():
		x, y = p = random.randint(-d, d), random.randint(-d, d)
		if p not in taken and 4 < math.hypot(x, y) < d:
			taken.add(p)
			return p
		return randompos()
	for _ in range(int(d ** 2 * 0.1)):
		objs.append(GrowStar(randompos()))
		objs.append(Mine(randompos()))

	del walls[:]
	ps = math.CSround(12, r = R, jtheta0 = 0.5)
	for j, p0 in enumerate(ps):
		p1 = ps[(j + 1) % len(ps)]
		walls.append(Wall(p0, p1))



def think(dt):
	for obj in objs:
		obj.think(dt)
		if geometry.collides(obj, you):
			obj.collide()
	for wall in walls:
		if wall.collides(you):
			wall.collide()
	objs[:] = [obj for obj in objs if obj.alive]

def gameover():
	return not you.alive


