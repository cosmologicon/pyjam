import math, random
from . import window, ptext, state, image, settings
from .enco import Component
from .util import F

class WorldBound(Component):
	def __init__(self):
		self.x, self.y, self.z = 0, 0, 0
	def init(self, obj):
		if "pos" in obj:
			self.x, self.y, self.z = obj["pos"]
	def screenpos(self, dz = 0):
		return window.worldtoscreen(self.x, self.y, self.z + dz)

class DrawName(Component):
	def __init__(self, hoverdz = 0):
		self.hoverdz = hoverdz
	def draw(self):
		pos = self.screenpos(dz = self.hoverdz * math.sin(2 * self.t))
		ptext.draw(self.__class__.__name__, center = pos, color = "red", fontsize = F(24), owidth = 1)

class DrawShip(Component):
	def __init__(self, imgname):
		self.imgname = imgname
	def init(self, obj):
		self.hphi0 = random.uniform(0, 100)
		self.homega = random.uniform(1.6, 2.3)
	def draw(self):
		pos = self.screenpos(dz = 0.5 * math.sin(self.homega * self.t + self.hphi0))
		n = settings.shipframes
		frame = int(round(self.angle * n / 360)) % n
		imgname = "data/ships/%s-%04d.png" % (self.imgname, frame + 1)
		image.draw(imgname, pos, scale = 3)
	def drawshadow(self):
		pos = window.worldtoscreen(self.x, self.y, 0)
		image.draw("data/shadow.png", pos, scale = 1)

class FacesForward(Component):
	def __init__(self):
		self.angle = 0
		self.targetangle = 0
		self.omega = 500
	def init(self, obj):
		self.angle = self.targetangle = random.uniform(0, 360)
	def think(self, dt):
		if self.vx or self.vy:
			self.targetangle = math.degrees(math.atan2(self.vx, self.vy)) % 360
		dangle = (self.targetangle - self.angle + 180) % 360 - 180
		if dangle:
			f = abs(dangle / (self.omega * dt))
			if f >= 1:
				self.angle += dangle / f
			else:
				self.angle = self.targetangle

class Rechargeable(Component):
	def __init__(self, needmax):
		self.needmax = needmax
	def init(self, obj):
		self.needs = { k: 0 for k in self.needmax }
		for k, v in obj.items():
			if k.startswith("need"):
				self.needs[k[4:]] = v
	def charge(self, dt, chargerates):
		for k, v in chargerates.items():
			if k in self.needs and self.needs[k] > 0:
				self.needs[k] = max(self.needs[k] - dt * v, 0)
	def draw(self):
		for k, v in self.needs.items():
			if not v:
				continue
			pos = self.screenpos(dz = -1)
			text = "%s: %d/%d" % (k, int(self.needmax[k] - v), self.needmax[k])
			ptext.draw(text, center = pos, color = "yellow", fontsize = F(24), owidth = 1)


class Charges(Component):
	def __init__(self, chargerates):
		self.chargerates = chargerates
	def think(self, dt):
		for building in state.state.buildingsnear(self.x, self.y):
			dx = building.x - self.x
			dy = building.y - self.y
			if dx ** 2 + dy ** 2 < 2 ** 2:
				building.charge(dt, self.chargerates)


class ApproachesTarget(Component):
	def __init__(self, speed = 2):
		self.target = None
		self.speed = speed
		self.vx = 0
		self.vy = 0
	def settarget(self, target):
		self.target = target
	def think(self, dt):
		if not self.target:
			return
		dx = self.target[0] - self.x
		dy = self.target[1] - self.y
		if not dx and not dy:
			self.target = None
			return
		d = self.speed * dt
		f = d / math.sqrt(dx ** 2 + dy ** 2)
		self.vx = f * dx / dt
		self.vy = f * dy / dt
		if f >= 1:
			self.x, self.y = self.target
			self.target = None
		else:
			self.x += f * dx
			self.y += f * dy

class BuildTarget(Component):
	def __init__(self):
		self.btarget = None
	def setbuildtarget(self, btarget):
		self.target = btarget.x, btarget.y
		self.btarget = btarget
	def think(self, dt):
		if self.btarget and not self.target:
			state.state.buildings.append(self.btarget)
			self.btarget = None

@WorldBound()
class Thing(object):
	def __init__(self, **kwargs):
		self.init(kwargs)
		self.t = 0
	def draw(self):
		pass
	def think(self, dt):
		self.t += dt

@ApproachesTarget()
@BuildTarget()
@FacesForward()
@DrawShip("test")
@Charges({"power": 1})
class You(Thing):
	pass

@DrawName()
@Rechargeable({"power": 10})
class Building(Thing):
	brange = 30


