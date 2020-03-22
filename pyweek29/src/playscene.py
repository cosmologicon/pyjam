import pygame
from . import pview, view, thing, state
from .pview import T


class self:
	pass

def init():
	state.you = thing.You()
	state.w = 10
	state.h = 10


def think(dt, kdowns):
	state.you.control(kdowns)
	state.you.think(dt)
	view.think(dt)

def draw():
	pview.fill((40, 40, 120))
	for x in range(0, state.w + 1):
		p0 = view.worldtoscreen((x, 0))
		p1 = view.worldtoscreen((x, state.h))
		pygame.draw.line(pview.screen, (255, 0, 255), p0, p1, T(1))
	for y in range(0, state.h + 1):
		p0 = view.worldtoscreen((0, y))
		p1 = view.worldtoscreen((state.w, y))
		pygame.draw.line(pview.screen, (255, 0, 255), p0, p1, T(1))
	state.you.draw()

