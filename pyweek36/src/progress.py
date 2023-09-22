import math
from . import state, thing, sector, quest

cost = {
	"engine": [5, 10, 20],
	"gravnet": [5, 10, 20],
	"beam": [5, 10, 20],
}


def init():
	state.xp = 0
	state.you = thing.You((10, 6))
	state.DMs = [
#		thing.Orbiter((0, 0), j * math.tau / 3, 0.3, 5, 0.4)
#		for j in range(3)
	]
	state.home = thing.Spot((0, 0))
	state.spots = [state.home]
	state.spots += [thing.Spot(spot) for spot in sector.spots if spot != state.home.pos]
	for jspot, (spot, adjs) in enumerate(sector.adjs.items()):
		for jDM in range(10):
			state.DMs += [randomvisitor(spot, adjs, jspot, jDM)]
	if False:
		for _ in range(100):
			pos0 = math.CS(random.uniform(0, math.tau), random.uniform(0, 50))
			Rorbit = random.uniform(60, 100)
			v = random.uniform(1, 3)
			reverse = random.choice([False, True])
			r = random.uniform(0.4, 1)
			state.DMs += [thing.CircleRock(pos0, Rorbit, v, r, reverse)]
	state.pulses = []
	state.tracers = []
	state.spawners = []
	state.shots = []
	state.techlevel = {
		"count": 0,
		"engine": 0,
		"gravnet": -1,  # Not enabled.
		"beam": -1,
		"drag": -1,  # drag level 2, cannot be set.
	}
	state.charge = {
		"gravnet": 1,
		"beam": 1,
	}
	state.at = None
	state.homeconvo = None
	quest.init()


def randomvisitor(spot, adjs, *seed):
	A0 = math.fuzzrange(0, math.tau, 1.01, *seed)
	r0 = math.fuzzrange(0, 5, 1.02, *seed)
	pos0 = math.CS(A0, r0, spot)
	Rorbit = math.fuzzrange(10, 20, 1.03, *seed)
	adj = math.fuzzchoice(adjs, 1.04, *seed)
	A1 = math.fuzzrange(0, math.tau, 1.05, *seed)
	r1 = math.fuzzrange(0, 5, 1.06, *seed)
	pos1 = math.CS(A1, r1, adj)
	v = math.fuzzrange(1.5, 3, 1.07, *seed)
	Nstay = math.fuzzrandint(10, 20, 1.08, *seed)
	reverse = math.fuzzflip(1.09, *seed)
	return thing.Visitor(pos0, pos1, Nstay, Rorbit, v, reverse=reverse)


def getcost(techname):
	if state.techlevel[techname] <= 0:
		return None
	if state.techlevel[techname] > len(cost[techname]):
		return None
	return cost[techname][state.techlevel[techname] - 1]

def upgrade(techname):
	if techname == "drag":
		state.techlevel["drag"] = (state.techlevel["drag"] + 1) % 5
		return
	if state.techlevel[techname] > 0:
		state.xp -= cost[techname][state.techlevel[techname] - 1]
	state.techlevel[techname] += 1



