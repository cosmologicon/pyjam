import random, pygame, math
from OpenGL.GL import *
from . import view, state, thing, graphics, settings, section, level, ptext, sound, scene, mapscene

def init():
	state.animation = graphics.Animations()
	state.you = thing.You()
	level.load()
	if settings.GenerateOpenSCADScripts: # output scad scripts for building section 3D models
		graphics.build_openscad_commands()
	
#	for _ in range(100):
#		obj = thing.Debris()
#		obj.pos.x = random.uniform(-4 + obj.r, 4 - obj.r)
#		obj.pos.y = random.uniform(-400, 400)
#		state.objs.append(obj)
	

def think(dt, kpressed, kdowns, dmx, dmy):
	if kdowns["map"]:
		scene.push(mapscene)

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

	for obj in state.objs:
		if obj.collides(state.you):
			obj.hit(state.you)

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
#	for obj in state.objs:
#		graphics.drawobj(obj)
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
		state.animation.draw()

	drawminimap()
	
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
	
def drawminimap():
	w, h = settings.resolution
	a = int(h / 4)
	d = int(h / 30)
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	glMatrixMode(GL_PROJECTION)
	glPushMatrix()
	glClear(GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()
	glEnable(GL_SCISSOR_TEST)
	glScissor(w - a - d, d, a, a)
	glColor(0, 0, 0.4, 1)
	glBegin(GL_QUADS)
	glVertex(1, 1, 0.8)
	glVertex(-1, 1, 0.8)
	glVertex(-1, -1, 0.8)
	glVertex(1, -1, 0.8)
	glEnd()
	glScale(2 / w, 2 / h, 2 / 1000)
	glTranslate((w - d - a / 2) - (w / 2), -(h / 2) + (d + a / 2), 0)
	glRotate(-math.degrees(state.you.heading), 0, 0, 1)
	glDisable(GL_DEPTH_TEST)
	glColor(1, 0.5, 0, 1)
	glBegin(GL_TRIANGLES)
	glVertex(-5, -5)
	glVertex(5, -5)
	glVertex(0, 10)
	glEnd()
	glEnable(GL_DEPTH_TEST)
	glDisable(GL_SCISSOR_TEST)
	glPopMatrix()
