from src.enco import Component

things = {}
nextthingid = 1

def add(thing):
	things[thing.thingid] = thing
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

# Base class for things
@HasId()
@HasType()
class Thing(object):
	def __init__(self, **kwargs):
		self.init(**kwargs)


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


