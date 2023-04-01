import random, math, pygame
from . import pview, state, grid, view, thing, control, sound, ptext, levels, graphics, progress
from .pview import T



def init():
	global grid0, goals
	cells = []
	goals = []
	for cell, stage in progress.stages.items():
		if stage in progress.unlocked:
			goal = thing.Goal(cell)
			goals.append(goal)
			if stage not in progress.completed:
				goal.there = False
			cells.append(cell)
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
	graphics.drawblueprint()
	shading = []
	if cursorH is not None:
		shading += [(cursorH, 0.6, (255, 255, 255))]

	graphics.qclear()
	grid0.draw(shading)
	graphics.qrender()

	for goal in goals:
		goal.draw()
	graphics.qrender()

	for cell, stage in progress.stages.items():
		if stage in progress.unlocked:
			pV = view.VconvertG(grid.GconvertH(cell))
			ptext.draw(stage, center = pV, fontsize = T(view.VscaleG * 0.2),
				owidth = 1)

