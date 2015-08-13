from __future__ import division
import math, random, pygame
from src import window, image, state, hud, sound
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
	if thing.thingid in things:
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
	def die(self):
		kill(self)

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
	def die(self):
		self.alive = False

class Lifetime(Component):
	def __init__(self, lifetime = 1):
		self.lifetime = lifetime
		self.flife = 0
	def think(self, dt):
		if self.t > self.lifetime:
			self.alive = False
		self.flife = math.clamp(self.t / self.lifetime, 0, 1)

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

class DropsDown(Component):
	def __init__(self, dropay = 10):
		self.dropay = dropay
	def think(self, dt):
		self.vy -= self.dropay * dt

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

class DrawHiddenImage(Component):
	def __init__(self, imgname, imgr = 1):
		self.imgname = imgname
		self.imgr = imgr
	def init(self, tvisible = 0, **kwargs):
		self.tvisible = tvisible
	def dump(self, obj):
		obj["tvisible"] = self.tvisible
	def isvisible(self):
		for obj in state.beacons:
			if window.distance(obj, self) < settings.beacondetect:
				return True
		return False		
	def think(self, dt):
		if self.isvisible():
			self.tvisible += dt
		else:
			self.tvisible = 0
	def draw(self):
		if self.y <= 0:
			return
		if not self.isvisible():
			return
		alpha = min(self.tvisible, 0.5 * math.sin(self.t))
		image.worlddraw(self.imgname, self.X, self.y, self.imgr, alpha = alpha)

class DrawImageOverParent(Component):
	def __init__(self, imgname, imgr = 1):
		self.imgname = imgname
		self.imgr = imgr
	def init(self, parentid = None, **kwargs):
		self.parentid = parentid
	def dump(self, obj):
		obj["parentid"] = self.parentid
	def think(self, dt):
		if get(self.parentid) is state.you:
			self.alive = False
	def draw(self):
		parent = get(self.parentid)
		image.worlddraw(self.imgname, parent.X, parent.y, self.imgr)

class LeavesCorpse(Component):
	def die(self):
		corpse = Corpse(X = self.X, y = self.y, vx = self.vx, vy = self.vy,
			imgname = self.imgname, imgr = self.imgr)
		add(corpse)
		state.effects.append(corpse)

class DrawCorpse(Component):
	def init(self, imgname = None, imgr = None, imgomega = None, **kwargs):
		self.imgname = imgname
		self.imgr = imgr
		self.imgomega = random.uniform(4, 8) * random.choice([-1, 1]) if imgomega is None else imgomega
	def dump(self, obj):
		obj["imgname"] = self.imgname
		obj["imgr"] = self.imgr
		obj["imgomega"] = self.imgomega
	def draw(self):
		if self.y <= 0:
			return
		image.worlddraw(self.imgname, self.X, self.y, self.imgr, angle = self.imgomega * self.t,
			alpha = 1 - self.flife)

class DrawTremor(Component):
	def __init__(self):
		self.nimgs = 20
		self.timg = 1.5
	def init(self, imgs = None, **kwargs):
		self.imgs = imgs or []
	def dump(self, obj):
		obj["imgs"] = self.imgs
	def think(self, dt):
		while self.imgs and self.t - self.imgs[0][2] > self.timg:
			self.imgs.pop(0)
		while len(self.imgs) < self.nimgs:
			st = self.timg / 2
			X = random.gauss(self.X + self.vx * st / self.y, 2 / self.y)
			y = random.gauss(self.y + self.vy * st, 2)
			t = self.t - (self.nimgs - len(self.imgs) - 1) * self.timg / self.nimgs
			self.imgs.append((X, y, t))
	def draw(self):
		for X, y, t in self.imgs:
			t = (self.t - t) / self.timg
			if not 0 < t < 1:
				continue
			alpha = t * (1 - t)
			image.worlddraw("tremor", X, y, 6, rotate = False, alpha = alpha)

