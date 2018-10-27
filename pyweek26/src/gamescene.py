import random, pygame, math
from OpenGL.GL import *
from . import view, state, thing, graphics, settings, section, level, ptext, sound, scene, mapscene

def init():
	state.animation = graphics.Animations()
	state.you = thing.You()
	level.load()
	if settings.GenerateOpenSCADScripts: # output scad scripts for building section 3D models
		graphics.build_openscad_commands()
	for section in state.sections:
		section.spawn(None)
#	for section in state.sections:
#		print(section.pos)
	if not settings.reset:
		state.load()
#	for section in state.sections:
#		print(section.pos)
		

def think(dt, kpressed, kdowns, dmx, dmy):
	if kdowns["map"]:
		scene.push(mapscene)

	dx = kpressed["right"] - kpressed["left"]
	dy = kpressed["up"] - kpressed["down"]

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
	state.think(dt)
	view.think(dt, dmx, dmy)
	
	sound.manager.Update()

def draw():
	view.clear((0.1, 0.1, 0.1, 1))
	view.look()
	
#	for obj in state.objs:
#		graphics.drawobj(obj)
	
	# If you are rendering the ocean, call the skybox here first:
	#if state.sections.index(state.you.section) == section_ocean: etc.
	#	graphics.draw_skybox(state.you.section.pos)
	
	graphics.drawyou()
	for obj in state.objs:
		obj.draw()
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
		
		# If rendering the ocean:
		#graphics.drawmodel_ocean(state.you.section)
		#graphics.drawfriendfish(state.you.section.pos,0.0)
		# etc.


	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glClear(GL_DEPTH_BUFFER_BIT)

	drawminimap()
	drawhud()
	
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
	glPushMatrix()
	a = int(h / 4)
	d = int(h / 30)
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
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

def drawhud():
	glMatrixMode(GL_PROJECTION)
	glPushMatrix()
	glLoadIdentity()
	glClear(GL_DEPTH_BUFFER_BIT)
	glDisable(GL_DEPTH_TEST)
	section = state.you.section
	if section.label == "pool":
		pressure = section.pressure()
		glPushMatrix()
		ptext.draw("WATER\nPRESSURE", fontsize = 40, color = "gray", ocolor = "black", owidth = 2,
			shade = 2, center = (1160, 540), fontname = "PassionOne")
		glPopMatrix()
		glTranslate(-1, -1, 0)
		glScale(2 / 1280, 2 / 720, 1)
		glColor(0.2, 0.2, 0.2, 1)
		x0, y0 = 1160, 600
#		glRectf(x0 - 42, y0 - 14 - 6 * 26, x0 + 42, y0 + 14)
		for jpressure in range(6):
			if jpressure < pressure:
				glColor(0, 0, 0.5, 1)
			else:
				glColor(0, 0, 0, 1)
			x0, y0 = 1160, 600 + 26 * (jpressure - 6)
			glRectf(x0 - 40, y0 - 12, x0 + 40, y0 + 12)
	glEnable(GL_DEPTH_TEST)
	glPopMatrix()

