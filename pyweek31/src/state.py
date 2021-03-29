

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

