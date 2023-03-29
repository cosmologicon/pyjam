import random
from . import pview, state, grid, view, thing, control, sound

cursorG = None
cursorH = None
held = None

def init():
	cells = [(x, y) for x in range(-7, 8) for y in range(-7, 8) if abs(x + y) <= 7]
	random.shuffle(cells)
	cells = cells[:-50]
	state.grid0 = grid.Grid(cells)
	view.framegrid(state.grid0)
	for cell in cells[:3]:
		state.lights.append(thing.Light(state.grid0, cell, grid.adjs))
	for cell in cells[3:6]:
		state.obstacles.append(thing.Obstacle(cell, state.grid0))
	updategrid()
	canstand = state.grid0.open - state.grid0.lit
	pHyou = next(cell for cell in cells[6:] if cell in canstand)
	state.you = thing.You(pHyou, state.grid0)
	state.turn = 1
	state.maxturn = 3

def updategrid():
	state.grid0.reset()
	for obj in state.lights + state.obstacles:
		state.grid0.block(obj.pH)
	for light in state.lights:
		light.illuminate()

def think(dt):
	global cursorG, cursorH, held
	cursorV, cursorG, click, release, drop = control.getstate()
	cursorH = grid.HnearestG(cursorG)
	if click and not held:
		held = state.grabat(cursorH)
		if held is not None:
			sound.play("grab")
	elif drop and held or click and held:
		if held.canplaceat(cursorH):
			held.placeat(cursorH)
			sound.play("place")
			updategrid()
		else:
			sound.play("no")
		held = None
	state.grid0.killtime(0.01)

def draw():
	pview.fill((100, 100, 100))
	shading = [
		(cursorH, 0.6, (255, 255, 255)),
	]
	shading += [(cell, 0.5, (255, 0, 0)) for cell in state.grid0.lit]
	state.grid0.draw0(shading)
	for light in state.lights:
		light.draw0()
	for obstacle in state.obstacles:
		obstacle.draw0()
	state.you.draw0()
	if held and cursorH != held.pH and held.canplaceat(cursorH):
		held.drawghost(cursorH)

