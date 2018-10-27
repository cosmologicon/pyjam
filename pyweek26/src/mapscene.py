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

	glDisable(GL_DEPTH_TEST)
#	graphics.drawyou()

