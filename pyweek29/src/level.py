import random
from . import state, thing

def load():
	state.thang = 1
	state.maxleaps = 1
	state.ngoal = 0
	state.you = thing.You()
	state.held = None

	randomlevel()
	state.leaps = state.maxleaps

def level1():
	state.w = 4
	state.h = 6
	state.leps = [
		thing.Lep((1, 2), [(1, 1)]),
		thing.Lep((2, 1), [(0, 1)]),
		thing.Lep((3, 3), [(0, 1)]),
		thing.GoalLep((1, 4)),
	]

allds = (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0)

def randomlevel():
	state.w = 10
	state.h = 40
	state.maxleaps = 5
	state.leps = []
	for y in range(1, state.h):
#	for y in range(1, 2):
		for x in set(random.choices(list(range(state.w)), k = 3)):
			ds = { random.choice(allds) }
			while random.random() < 0.7:
				ds.add(random.choice(allds))
			r = random.random()
			if r < 0.6:
				lep = thing.FlowLep((x, y), ds)
			elif r < 0.8:
				lep = thing.BoostLep((x, y))
			else:
				lep = thing.SlingLep((x, y), ds)
			state.leps.append(lep)


