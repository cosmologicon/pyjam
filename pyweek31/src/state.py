import pickle, os, random
from . import settings

bugs = []
spawners = []
trees = []
rings = []

def addtree(tree):
	trees.append(tree)
def addspawner(spawner):
	spawners.append(spawner)
def addring(ring):
	rings.append(ring)


def treeat(pH):
	for tree in trees:
		if tree.pH == pH:
			return tree
	return None

def ringat(pH):
	for ring in rings:
		if pH in ring.tiles:
			return ring
	return None

def spawnerat(pH):
	for spawner in spawners:
		if spawner.pH == pH:
			return spawner
	return None

def empty(pH):
	return treeat(pH) is None and ringat(pH) is None and spawnerat(pH) is None


def save():
	obj = bugs, spawners, trees, rings
	pickle.dump(obj, open(settings.savename, "wb"))

def load():
	global bugs, spawners, trees, rings
	if os.path.exists(settings.savename):
		bugs, spawners, trees, rings = pickle.load(open(settings.savename, "rb"))


# DEBUG functions
def shuffle():
	colors = [settings.colors[j % 3] for j, _ in enumerate(rings)]
	random.shuffle(colors)
	for color, ring in zip(colors, rings):
		ring.color = color
	for spawner in spawners:
		spawner.color = random.choice(settings.colors)

def getspec():
	return {
		"rings": [{
			"pH": ring.pH,
			"rH": ring.rH,
			"jcolor": ring.jcolor,
		} for ring in rings],
		"spawners": [{
			"pH": spawner.pH,
			"spec": spawner.spec,
			"tspawn": spawner.tspawn,
		} for spawner in spawners],
		"trees": [],
	}

def setspec(spec):
	from . import thing
	del rings[:]
	for ring in spec["rings"]:
		rings.append(thing.ChargeRing(**ring))
	del spawners[:]
	for spawner in spec["spawners"]:
		spawners.append(thing.MultiSpawner(**spawner))
	del trees[:]




