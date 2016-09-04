import random, math
from . import ptext, state, thing, view, control
from .util import F

def init():
	state.atp = 0
	state.health = 100
	state.mouseables = [
		thing.Organelle(x = 100, y = 0),
		thing.Organelle(x = -100, y = 0),
		thing.Organelle(x = 0, y = 50),
		thing.ATP(x = 50, y = -30),
	]
	state.things = [
		thing.Amoeba(x = 0, y = 0, r = 30)
	] + state.mouseables
	control.cursor = None
	control.buttons = [
		control.Button((10, 10, 50, 20), "build"),
	]

def think(dt, mpos, mdown, mup):
	hover = None
	for button in control.buttons:
		if button.within(mpos):
			hover = button
			if mdown:
				click(button.name)
	gpos = view.gamepos(mpos)
	for obj in state.mouseables:
		if hover is None:
			if obj.within(gpos):
				obj.onhover()
				if mdown:
					obj.onmousedown()
	for obj in state.things:
		obj.think(dt)
	if control.cursor:
		control.cursor.ondrag(gpos)
	if mup:
		control.cursor = None

	if random.random() < dt:
		atp = thing.ATP(x = random.randrange(-200, 200), y = random.randrange(-200, 200))
		state.mouseables.append(atp)
		state.things.append(atp)
	if 2 * random.random() < dt:
		theta = random.angle()
		x, y = 200 * math.sin(theta), 200 * math.cos(theta)
		virus = thing.Virus(x = x, y = y)
		virus.target = state.things[0]
		state.things.append(virus)
	state.mouseables = [m for m in state.mouseables if m.alive]
	state.things = [m for m in state.things if m.alive]

def click(bname):
	print bname

def draw():
	view.clear()
	for obj in state.things:
		obj.drawback()
	view.applyback()
	for obj in state.things:
		obj.draw()
	for button in control.buttons:
		button.draw()

	ptext.draw("ATP: %d\nhealth: %d" % (state.atp, state.health),
		bottom = F(470), left = F(10), fontsize = F(26), color = "yellow")

