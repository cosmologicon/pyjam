import random, math, pygame
from . import pview, state, grid, view, thing, control, sound, ptext, levels, graphics, progress
from .pview import T

current = None
cursorG = None
cursorH = None
held = None
buttons = [("undo", (1000, 30), 30), ("reset", (1100, 30), 30), ("quit", (1200, 30), 30)]
bpointed = None

def init(levelname):
	global fflash, flose, fcaught, fwin, current
	current = levelname
	state.init()
	if levelname is None:
		cells = [(x, y) for x in range(-7, 8) for y in range(-7, 8) if abs(x + y) <= 7]
		random.shuffle(cells)
		cells = cells[:-50]
		state.grid0 = grid.Grid(cells)
		view.framegrid(state.grid0)
		for cell in cells[:3]:
			state.lights.append(thing.Light(cell, grid.adjs))
		for cell in cells[3:6]:
			state.obstacles.append(thing.Pawn(cell))
		state.updategrid()
		canstand = state.grid0.open - state.grid0.lit
		freecells = (cell for cell in cells[6:] if cell in canstand)
		for j in range(3):
			state.goals.append(thing.Goal(next(freecells)))
		pHyou = next(freecells)
		state.you = thing.You(pHyou)
		state.escape = pHyou
	else:
		ldata = levels.levels[levelname]
		state.grid0 = grid.Grid(ldata["floor"])
		view.framegrid(state.grid0)
		for pos, dirHs in ldata["lights"].items():
			state.lights.append(thing.Light(pos, dirHs))
		for pos, name in ldata["obstacles"].items():
			if name == "P":
				state.obstacles.append(thing.Pawn(pos))
		for pos in ldata["goals"]:
			state.goals.append(thing.Goal(pos))
		state.you = thing.You(ldata["you"])
		state.escape = ldata["you"]
		state.updategrid()

	state.turn = 1
	state.maxturn = 10
	state.snapshot()
	fflash = 1
	flose = 0
	fcaught = 0
	fwin = 0
	think(0)

def think(dt):
	global cursorG, cursorH, held, bpointed, fflash, flose, fcaught, fwin
	fflash = math.approach(fflash, 0, 3 * dt)
	if state.caught():
		fcaught = math.approach(fcaught, 1, dt)
		flose = fwin = 0
	elif state.lost():
		flose = math.approach(flose, 1, dt)
		fcaught = fwin = 0
	elif state.won():
		fwin = math.approach(fwin, 10, dt)
		fcaught = flose = 0
	cursorV, cursorG, click, release, drop = control.getstate()
	bpointed = None
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
		progress.complete(current)
		from . import main, menu
		menu.init()
		main.scene = menu


def handle(bname):
	global fflash
	if bname == "undo":
		if state.canundo():
			state.undo()
			sound.play("undo")
			fflash = 1
		else:
			sound.play("no")
	if bname == "reset":
		fflash = 1
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

	pview.fill((100, 100, 100))
	shading = []
	if cursorH is not None and note is None:
		shading += [(cursorH, 0.6, (255, 255, 255))]
#	shading += [(cell, 0.5, (255, 0, 0)) for cell in state.grid0.lit]
	if held is not None:
		for cell in state.grid0.cells:
			if not held.canplaceat(cell):
				shading += [(cell, 0.3, (0, 0, 0))]
	fglow = math.mix(0.1, 0.9, math.cycle(pygame.time.get_ticks() * 0.001))
	for pH in [goal.pH for goal in state.goals] or [state.escape]:
		shading += [(pH, fglow, (255, 255, 200))]
	state.grid0.draw0(shading)
	if held is state.you:
		if state.you.canplaceat(cursorH):
			state.grid0.drawpath(state.you.pH, cursorH)
	for light in state.lights:
		light.draw()
	for obstacle in state.obstacles:
		obstacle.draw()
	for goal in state.goals:
		goal.draw()
	state.you.draw()
	if held and cursorH != held.pH and held.canplaceat(cursorH):
		held.drawghost(cursorH)

	text = f"Turn: {state.turn}/{state.maxturn}" if state.turn <= state.maxturn else "Time's up!"
	ptext.draw(text, T(10, 10), fontsize = T(80),
		color = "white", owidth = 1, shade = 1, shadow = (1, 1))

	if state.turn < 2:
		graphics.draw("talk", T(1120, 720 - 150), scale = 0.5 * pview.f)
		text = "Good evening my darling followers, it's me, Francois Debonair, coming at you with another daring jewel heist live stream."
		ptext.draw(text, midbottom = T(500, 700), width = T(900), fontsize = T(40), owidth = 1)

	if note is not None:
		pview.fill((80, 20, 20, math.imix(0, 200, nalpha)))
		ptext.draw(note, color = (255, 127, 127), alpha = nalpha,
			center = pview.center, fontsize = T(150),
			owidth = 0.5, shadow = (1, 1), shade = 1)

	for bname, bpos, r in buttons:
		size = 70 if bname == bpointed else 50
		ptext.draw(bname, center = T(bpos), fontsize = T(size), owidth = 1)

	if fflash > 0:
		alpha = math.imix(0, 255, fflash)
		pview.fill((40, 40, 40, alpha))

	text = "\n".join([
		f"cursorG: {cursorG[0]:.2f},{cursorG[1]:.2f}",
		f"cursorH: {cursorH[0]},{cursorH[1]}",
	])
	ptext.draw(text, bottomleft = pview.bottomleft, fontsize = T(30), owidth = 1)


