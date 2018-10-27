import random, pygame, math
from OpenGL.GL import *
from . import view, state, thing, graphics, settings, section, level, ptext, sound, scene, gamescene


thought = False

def init():
	draw()
	sound.manager.Update_Music()
	

def think(dt, kpressed, kdowns, dmx, dmy):
	global thought
	if kdowns["act"]:
		scene.swap(gamescene)
	sound.manager.Update_Music()
	thought = True
	

def draw():
	view.clear((0, 0.3, 0.6, 1))
	glClear(GL_DEPTH_BUFFER_BIT)

	ptext.draw(settings.gamename, fontsize = 100, owidth = 1, ocolor = "black", color = "white",
		shade = 1, fontname = "PassionOne", bottomleft = (20, 500))
	text = [
		"by Team Universe Factory 26",
		"",
		"Press Space to begin" if thought else "Loading 3d models. Thank you for your patience....",
	]
	ptext.draw("\n".join(text), fontsize = 40, owidth = 1, ocolor = "black", color = "yellow",
		shade = 1, fontname = "PassionOne", bottomleft = (50, 100))

	pygame.display.flip()
