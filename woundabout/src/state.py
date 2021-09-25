import random, math, pygame
from . import pview, view, geometry, settings, ptext, snek, graphics, progress, leveldata, sound, scene, profiler
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

	def collides(self, obj):
		return geometry.collides(self, obj)

	def collide(self):
		pass

	def collect(self):
		pass

	def visible(self):
		return view.pointvisible(self.pos, d = self.r + 1)

class Star(Obj):
	color = 128, 128, 128
	num = 1

	def __init__(self, pos, r = 0.3, windreq = None, numreq = 0, display = False):
		Obj.__init__(self, pos)
		self.r = r
		self.windreq = windreq
		self.numreq = numreq
		self.imgname = "key"
		if numreq:
			self.imgname += "X" if numreq == -1 else str(numreq)
		if windreq:
			self.imgname += "L" if windreq > 0 else "R"
		self.tanim = math.fuzzrange(0, 100, 0, *self.pos)
		self.vanim = math.fuzzrange(0.4, 1, 1, *self.pos)
		if windreq:
			self.vanim = math.fuzzrange(0.3, 0.5, 1, *self.pos)
		else:
			self.vanim *= random.choice([-1, 1])
		self.tcloud = math.fuzzrange(0, 100, 2, *self.pos)
		self.fappear = 0
		self.appeared = False
		self.display = display

	def getcolor(self):
		if self in active:
			return math.imix(self.color, (255, 255, 255), 0.6)
		else:
			return self.color

	def currentimg(self):
		j = int(self.tanim * 60) % 60
		return "frames/%s-%d" % (self.imgname, j)

	def think(self, dt):
		Obj.think(self, dt)
		if not self.appeared:
			fappear = 0 if (not self.display and geometry.collides(self, you)) else 1
			self.fappear = math.approach(self.fappear, fappear, 1 * dt)
			if self.fappear == 1:
				self.appeared = True
		self.tanim += dt * self.vanim
		self.tcloud += dt

	def draw(self):
		if not self.visible:
			return
#		graphics.drawflare(self.pos, self.r, self.tanim, color = self.color)
		alpha = math.smoothfadebetween(self.fappear, 0.6, 0, 1, 1)
		if alpha > 0:
			graphics.drawimg(self.pos, self.currentimg(), self.r, 0, alpha)
		if self.fappear < 1:
			graphics.drawcloud(self.pos, 0.9 * self.r, self.tcloud, 1 - self.fappear)

	def activate(self):
		if not self.alive: return
		self.alive = False
		effects.append(ShedStar(self.pos, self.currentimg(), self.r))
		self.act()
	
	def act(self):
		pass

class GrowStar(Star):
	color = 100, 100, 200
	num = 0
	r = 0.6
	def __init__(self, pos, r = 0.6, display = False):
		Star.__init__(self, pos, r, windreq = None, numreq = 0, display = display)

	def act(self):
		you.lengthen()

	def draw(self):
		if not self.visible:
			return
		color = self.getcolor()
		graphics.drawcloud(self.pos, self.r, -0.3 * self.tcloud, f = 1.6, color = color)


class ShedStar:
	def __init__(self, pos, imgname, r):
		self.pos = pos
		self.imgname = imgname
		self.r = r
		self.t = 0

	def think(self, dt):
		self.t += dt
		self.alive = self.t < 0.5
		
	def draw(self):
		f = math.fadebetween(self.t, 0, 0, 0.5, 1) ** 0.5
		r = self.r * math.mix(1.3, 3, f)
		alpha = math.mix(0.5, 0, f)
		graphics.drawimg(self.pos, self.imgname, r, 0, alpha)


class Wall:
	color = 140, 20, 20
	r = 0.05
	def __init__(self, pos0, pos1):
		self.pos0 = pos0
		self.pos1 = pos1
		
		n = int(math.ceil(math.distance(self.pos0, self.pos1) / 0.5))
		self.blockps = [(math.mix(self.pos0, self.pos1, j / n), 1) for j in range(n + 1)]
		self.makefenceps()
		self.lock = None

	def active(self):
		return self.lock is None or self.lock.active

	def makefenceps(self):
