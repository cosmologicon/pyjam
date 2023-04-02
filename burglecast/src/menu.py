import random, math, pygame
from . import pview, state, grid, view, thing, control, sound, ptext, levels, graphics, progress, settings
from .pview import T



def init():
	global grid0, goals
	cells = [(4, -4)]
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
	view.VscaleG = min(view.VscaleG, 80)
	think(0)


def think(dt):
	global cursorG, cursorH
	cursorV, cursorG, click, release, drop = control.getstate()
	if cursorG is not None:
		cursorH = grid.HnearestG(cursorG)
	if click and cursorH in grid0.cells:
		sound.play("select")
		from . import main, play
		if progress.stages[cursorH] == "quit":
			main.playing = False
		else:
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
	thing.Pawn((4, -4)).draw()
	graphics.qrender()

	stage = progress.stages.get(cursorH)
	if stage in progress.unlocked or stage == "quit":
		if stage == "quit":
			text = "EXIT GAME"
		else:
			text = f"The {levels.titles[stage]} Caper"
			if stage in progress.completed:
				text += ": COMPLETE"
		ptext.draw(text, center = T(640, 680), fontsize = T(40),
				owidth = 0.5, shade = 1, shadow = (0.6, 0.6), color = (200, 200, 255))

	text = settings.gamename
	ptext.draw(text, T(10, 10), fontsize = T(40),
			color = (200, 200, 255), owidth = 0.6, shade = 1, shadow = (0.6, 0.6))


