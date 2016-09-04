import random
from . import ptext, state, thing, view, control
from .util import F

def init():
	state.atp = 0
	state.mouseables = [
		thing.Organelle(x = 100, y = 0),
		thing.ATP(x = 50, y = -30),
	]
	state.things = [
		thing.Amoeba(x = 0, y = 0, r = 30)
	] + state.mouseables
	control.cursor = None

def think(dt, mpos, mdown, mup):
	gpos = view.gamepos(mpos)
	for obj in state.mouseables:
		if obj.within(gpos):
			obj.onhover()
			if mdown:
				obj.onmousedown()
		obj.think(dt)
	if control.cursor:
		control.cursor.ondrag(gpos)
	if mup:
		control.cursor = None

	if 3 * random.random() < dt:
		atp = thing.ATP(x = random.randrange(-200, 200), y = random.randrange(-200, 200))
	state.mouseables = [m for m in state.mouseables if m.alive]
	state.things = [m for m in state.things if m.alive]


def draw():
	view.clear()
	for obj in state.things:
		obj.draw()

	ptext.draw("ATP: %d" % state.atp,
		bottom = F(470), left = F(10), fontsize = F(26), color = "yellow")