#		pos0 = view.screenpos(self.pos0)
#		pos1 = view.screenpos(self.pos1)
#		pygame.draw.line(pview.screen, self.color, pos0, pos1, T(2 * view.scale * self.r))
		self.fenceps = []
		for _ in range(50):
			ps = [self.pos0, self.pos1]
			d = 0.4
			a = 1
			amax = math.distance(self.pos0, self.pos1)
			while a < amax:
				ps, ps1 = ps[:1], ps[1:]
				for p1 in ps1:
					center = math.mix(ps[-1], p1, 0.5)
					ps.append(math.CS(random.uniform(0, math.tau), d, center = center))
					ps.append(p1)
				d *= 0.7
				a *= 1.9
			self.fenceps.append(ps)

	def visible(self):
		return view.linevisible(self.pos0, self.pos1, d = 2)

	def draw(self):
#		alpha = int(math.fadebetween(view.scale, 5, 50, 100, 255))
		if view.scale > 5:
			ps = random.choice(self.fenceps)
		else:
			ps = [self.pos0, self.pos1]
		ps = [view.screenpos(p) for p in ps]
		pygame.draw.aalines(pview.screen, (200, 200, 255), False, ps, 1)
			

	def collides(self, you):
		return self.active() and geometry.dtoline(you.pos, self.pos0, self.pos1) < you.r + self.r

	def collide(self):
		you.alive = False


class Lock(Obj):
	r = 1
	def __init__(self, pos, stage):
		Obj.__init__(self, pos)
		self.stage = stage
		self.active = True
		self.tactive = 100
		self.toshed = True
		for wall in walls:
			if self.pos in (wall.pos0, wall.pos1):
				wall.lock = self
		self.makezotps()
		self.fappear = 1

	def makezotps(self):
		self.zotps = []
		for _ in range(50):
			ps = math.CSround(16, self.r * 1.3, center = self.pos)
			ps = [(
				x + self.r * 0.3 * random.uniform(-1, 1),
				y + self.r * 0.3 * random.uniform(-1, 1),
			) for x, y in ps]
			self.zotps.append(ps)

	def think(self, dt):
		Obj.think(self, dt)
		if not self.active:
			self.tactive = 0
			if self.toshed:
				self.toshed = False
				effects.append(ShedStar(self.pos, "fencepost", self.r))
		else:
			self.tactive += dt
			self.toshed = True
		self.fappear = math.fadebetween(self.tactive, 0, 0, 1, 1)

	def draw(self):
		if not self.active:
			return
		alpha = math.smoothfadebetween(self.fappear, 0, 0, 1, 1)
		graphics.drawimg(self.pos, "fencepost", self.r, 0, alpha)
		if self.fappear < 1:
			graphics.drawcloud(self.pos, self.r, self.t, self.fappear)
		else:
			ps = random.choice(self.zotps)
			ps = [view.screenpos(p) for p in ps]
			pygame.draw.aalines(pview.screen, (200, 200, 255), True, ps, 1)

	def collides(self, you):
		return self.active and Obj.collides(self, you)


def inregion(p):
	return geometry.polywind(region, p) != 0

def regionbounds():
	xs, ys = zip(*region)
	return min(xs), min(ys), max(xs), max(ys)

def adventure_vtarget(d = 2):
	if adventure_winning():
		return (0, 20), 2.4
	return endless_vtarget(d)

def endless_vtarget(d = 2):
	x0, y0, x1, y1 = regionbounds()
	sx = 1280 / (x1 - x0 + 2 * d)
	sy = 720 / (y1 - y0 + 2 * d)
	return ((x0 + x1) / 2, (y0 + y1) / 2), min(sx, sy)

# Random point within the region
def randompos():
	x0, y0, x1, y1 = regionbounds()
	while True:
		p = random.uniform(x0, x1), random.uniform(y0, y1)
		if inregion(p):
			return p

# Choose a point within the arena that's not too close to any of the given points.	
def randomspawn(ps, r0, dmin = 1):
	j = 0
	while True:
		x, y = randompos()
		j += 1
		if any(math.hypot(x - px, y - py) < r0 + pr + dmin for (px, py), pr in ps):
			dmin *= math.exp(-0.01)
			continue
		if settings.DEBUG and j > 10:
			print("randomspawn", j)
		return x, y

region = []
walls = []

