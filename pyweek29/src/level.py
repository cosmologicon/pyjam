import random, json, math
from . import state, thing, progress, view

leveldata = {
	"learnguide": {"w": 3, "h": 5, "goal": [{"x": 1, "y": 4}, {"x": 1, "y": 2}, {"x": 0, "y": 3}], "flow": [{"x": 2, "y": 3, "ds": [[0, 1]], "guidable": True}, {"x": 2, "y": 1, "ds": [[0, 1]], "guidable": True}, {"x": 0, "y": 2, "ds": [[1, 1]], "guidable": True}]},


	"crowd": {"w": 6, "h": 5, "goal": [{"x": 2, "y": 4}, {"x": 5, "y": 3}, {"x": 1, "y": 2}], "flow": [{"x": 1, "y": 1, "ds": [[1, 1]]}, {"x": 0, "y": 4, "ds": [[1, -1]]}, {"x": 1, "y": 4, "ds": [[-1, 0], [1, 0], [0, -1]]}, {"x": 3, "y": 4, "ds": [[-1, -1], [1, -1]]}, {"x": 4, "y": 4, "ds": [[-1, 0], [1, -1]]}, {"x": 5, "y": 4, "ds": [[-1, 1]]}, {"x": 0, "y": 3, "ds": [[1, 1], [1, 0]]}, {"x": 1, "y": 3, "ds": [[-1, -1]]}, {"x": 2, "y": 3, "ds": [[-1, -1], [1, -1]]}, {"x": 3, "y": 3, "ds": [[1, 1]]}, {"x": 4, "y": 3, "ds": [[1, 1], [-1, 1]]}, {"x": 5, "y": 2, "ds": [[-1, 1]]}, {"x": 4, "y": 2, "ds": [[-1, 1], [1, 0]]}, {"x": 3, "y": 2, "ds": [[1, 0]]}, {"x": 2, "y": 2, "ds": [[-1, 1]]}, {"x": 0, "y": 2, "ds": [[0, 1], [0, -1]]}, {"x": 0, "y": 1, "ds": [[1, 0]]}, {"x": 2, "y": 1, "ds": [[1, 1]]}, {"x": 3, "y": 1, "ds": [[-1, 1], [1, 0]]}, {"x": 4, "y": 1, "ds": [[1, 1]]}, {"x": 5, "y": 1, "ds": [[0, 1], [-1, 0]]}]},


	"test": {'w': 9, 'h': 3, 'goal': [{'x': 4, 'y': 1}, {'x': 4, 'y': 2}], 'flow': [{'x': 0, 'y': 1, 'ds': [(0, 1), (1, 1)], 'guidable': False}, {'x': 5, 'y': 1, 'ds': [(0, 1), (1, 1)], 'guidable': True}], 'spin': [{'x': 1, 'y': 1, 'guidable': False}, {'x': 6, 'y': 1, 'guidable': True}], 'boost': [{'x': 2, 'y': 1, 'ds': [(1, 0), (0, 1)], 'guidable': False}, {'x': 7, 'y': 1, 'ds': [(-1, 0), (0, 1)], 'guidable': True}], 'continue': [{'x': 3, 'y': 1, 'guidable': False}, {'x': 8, 'y': 1, 'guidable': True}]},


	# Rook motion only
	"tutorial1": {'w': 3, 'h': 4, 'goal': [{'x': 0, 'y': 2}, {'x': 0, 'y': 3}, {'x': 2, 'y': 2}], 'flow': [{'x': 0, 'y': 1, 'ds': [(0, 1)], 'guidable': False}, {'x': 1, 'y': 1, 'ds': [(0, 1)], 'guidable': False}, {'x': 1, 'y': 2, 'ds': [(1, 0), (0, 1)], 'guidable': False}, {'x': 1, 'y': 3, 'ds': [(-1, 0)], 'guidable': False}], 'spin': [], 'boost': [], 'continue': []},
	# Pawn motion only
	"tutorial2": {'w': 5, 'h': 5, 'goal': [{'x': 3, 'y': 4}, {'x': 2, 'y': 4}, {'x': 1, 'y': 4}], 'flow': [{'x': 1, 'y': 1, 'ds': [(1, 1), (-1, 1)], 'guidable': False}, {'x': 2, 'y': 1, 'ds': [(1, 1), (-1, 1)], 'guidable': False}, {'x': 3, 'y': 1, 'ds': [(1, 1), (-1, 1)], 'guidable': False}, {'x': 4, 'y': 2, 'ds': [(-1, 1)], 'guidable': False}, {'x': 3, 'y': 2, 'ds': [(1, 1), (-1, 1)], 'guidable': False}, {'x': 2, 'y': 2, 'ds': [(1, 1), (-1, 1)], 'guidable': False}, {'x': 1, 'y': 2, 'ds': [(-1, 1), (1, 1)], 'guidable': False}, {'x': 0, 'y': 2, 'ds': [(1, 1)], 'guidable': False}, {'x': 0, 'y': 3, 'ds': [(1, 1)], 'guidable': False}, {'x': 1, 'y': 3, 'ds': [(-1, 1), (1, 1)], 'guidable': False}, {'x': 2, 'y': 3, 'ds': [(-1, 1), (1, 1)], 'guidable': False}, {'x': 3, 'y': 3, 'ds': [(-1, 1), (1, 1)], 'guidable': False}, {'x': 4, 'y': 3, 'ds': [(-1, 1)], 'guidable': False}], 'spin': [], 'boost': [], 'continue': []},
	# Tower
	"tutorial3": {'w': 4, 'h': 14, 'goal': [{'x': 2, 'y': 13}, {'x': 3, 'y': 5}, {'x': 2, 'y': 10}], 'flow': [{'x': 1, 'y': 1, 'ds': [(0, 1)], 'guidable': False}, {'x': 1, 'y': 2, 'ds': [(-1, 1)], 'guidable': False}, {'x': 0, 'y': 3, 'ds': [(1, 1)], 'guidable': False}, {'x': 1, 'y': 4, 'ds': [(1, 1)], 'guidable': False}, {'x': 2, 'y': 5, 'ds': [(0, 1)], 'guidable': False}, {'x': 2, 'y': 6, 'ds': [(1, 1)], 'guidable': False}, {'x': 3, 'y': 7, 'ds': [(-1, 1)], 'guidable': False}, {'x': 2, 'y': 8, 'ds': [(0, 1)], 'guidable': False}, {'x': 2, 'y': 9, 'ds': [(-1, 1)], 'guidable': False}, {'x': 1, 'y': 10, 'ds': [(-1, 1)], 'guidable': False}, {'x': 0, 'y': 11, 'ds': [(1, 1)], 'guidable': False}, {'x': 1, 'y': 12, 'ds': [(1, 1)], 'guidable': False}, {'x': 2, 'y': 1, 'ds': [(1, 1)], 'guidable': False}, {'x': 3, 'y': 2, 'ds': [(-1, 1)], 'guidable': False}, {'x': 2, 'y': 3, 'ds': [(0, 1)], 'guidable': False}, {'x': 2, 'y': 4, 'ds': [(-1, 1)], 'guidable': False}, {'x': 1, 'y': 5, 'ds': [(-1, 1)], 'guidable': False}, {'x': 0, 'y': 6, 'ds': [(1, 1)], 'guidable': False}, {'x': 1, 'y': 7, 'ds': [(-1, 1), (1, 0)], 'guidable': False}, {'x': 2, 'y': 7, 'ds': [(1, -1)], 'guidable': False}, {'x': 3, 'y': 6, 'ds': [(0, -1)], 'guidable': False}, {'x': 0, 'y': 8, 'ds': [(1, 1)], 'guidable': False}, {'x': 1, 'y': 9, 'ds': [(1, 1)], 'guidable': False}], 'spin': [], 'boost': [], 'continue': []},
	# Guiding
	"tutorial4": {'w': 3, 'h': 4, 'goal': [{'x': 2, 'y': 3}, {'x': 1, 'y': 3}, {'x': 0, 'y': 3}], 'flow': [{'x': 0, 'y': 1, 'ds': [(1, 1)], 'guidable': False}, {'x': 1, 'y': 1, 'ds': [(1, 1), (-1, 1)], 'guidable': False}, {'x': 2, 'y': 1, 'ds': [(-1, 1)], 'guidable': False}, {'x': 2, 'y': 2, 'ds': [(0, 1)], 'guidable': True}], 'spin': [], 'boost': [], 'continue': []},

 

	# Continue
	"D0": {'w': 5, 'h': 4, 'goal': [{'x': 0, 'y': 3}, {'x': 2, 'y': 2}, {'x': 4, 'y': 2}], 'flow': [{'x': 0, 'y': 1, 'ds': [(1, 1)], 'guidable': False}, {'x': 1, 'y': 1, 'ds': [(0, 1)], 'guidable': False}, {'x': 2, 'y': 1, 'ds': [(-1, 1), (1, 1)], 'guidable': False}, {'x': 2, 'y': 3, 'ds': [(-1, -1), (1, -1)], 'guidable': False}, {'x': 4, 'y': 1, 'ds': [(-1, 0)], 'guidable': False}], 'spin': [], 'boost': [], 'continue': [{'x': 3, 'y': 2, 'guidable': False}, {'x': 3, 'y': 1, 'guidable': False}, {'x': 1, 'y': 2, 'guidable': False}]},
	"D1": {'w': 5, 'h': 7, 'goal': [{'x': 0, 'y': 3}, {'x': 1, 'y': 6}, {'x': 0, 'y': 5}], 'flow': [{'x': 2, 'y': 1, 'ds': [(0, 1)], 'guidable': False}, {'x': 1, 'y': 2, 'ds': [(1, 1), (1, -1)], 'guidable': False}, {'x': 3, 'y': 2, 'ds': [(-1, -1), (-1, 1)], 'guidable': False}, {'x': 2, 'y': 2, 'ds': [(0, 1), (-1, 1), (1, 1)], 'guidable': False}, {'x': 1, 'y': 3, 'ds': [(-1, 1), (1, 0), (0, -1)], 'guidable': False}, {'x': 0, 'y': 4, 'ds': [(1, 0)], 'guidable': False}, {'x': 1, 'y': 5, 'ds': [(-1, 1), (1, 0)], 'guidable': False}, {'x': 2, 'y': 6, 'ds': [(1, 0), (-1, -1)], 'guidable': False}, {'x': 3, 'y': 5, 'ds': [(-1, 0), (1, 0)], 'guidable': False}, {'x': 3, 'y': 6, 'ds': [(-1, -1), (0, -1)], 'guidable': False}, {'x': 4, 'y': 5, 'ds': [(-1, 0), (0, 1)], 'guidable': False}, {'x': 4, 'y': 4, 'ds': [(-1, 1), (0, 1), (0, -1)], 'guidable': False}, {'x': 4, 'y': 3, 'ds': [(-1, 1), (0, -1)], 'guidable': False}, {'x': 3, 'y': 3, 'ds': [(0, 1), (0, -1)], 'guidable': False}], 'spin': [], 'boost': [], 'continue': [{'x': 2, 'y': 3, 'guidable': False}, {'x': 1, 'y': 4, 'guidable': False}, {'x': 2, 'y': 4, 'guidable': False}, {'x': 3, 'y': 4, 'guidable': False}, {'x': 2, 'y': 5, 'guidable': False}]},
	# Continue guide
	"D2": {'w': 5, 'h': 7, 'goal': [{'x': 1, 'y': 6}, {'x': 2, 'y': 6}, {'x': 3, 'y': 6}], 'flow': [{'x': 1, 'y': 1, 'ds': [(1, 1)], 'guidable': False}, {'x': 0, 'y': 2, 'ds': [(0, 1)], 'guidable': False}, {'x': 1, 'y': 3, 'ds': [(1, 1)], 'guidable': False}, {'x': 2, 'y': 3, 'ds': [(-1, 1)], 'guidable': False}, {'x': 3, 'y': 2, 'ds': [(0, 1)], 'guidable': False}, {'x': 4, 'y': 2, 'ds': [(-1, 1)], 'guidable': False}, {'x': 3, 'y': 4, 'ds': [(-1, 1)], 'guidable': False}, {'x': 3, 'y': 5, 'ds': [(0, 1)], 'guidable': False}, {'x': 1, 'y': 5, 'ds': [(1, 1)], 'guidable': False}], 'spin': [], 'boost': [], 'continue': [{'x': 2, 'y': 2, 'guidable': True}, {'x': 4, 'y': 4, 'guidable': True}, {'x': 0, 'y': 3, 'guidable': True}]},


	# Spin
	"C0": {'w': 5, 'h': 4, 'goal': [{'x': 2, 'y': 3}, {'x': 4, 'y': 2}, {'x': 0, 'y': 2}], 'flow': [], 'spin': [{'x': 1, 'y': 1, 'guidable': False}, {'x': 2, 'y': 1, 'guidable': False}, {'x': 3, 'y': 1, 'guidable': False}, {'x': 2, 'y': 2, 'guidable': False}], 'boost': [], 'continue': []},
	# Spin chimney
	"C1": {'w': 5, 'h': 6, 'goal': [{'x': 2, 'y': 5}, {'x': 0, 'y': 4}, {'x': 4, 'y': 4}], 'flow': [{'x': 1, 'y': 4, 'ds': [(1, -1), (-1, -1)], 'guidable': False}, {'x': 1, 'y': 3, 'ds': [(-1, -1)], 'guidable': False}, {'x': 1, 'y': 2, 'ds': [(1, -1)], 'guidable': False}, {'x': 3, 'y': 4, 'ds': [(1, -1), (-1, -1)], 'guidable': False}, {'x': 3, 'y': 3, 'ds': [(-1, -1)], 'guidable': False}, {'x': 3, 'y': 2, 'ds': [(1, -1)], 'guidable': False}], 'spin': [{'x': 0, 'y': 1, 'guidable': True}, {'x': 1, 'y': 1, 'guidable': True}, {'x': 2, 'y': 1, 'guidable': True}, {'x': 3, 'y': 1, 'guidable': True}, {'x': 4, 'y': 1, 'guidable': True}], 'boost': [], 'continue': []},


	# Boost
	"A0": {'w': 5, 'h': 8, 'goal': [{'x': 1, 'y': 7}, {'x': 2, 'y': 7}, {'x': 3, 'y': 7}], 'flow': [], 'spin': [], 'boost': [{'x': 1, 'y': 1, 'ds': [(1, 1)], 'guidable': False}, {'x': 2, 'y': 1, 'ds': [(-1, 1)], 'guidable': False}, {'x': 3, 'y': 1, 'ds': [(1, 1)], 'guidable': False}, {'x': 4, 'y': 3, 'ds': [(-1, 1), (0, 1)], 'guidable': False}, {'x': 3, 'y': 3, 'ds': [(-1, 0), (0, 1)], 'guidable': False}, {'x': 2, 'y': 3, 'ds': [(1, 1)], 'guidable': False}, {'x': 1, 'y': 3, 'ds': [(0, 1)], 'guidable': False}, {'x': 0, 'y': 3, 'ds': [(1, 0)], 'guidable': False}, {'x': 0, 'y': 5, 'ds': [(1, 1), (1, 0)], 'guidable': False}, {'x': 1, 'y': 5, 'ds': [(1, 1)], 'guidable': False}, {'x': 2, 'y': 5, 'ds': [(0, 1)], 'guidable': False}, {'x': 3, 'y': 5, 'ds': [(-1, 1)], 'guidable': False}, {'x': 4, 'y': 5, 'ds': [(-1, 0)], 'guidable': False}], 'continue': []},
	"A1": {'w': 5, 'h': 8, 'goal': [{'x': 2, 'y': 4}, {'x': 2, 'y': 5}, {'x': 1, 'y': 3}], 'flow': [{'x': 3, 'y': 2, 'ds': [(0, 1)], 'guidable': False}, {'x': 1, 'y': 2, 'ds': [(1, 0)], 'guidable': False}, {'x': 2, 'y': 7, 'ds': [(-1, -1), (1, -1)], 'guidable': False}], 'spin': [], 'boost': [{'x': 2, 'y': 1, 'ds': [(0, 1)], 'guidable': False}, {'x': 2, 'y': 2, 'ds': [(-1, 1), (1, 1)], 'guidable': False}, {'x': 2, 'y': 3, 'ds': [(-1, 1), (1, 1)], 'guidable': False}, {'x': 2, 'y': 6, 'ds': [(0, -1)], 'guidable': False}, {'x': 3, 'y': 6, 'ds': [(-1, -1)], 'guidable': False}, {'x': 3, 'y': 5, 'ds': [(-1, 0), (0, -1)], 'guidable': False}, {'x': 3, 'y': 4, 'ds': [(0, 1), (-1, 0), (-1, -1)], 'guidable': False}, {'x': 4, 'y': 5, 'ds': [(-1, 1), (0, -1)], 'guidable': False}, {'x': 4, 'y': 4, 'ds': [(-1, 1), (-1, -1)], 'guidable': False}, {'x': 4, 'y': 3, 'ds': [(-1, 1), (-1, 0)], 'guidable': False}, {'x': 3, 'y': 3, 'ds': [(0, 1), (-1, -1)], 'guidable': False}, {'x': 1, 'y': 4, 'ds': [(0, 1), (1, 0), (1, -1)], 'guidable': False}, {'x': 1, 'y': 5, 'ds': [(1, 0), (0, -1)], 'guidable': False}, {'x': 1, 'y': 6, 'ds': [(1, -1)], 'guidable': False}, {'x': 0, 'y': 5, 'ds': [(1, 1), (0, -1)], 'guidable': False}, {'x': 0, 'y': 4, 'ds': [(1, 1), (1, -1)], 'guidable': False}, {'x': 0, 'y': 3, 'ds': [(1, 1), (1, 0)], 'guidable': False}], 'continue': []},
	"A2": {'w': 5, 'h': 10, 'goal': [{'x': 3, 'y': 9}, {'x': 2, 'y': 9}, {'x': 1, 'y': 9}], 'flow': [{'x': 0, 'y': 1, 'ds': [(1, -1)], 'guidable': False}, {'x': 4, 'y': 1, 'ds': [(-1, -1)], 'guidable': False}, {'x': 4, 'y': 3, 'ds': [(-1, 1)], 'guidable': False}, {'x': 3, 'y': 3, 'ds': [(1, 1)], 'guidable': False}, {'x': 1, 'y': 3, 'ds': [(-1, 1)], 'guidable': False}, {'x': 0, 'y': 3, 'ds': [(1, 1)], 'guidable': False}, {'x': 1, 'y': 6, 'ds': [(1, 1)], 'guidable': False}, {'x': 2, 'y': 6, 'ds': [(-1, 1)], 'guidable': False}, {'x': 3, 'y': 6, 'ds': [(1, 1)], 'guidable': False}], 'spin': [], 'boost': [{'x': 1, 'y': 1, 'ds': [(-1, 1)], 'guidable': True}, {'x': 2, 'y': 1, 'ds': [(0, 1)], 'guidable': True}, {'x': 3, 'y': 1, 'ds': [(1, 1)], 'guidable': True}], 'continue': []}
,

}

