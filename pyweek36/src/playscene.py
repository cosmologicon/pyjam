import random, math
from . import state, thing, view
from . import pview


def init():
	state.you = thing.You((0, 0))
	state.DMs = [
		thing.Stander((math.fuzzrange(-10, 10, j, 0), math.fuzzrange(-10, 10, j, 1)), 0.4)
		for j in range(20)
	]

def think(dt, kdowns, kpressed):
	state.you.control(kdowns, kpressed)
	state.you.think(dt)
	for DM in state.DMs:
		DM.think(dt)
	view.xG0, view.yG0 = state.you.pos


def draw():
	pview.fill((20, 20, 20))
	pview.fill((0, 0, 0))
	for DM in state.DMs:
		DM.draw()
	state.you.draw()

