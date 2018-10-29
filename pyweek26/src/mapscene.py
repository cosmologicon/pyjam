import random, pygame, math
from OpenGL.GL import *
from . import view, state, thing, graphics, settings, section, level, ptext, sound, scene
from .pview import T

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
	gamescene.drawgame()
	view.overlay((0, 0, 0, 0.8))
	glClear(GL_DEPTH_BUFFER_BIT)

	if True:
		view.maplook()
		for section in state.sections:
			section.drawmap()

		if pygame.time.get_ticks() * 0.001 % 0.6 > 0.1:
			glDisable(GL_DEPTH_TEST)
			glPushMatrix()
			glTranslate(*state.you.pos)
			glRotate(-math.degrees(state.you.heading), 0, 0, 1)
			glColor(1, 0.8, 0.5, 1)
			glBegin(GL_TRIANGLES)
			glVertex(-2, -2, 500)
			glVertex(2, -2, 500)
			glVertex(0, 4, 500)
			glEnd()
			glPopMatrix()
			glEnable(GL_DEPTH_TEST)

	text = [
		"M: resume game",
		"",
		"CONTROLS:",
		"Arrows or WASD: move",
		"Shift or Z: about face",
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
		"Small higher pipes may only be entered when",
		"charged up with fish food.",
		"",
		"CHEAT CODES:",
		"0: jump to central pool",
		"1: jump to end of NW challenge",
		"2: jump to end of NE challenge",
		"3: jump to end of SW challenge",
		"4: jump to end of SE challenge",
		"5: get food",
	]
	ptext.draw("\n".join(text), fontsize = T(21), owidth = 2, ocolor = "black", color = "white",
		shade = 1, fontname = "PassionOne", bottomleft = T(20, 20)
	)


