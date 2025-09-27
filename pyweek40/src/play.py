import pygame, math
from . import pview
from . import view, grid, control, graphics, state, thing, effects, ptext
from .pview import T


def init():
	state.init()
	if False:
		grid.addsegment(((0, 1), (1, 2)))
		grid.addstructure("residence2", (1, 2))
		grid.addsegment(((0, 3), (1, 4)))
		grid.addstructure("vending2", (1, 4))
	if False:
		grid.addsegment(((0, 3), (1, 4)))
		grid.addstructure("spire", (1, 4))
		grid.addsegment(((3, 3), (3, 4)))
		grid.addsegment(((3, 4), (3, 5)))
		grid.addstructure("spire", (3, 5))
#	for x in range(-5, 6):
#		state.things.append(thing.Tenant((x, 0)))

def think(dt):
	if control.halted():
		dt = 0
	grid.think(dt)
	for obj in state.things:
		obj.think(dt)
	effects.think(dt)
	state.things = [obj for obj in state.things if obj.alive]
	state.grow()

def drawedge(pG0, pG1):
	pygame.draw.line(pview.screen, (100, 50, 50), view.VconvertG(pG0), view.VconvertG(pG1), 1) 

def draw():
	graphics.drawbackdrop()
	grid.draw()
	control.drawselectors()
	if False:
		drawedge((-0.5, 0), (-0.5, 10))
		drawedge((0.5, 0), (10.5, 10))
		for yG in range(10):
			drawedge((-0.5, yG), (-0.5 + 10 - yG, 10))
			drawedge((0.5 + yG, yG), (0.5 + yG, 10))
#	pygame.draw.circle(pview.screen, (100, 100, 100), view.VconvertG(control.Gcursor()), view.VscaleP(0.1))
	for obj in state.things:
		obj.draw()
	effects.draw()
	control.drawhud()
	control.drawcursor()
	if control.halted():
		pview.fill((255, 0, 0, 40))
	message = {
		0: ["Click to extend\nthe tower", (4, 2)],
		1: ["Click on the coral\nshop then click\nwhere to place it", (-4, 2)],
		2: ["Add a condo\nso the shop\ngets customers", (4, 2)],
		3: ["Fish travel from\nhome to the\nnearest shop and\nback, following\nthe coral", (-6.5, 4)],
		5: ["Airscraper\nby Christopher Night\nMusic by Kevin MacLeod", (-12, 7)],
	}.get(state.level)
	if message is not None:
		text, pP = message
		t = 0.001 * pygame.time.get_ticks()
		pP = math.vtplus(pP, (0, 0.1), math.sin(t))
		pV = view.VconvertP(pP)
		rV = view.VscaleP(0.6)
		ptext.draw(text, center = pV, fontsize = rV, fontname = "Felipa",
			color = (50, 50, 150), ocolor = (0, 0, 20), owidth = 1)

#	graphics.drawsegment(*control.Gsegment(), lit = True)
#	graphics.drawlight()


