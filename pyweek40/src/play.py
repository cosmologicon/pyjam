import pygame
from . import pview
from . import view, grid, control, graphics, state, thing
from .pview import T


def init():
	for x in range(-5, 6):
		state.things.append(thing.Tenant((x, 0)))

def think(dt):
	for obj in state.things:
		obj.think(dt)

def drawedge(pG0, pG1):
	pygame.draw.line(pview.screen, (100, 50, 50), view.VconvertG(pG0), view.VconvertG(pG1), 1) 

def draw():
	pview.fill((0, 0, 40))
	for pG0, pG1 in grid.segments():
		graphics.drawsegment(pG0, pG1)
	drawedge((-0.5, 0), (-0.5, 10))
	drawedge((0.5, 0), (10.5, 10))
	for yG in range(10):
		drawedge((-0.5, yG), (-0.5 + 10 - yG, 10))
		drawedge((0.5 + yG, yG), (0.5 + yG, 10))
#	pygame.draw.circle(pview.screen, (100, 100, 100), view.VconvertG(control.Gcursor()), view.VscaleP(0.1))
	for obj in state.things:
		obj.draw()
	graphics.drawsegment(*control.Gsegment(), lit = True)
#	graphics.drawlight()