levelnames = {
	"tutorial1": "Miranda's backyard",
	"tutorial4": "The Ministry of Insects",
	"nexus": "Nexus Point",
	"finale0": "Crash site of the RSS Argus",
	"finale1": "The Eldritch Vortex",
}
def currentname():
	return levelnames.get(progress.at, progress.at)


def load():
	state.thang0 = 0.7
	state.thang = 4
	state.maxleaps = 1
	state.ngoal = 0
	state.you = thing.You()
	state.guided = None
	state.goals = []
	state.yfloor = 0
	state.jspin = 0
	state.ychecks = []
	state.panel = progress.at != "finale1"

#	randomlevel()
#	levelspin()
	if progress.at == "nexus":
		loadnexus()
	elif progress.at == "finale1":
		randomlevel()
	else:
		loaddata(leveldata[progress.at])
	state.ngoal = sum(isinstance(lep, thing.GoalLep) for lep in state.leps)
	state.leaps = state.maxleaps
	view.zoom = 224 if state.w <= 3 else 144
	if state.w == 7 and not state.panel:
		view.zoom = 180

def loaddata(data):
	state.leps = []
	state.w = data["w"]
	state.h = data["h"]
	for spec in data["goal"]:
		state.leps.append(thing.GoalLep((spec["x"], spec["y"])))
	for spec in data["flow"]:
		ds = [tuple(d) for d in spec["ds"]]
		lep = thing.FlowLep((spec["x"], spec["y"]), ds)
		lep.guidable = spec["guidable"]
		state.leps.append(lep)
	for spec in data["spin"]:
		lep = thing.SpinLep((spec["x"], spec["y"]))
		lep.guidable = spec["guidable"]
		state.leps.append(lep)
	for spec in data["boost"]:
		ds = [tuple(d) for d in spec["ds"]]
		lep = thing.BoostLep((spec["x"], spec["y"]), ds)
		lep.guidable = spec["guidable"]
		state.leps.append(lep)
	for spec in data["continue"]:
		lep = thing.ContinueLep((spec["x"], spec["y"]))
		lep.guidable = spec["guidable"]
		state.leps.append(lep)

