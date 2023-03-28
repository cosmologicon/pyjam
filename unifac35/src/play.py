import random
from . import pview, state, grid, view, thing, control

cursorG = None
cursorH = None

def init():
	cells = [(x, y) for x in range(-7, 8) for y in range(-7, 8) if abs(x + y) <= 7]
	random.shuffle(cells)
	cells = cells[:-30]
	state.grid0 = grid.Grid(cells)
	view.framegrid(state.grid0)
	for cell in cells[:10]:
		state.lights.append(thing.Light(state.grid0, cell, grid.adjs))
	for cell in cells[10:15]:
		state.obstacles.append(thing.Obstacle(cell))
	state.you = thing.You(cells[15])

def think(dt):
	global cursorG, cursorH
	cursorV, cursorG, click, release = control.getstate()
	cursorH = grid.HnearestG(cursorG)
	

def draw():
	pview.fill((100, 100, 100))
	shading = [
		(cursorH, 0.6, (255, 255, 255)),
	]
	state.grid0.draw0(shading)
	for light in state.lights:
		light.draw0()
	for obstacle in state.obstacles:
		obstacle.draw0()
	state.you.draw0()

