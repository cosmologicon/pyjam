import math, random
from . import state, thing, sector, quest

cost = {
	"engine": [5, 10, 20],
	"gravnet": [5, 10, 20],
	"beam": [5, 10, 20],
	"health": [5, 10, 20],
	"energy": [5, 10, 20, 50],
}


def init():
	state.xp = 0
	state.you = thing.You((5, 3))
	state.DMs = []
	state.home = thing.Home((0, 0))
	state.home.unlocked = True
	state.spots = [state.home]
	state.spots += [thing.Spot(spot) for spot in sector.spots if spot != state.home.pos]
	for jspot, (spot, adjs) in enumerate(sector.adjs.items()):
		for jDM in range(10):
			state.DMs += [randomvisitor(spot, adjs, jspot, jDM)]
	for jrock in range(400):
		state.DMs += [randomrock(jrock)]
#	for jrock in range(10):
#		state.DMs += [thing.CircleRock((0, 0), 10 + jrock, 2, 0.5 + 0.1 * jrock)]
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
		"health": -1,
		"energy": -1,
	}
	state.charge = {
		"gravnet": 1,
		"beam": 1,
	}
	state.hp = 3
	state.at = None
	state.homeconvo = None
	state.DMtracker = ThinkTracker(state.DMs)
	state.energy = 1
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
	Nstay = math.fuzzrandint(8, 12, 1.08, *seed)
	reverse = math.fuzzflip(1.09, *seed)
	return thing.Visitor(pos0, pos1, Nstay, Rorbit, v, reverse=reverse)

def randomrock(*seed):
	A0 = math.fuzzrange(0, math.tau, 2.01, *seed)
	r0 = math.fuzzrange(0, 100, 2.02, *seed)
	pos0 = math.CS(A0, r0)
	Rorbit = math.fuzzrange(200, 1000, 2.03, *seed)
	v = math.fuzzrange(5, 10, 2.07, *seed)
	r = math.fuzzrange(0.5, 2, 2.08, *seed)
	reverse = math.fuzzflip(2.09, *seed)
	return thing.CircleRock(pos0, Rorbit, v, r, reverse = reverse)


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

def takedamage(dhp):
	state.hp = math.approach(state.hp, 0, dhp)

def getmaxhp():
	return 3 if state.techlevel["health"] < 0 else [3, 5, 7, 10][state.techlevel["health"]]

def useenergy(denergy):
	state.energy = math.approach(state.energy, 0, denergy)

def getmaxenergy():
	return 0 if state.techlevel["energy"] < 0 else [1, 2, 4, 8][state.techlevel["energy"]]

class ThinkTracker:
	T = 0.5  # All objs should have their think function called at least this often.
	def __init__(self, objs):
		self.objs = objs
		self.t = 0
		self.N = len(self.objs)
		self.lastthink = [0 for obj in self.objs]
		self.isactive = [True for obj in self.objs]
		self.sactive = set(j for j in range(self.N))
		self.active = self.objs
		self.jcheck = 0
	def thinkobj(self, j):
		dt = self.t - self.lastthink[j]
		self.objs[j].think(dt)
		self.lastthink[j] = self.t
		isactive = self.objs[j].isactive(self.T)
		self.isactive[j] = isactive
		return isactive
	def think(self, dt):
		self.t += dt
		jcheck = max(int(self.t * self.N / self.T), self.N)
		if math.fuzzflip(jcheck):
			jcheck += 1
		tocheck = self.sactive | set(j % self.N for j in range(self.jcheck, jcheck))
		toadd, toremove = set(), set()
		for j in tocheck:
			if self.thinkobj(j):
				toadd.add(j)
			else:
				toremove.add(j)
		self.sactive -= toremove
		self.sactive |= toadd
		self.active = [self.objs[j] for j in sorted(self.sactive)]
		self.jcheck = jcheck