objs = []
active = []
wound = []
keys = []
locks = []
effects = []
def endless_init():
	global you, stage, numgrow, nextbomb
	del region[:], walls[:], objs[:], active[:], wound[:], keys[:], effects[:]

	stage = progress.endless + 1
	act = (stage - 1) // 20
	stage -= act * 20
	headstart = 0 if stage <= 2 else 2 if stage <= 5 else 4 if stage <= 7 else 8 if stage <= 12 else 12 if stage <= 16 else 20
	numgrow = 1 if stage <= 2 else 2 if stage <= 5 else 3 if stage <= 15 else 4
	
	if stage == 1:
		R = 12
		objs.append(Star((0, 0), r = 4))
	if stage == 2:
		R = 10
		objs.append(Star((7, 0), r = 1.4, numreq = 2))
		objs.append(Star((-7, 0), r = 1.4, numreq = 2))
	if stage == 3:
		R = 12
		objs.append(Star((8, 0), r = 1.4, numreq = 2))
		objs.append(Star((-8, 0), r = 1.4, numreq = 2))
		walls.append(Wall((0, -4), (0, 4)))
	if stage == 4:
		R = 14
		objs.append(Star((12, 0), r = 2.6, numreq = 2, windreq = 1))
		objs.append(Star((-12, 0), r = 2.6, numreq = 2, windreq = -1))
	if stage == 5:
		R = 14
		objs.append(Star((7, 0), r = 1.4, numreq = 2))
		objs.append(Star((-7, 0), r = 1.4, numreq = 2))
		for p0, p1 in [
			((-10, 6), (0, 6)),
			((10, 6), (0, 6)),
			((-10, -6), (0, -6)),
			((10, -6), (0, -6)),
			((0, -6), (0, 6)),
		]:
			walls.append(Wall(p0, p1))
	if stage == 6:
		R = 14
		objs.append(Star((0, 0), r = 2.6, numreq = -1))
		objs.append(Star((11, -7), r = 1.4, numreq = -1))
		objs.append(Star((-11, 7), r = 1.4, numreq = -1))
		objs.append(Star((11, 7), r = 1.4, numreq = 2))
		objs.append(Star((-11, -7), r = 1.4, numreq = 2))
	if stage == 7:
		R = 12
		for x, y in math.CSround(3, 8, jtheta0 = 3/4):
			objs.append(Star((1.4 * x, y), r = 2, numreq = 3))
	if stage == 8:
		R = 18
		objs.append(Star((12, 0), r = 1, numreq = 2))
		objs.append(Star((-12, 0), r = 1, numreq = 2))
		ps = [(-15, 7), (-22, 0), (-12, -7)]
		ps.extend([(-x, -y) for x, y in reversed(ps)])
		for j in range(len(ps) - 1):
			walls.append(Wall(ps[j], ps[j+1]))
	if stage == 9:
		R = 16
		objs.append(Star((15, 9), r = 2.6, numreq = 4, windreq = 1))
		objs.append(Star((5, 3), r = 2.6, numreq = 4, windreq = -1))
		objs.append(Star((-5, -3), r = 2.6, numreq = 4, windreq = 1))
		objs.append(Star((-15, -9), r = 2.6, numreq = 4, windreq = -1))
	if stage == 10:
		R = 14
		objs.append(Star((0, 0), r = 3, numreq = -1))
		objs.append(Star((12, 8), r = 2, numreq = 2))
		objs.append(Star((-12, -8), r = 2, numreq = 2))
		walls.append(Wall((-10, 7), (10, -7)))
	if stage == 11:
		R = 13
		objs.append(Star((0, 0), r = 2, numreq = -1))
		for x, y in math.CSround(3, 6, jtheta0 = 1/4):
			objs.append(Star((x, y), r = 2, numreq = 3))
			walls.append(Wall((0, 0), (-1.4 * x, -1.4 * y)))
	if stage == 12:
		R = 16
		objs.append(Star((0, 0), r = 2.6, numreq = -1))
		objs.append(Star((12, -8), r = 2.6, numreq = 4))
		objs.append(Star((-12, 8), r = 2.6, numreq = 4))
		objs.append(Star((12, 8), r = 2.6, numreq = 4))
		objs.append(Star((-12, -8), r = 2.6, numreq = 4))
	if stage == 13:
		R = 18
		for j, pos in enumerate(math.CSround(4, 8, jtheta0 = 1/2)):
			objs.append(Star(pos, r = 2, numreq = 4, windreq = (1 if j % 2 == 0 else -1)))
		walls.append(Wall((0, -10), (0, 10)))
		walls.append(Wall((-10, 0), (10, 0)))
	if stage == 14:
		R = 16
		objs.append(Star((0, 0), r = 3, numreq = 3))
		objs.append(Star((18, 0), r = 2, numreq = 3, windreq = 1))
		objs.append(Star((-18, 0), r = 2, numreq = 3, windreq = -1))
		walls.append(Wall((-10, 10), (-10, -10)))
		walls.append(Wall((10, 10), (10, -10)))
	if stage == 15:
		R = 18
		objs.append(Star((12, 0), r = 1, numreq = 2, windreq = 1))
		objs.append(Star((-12, 0), r = 1, numreq = 2, windreq = -1))
		ps = [(-15, 7), (-22, 0), (-12, -7)]
		ps.extend([(-x, -y) for x, y in reversed(ps)])
		for j in range(len(ps) - 1):
			walls.append(Wall(ps[j], ps[j+1]))
	if stage == 16:
		R = 14
		objs.append(Star((14, -7), r = 1.4, numreq = 2))
		objs.append(Star((-14, 7), r = 1.4, numreq = 2))
		walls.append(Wall((3, -13), (13, 7)))
		walls.append(Wall((-3, 13), (-13, -7)))
	if stage == 17:
		R = 12
		for x, y in math.CSround(3, 8, jtheta0 = 3/4):
			objs.append(Star((1.4 * x, y - 2), r = 2, numreq = 3))
		objs.append(Star((5, 0), r = 3, numreq = -1))
		objs.append(Star((-5, 0), r = 3, numreq = -1))
	if stage == 18:
		R = 14
		objs.append(Star((11, -8), r = 2, numreq = 4))
		objs.append(Star((-11, 8), r = 2, numreq = 4))
		objs.append(Star((11, 8), r = 2, numreq = 4))
		objs.append(Star((-11, -8), r = 2, numreq = 4))
		walls.append(Wall((-25, 0), (-7, 0)))
		walls.append(Wall((25, 0), (7, 0)))
	if stage == 19:
		R = 16
		objs.append(Star((0, 0), r = 3, numreq = 3))
		objs.append(Star((18, 0), r = 2, numreq = 3, windreq = 1))
		objs.append(Star((-18, 0), r = 2, numreq = 3, windreq = -1))
		objs.append(Star((-10, 0), r = 1.4, numreq = -1))
		objs.append(Star((10, 0), r = 1.4, numreq = -1))
		walls.append(Wall((-10, 10), (-10, -10)))
		walls.append(Wall((10, 10), (10, -10)))
	if stage == 20:
		R = 18
		for j, pos in enumerate(math.CSround(4, 8, jtheta0 = 1/2)):
			objs.append(Star(pos, r = 2, numreq = 4, windreq = (1 if j % 2 == 0 else -1)))
		walls.append(Wall((0, -10), (0, 10)))
		walls.append(Wall((-10, 0), (10, 0)))
		objs.append(Star((0, 0), r = 1.4, numreq = -1))

	if stage >= 21:
		exit()

	keys.extend([star for star in objs if star.numreq >= 0])
	from . import snek
	you = snek.You((0, -R + 2), 0)
	you.length = 10
	you.dlength = 5
	you.speed = 5 + 2.5 * act
	you.dspeed = 0.1 + 0.05 * act
	you.length += headstart * you.dlength
	you.speed += headstart * you.dspeed
	nextbomb = 20

	stage += act * 20

	ps = math.CSround(12, r = R, jtheta0 = 0.5)
	a = 7/9 * (R + 2)
	region[:] = [(x + a * math.sign(x), y) for x, y in ps]
	for j, p0 in enumerate(region):
		p1 = region[(j + 1) % len(region)]
		walls.append(Wall(p0, p1))

