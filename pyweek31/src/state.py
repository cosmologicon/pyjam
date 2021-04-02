import os, pickle, random
from . import settings, progress


currentlevel = "empty"
bugs = []
ghosts = []
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
	from . import view, graphics
	trees.append(tree)
	grid[tree.pH] = tree
	for pH in view.HsurroundH(tree.pH, 1):
		taken.add(pH)
	graphics.addtree(tree)
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
	from . import graphics
	trees.remove(treeat(pH))
	del grid[pH]
	resettaken()
	graphics.shadesurfs.clear()
	for tree in trees:
		graphics.addtree(tree)
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
	obj = currentlevel, bugs, ghosts, spawners, trees, rings, progress.getstate()
	pickle.dump(obj, open(settings.savename, "wb"))

def load():
	global currentlevel, bugs, ghosts, spawners, trees, rings
	if os.path.exists(settings.savename):
		currentlevel, bugs, ghosts, spawners, trees, rings, pstate = pickle.load(open(settings.savename, "rb"))
		progress.setstate(pstate)


# DEBUG functions
def shuffle():
	jcolors = [ring.jcolor for ring in rings]
	random.shuffle(jcolors)
	for jcolor, ring in zip(jcolors, rings):
		ring.jcolor = jcolor

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
	from . import view, thing, graphics
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
	del ghosts[:]
	graphics.shadesurfs.clear()




