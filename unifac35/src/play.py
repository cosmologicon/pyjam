import random, math, pygame
from . import pview, state, grid, view, thing, control, sound, ptext, levels
from .pview import T

cursorG = None
cursorH = None
held = None
buttons = [("undo", (1000, 30), 30), ("reset", (1100, 30), 30), ("quit", (1200, 30), 30)]
bpointed = None

def init():
	levelname = "test"
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
	state.maxturn = 7
	state.snapshot()

def think(dt):
	global cursorG, cursorH, held, bpointed
	cursorV, cursorG, click, release, drop = control.getstate()
	bpointed = None
	for bname, bpos, r in buttons:
		if math.distance(T(bpos), cursorV) <= T(r):
			bpointed = bname
	if bpointed is None:
		cursorH = grid.HnearestG(cursorG)
		if click and not held:
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
	state.grid0.killtime(0.01)

def handle(bname):
	if bname == "undo":
		if state.canundo():
			state.undo()
			sound.play("undo")
		else:
			sound.play("no")
	if bname == "reset":
		state.reset()
		sound.play("reset")
	if bname == "quit":
		from . import main
		main.playing = False

def draw():
	pview.fill((100, 100, 100))
	shading = []
	if cursorH is not None:
		shading += [(cursorH, 0.6, (255, 255, 255))]
	shading += [(cell, 0.5, (255, 0, 0)) for cell in state.grid0.lit]
	fglow = math.mix(0.1, 0.9, math.cycle(pygame.time.get_ticks() * 0.001))
	for pH in [goal.pH for goal in state.goals] or [state.escape]:
		shading += [(pH, fglow, (255, 255, 200))]
	state.grid0.draw0(shading)
	for light in state.lights:
		light.draw0()
	for obstacle in state.obstacles:
		obstacle.draw0()
	for goal in state.goals:
		goal.draw0()
	state.you.draw0()
	if held and cursorH != held.pH and held.canplaceat(cursorH):
		held.drawghost(cursorH)

	text = f"Turn: {state.turn}/{state.maxturn}" if state.turn <= state.maxturn else "Time's up!"
	ptext.draw(text, T(10, 10), fontsize = T(80),
		color = "white", owidth = 1, shade = 1, shadow = (1, 1))

	for bname, bpos, r in buttons:
		size = 70 if bname == bpointed else 50
		ptext.draw(bname, center = T(bpos), fontsize = T(size), owidth = 1)
	text = "\n".join([
		f"cursorG: {cursorG[0]:.2f},{cursorG[1]:.2f}",
		f"cursorH: {cursorH[0]},{cursorH[1]}",
	])
	ptext.draw(text, bottomleft = pview.bottomleft, fontsize = T(30), owidth = 1)


