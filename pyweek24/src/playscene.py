import random, math
from . import view, pview, state, thing, mist, challenge

def init():
	state.you = thing.You(x = 0, y = 0, z = 0)
	if False:
		state.addhill(thing.Hill(x = 0, y = 0, z = 0, spec = [
			((-10, 0), (40, 0)),
			((-10, -30), (40, -30)),
		]))
		state.addhill(thing.Hill(x = 60, y = 0, z = 0, spec = [
			((-10, -7), (10, -2), (25, 3)),
			((-14, -30), (24, -30)),
		]))
		state.addhill(thing.Hill(x = 100, y = 0, z = -10, spec = [
			((-10, 1), (10, 1)),
			((-10, -30), (10, -30)),
		]))
		state.addhill(thing.Hill(x = 40, y = 0, z = -15, spec = [
			((-10, 20), (-5, 28), (5, 30), (10, 20)),
			((-15, -50), (5, -50)),
		]))
		state.addhill(thing.Hill(x = 130, y = 0, z = 0, spec = [
			((-10, -5), (10, 1)),
			((-10, -30), (10, -30)),
		]))
		state.addhill(thing.Hill(x = 20, y = 0, z = 30, spec = [
			((5, 10),),
			((0, 0), (1, -0.5)),
			((0, -20), (1.5, -20)),
		]))
		state.addhill(thing.Hill(x = 30, y = -10, z = 10, spec = [
			((-10, 0), (40, 0)),
			((-10, -30), (40, -30)),
		]))
	elif True:
		import json, hill
		hills = json.load(open("leveldata/test.json", "r"))
		for h in hills:
			state.addhill(thing.Hill(x = h["x"], y = h["y"], z = h["z"],
				spec = hill.getspec(h)))
		challenge.addchallenge(None)

	state.effects.append(mist.Mist(20))
	state.effects.append(mist.Mist(8))
	state.effects.append(mist.Mist(-8))
	state.effects.append(mist.Mist(-20))

def think(dt, kdowns, kpressed):
	state.you.control(kdowns, kpressed)
	state.think(dt, kdowns, kpressed)
	state.resolve()

def draw():
	pview.fill((100, 100, 255))
	objs = list(state.boards.values()) + list(state.blocks) + list(state.effects)
	objs = list(state.hills) + list(state.effects)
	objs.sort(key = lambda obj: (obj.z, -obj.y))
	for obj in objs:
		obj.draw()
	state.you.draw()


