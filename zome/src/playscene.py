import random, math
from . import ptext, state, thing, view, control, bounce, quest, dialog, background, progress, sound, img, settings
from . import scene, cutscene
from .util import F

def init():
	img.clearcache()
	state.reset(progress.chosen)
	control.cursor = None
	control.dragpos = None
	control.tdrag = 0
	control.reset()
	background.init()
	from . import menuscene
	menuscene.clearmessage()
	state.choosemusic()

def think(dt, mpos, mdown, mup, mwheel, rdown, mclick):
	n = control.playspeed
	if n < 1 or n != int(n):
		n, dt = 1, dt * n
	control.towerinfo.target = None
	if control.cursor:
		dragthink(n * dt, mpos, mdown, mup, mwheel, rdown, mclick)
	elif control.dragpos:
		pdragthink(n * dt, mpos, mdown, mup, mwheel, rdown, mclick)
	else:
		nodragthink(n * dt, mpos, mdown, mup, mwheel, rdown, mclick)

	if mwheel:
		view.zoom(mwheel)

	for _ in range(n):
		for obj in state.thinkers:
			obj.think(dt)

		bounce.adjust(state.colliders, dt)
		for obj in state.buildables:
			obj.constraintoworld()
		dialog.currenttip = None
		state.think(dt)
		quest.think(dt)
		dialog.think(dt)
		control.towerinfo.think(dt)

	if state.twin > 2 and not state.tlose:
		progress.complete(progress.chosen)
		if progress.chosen == 9:
			scene.pop()
			scene.push(cutscene.Final())
			scene.push(cutscene.FinalWin())
		else:
			scene.push(cutscene.Win())
			sound.playmusic(None, "win")
	if state.tlose > 2:
		scene.push(cutscene.Lose())
		sound.playmusic(None, "lose")


def dragthink(dt, mpos, mdown, mup, mwheel, rdown, mclick):
	control.tdrag += dt
	gpos = view.gamepos(mpos)
	if not control.cursor.alive:
		control.cursor = None
		return
	if mclick:
		toclick = control.cursor
		drop()
		if toclick.alive:
			toclick.onclick()
		return
	elif mup:
		drop()
		return
	control.cursor.scootch(gpos[0] - control.cursor.x, gpos[1] - control.cursor.y)
	control.cursor.think(dt)
	control.cursor.reset()
	control.cursor.constraintoworld()

def pdragthink(dt, mpos, mdown, mup, mwheel, rdown, mclick):
	control.tdrag += dt
	if control.tdrag > 0.5:
		control.done.add("pdrag")
	view.drag(control.dragpos, mpos)
	if mwheel or mup or rdown:
		control.dragpos = None

def nodragthink(dt, mpos, mdown, mup, mwheel, rdown, mclick):
	control.tdrag = 0
	for button in control.buttons:
		if button.within(mpos):
			control.towerinfo.target = button
			if mdown:
				click(button.name)
				return
	gpos = view.gamepos(mpos)
	toclick = None
	for obj in state.mouseables:
		if obj.within(gpos, rfactor = settings.grabfactor):
			obj.onhover()
			if toclick is None or obj.distanceto(gpos) < toclick.distanceto(gpos):
				toclick = obj
	downed = None
	if toclick:
		if toclick in state.buildables:
			control.towerinfo.target = toclick
		elif hasattr(toclick, "container"):
			if toclick.container is not state.cell:
				control.towerinfo.target = toclick.container
		if mdown:
			toclick.onmousedown()
			downed = toclick
			control.dragpos = None
		if rdown:
			toclick.onrdown()
	if mdown and not downed:
		control.dragpos = gpos


def click(bname):
	if bname.startswith("Grow"):
		control.done.add("grow")
		if state.cell.isfull():
			return
		flavor = bname[-1]
		if not state.canbuy(flavor):
			sound.playsfx("no")
			return
		sound.playsfx("yes")
		state.buy(flavor)
		egg = thing.Egg(container = state.cell, flavor = "XYZ".index(flavor))
		state.cell.add(egg)
		egg.addtostate()
	elif bname == "speed":
		control.playspeed = {
			0.5: 1,
			1: 1.5,
			1.5: 2,
			2: 3,
			3: 0.5,
		}[control.playspeed]
	elif bname.endswith("combos"):
		scene.push(cutscene.Combos())
	elif "Eject" in bname:
		state.cell.ejectall()
	elif bname.endswith("ause"):
		scene.push(cutscene.ExitToMenu())

def drop():
	droptos = []
	for obj in state.buildables:
		if obj.cantake(control.cursor):
			droptos.append(obj)
	if droptos:
		obj = min(droptos, key = lambda obj: control.cursor.distanceto((obj.x, obj.y)))
		for x in control.cursor.slots:
			obj.add(x)
			x.container = obj
			control.cursor.die()
	else:
		control.cursor.addtostate()
	control.cursor = None
	sound.playsfx("blobdown")

def draw():
	culturecolor = 0, 50, 50
	if state.levelname in (2, 5, 8):
		culturecolor = 30, 50, 10
	elif state.levelname in (3, 6, 9):
		culturecolor = 50, 20, 20
	view.clear(color = culturecolor)
	state.drawwaves()
	for obj in state.drawables:
		obj.draw()
	if control.cursor:
		control.cursor.draw()
	background.draw()
	view.drawiris(state.Rlevel)
	for button in control.buttons:
		button.draw()

	text = "RNA: %s" % (state.atp[0] if state.atp[0] < 1000000 else "unlimited")
	if "Z" in progress.learned:
		text += "\nDNA: %s" % (state.atp[1] if state.atp[1] < 1000000 else "unlimited")
	text += "\nCell health: %d" % max(int(state.health), 0)
	if state.levelname == "endless":
		text += "\nWave: %d" % len(state.donewaves)
	ptext.draw(text, bottom = F(470), left = F(10), fontsize = F(26), color = "yellow",
		fontname = "SansitaOne")
	control.towerinfo.draw()
	dialog.draw()

def abort():
	state.save()