def loadnexus():
	state.w = 5
	state.h = 14
	state.leps = []
	if "A2" in progress.beaten:  # Boost
		ds = [(-1, 1), (1, 1)]
		for p in [(1, 1), (3, 1)]:
			state.leps.append(thing.BoostLep(p, ds))
	if "C1" in progress.beaten:  # Spin
		for p in [(0, 2), (2, 1), (2, 2), (4, 2)]:
			state.leps.append(thing.SpinLep(p))
	if "D2" in progress.beaten:  # Continue
		for p in [(0, 1), (1, 2), (3, 2), (4, 1)]:
			state.leps.append(thing.ContinueLep(p))
	for lep in state.leps:
		lep.guidable = True
	for y in (5, 9, 13):
		state.leps.append(thing.GoalLep((2, y)))

def checkpoint():
	if not state.ychecks:
		return
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

def levelcrowd():
	state.w = 6
	state.h = 4
	state.leps = [
		thing.FlowLep((0, 4), [(1, -1)]),
		thing.FlowLep((2, 1), [(0, 1)]),
		thing.FlowLep((3, 3), [(0, 1)]),
		thing.GoalLep((1, 4)),
	]


def levelspin():
	state.w = 4
	state.h = 6
	state.leps = [
		thing.FlowLep((1, 1), [(0, 1)]),
		thing.FlowLep((1, 2), [(-1, 0), (1, 1)]),
		thing.FlowLep((2, 5), [(-1, 0)]),
		thing.FlowLep((3, 2), [(0, 1)]),
		thing.SpinLep((0, 2)),
		thing.SpinLep((2, 3)),
		thing.SpinLep((3, 3)),
		thing.SpinLep((3, 4)),
		thing.SpinLep((1, 5)),
		thing.GoalLep((0, 4)),
	]

