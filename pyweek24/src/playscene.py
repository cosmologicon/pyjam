import random, math
from . import view, pview, state, thing

def init():
	state.you = thing.You(x = 0, y = 0, z = 0)
	ps = [(-10, 0), (10, 0), (30, 2), (50, 8), (70, 9), (90, 6), (110, -4), (120, -5), (140, -6)]
	for j in range(len(ps) - 1):
		x, y = ps[j]
		x1, y1 = ps[j+1]
		state.addboard(thing.Board(x = x, y = y, x1 = x1, y1 = y1, z = 0))



def think(dt, kdowns, kpressed):

	state.you.control(kdowns, kpressed)
	state.think(dt)
	state.resolve()

	

def draw():
	pview.fill((0, 0, 0))
	state.you.draw()
	objs = list(state.boards.values()) + list(state.blocks)
	objs.sort(key = lambda obj: obj.z)
	for obj in objs:
		obj.draw()


