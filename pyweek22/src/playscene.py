import random, math
from . import ptext, state, thing, view, control, bounce
from .util import F

def init():
	state.atp = 0
	state.health = 100
	state.drawables = []
	state.colliders = []
	state.mouseables = []
	state.thinkers = []
	state.amoeba = thing.Amoeba(x = 0, y = 0, r = 30)
	state.amoeba.addtostate()
	thing.Organelle(x = 100, y = 0).addtostate()
	thing.Organelle(x = -100, y = 0).addtostate()
	control.cursor = None
	control.buttons = [
		control.Button((10, 10, 100, 40), "build 1"),
		control.Button((10, 60, 100, 40), "build 2"),
		control.Button((10, 110, 100, 40), "build 3"),
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
	for obj in state.thinkers:
		obj.think(dt)

	cspecs = [obj.getcollidespec() for obj in state.colliders]
	for (dx, dy), obj in zip(bounce.getbounce(cspecs, dt), state.colliders):
		obj.x += dx
		obj.y += dy

	if control.cursor:
		control.cursor.ondrag(gpos)
	if mup:
		control.cursor = None

	if random.random() < dt:
		thing.ATP(x = random.randrange(-200, 200), y = random.randrange(-200, 200)).addtostate()
	if 2 * random.random() < dt:
		theta = random.angle()
		x, y = 200 * math.sin(theta), 200 * math.cos(theta)
		virus = thing.Virus(x = x, y = y)
		virus.target = state.amoeba
		virus.addtostate()
	state.mouseables = [m for m in state.mouseables if m.alive]
	state.colliders = [m for m in state.colliders if m.alive]
	state.drawables = [m for m in state.drawables if m.alive]
	state.thinkers = [m for m in state.thinkers if m.alive]

def click(bname):
	print bname

def draw():
	view.clear()
	for obj in state.drawables:
		obj.drawback()
	view.applyback()
	for obj in state.drawables:
		obj.draw()
	for button in control.buttons:
		button.draw()

	ptext.draw("ATP: %d\nhealth: %d" % (state.atp, state.health),
		bottom = F(470), left = F(10), fontsize = F(26), color = "yellow")

