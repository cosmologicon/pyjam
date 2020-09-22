import pygame, math
from OpenGL.GL import *
from OpenGL.GLU import *
from . import settings, pview, world, state

pview.WINDOW_FLAGS = pygame.DOUBLEBUF | pygame.OPENGL
pview.FULLSCREEN_FLAGS |= pygame.OPENGL

def init():
	pygame.display.init()
	pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, 24)
	pview.set_mode(settings.size0, settings.height, fullscreen=settings.fullscreen)
	pygame.display.set_caption(settings.gamename)
	glClearColor(0.1, 0.1, 0.1, 1)


def clear():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


class self:
	mode = 1
	tmode = None
	tswap = 0
	cdistance = 700

def swapmode():
	self.tmode = 3 if self.mode == 1 else 1
	self.tswap = 0

def think(dt):
	if self.tmode is not None:
		d = math.log(self.cdistance)
		target = math.log(2600 if self.tmode == 3 else 700)
		d = math.softapproach(d, target, 6 * dt, dymin = 0.001)
		self.cdistance = math.exp(d)
		if d == target:
			self.mode = self.tmode
			self.tmode = None

def moonalpha():
	return math.fadebetween(math.log(self.cdistance), math.log(700), 0, math.log(1800), 1)


def look():
	glLoadIdentity()
	gluPerspective(5, pview.aspect, 100, 200 * world.R)

	dup, dforward = math.norm([3, -1], self.cdistance)
	camera = world.linsum(state.you.pos, 1, state.you.up, dup, state.you.forward, dforward)
	y = tuple(state.you.pos)
	u = tuple(state.you.up)
	l = camera + y + u

	gluLookAt(*l)


