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

@HasId()
@HasType()
@WorldBound()
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


