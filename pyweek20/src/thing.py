import math, random, pygame
from src import window, image, state
from src.window import F
from src.enco import Component

things = {}
nextthingid = 1

def add(thing):
	things[thing.thingid] = thing
	return thing.thingid
def get(thingid):
	return things[thingid]
def kill(thing):
	del things[thing.thingid]
def newid():
	global nextthingid
	n = nextthingid
	nextthingid += 1
	return n

class HasId(Component):
	def init(self, thingid = None, **kwargs):
		self.thingid = newid() if thingid is None else thingid
	def dump(self, obj):
		obj["thingid"] = self.thingid

class HasType(Component):
	def dump(self, obj):
		obj["type"] = self.__class__.__name__

class KeepsTime(Component):
	def init(self, t = 0, **kwargs):
		self.t = t
	def think(self, dt):
		self.t += dt
	def dump(self, obj):
		obj["t"] = self.t

class WorldBound(Component):
	def init(self, X = None, y = None, pos = None, **kwargs):
		self.X = X or 0
		self.y = y or 0
		if pos is not None:
			self.X, self.y = pos
	def dump(self, obj):
		obj["X"] = self.X
		obj["y"] = self.y
	def screenpos(self):
		return window.screenpos(self.X, self.y)

class HasVelocity(Component):
	def init(self, vx = 0, vy = 0, **kwargs):
		self.vx = vx
		self.vy = vy
	def dump(self, obj):
		obj["vx"] = self.vx
		obj["vy"] = self.vy
	def think(self, dt):
		self.X += self.vx * dt / self.y
		self.y += self.vy * dt
	def screenpos(self):
		return window.screenpos(self.X, self.y)

class Drifts(Component):
	def init(self, driftax = 0, **kwargs):
		self.driftax = driftax
	def dump(self, obj):
		obj["driftax"] = self.driftax
	def think(self, dt):
		if self is not state.you:
			self.driftax += dt * random.uniform(-0.3, 0.3)
			self.driftax = math.clamp(self.driftax, -0.5, 0.5)
			self.vx += dt * self.driftax

class FeelsLinearDrag(Component):
	def __init__(self, beta):
		self.beta = beta
	def think(self, dt):
		if self.vx or self.vy:
			f = math.exp(-self.beta * dt)
			self.vx *= f
			self.vy *= f

class HasMaximumHorizontalVelocity(Component):
	def __init__(self, vxmax):
		self.vxmax = vxmax
	def think(self, dt):
		self.vx = math.clamp(self.vx, -self.vxmax, self.vxmax)

class HasMaximumVerticalVelocity(Component):
	def __init__(self, vymax):
		self.vymax = vymax
	def think(self, dt):
		self.vy = math.clamp(self.vy, -self.vymax, self.vymax)

# Position appearing on screen is offset horizontally
class HorizontalOscillation(Component):
	def __init__(self, xA, xomega):
		self.xA = xA
		self.xomega = xomega
	def screenpos(self):
		dX = self.xA * math.sin(self.xomega * self.t) / self.y
		return window.screenpos(self.X + dX, self.y)

class DrawImage(Component):
	def __init__(self, imgname):
		self.imgname = imgname
	def draw(self):
		if self.y <= 0:
			return
		img = image.get(self.imgname)
		rect = img.get_rect(center = self.screenpos())
		window.screen.blit(img, rect)

# Freezes in place when deployed
class DeployComm(Component):
	def init(self, deployed = False, **kwargs):
		self.deployed = deployed
	def dump(self, obj):
		obj["deployed"] = self.deployed
	def deploy(self):
		self.deployed = not self.deployed
	def think(self, dt):
		if self.deployed:
			self.vx = self.vy = 0
	def draw(self):
		if self.deployed:
			dX = 3 * math.sin(4 * self.t) / self.y
			dy = 3 * math.cos(4 * self.t)
			px, py = window.screenpos(self.X + dX, self.y + dy)
			size = F(2)
			window.screen.fill((255, 255, 255), (px, py, size, size))

class Laddered(Component):
	def init(self, ladderps = None, **kwargs):
		self.ladderps = ladderps
	def dump(self, obj):
		obj["ladderps"] = self.ladderps

class DrawFilament(Component):
	def draw(self):
		ps = []
		for j, (X, y) in enumerate(self.ladderps):
			ps.append(window.screenpos(X, y))
		pygame.draw.aalines(window.screen, (255, 255, 0), False, ps)


# Base class for things
@HasId()
@HasType()
@KeepsTime()
class Thing(object):
	def __init__(self, **kwargs):
		self.init(**kwargs)
		add(self)

@WorldBound()
@HasVelocity()
@HorizontalOscillation(2, 1)
@DrawImage("payload")
class Payload(Thing):
	pass


@WorldBound()
@HasVelocity()
@Drifts()
# @FeelsLinearDrag(3)
@HasMaximumHorizontalVelocity(20)
@HasMaximumVerticalVelocity(4)
@DrawImage("skiff")
class Skiff(Thing):
	pass

@WorldBound()
@HasVelocity()
@Drifts()
# @FeelsLinearDrag(3)
@HasMaximumHorizontalVelocity(12)
@HasMaximumVerticalVelocity(2)
@DrawImage("comm")
@DeployComm()
class CommShip(Thing):
	pass

@Laddered()
@DrawFilament()
class Filament(Thing):
	pass

def dump():
	obj = {}
	obj["nextthingid"] = nextthingid
	obj["things"] = {}
	for thingid, thing in things.items():
		data = {}
		thing.dump(data)
		obj["things"][thingid] = data
	return obj

def load(obj):
	global nextthingid
	things.clear()
	nextthingid = obj["nextthingid"]
	for thingid, data in obj["things"].items():
		things[thingid] = globals()[data["type"]](**data)


