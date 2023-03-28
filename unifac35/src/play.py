import random
from . import pview, state, grid, view, thing

def init():
	cells = [(x, y) for x in range(-7, 8) for y in range(-7, 8) if abs(x + y) <= 7]
	random.shuffle(cells)
	cells = cells[:-30]
	state.grid0 = grid.Grid(cells)
	view.framegrid(state.grid0)
	for cell in cells[:10]:
		state.lights.append(thing.Light(state.grid0, cell, grid.adjs))

def think(dt):
	pass
def draw():
	pview.fill((100, 100, 100))
	state.grid0.draw0()
	for light in state.lights:
		light.draw0()

