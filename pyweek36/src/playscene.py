from . import state, thing, view
from . import pview


def init():
	state.you = thing.You((0, 0))
	state.DMs = [
		thing.Stander((3, 3), 0.4),
		thing.Stander((-3, 3), 0.2),
	]

def think(dt, kdowns, kpressed):
	state.you.control(kdowns, kpressed)
	state.you.think(dt)
	view.xG0, view.yG0 = state.you.pos


def draw():
	pview.fill((20, 20, 20))
	for DM in state.DMs:
		DM.draw()
	state.you.draw()

