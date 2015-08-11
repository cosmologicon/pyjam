import json, os.path

worlddata = json.load(open(os.path.join("data", "worlddata.json")))
R = worlddata["R"]
Rcore = worlddata["Rcore"]

you = None
ships = []
objs = []
filaments = []
hazards = []
network = []

goals = []


def buildnetwork():
	from src import thing, window
	del network[:]
	nobjs = [ship.thingid for ship in ships if ship.rnetwork()]
	if len(nobjs) < 2:
		return
	ds = {}
	for id0 in nobjs:
		for id1 in nobjs:
			if id0 >= id1:
				continue
			thing0, thing1 = thing.get(id0), thing.get(id1)
			rmax = max(thing0.rnetwork(), thing1.rnetwork())
			ds[(id0, id1)] = window.distance(thing0, thing1)
	# TODO: remove triangles
	for id0, id1 in ds:
		network.append((thing.get(id0), thing.get(id1)))