def adventure_init():
	global you, stage, numgrow
	del region[:], walls[:], objs[:], active[:], wound[:], keys[:], locks[:], effects[:]

	for p0, p1 in leveldata.walls:
		walls.append(Wall(p0, p1))

	stage = progress.adventure + 1
	data = leveldata.data[stage - 1]

	region[:] = data["region"]

	for spec in data["keys"]:
		key = Star(**spec)
		objs.append(key)
		keys.append(key)
	for spec in data["stars"]:
		star = Star(**spec)
		objs.append(star)
	for pos in data["energy"]:
		star = GrowStar(pos)
		objs.append(star)
		keys.append(star)

	for lockp, jregion in leveldata.lockps:
		lock = Lock(lockp, jregion + 1)
		locks.append(lock)
		objs.append(lock)

	numgrow = 0
	you = snek.You(data["youpos"], data["youtheta"])
	headstart = data["headstart"]
	you.length = 20 + 5 * headstart
	you.dlength = 5
	you.speed = 4 + 0.1 * headstart
	you.dspeed = 0.1

def adventure_advance():
	global stage
	if stage > leveldata.maxstage:
		if not progress.adventuredone:
			progress.completeadventure()
		return
	progress.beatadventure(stage)
	stage += 1
	if stage > leveldata.maxstage:
		return
	data = leveldata.data[stage - 1]
	region[:] = data["region"]
	for spec in data["keys"]:
		key = Star(**spec)
		objs.append(key)
		keys.append(key)
	for spec in data["stars"]:
		star = Star(**spec)
		objs.append(star)
	for pos in data["energy"]:
		star = GrowStar(pos)
		objs.append(star)
		keys.append(star)


