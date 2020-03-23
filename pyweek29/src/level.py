import random
from . import state, thing

def load():
	state.thang0 = 0.7
	state.thang = 4
	state.maxleaps = 1
	state.ngoal = 0
	state.you = thing.You()
	state.held = None
	state.goals = []
	state.yfloor = 0

	randomlevel()
	state.ngoal = sum(isinstance(lep, thing.GoalLep) for lep in state.leps)
	state.leaps = state.maxleaps

def checkpoint():
	state.xfloor = state.you.x
	state.yfloor = state.you.y
	if state.h < state.ychecks[-1] + 1:
		state.h = min(y + 1 for y in state.ychecks if y > state.yfloor)
	state.leaps = state.maxleaps

def level1():
	state.w = 4
	state.h = 6
	state.leps = [
		thing.FlowLep((1, 2), [(1, 1)]),
		thing.FlowLep((2, 1), [(0, 1)]),
		thing.FlowLep((3, 3), [(0, 1)]),
		thing.GoalLep((1, 4)),
	]

allds = (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0)

def fill(ys):
	ys = list(ys)
	

def randomlevel():
	state.ychecks = 15, 30, 50, 80, 119
#	state.ychecks = 3, 7, 11
	state.w = 10
	state.h = state.ychecks[0] + 1
	state.maxleaps = 5
	state.leps = []
	xs = list(range(state.w))
	for y in state.ychecks:
		x = random.choice([3, 4, 5, 6])
		state.leps.append(thing.GoalLep((x, y)))
#	fill(range(1, state.ychecks[0]))
	ys = [y for y in range(1, max(state.ychecks) + 1) if y not in state.ychecks]
	for y in ys:
		for x in random.choices(xs, k = 7):
			if state.lepat((x, y)):
				continue
			ds = { random.choice(allds) }
			while random.random() < 0.7:
				ds.add(random.choice(allds))
			r = random.random()
			if r < 0.2:
				lep = thing.BoostLep((x, y))
			elif r < 0.8:
				lep = thing.SlingLep((x, y), ds)
			else:
				lep = thing.ChargeLep((x, y))
			state.leps.append(lep)