allds = (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0)

def fill(ys):
	ys = list(ys)
	

def randompath(p0, p1, xmax):
	x0, y0 = p0
	x1, y1 = p1
	dx = x1 - x0
	dy = y1 - y0
	assert abs(dx) <= abs(dy)
	if not dx and not dy:
		return []
	if abs(dy) <= 1:
		return [p1]
	f = random.choice([math.Phi, 1 - math.Phi])
	xmid = math.imix(x0, x1, f)
	ymid = math.imix(y0, y1, f)
	nsteps = min(abs(y0 - ymid) - abs(x0 - xmid), abs(y1 - ymid) - abs(x1 - xmid))
	for _ in range(nsteps):
		dx = random.choice((-1, -1, -1, 0, 1, 1, 1))
		if 0 <= xmid + dx < xmax:
			xmid += dx
	return randompath(p0, (xmid, ymid), xmax) + randompath((xmid, ymid), p1, xmax)
		
def randomds(rfactor = 0.5, d0 = None):
	ds = { random.choice(allds) }
	while random.random() < rfactor:
		ds.add(random.choice(allds))
	if d0 is not None:
		ds.add(d0)
	return sorted(ds)



def randomlevel():
#	state.ychecks = 15, 30, 50, 80, 119
#	state.ychecks = 3, 7, 11
	state.ychecks = 20, 50, 90
	state.w = 7
	state.h = state.ychecks[0] + 1
