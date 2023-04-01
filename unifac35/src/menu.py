import random, math, pygame
from . import pview, state, grid, view, thing, control, sound, ptext, levels, graphics, progress
from .pview import T



def init():
	global grid0
	cells = [cell for cell, stage in progress.stages.items() if stage in progress.unlocked]
	grid0 = grid.Grid(cells)
	view.framegrid(grid0)
	think(0)


def think(dt):
	global cursorG, cursorH
	cursorV, cursorG, click, release, drop = control.getstate()
	if cursorG is not None:
		cursorH = grid.HnearestG(cursorG)
	if click and cursorH in grid0.cells:
		sound.play("select")
		from . import main, play
		play.init(progress.stages[cursorH])
		main.scene = play
	grid0.killtime(0.01)

def draw():
	pview.fill((100, 100, 100))
	shading = []
	if cursorH is not None:
		shading += [(cursorH, 0.6, (255, 255, 255))]
	grid0.draw0(shading)
	for cell, stage in progress.stages.items():
		if stage in progress.unlocked:
			pV = view.VconvertG(grid.GconvertH(cell))
			ptext.draw(stage, center = pV, fontsize = T(view.VscaleG * 0.2),
				owidth = 1)

