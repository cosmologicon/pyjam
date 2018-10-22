import random, pygame
from . import view, state, thing, graphics, settings, section

def init():
	state.you = thing.You()
	state.sections.append(section.Pool(pygame.math.Vector3(5, 5, 0), 10))
	state.sections.append(section.Pool(pygame.math.Vector3(40, 40, 0), 6))
	state.sections.append(section.Pool(pygame.math.Vector3(80, 0, 0), 12))
	state.sections.append(section.Pool(pygame.math.Vector3(-30, 10, 0), 8))
	state.sections.extend(section.connectpools(state.sections[0], state.sections[1], waypoints = [pygame.math.Vector3(0, 40, 0)]))
	state.sections.extend(section.connectpools(state.sections[1], state.sections[2], waypoints = [pygame.math.Vector3(40, 20, 0), pygame.math.Vector3(100, 30, 0)]))
	state.sections.extend(section.connectpools(state.sections[2], state.sections[0], waypoints = [], rate = 20, width = 8))
	state.sections.extend(section.connectpools(state.sections[0], state.sections[3], waypoints = []))
	thing.SolidGrate(state.sections[-1], 0.6)
	state.sections.extend(section.connectpools(state.sections[0], state.sections[3], waypoints = [pygame.math.Vector3(-10, -50, 0)], rate = 1, width = 2))
	state.you.section = state.sections[0]
#	for _ in range(100):
#		obj = thing.Debris()
#		obj.pos.x = random.uniform(-4 + obj.r, 4 - obj.r)
#		obj.pos.y = random.uniform(-400, 400)
#		state.objs.append(obj)
	

def think(dt, kpressed, kdowns):
	dx = kpressed["right"] - kpressed["left"]
	dy = kpressed["up"] - kpressed["down"]

	for section in state.sections:
		section.spawn(dt)
	state.you.move(dt, dx, dy, kdowns["turn"])
	state.you.think(dt)
	for obj in state.objs:
		obj.think(dt)

	state.you.flow(dt)
	for obj in state.objs:
		obj.flow(dt)

	state.objs = [obj for obj in state.objs if obj.alive]
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


