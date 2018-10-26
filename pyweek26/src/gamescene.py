import random, pygame
from . import view, state, thing, graphics, settings, section, level, ptext, sound

def init():
	state.you = thing.You()
	level.load()
	
	"""
	pygame.mixer.music.load('/Users/mitch/Code/games/pyweek/week26_entry/music/Flow_Sample1_A-Section-OnlyB.ogg')
	pygame.mixer.music.set_volume(0.5)
	pygame.mixer.music.play(-1)
	"""
	
	# turn these on to see final boss and vortex animation
	#graphics.animation.stalker.append(graphics.Stalker(state.sections[5].pos,state.sections[5]))
	#graphics.animation.vortexes.append(graphics.Vortex(state.sections[5].pos,state.sections[5],state.sections[5].r,speed=2.0))
	
#	for _ in range(100):
#		obj = thing.Debris()
#		obj.pos.x = random.uniform(-4 + obj.r, 4 - obj.r)
#		obj.pos.y = random.uniform(-400, 400)
#		state.objs.append(obj)
	

def think(dt, kpressed, kdowns, dmx, dmy):
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
	state.effects = [effect for effect in state.effects if effect.alive]
#	state.you.pos.y -= 10 * dt
#	for obj in state.objs:
#		obj.pos.y -= 10 * dt
	state.think(dt)
	view.think(dt, dmx, dmy)
	
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
		p0 = state.you.section.pos
		for section in state.sections:
			if section.pos.z > p0.z + 3 or (section.pos - p0).length() > 50:
				continue
			section.draw()
	else:
		graphics.drawmodel_watersurface()
		graphics.drawmodel_section_pools()
		graphics.drawmodel_section_tubes()
		graphics.animation.draw()
	
	graphics.drawglow(0.5, [1, 0, 0, 1])
	
	text = [
		"Food: %d/%d" % (state.food, state.foodmax),
		"Current section: %s %s" % (state.you.section.label, state.you.section.sectionid),
		"Current music: %s" % state.currentmusic()
	]
	if state.you.section.label == "pool":
		pool = state.you.section
		text += [
			"Current pressure: %d" % pool.pressure(),
			"Baseline pressure: %d" % pool.pressure0,
		]
		if pool.candrainfrom(state.you):
			ptext.draw("Space: drain", fontsize = 35, midbottom = (512, 100))
	ptext.draw("\n".join(text), fontsize = 28, midbottom = (512, 20))
	

