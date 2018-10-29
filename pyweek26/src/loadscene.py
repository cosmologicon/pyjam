import random, pygame, math
from OpenGL.GL import *
from . import view, state, thing, graphics, settings, section, level, ptext, sound, scene, gamescene


class self:
	f = 0
	done = False

def init():
	draw()
	pygame.display.flip()
	sound.manager.Update_Music()

def think(dt, kpressed, kdowns, dmx, dmy):
	self.f = graphics.load(0.03)
	if self.f == 1:
		self.done = True
	if self.done and kdowns["act"]:
		scene.swap(gamescene)
	sound.manager.Update_Music()

def draw():
	view.clear((0, 0.3, 0.6, 1))
	glClear(GL_DEPTH_BUFFER_BIT)

	ptext.draw(settings.gamename, fontsize = 100, owidth = 1, ocolor = "black", color = "white",
		shade = 1, fontname = "PassionOne", bottomleft = (20, 500))
	text = [
		"by Team Universe Factory 26",
		"",
		"Press Space to begin" if self.done else "Loading.... %d%%" % round(100 * self.f),
	]
	ptext.draw("\n".join(text), fontsize = 40, owidth = 1, ocolor = "black", color = "yellow",
		shade = 1, fontname = "PassionOne", bottomleft = (50, 100))

