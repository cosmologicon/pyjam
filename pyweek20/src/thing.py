import math
from src import window, image
from src.enco import Component

things = {}
nextthingid = 1

def add(thing):
	things[thing.thingid] = thing
	return thing.thingid
def get(thingid):
	return things[thingid]
def kill(thingid):
	del things[thingid]
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

class WorldBound(Component):
	def init(self, X = 0, y = 0, **kwargs):
		self.X = X
		self.y = y
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

class DrawImage(Component):
	def __init__(self, imgname):
		self.imgname = imgname
	def draw(self):
		img = image.get(self.imgname)
		rect = img.get_rect(center = self.screenpos())
		window.screen.blit(img, rect)

# Base class for things
@HasId()
@HasType()
class Thing(object):
	def __init__(self, **kwargs):
		self.init(**kwargs)
		add(self)

@HasId()
@HasType()
@WorldBound()
@HasVelocity()
# @FeelsLinearDrag(3)
@HasMaximumHorizontalVelocity(20)
@DrawImage("skiff")
class Skiff(Thing):
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


