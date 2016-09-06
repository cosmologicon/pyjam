import random, math
from . import ptext, state, thing, view, control, bounce, quest, dialog, background, progress
from . import scene, cutscene
from .util import F

def init():
	state.reset(progress.chosen)
	control.cursor = None
	control.dragpos = None
	control.buttons = [
		control.Button((10, 10, 100, 40), "build 1"),
		control.Button((10, 60, 100, 40), "build 2"),
		control.Button((10, 110, 100, 40), "build 3"),
	]
	background.init()

def think(dt, mpos, mdown, mup, mwheel, rdown):
	hover = None
	downed = None
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
					downed = obj
					control.dragpos = None
				if rdown:
					obj.onrdown()
	if mdown and not downed:
		control.dragpos = gpos
	for obj in state.thinkers:
		obj.think(dt)

	bounce.adjust(state.colliders, dt)

	if control.cursor:
		control.cursor.scootch(gpos[0] - control.cursor.x, gpos[1] - control.cursor.y)
		control.cursor.think(dt)
		control.cursor.reset()
	if control.dragpos:
		view.drag(control.dragpos, mpos)
	if (mup or mwheel) and control.cursor:
		drop()
	if mup or mwheel:
		control.dragpos = None
	if mwheel:
		view.zoom(mwheel)

	state.think(dt)
	quest.think(dt)
	dialog.think(dt)
	if state.twin > 2 and not state.tlose:
		progress.complete(progress.chosen)
		scene.push(cutscene.Win())
	if state.tlose > 2:
		scene.push(cutscene.Lose())


def click(bname):
	if state.cell.isfull():
		return
	flavor = {
		"build 1": 0,
		"build 2": 1,
		"build 3": 2,
	}[bname]
	egg = thing.Egg(container = state.cell, flavor = flavor)
	state.cell.add(egg)
	egg.addtostate()

def drop():
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

def draw():
	view.clear(color = (0, 50, 50))
	state.drawwaves()
	for obj in state.drawables:
		obj.draw()
	if control.cursor:
		control.cursor.draw()
	background.draw()
	view.drawiris(state.Rlevel)
	for button in control.buttons:
		button.draw()
	dialog.draw()

	ptext.draw("ATP: %d\nhealth: %d" % (state.atp, state.health),
		bottom = F(470), left = F(10), fontsize = F(26), color = "yellow")

def abort():
	state.save()

