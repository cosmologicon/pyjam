import pickle, os
from . import settings

bugs = []
spawners = []
trees = []
rings = []

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
load()


