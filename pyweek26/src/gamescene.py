import random, pygame
from . import view, state, thing, graphics, settings, section

def init():
	state.you = thing.You()
	state.sections.append(section.Pool(pygame.math.Vector3(5, 5, 0), 10))
	state.sections.append(section.Pool(pygame.math.Vector3(40, 40, 0), 6))
	state.sections.append(section.Pool(pygame.math.Vector3(100, 0, 0), 12))
	state.sections.append(section.Connector(state.sections[0], state.sections[1]))
	state.sections.append(section.Connector(state.sections[1], state.sections[2]))
	state.sections.append(section.Connector(state.sections[2], state.sections[0], width=8, rate=20))
	state.you.section = state.sections[0]
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
	
	for section in state.sections:
		section.draw()
	
	for obj in state.objs:
		graphics.drawobj(obj)
	graphics.drawyou()


