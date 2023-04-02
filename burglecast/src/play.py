import random, math, pygame
from . import pview, state, grid, view, thing, control, sound, ptext, levels, graphics, progress
from .pview import T

current = None
cursorG = None
cursorH = None
cursorV = None
held = None
buttons = [("undo", (780, 30), 50), ("reset", (980, 30), 50), ("quit", (1180, 30), 50)]
bpointed = None
talktext = None

def init(levelname):
	global fflash, flose, fcaught, fwin, current, t, talktext
	current = levelname
	if levelname in ["delta", "finale"]:
		sound.playmusic("fearless-first")
	else:
		sound.playmusic("spy-glass")
	state.init()
	ldata = levels.levels[levelname]
	state.grid0 = grid.Grid(ldata["floor"])
	view.framegrid(state.grid0)
	for pos, dirHs in ldata["lights"].items():
		state.lights.append(thing.Light(pos, dirHs))
	for pos, name in ldata["obstacles"].items():
		if name == "P":
			state.obstacles.append(thing.Pawn(pos))
		if name == "B":
			state.obstacles.append(thing.Bishop(pos))
		if name == "U":
			state.obstacles.append(thing.Urook(pos))
		if name == "D":
			state.obstacles.append(thing.Drook(pos))
	for pos in ldata["goals"]:
		state.goals.append(thing.Goal(pos))
		state.grid0.addgoal(pos)
	state.you = thing.You(ldata["you"])
	state.escape = ldata["you"]
	state.updategrid()

	state.turn = 1
	state.maxturn = levels.maxturns[levelname]
	state.snapshot()
	fflash = 1
	flose = 0
	fcaught = 0
	fwin = 0
	t = 0
	talktext = levels.talktext.get(levelname)
	think(0)

def think(dt):
	global cursorV, cursorG, cursorH, held, bpointed, fflash, flose, fcaught, fwin, t, talktext
	t += dt
	fflash = math.approach(fflash, 0, 3 * dt)
	if state.caught():
		if fcaught == 0:
			sound.play("lose")
		fcaught = math.approach(fcaught, 1, dt)
		flose = fwin = 0
	elif state.won():
		if fwin == 0:
			progress.complete(current)
			sound.play("win")
		fwin = math.approach(fwin, 10, dt)
		fcaught = flose = 0
	elif state.lost():
		if flose == 0:
			sound.play("lose")
		flose = math.approach(flose, 1, dt)
		fcaught = fwin = 0
	cursorV, cursorG, click, release, drop = control.getstate()
	bpointed = None
	if talktext:
		if t > 0.5 and click:
			talktext = None
	else:
		for bname, bpos, r in buttons:
			if math.distance(T(bpos), cursorV) <= T(r):
				bpointed = bname
		if bpointed is None:
			cursorH = grid.HnearestG(cursorG)
			if flose or fcaught or fwin:
				held = None
			elif click and not held:
				held = state.grabat(cursorH)
				if held is not None:
					sound.play("grab")
			elif drop and held or click and held:
				if held.canplaceat(cursorH):
					moving = cursorH != held.pH
					held.placeat(cursorH)
					if moving:
						sound.play("place")
						state.updategrid()
						state.snapshot()
					else:
						sound.play("ungrab")
				else:
					sound.play("no")
				held = None
		else:
			if click:
				handle(bpointed)
	state.you.think(dt)
	for obstacle in state.obstacles:
		obstacle.think(dt)
	state.grid0.killtime(0.01)

	if fwin >= 2:
		from . import main, menu
		menu.init()
		main.scene = menu


def handle(bname):
	global fflash, flose, fcaught, fwin
	if bname == "undo":
		if state.canundo():
			state.undo()
			sound.play("undo")
			fflash = 1
			flose = 0
			fcaught = 0
			fwin = 0
		else:
			sound.play("no")
	if bname == "reset":
		fflash = 1
		flose = 0
		fcaught = 0
		fwin = 0
		state.reset()
		sound.play("reset")
	if bname == "quit":
		from . import main, menu
		menu.init()
		main.scene = menu

def draw():
	note = None
	nalpha = 0
	if fcaught > 0:
		note = "Caught!"
		nalpha = fcaught
	elif flose > 0:
		note = "Time's up!"
		nalpha = flose
	elif fwin > 0:
		note = "Heist complete!"
		nalpha = fwin

	graphics.drawblueprint()
	graphics.qclear()
	shading = []
	if cursorH is not None and note is None:
		shading += [(cursorH, 0.6, (255, 255, 255))]
