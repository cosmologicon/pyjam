import random, pygame
from . import view, state, thing, graphics, settings, section, level, ptext, sound

def init():
	state.you = thing.You()
	level.load()
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
	state.you.move(dt, dx, dy, kdowns["turn"], kdowns["act"], kpressed["act"])
	state.you.think(dt)
	for obj in state.objs + state.effects:
		obj.think(dt)

	state.you.flow(dt)
	for obj in state.objs:
		obj.flow(dt)

	state.objs = [obj for obj in state.objs if obj.alive]
	state.effects = [effect for effect in state.effects if obj.alive]
#	state.you.pos.y -= 10 * dt
#	for obj in state.objs:
#		obj.pos.y -= 10 * dt
	view.think(dt)
	
	sound.manager.Update()

def draw():
	view.clear((0.1, 0.1, 0.1, 1))
	view.look()
	
	for obj in state.objs:
		graphics.drawobj(obj)
	graphics.drawyou()
	for effect in state.effects:
		effect.draw()
	
	if settings.debug_graphics:
		for section in state.sections:
			section.draw()
	else:
		graphics.drawmodel_watersurface()
		graphics.drawmodel_section_pools()
		graphics.drawmodel_section_tubes()
		graphics.animation.draw()
	
	if state.you.section.label == "pool":
		pool = state.you.section
		text = "Current pressure: %d\nBaseline pressure: %d" % (pool.pressure(), pool.pressure0)	
		ptext.draw(text, fontsize = 28, midbottom = (512, 20))
		if pool.candrainfrom(state.you):
			ptext.draw("Space: drain", fontsize = 35, midbottom = (512, 60))

