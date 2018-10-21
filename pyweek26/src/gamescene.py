import random, pygame
from . import view, state, thing, graphics, settings, section

def init():
	state.you = thing.You()
	pool = section.Pool(pygame.math.Vector3(5, 5, 0), 10)
	state.you.section = pool
#	for _ in range(100):
#		obj = thing.Debris()
#		obj.pos.x = random.uniform(-4 + obj.r, 4 - obj.r)
#		obj.pos.y = random.uniform(-400, 400)
#		state.objs.append(obj)
	

def think(dt, kpressed, kdowns):
	dx = kpressed["right"] - kpressed["left"]
	dy = kpressed["up"] - kpressed["down"]
	state.you.move(dt, dx, dy, kdowns["turn"])
	state.you.think(dt)

	# Flow
	state.you.flow(dt)
	for obj in state.objs:
		obj.flow(dt)
#	state.you.pos.y -= 10 * dt
#	for obj in state.objs:
#		obj.pos.y -= 10 * dt

def draw():
	view.clear((0.1, 0.1, 0.1, 1))
	view.look()
	
	state.you.section.draw()
	
	for obj in state.objs:
		graphics.drawobj(obj)
	graphics.drawyou()


