import random
from . import view, state, thing, graphics, settings

def init():
	state.you = thing.You()
	for _ in range(100):
		obj = thing.Debris()
		obj.pos.x = random.uniform(-4 + obj.r, 4 - obj.r)
		obj.pos.y = random.uniform(-400, 400)
		state.objs.append(obj)
	

def think(dt, kpressed, kdowns):
	dx = kpressed["right"] - kpressed["left"]
	dy = kpressed["up"] - kpressed["down"]
	if kdowns["turn"]:
		state.you.upstream = not state.you.upstream
	state.you.move(dt, dx, dy)
	state.you.think(dt)

	# Flow
	state.you.pos.y -= 10 * dt
	for obj in state.objs:
		obj.pos.y -= 10 * dt

def draw():
	view.clear((0.1, 0.1, 0.1, 1))
	view.look()
	
	graphics.drawwater()
	
	for obj in state.objs:
		graphics.drawobj(obj)
	graphics.drawyou()