def setactive(poly):
	global actfail
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
	if wound and not active:
		sound.playsound("no")
	for obj in active:
		obj.activate()
	del active[:], wound[:]

def blockps():
	ps = [(obj.pos, obj.r) for obj in objs]
	ps.extend(you.blockps())
	for wall in walls:
		ps.extend(wall.blockps)
	return ps


def adventure_think(dt):
	for obj in objs:
		obj.think(dt)
		if not you.chompin and obj.collides(you):
			you.alive = False
	for wall in walls:
		if wall.collides(you):
			wall.collide()
	for effect in effects:
		effect.think(dt)
	objs[:] = [obj for obj in objs if obj.alive]
	effects[:] = [effect for effect in effects if effect.alive]


	if not any(key.alive for key in keys):
		played = False
		for lock in locks:
			if lock.stage == stage and lock.active:
				lock.active = False
				if not played:
					sound.playsound("unlock")
					played = True
	if not inregion(you.pos):
		adventure_advance()
	for lock in locks:
		if lock.stage < stage <= leveldata.maxstage and not lock.active:
			ps = [p for d, p, theta in you.ps]
			random.shuffle(ps)
			if all(inregion(p) for p in ps):
				lock.active = True

def endless_think(dt):
	global nextbomb
	while sum(isinstance(obj, GrowStar) for obj in objs) < numgrow:
		r = 0.6
		pos = randomspawn(blockps(), r, dmin = 2)
		objs.append(GrowStar(pos, r))

	for obj in objs:
		obj.think(dt)
		if not you.chompin and obj.fappear == 1 and obj.collides(you):
			you.alive = False
		if isinstance(obj, GrowStar) and not obj.alive and you.length > nextbomb:
			objs.append(Star(obj.pos, r = 1, numreq = -1))
			nextbomb += 15
	for wall in walls:
		if wall.collides(you):
			wall.collide()
	for effect in effects:
		effect.think(dt)
	objs[:] = [obj for obj in objs if obj.alive]
	effects[:] = [effect for effect in effects if effect.alive]


def drawwalls():
	postps = set()
	for wall in walls:
		if not wall.active() or not wall.visible():
			continue
		wall.draw()
		postps.add(wall.pos0)
		postps.add(wall.pos1)
	for pos in sorted(postps):
		graphics.drawimg(pos, "fencepost", r = 0.35, angle = 0)
	


def gameover():
	return not you.alive

def adventure_winning():
	return stage > leveldata.maxstage

def endless_winning():
	return not any(key.alive for key in keys)

def cheatwin():
	if scene.current == "adventure":
		progress.beatadventure(stage)
		from . import playscene
		playscene.init()
	else:
		for obj in keys:
			obj.activate()
def cheatgrow():
	you.lengthen()


