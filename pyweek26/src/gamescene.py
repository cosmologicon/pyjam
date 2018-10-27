import random, pygame, math
from pygame.math import Vector3
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
		if not state.section.ocean:
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

	sections = graphics.get_sections_to_draw()
	for obj in state.objs:
		if obj.section in sections:
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
		
		if state.you.section.ocean:
			graphics.drawmodel_ocean(state.you.section)
			graphics.drawfriendfish(state.you.section.pos + Vector3(0, 0, 0.2), 0.0)
			graphics.drawfriendfish(state.you.section.pos + Vector3(5, 8, 0.2), -20.0)
			graphics.drawfriendfish(state.you.section.pos + Vector3(-8, 5, 0.2), 10.0)


	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glClear(GL_DEPTH_BUFFER_BIT)

	if not state.you.section.ocean:
		drawminimap()
		drawhud()
	
	text = []
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
			ptext.draw("Space: open drain", fontsize = 80, center = (1280/2, 500),
				fontname = "PassionOne", color = "orange", shade = 1, owidth = 1, ocolor = "black"
				)
	if settings.DEBUG:
		ptext.draw("\n".join(text), fontsize = 28, midbottom = (512, 20))

	text = [
		"M: map/help",
	]
	if ("pool", 0) in state.explored:
		pass
	else:
		text += [
			"",
			"CONTROLS:",
			"Arrows or WASD: move",
			"Click: enable/disable manual camera control",
			"Space or Enter: jump / open drains",
			"Double-tap space to dive",
			"",
			"HOW TO PLAY:",
			"Can't swim uphill.",
			"Can only swim against the current if the",
			"pressure difference betewen rooms is 1.",
			"Watch the pressure gauge in each room.",
			"Opening a drain into a room raises the",
			"lower room's pressure value by 1.",
			"",
			"Find fish food to gain the ability to go",
			"up one pipe.",
		]
	if not state.you.section.ocean:
		ptext.draw("\n".join(text), fontsize = 21, owidth = 2, ocolor = "black", color = "white",
			shade = 1, fontname = "PassionOne", bottomleft = (20, 20)
		)
	if state.you.section.ocean:
		ptext.draw(settings.gamename, fontsize = 100, owidth = 1, ocolor = "black", color = "white",
			shade = 1, fontname = "PassionOne", bottomleft = (20, 500))
		text = [
			"by Team Universe Factory 26",
			"",
			"Christopher Night",
			"Mitch Bryson",
			"Mary Bichner",
			"Charles McPillan",
			"Minh Huynh",
			"Jules Van Oosterom",
		]
		ptext.draw("\n".join(text), fontsize = 40, owidth = 1, ocolor = "black", color = "yellow",
			shade = 1, fontname = "PassionOne", bottomleft = (50, 100))
		ptext.draw("Thank you for playing!", fontsize = 40, owidth = 1, ocolor = "black", color = "white",
			shade = 1, fontname = "PassionOne", bottomleft = (20, 20))
	
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

