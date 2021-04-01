import os, pickle, random
from . import settings, progress


currentlevel = "empty"
bugs = []
spawners = []
trees = []
rings = []
grid0 = []
taken = set()
grid = {}

def canbuildat(pH):
	return pH in grid0 and pH not in taken

def resettaken():
	from . import view
	taken.clear()
	for tree in trees:
		for pH in view.HsurroundH(tree.pH, 1):
			taken.add(pH)
	for spawner in spawners:
		taken.add(spawner.pH)
	for ring in rings:
		for pH in ring.tiles:
			taken.add(pH)
def addtree(tree):
	from . import view
	trees.append(tree)
	grid[tree.pH] = tree
	for pH in view.HsurroundH(tree.pH, 1):
		taken.add(pH)
def addspawner(spawner):
	spawners.append(spawner)
	grid[spawner.pH] = spawner
	taken.add(spawner.pH)
def addring(ring):
	rings.append(ring)
	for pH in ring.tiles:
		grid[pH] = ring
		taken.add(pH)
def removetree(pH):
	trees.remove(treeat(pH))
	del grid[pH]
	resettaken()
def removespawner(pH):
	spawners.remove(spawnerat(pH))
	del grid[pH]
	resettaken()
def removering(pH):
	ring = ringat(pH)
	for tile in ring.tiles:
		del grid[tile]
	rings.remove(ring)
	resettaken()

def objat(pH, objtype):
	if pH in grid and isinstance(grid[pH], objtype):
		return grid[pH]
	return None

def treeat(pH):
	from . import thing
	return objat(pH, thing.Tree)

def ringat(pH):
	from . import thing
	return objat(pH, thing.Ring)

def spawnerat(pH):
	from . import thing
	return objat(pH, thing.Spawner)

def empty(pH):
	return treeat(pH) is None and ringat(pH) is None and spawnerat(pH) is None


def save():
	obj = currentlevel, bugs, spawners, trees, rings, progress.getstate()
	pickle.dump(obj, open(settings.savename, "wb"))

def load():
	global currentlevel, bugs, spawners, trees, rings
	if os.path.exists(settings.savename):
		currentlevel, bugs, spawners, trees, rings, pstate = pickle.load(open(settings.savename, "rb"))
		progress.setstate(pstate)


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
	from . import view, thing
	grid0[:] = view.Hfill(R)
	taken.clear()
	grid.clear()
	del rings[:]
	for ring in spec["rings"]:
		addring(thing.Ring(**ring))
	del spawners[:]
	for spawner in spec["spawners"]:
		addspawner(thing.Spawner(**spawner))
	del trees[:]
	for tree in spec["trees"]:
		raise ValueError
	del bugs[:]