#	state.maxleaps = 1
	state.leps = []
	xs = list(range(state.w))
	for y in state.ychecks:
		x = 3
		state.leps.append(thing.GoalLep((x, y)))

	ys = [y for y in range(1, max(state.ychecks) + 1) if y not in state.ychecks]
	for y in ys:
#		if y % 3 == 0:
#			x = random.choice([x for x in xs if not state.lepat((x, y))])
#			state.leps.append(thing.ChargeLep((x, y)))

		x = random.choice([x for x in xs if not state.lepat((x, y))])
		state.leps.append(thing.BoostLep((x, y), randomds(0.4)))

		x = random.choice([x for x in xs if not state.lepat((x, y))])
		state.leps.append(thing.SpinLep((x, y)))

		x = random.choice([x for x in xs if not state.lepat((x, y))])
		state.leps.append(thing.ContinueLep((x, y)))
		
		for x in range(state.w):
			if state.lepat((x, y)):
				continue
			if random.random() < 0.5:
				continue
			lep = thing.FlowLep((x, y), randomds(0.6))
			state.leps.append(lep)

	path = [(3, 1)]
	for ycheck in state.ychecks:
		path += randompath(path[-1], (3, ycheck), 7)
	for j, (x0, y0) in enumerate(path):
		if y0 in state.ychecks:
			continue
		x1, y1 = path[j + 1]
		d = x1 - x0, y1 - y0
		lep = state.lepat((x0, y0))
		if lep:
			if isinstance(lep, thing.FlowLep):
				lep.ds = sorted(set(list(lep.ds) + [d]))
			else:
				state.leps.remove(lep)
				state.leps.append(thing.FlowLep((x0, y0), randomds(0.4, d)))
		else:
			state.leps.append(thing.FlowLep((x0, y0), randomds(0.4, d)))