# Whether the object is important to the plot, and should not be discarded if it's offscreen.
class HasSignificance(Component):
	def init(self, significant = False, **kwargs):
		self.significant = significant
	def dump(self, obj):
		obj["significant"] = self.significant


class IgnoresNetwork(Component):
	def rnetwork(self):
		return 0

class CanDeploy(Component):
	def init(self, deployed = False, **kwargs):
		self.deployed = deployed
	def dump(self, obj):
		obj["deployed"] = self.deployed
	def deploy(self):
		self.deployed = not self.deployed
		self.significant = self.deployed
		sound.play("chirpup" if self.deployed else "chirpdown")

class CantDeploy(Component):
	def deploy(self):
		sound.play("splat")

class DeployFreeze(Component):
	def think(self, dt):
		if self.deployed:
			self.vx = self.vy = 0

# Freezes in place when deployed
class DeployComm(Component):
	def __init__(self, networkreach = 20):
		self.networkreach = networkreach
	def deploy(self):
		state.buildnetwork()
	def rnetwork(self):
		return self.networkreach if self.deployed else 0
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

class BeaconDeploy(Component):
	def deploy(self):
		if self in state.beacons:
			state.beacons.remove(self)
		if self.deployed:
			state.beacons.append(self)
		state.buildnetwork()

class DrawGoalArrows(Component):
	def draw(self):
		if not self.deployed:
			return
		px0, py0 = window.screenpos(self.X, self.y)
		for obj in state.goals:
			dx = math.Xmod(obj.X - self.X) * (self.y + obj.y) / 2
			dy = obj.y - self.y
			d = math.sqrt(dx ** 2 + dy ** 2)
			if d < 8:
				continue
			dx /= d
			dy /= d
			px = px0 + int(window.camera.R * 2 * dx)
			py = py0 - int(window.camera.R * 2 * dy)
			pygame.draw.circle(window.screen, (0, 0, 255), (px, py), F(2))


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
@DrawHiddenImage("payload")
class Payload(WorldThing):
	pass

@EmptyDrawHUD()
@HasSignificance()
@LeavesCorpse()
class Ship(WorldThing):
	pass

@HasMaximumHorizontalVelocity(6)
@HasMaximumVerticalVelocity(6)
@DrawImage("trainer")
@IgnoresNetwork()
class Trainer(Ship):
	pass

@Drifts()
# @FeelsLinearDrag(3)
@HasMaximumHorizontalVelocity(20)
@VerticalWeight(1)
@HasMaximumVerticalVelocity(10)
@DrawImage("skiff")
@IgnoresNetwork()
@CantDeploy()
class Skiff(Ship):
	pass

@Drifts()
@HasMaximumHorizontalVelocity(6)
@VerticalWeight(3)
@HasMaximumVerticalVelocity(3)
@DrawImage("beacon")
@IgnoresNetwork()
@DrawGoalArrows()
@DrawMinimap()
@CanDeploy()
@DeployFreeze()
@BeaconDeploy()
class Beacon(Ship):
	pass

@Drifts()
@HasMaximumHorizontalVelocity(6)
@VerticalWeight(2)
@HasMaximumVerticalVelocity(4)
@DrawImage("comm")
@CanDeploy()
@DeployFreeze()
@DeployComm()
class CommShip(Ship):
	pass

@MovesCircularWithConstantSpeed(8, 0.2)
@DrawTremor()
class Tremor(WorldThing):
	pass

@DrawImage("mother", 4)
@IgnoresNetwork()
class Mother(WorldThing):
	pass


@Laddered()
@DrawFilament()
class Filament(Thing):
	pass

@Lifetime(1)
@DropsDown(10)
@DrawCorpse()
class Corpse(WorldThing):
	pass

@DrawImage("target")
class Target(WorldThing):
	pass

@Alive()
@DrawImageOverParent("starget", 2)
class ShipTarget(Thing):
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


