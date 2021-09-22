import random, math, pygame
from . import pview, view, geometry, settings, ptext, snek, graphics, progress
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
	num = 1

	def __init__(self, pos, r = 0.3, windreq = None, numreq = 0):
		Obj.__init__(self, pos)
		self.r = r
		self.windreq = windreq
		self.numreq = numreq

	def getcolor(self):
		if self in active:
			return math.imix(self.color, (255, 255, 255), 0.6)
		else:
			return self.color

	def draw(self):
		Obj.draw(self)
		if self.windreq is not None:
			size = T(view.scale * 0.1 * self.r)
			jtheta0 = 2 * self.windreq * self.t % 1
			for pos in math.CSround(3, self.r, jtheta0 = jtheta0, center = self.pos):
				pygame.draw.circle(pview.screen, (255, 255, 255), view.screenpos(pos), size)
		if self.numreq != 0:
			ptext.draw(str(self.numreq), center = view.screenpos(self.pos),
				fontsize = T(view.scale * self.r), shadow = (1, 1))

	def collide(self):
		if not self.alive: return
		you.length = max(you.length - 5, 10)
		self.alive = False

	def activate(self):
		if not self.alive: return
		self.alive = False
		self.act()
	
	def act(self):
		pass

class GrowStar(Star):
	color = 100, 100, 200
	num = 0
	def __init__(self, pos, r = 0.3):
		Star.__init__(self, pos, r, windreq = None, numreq = 0)

	def act(self):
		you.lengthen()

	def draw(self):
		color = self.getcolor()
		graphics.drawhill(view.screenpos(self.pos), color, T(view.scale * self.r * 2), 1)
		for k in range(3):
			j, a = divmod(3 * self.t + 1000 * math.fuzz(k, *self.pos), 1)
			pos = math.CS(j * math.phyllo, r = self.r * math.sqrt(a) * 1.3, center = self.pos)
			size = T(view.scale * self.r * 1)
			alpha = math.smoothfadebetween(a, 0, 1, 1, 0)
			graphics.drawhill(view.screenpos(pos), color, size, alpha)


class WindStar(Star):
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
		
		n = int(math.ceil(math.distance(self.pos0, self.pos1) / 0.5))
		self.blockps = [(math.mix(self.pos0, self.pos1, j / n), 1) for j in range(n + 1)]

	def draw(self):
		pos0 = view.screenpos(self.pos0)
		pos1 = view.screenpos(self.pos1)
		pygame.draw.line(pview.screen, self.color, pos0, pos1, T(2 * view.scale * self.r))

	def collides(self, you):
		return geometry.dtoline(you.pos, self.pos0, self.pos1) < you.r + self.r

	def collide(self):
		you.length = 0
		you.alive = False


# Choose a point within the arena that's not too close to any of the given points.	
def randompos(R, ps, r0, dmin = 1):
	j = 0
	while True:
		d = R - dmin
		x, y = p = random.uniform(-d, d), random.uniform(-d, d)
		if math.hypot(x, y) > d:
			continue
		j += 1
		if any(math.hypot(x - px, y - py) < r0 + pr + dmin for (px, py), pr in ps):
			dmin *= math.exp(-0.01)
			continue
		print("randompos", j)
		return x, y

objs = []
walls = []
active = []
wound = []
keys = []
def init():
	global R, you, stage, numgrow
	del objs[:], active[:], wound[:], keys[:], walls[:]

	stage = progress.endless + 1
	if stage == 1:
		R = 12
		objs.append(Star((0, 0), r = 4))
		numgrow = 1
		headstart = 0
	elif stage == 2:
		R = 14
		objs.append(Star((7, 0), r = 1.4, numreq = 2))
		objs.append(Star((-7, 0), r = 1.4, numreq = 2))
		numgrow = 2
		headstart = 1
	elif stage == 3:
		R = 15
		objs.append(Star((8, 0), r = 1.4, numreq = 2))
		objs.append(Star((-8, 0), r = 1.4, numreq = 2))
		walls.append(Wall((0, -6), (0, 6)))
		numgrow = 3
		headstart = 2
	elif stage == 4:
		R = 16
		for pos in math.CSround(4, 10, jtheta0 = 0.5):
			objs.append(Star(pos, r = 2, numreq = 2))
		objs.append(Star((0, 0), r = 4, numreq = -1))
		numgrow = 3
		headstart = 3
	elif stage == 5:
		R = 16
		for pos in math.CSround(3, 10, jtheta0 = 3/4):
			objs.append(Star(pos, r = 2, numreq = 3))
		objs.append(Star((0, 0), r = 4, numreq = -1))
		numgrow = 3
		headstart = 6
	elif stage == 6:
		R = 17
		for j, pos in enumerate(math.CSround(4, 8, jtheta0 = 1/2)):
			objs.append(Star(pos, r = 2, numreq = 4, windreq = (1 if j % 2 == 0 else -1)))
		walls.append(Wall((0, -10), (0, 10)))
		walls.append(Wall((-10, 0), (10, 0)))
		numgrow = 3
		headstart = 10
	else:
		exit()

	keys.extend([star for star in objs if star.numreq >= 0])

	from . import snek
	you = snek.You((0, -R + 2))
	you.length = 10
	you.dlength = 5
	you.speed = 5
	you.dspeed = 0.1
	you.length += headstart * you.dlength
	you.speed += headstart * you.dspeed

	ps = math.CSround(12, r = R, jtheta0 = 0.5)
	for j, p0 in enumerate(ps):
		p1 = ps[(j + 1) % len(ps)]
		walls.append(Wall(p0, p1))


def setactive(poly):
	del wound[:], active[:]
	for obj in objs:
		wind = geometry.polywind(poly, obj.pos)
		if wind:
			wound.append(obj)
			if obj.windreq is None or wind * obj.windreq > 0:
				active.append(obj)
	if any(obj.numreq < 0 for obj in wound):
		del active[:]
	num = sum(obj.num for obj in active)
	active[:] = [obj for obj in active if num >= obj.numreq]


def activate():
	for obj in active:
		obj.activate()
	del active[:], wound[:]

def blockps():
	ps = [(obj.pos, obj.r) for obj in objs]
	ps.extend(you.blockps())
	for wall in walls:
		ps.extend(wall.blockps)
	return ps


def think(dt):
	while sum(isinstance(obj, GrowStar) for obj in objs) < numgrow:
		r = 0.3
		pos = randompos(R * math.cos(math.tau / 24), blockps(), r, dmin = 2)
		objs.append(GrowStar(pos, r))


	for obj in objs:
		obj.think(dt)
		if not you.chompin and geometry.collides(obj, you):
			you.alive = False
	for wall in walls:
		if wall.collides(you):
			wall.collide()
	objs[:] = [obj for obj in objs if obj.alive]

def gameover():
	return not you.alive

def winning():
	return not any(key.alive for key in keys)

def cheatwin():
	for obj in keys:
		obj.alive = False

