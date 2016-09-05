import random, math
from . import ptext, state, thing, view, control, bounce, quest, dialog, background
from .util import F

def init():
	state.atp = 0
	state.health = 100
	state.reset()
	state.amoeba = thing.Amoeba(x = 0, y = 0, r = 30)
	state.amoeba.addtostate()
	control.cursor = None
	control.buttons = [
		control.Button((10, 10, 100, 40), "build 1"),
		control.Button((10, 60, 100, 40), "build 2"),
		control.Button((10, 110, 100, 40), "build 3"),
	]
	background.init()

def think(dt, mpos, mdown, mup, mwheel):
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
	for obj in state.thinkers:
		obj.think(dt)

	bounce.adjust(state.colliders, dt)

	if control.cursor:
		control.cursor.scootch(gpos[0] - control.cursor.x, gpos[1] - control.cursor.y)
		control.cursor.think(dt)
	if mup and control.cursor:
		for obj in state.buildables:
			if obj.cantake(control.cursor):
				for x in control.cursor.slots:
					obj.add(x)
					x.container = obj
					control.cursor.die()
				break
		else:
			control.cursor.addtostate()
		control.cursor = None
	if mwheel:
		view.zoom(mwheel)

	if random.random() < dt:
		thing.ATP(x = random.randrange(-200, 200), y = random.randrange(-200, 200)).addtostate()
	if 2 * random.random() < dt:
		theta = random.angle()
		x, y = 200 * math.sin(theta), 200 * math.cos(theta)
		virus = thing.VirusCarrier(x = x, y = y)
		virus.target = state.amoeba
		virus.addtostate()
	state.updatealive()
	
	quest.think(dt)
	dialog.think(dt)

def click(bname):
	if state.amoeba.isfull():
		return
	flavor = {
		"build 1": 0,
		"build 2": 1,
		"build 3": 2,
	}[bname]
	egg = thing.Egg(container = state.amoeba, flavor = flavor)
	state.amoeba.add(egg)
	egg.addtostate()

def draw():
	view.clear(color = (0, 50, 50))
	for obj in state.drawables:
		obj.draw()
	if control.cursor:
		control.cursor.draw()
	background.draw()
	view.drawiris(400)

	for button in control.buttons:
		button.draw()
	dialog.draw()

	ptext.draw("ATP: %d\nhealth: %d" % (state.atp, state.health),
		bottom = F(470), left = F(10), fontsize = F(26), color = "yellow")
	

