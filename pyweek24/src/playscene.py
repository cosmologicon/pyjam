import random, math
from . import view, pview, state, thing

def init():
	state.you = thing.You(x = 0, y = 0, z = 0)
	state.addboard(thing.Board(x = -10, y = 0, x1 = 40, y1 = 0, z = 0))

	for x in range(0, 400, 10000):
		z = random.uniform(-20, 20)
		dx = random.uniform(30, 60) / view.scale(z)
		y = random.uniform(-20, 10)
		dy = random.uniform(-5, 5)
#		state.addboard(thing.Board(x = x, y = y, x1 = x + dx, y1 = y + dy, z = z))
#	state.addboard(thing.Board(x = 0, y = 0, x1 = 36, y1 = 0, z = 10))
#	state.addboard(thing.Board(x = 0, y = -10, x1 = 50, y1 = 10, z = 0))
#	state.addboard(thing.Board(x = 0, y = 20, x1 = 36, y1 = 20, z = 0))

#	state.blocks.append(thing.Block(x = 30, y = 0, z = 1, ps = [(-5, -5), (0, 5), (5, -5)]))
#	state.blocks.append(thing.Block(x = 10, y = 0, z = 20, ps = [(-1, -60), (0, 60), (1, -60)]))


def think(dt, kdowns, kpressed):
	while state.lastboard().screenpos()[0] < pview.w * 2:
		last = state.lastboard()
		z = math.clamp(last.z + random.uniform(-50, 50), -25, 25)
		_, y0 = view.to0(last.x1, last.y1, last.z)
		y = math.clamp(view.atcamera(0, z, y0) + random.uniform(-3, 3), -20, 20)
		y1 = math.clamp(y + random.uniform(-5, 5), -20, 20)
		X0 = view.cameraat0(last.x1, last.z, 0)
		x = view.atcamera(X0, z, 0) + random.uniform(0, 5)
		x1 = x + random.uniform(8, 20)
		state.addboard(thing.Board(x = x, y = y, x1 = x1, y1 = y1, z = z))

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


