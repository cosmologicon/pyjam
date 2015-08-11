from __future__ import division
import math, random, pygame
from src import window, image, state, hud
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

class Alive(Component):
	def init(self, alive = True, **kwargs):
		self.alive = alive
	def dump(self, obj):
		obj["alive"] = self.alive

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
	def think(self, dt):
		if self.y < 0:
			self.alive = False

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

class VerticalWeight(Component):
	def __init__(self, vy0):
		self.vy0 = vy0
	def think(self, dt):
		if self is not state.you:
			vy = -self.vy0 * min(state.R / self.y, 10)
			self.vy += 0.2 * dt * (vy - self.vy)

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

class MovesCircularWithConstantSpeed(Component):
	def __init__(self, speed, vomega):
		self.speed = speed
		self.vomega = vomega
	def init(self, vphi = None, **kwargs):
		self.vphi = random.uniform(0, math.tau) if vphi is None else vphi
	def dump(self, obj):
		obj["vphi"] = self.vphi
	def think(self, dt):
		self.vphi += self.vomega * dt
		self.vx = self.speed * math.sin(self.vphi)
		self.vy = self.speed * math.cos(self.vphi)

# Position appearing on screen is offset horizontally
class HorizontalOscillation(Component):
	def __init__(self, xA, xomega):
		self.xA = xA
		self.xomega = xomega
	def screenpos(self):
		dX = self.xA * math.sin(self.xomega * self.t) / self.y
		return window.screenpos(self.X + dX, self.y)

class DrawImage(Component):
	def __init__(self, imgname, imgr = 1):
		self.imgname = imgname
		self.imgr = imgr
	def draw(self):
		if self.y <= 0:
			return
		image.worlddraw(self.imgname, self.X, self.y, self.imgr)

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
		self.ladderds = []
		for j, (X, y) in enumerate(self.ladderps):
			X0, y0 = self.ladderps[max(j-1, 0)]
			X2, y2 = self.ladderps[min(j+1, len(self.ladderps)-1)]
			dx = (X2 - X0) * y
			dy = y2 - y0
			d = math.sqrt(dx ** 2 + dy ** 2)
			self.ladderds.append(((dy/d) / y, -(dx/d)))
	def dump(self, obj):
		obj["ladderps"] = self.ladderps

class DrawFilament(Component):
	def draw(self, surf, factor):
		data = []
		for j, ((X, y), (dX, dy)) in enumerate(zip(self.ladderps, self.ladderds)):
			if window.distancefromcamera(X, y) < 3:
				data.append((j, X, y, dX, dy))
		if len(data) < 2:
			return
		for alpha, r in [(40, 20), (60, 16), (100, 12), (140, 8)]:
			ps = []
			rps = []
			for j, X, y, dX, dy in data:
				omegax = 0.6 + 0.6 * (j ** 1.4 % 1)
				omegay = 0.6 + 0.6 * (j ** 1.7 % 1)
				omegar = 0.6 + 0.6 * (j ** 1.8 % 1)
				X += 4 * math.sin(omegax * self.t) / y
				y += 4 * math.sin(omegay * self.t)
				dr = r * (1 + 0.2 * math.sin(omegar * self.t))
				dX *= dr
				dy *= dr
				px, py = window.screenpos(X + dX, y + dy)
				ps.append((px / factor, py / factor))
				px, py = window.screenpos(X - dX, y - dy)
				rps.append((px / factor, py / factor))
			pygame.draw.polygon(surf, (255, 255, 0, alpha), ps + rps[::-1], 0)

class EmptyDrawHUD(Component):
	def drawhud(self):
		pass

class DrawMinimap(Component):
	def drawhud(self):
		hud.drawminimap()


# Base class for things
@HasId()
@HasType()
@KeepsTime()
class Thing(object):
	def __init__(self, **kwargs):
		self.init(**kwargs)
		add(self)

@Alive()
@WorldBound()
@HasVelocity()
class WorldThing(Thing):
	pass

@HorizontalOscillation(2, 1)
@DrawImage("payload")
class Payload(WorldThing):
	pass

@EmptyDrawHUD()
class Ship(WorldThing):
	pass

@Drifts()
# @FeelsLinearDrag(3)
@HasMaximumHorizontalVelocity(20)
@VerticalWeight(1)
@HasMaximumVerticalVelocity(10)
@DrawImage("skiff")
class Skiff(Ship):
	pass

@Drifts()
# @FeelsLinearDrag(3)
@HasMaximumHorizontalVelocity(12)
@VerticalWeight(2)
@HasMaximumVerticalVelocity(6)
@DrawImage("beacon")
@DrawMinimap()
class Beacon(Ship):
	pass

@Drifts()
# @FeelsLinearDrag(3)
@HasMaximumHorizontalVelocity(6)
@VerticalWeight(2)
@HasMaximumVerticalVelocity(4)
@DrawImage("comm")
@DeployComm()
class CommShip(Ship):
	pass

@MovesCircularWithConstantSpeed(8, 0.2)
@DrawImage("tremor", 6)
class Tremor(WorldThing):
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


