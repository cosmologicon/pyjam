import random, pygame
from OpenGL.GL import *
from . import view, state, thing, graphics, settings, section, level, ptext, sound, scene

def init():
	pass	

def think(dt, kpressed, kdowns, dmx, dmy):
	if kdowns["map"]:
		scene.pop()
	dx = kpressed["right"] - kpressed["left"]
	dy = kpressed["up"] - kpressed["down"]

	
	sound.manager.Update()

def draw():
	from . import gamescene
	gamescene.draw()
	glClear(GL_DEPTH_BUFFER_BIT)
	view.maplook()
	for section in state.sections:
		section.drawmap()

	# TODO: no idea why it's not showing up!
	if pygame.time.get_ticks() * 0.001 % 0.6 > 0.1:
		glDisable(GL_DEPTH_TEST)
		glPushMatrix()
		glTranslate(*state.you.pos)
#		glRotate(-math.degrees(state.you.heading), 0, 0, 1)
		glColor(1, 0.8, 0.5, 1)
		glBegin(GL_TRIANGLES)
		glVertex(-3, -3, 500)
		glVertex(3, -3, 500)
		glVertex(0, 6, 500)
		glEnd()
		glPopMatrix()
		glEnable(GL_DEPTH_TEST)

