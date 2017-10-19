import random, math
from . import view, pview, state, thing, mist, challenge, settings

class self:
	pass

def init():
	self.t = 0
	state.reset()
	state.you = thing.You(x = -settings.lag, y = 0, z = 0)
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
		state.addhill(thing.Hill(x = 0, y = 0, z = 0, spec = [
			((-40, 0), (10, 0)),
			((-40, -30), (10, -30)),
		]))

		challenge.addchallenge("tier3")
		challenge.addchallenge("tier3")
		challenge.addchallenge("tier3")
		challenge.addchallenge("tier3")
#		challenge.addsign("Hold Left then Right\nto Long Jump")
#		challenge.addchallenge("longjump3")
#		challenge.addchallenge("rolling")
#		challenge.addsign("Space or Up:\nJump")
#		challenge.addchallenge("rolling")
#		challenge.addchallenge("hopper0")
#		challenge.addsign("Hold left:\nFall back")
#		challenge.addchallenge("fallback")
#		challenge.addsign("Hold right:\nRun ahead")
#		challenge.addchallenge("forward")
#		challenge.addchallenge("rolling")
#		challenge.addchallenge("")
#		state.hazards.append(thing.Hazard(x = -30, y = 2, z = 0, vx = 10, vy = -20, r = 2, X0 = 60))
#		state.hazards.append(thing.Hazard(x = -30, y = 2, z = 0, vx = -20, vy = -10, r = 20, X0 = 60))

	state.effects.append(mist.Mist(20))
	state.effects.append(mist.Mist(8))
	state.effects.append(mist.Mist(-8))
	state.effects.append(mist.Mist(-20))

	state.effects.append(thing.Sign(text = settings.gamename,
		x = 120, y = -20, z = -25, fontsize = 15, color = "orange", owidth = 2,
		angle = 10))
	state.effects.append(thing.Sign(text = "by Christopher Night",
		x = 200, y = -20, z = -18, fontsize = 5, color = "orange", owidth = 2,
		angle = 10))

def think(dt, kdowns, kpressed):
	self.t += dt
	state.you.control(kdowns, kpressed)
	state.think(dt, kdowns, kpressed)
	state.resolve()

def draw():
	pview.fill((100, 100, 255))
#	objs = list(state.boards.values()) + list(state.blocks) + list(state.effects) + list(state.hazards)
	objs = list(state.hills) + list(state.effects) + list(state.hazards)
	objs.sort(key = lambda obj: (obj.z, -obj.y))
	for obj in objs:
		obj.draw()
	state.you.draw()
	if self.t < 1:
		a = math.clamp(int(255 * (1 - math.smoothfade(self.t, 0, 1))), 0, 255)
		pview.fill((255, 255, 255, a))