#	shading += [(cell, 0.5, (255, 0, 0)) for cell in state.grid0.lit]
	if state.goals:
		fglow = math.mix(0.1, 0.9, math.cycle(pygame.time.get_ticks() * 0.001))
		for pH in [goal.pH for goal in state.goals]:
			shading += [(pH, fglow, (255, 255, 200))]
		shading += [(state.escape, 1, (255, 200, 150))]
	else:
		fglow = math.mix(0.5, 1, math.cycle(2 * pygame.time.get_ticks() * 0.001))
		shading += [(state.escape, fglow, (255, 200, 150))]
	if held is not None:
		for cell in state.grid0.cells:
			if not held.canplaceat(cell):
				shading += [(cell, 0.3, (0, 0, 0))]
	state.grid0.draw(shading)
	graphics.qrender()

	if held is state.you:
		if state.you.canplaceat(cursorH):
			state.grid0.drawpath(state.you.pH, cursorH)
			graphics.qrender()

	for light in state.lights:
		light.draw()
	for obstacle in state.obstacles:
		obstacle.draw()
	for goal in state.goals:
		goal.draw()
	state.you.draw()
	if held and cursorH != held.pH and held.canplaceat(cursorH):
		held.drawghost(cursorH)
	graphics.qrender()

	if state.maxturn is not None:
		text = f"Turn: {state.turn}/{state.maxturn}" if state.turn <= state.maxturn else "Time's up!"
		ptext.draw(text, T(10, 40), fontsize = T(40),
			color = (200, 200, 255), owidth = 0.6, shade = 1, shadow = (0.6, 0.6))

	text = f"The {levels.titles[current]} Caper"
	ptext.draw(text, T(10, 10), fontsize = T(30),
			color = (200, 200, 255), owidth = 0.6, shade = 1, shadow = (0.6, 0.6))


	alpha = math.interp(cursorV[1], T(520), 1, T(580), 0.2)
		
	if talktext:
		pview.fill((0, 0, 60, 200))
		graphics.draw("talk", T(1120, 720 - 150), scale = 0.5 * pview.f, alpha = alpha)
		ptext.draw(talktext, midbottom = T(500, 700), width = T(1000), fontsize = T(60),
			color = (255, 220, 170), fontname = "BigshotOne",
			owidth = 0.7, shadow = (0.5, 0.5), shade = 1, alpha = alpha)
	else:
		text = None
		if flose or fcaught or fwin:
			pass
		elif current == "tutorial0" and state.turn == 1:
			text = "Click and drag to move."
		elif current == "tutorial0":
			text = "Collect all the jewels and return to the starting point."
		elif current == "tutorial1":
			text = "Finish before time is up."
		elif current == "tutorial2":
			text = "Sculptures can each be moved one space, once per turn."
		elif current == "tutorial3":
			text = "Use sculptures to cast shadows. Stay in the shadows and out of the security beam!"
		elif current == "bishop0" and state.turn < 4:
			text = "Differently shaped sculptures have different movement options."
		elif current == "rook1" and state.turn < 3:
			text = "Triangle sculptures can move an unlimited distance in any of 3 directions."
		elif current == "finale":
			text = "The end! Thank you for playing."
		ptext.draw(text, midbottom = T(640, 700), width = T(1200), fontsize = T(32),
			color = (200, 200, 255), alpha = alpha,
			owidth = 0.7, shadow = (0.5, 0.5), shade = 1)

	if note is not None:
		if fwin:
			pview.fill((20, 20, 120, math.imix(0, 200, nalpha)))
			color = (127, 127, 255)
		else:
			pview.fill((80, 20, 20, math.imix(0, 200, nalpha)))
			color = (255, 127, 127)
		ptext.draw(note, color = color, alpha = nalpha,
			center = T(640, 540), fontsize = T(100),
			owidth = 0.5, shadow = (0.6, 0.6), shade = 1)

	for bname, bpos, r in buttons:
		size = 70 if bname == bpointed else 50
		ptext.draw(bname, center = T(bpos), fontsize = T(size),
			color = (200, 200, 255), owidth = 0.6, shade = 1, shadow = (0.6, 0.6))

	if fflash > 0:
		alpha = math.imix(0, 255, fflash)
		pview.fill((40, 40, 40, alpha))

	if False:
		text = "\n".join([
			f"cursorG: {cursorG[0]:.2f},{cursorG[1]:.2f}",
			f"cursorH: {cursorH[0]},{cursorH[1]}",
		])
		ptext.draw(text, bottomleft = pview.bottomleft, fontsize = T(30), owidth = 1)


