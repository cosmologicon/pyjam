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

	def __init__(self, pos, r = 0.3, windreq = None, numreq = 0):
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
			self.vanim *= 0.4
		self.tcloud = math.fuzzrange(0, 100, 2, *self.pos)

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
		self.tanim += dt * self.vanim
		self.tcloud += dt

	def draw(self):
		if not self.visible:
			return
		alpha = math.smoothfadebetween(self.t, 0, 0, 1, 1)
		graphics.drawimg(self.pos, self.currentimg(), self.r, 0, alpha)
		if self.t < 1:
			f = math.fadebetween(self.t, 0, 1, 1, 0)
			graphics.drawcloud(self.pos, self.r, self.tcloud, f)

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
	def __init__(self, pos, r = 0.6):
		Star.__init__(self, pos, r, windreq = None, numreq = 0)

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
		r = self.r * math.mix(1, 2, f)
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
			a = 0.5
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

	def draw(self):
		if not self.active:
			return
		alpha = math.smoothfadebetween(self.t, 0, 0, 1, 1)
		graphics.drawimg(self.pos, "fencepost", self.r, 0, alpha)
		if self.tactive < 1:
			f = math.fadebetween(self.tactive, 0, 1, 1, 0)
			graphics.drawcloud(self.pos, self.r, self.t, f)

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
	global you, stage, numgrow
	del region[:], walls[:], objs[:], active[:], wound[:], keys[:], effects[:]

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
	you = snek.You((0, -R + 2), 0)
	you.length = 10
	you.dlength = 5
	you.speed = 5
	you.dspeed = 0.1
	you.length += headstart * you.dlength
	you.speed += headstart * you.dspeed

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
	while sum(isinstance(obj, GrowStar) for obj in objs) < numgrow:
		r = 0.6
		pos = randomspawn(blockps(), r, dmin = 2)
		objs.append(GrowStar(pos, r))

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


