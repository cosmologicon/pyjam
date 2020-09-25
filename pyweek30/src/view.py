import pygame, math
from OpenGL.GL import *
from OpenGL.GLU import *
from . import settings, pview, world, state, quest

pview.WINDOW_FLAGS = pygame.DOUBLEBUF | pygame.OPENGL
pview.FULLSCREEN_FLAGS |= pygame.OPENGL

def init():
	pygame.display.init()
	pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, 24)
	pview.set_mode(settings.size0, settings.height, fullscreen=settings.fullscreen)
	pygame.display.set_caption(settings.gamename)
	glClearColor(0, 0, 0, 1)


def clear():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)



class self:
	mode = 1
	tmode = None
	tswap = 0
	cdistance = 640
	cdistance0 = 640
	cdistance1 = 2600
	cdtarget = 640
	
	tcut = 0
	fshutter = 0
	cutscene = None
	cutting = False
	cutdelay = 0

def incutscene():
	return (self.cutting and self.cutdelay == 0) or self.fshutter > 0

def pendingcutscene():
	return self.cutting or self.cutdelay > 0 or self.fshutter > 0

def hudcutlevel():
	return math.clamp(2 * self.fshutter, 0, 1)

def swapmode():
	self.tmode = 3 if self.mode == 1 else 1
	self.tswap = 0

def think(dt):
#	cdistance0 = [700, 700, 700, 800, 900, 1100, 1400][quest.quests[0].progress]
	self.cdistance0 = math.softapproach(self.cdistance0, self.cdtarget, 0.2 * dt, dymin = 0.001)
	if self.tmode is not None:
		d = math.log(self.cdistance)
		target = math.log(self.cdistance1 if self.tmode == 3 else self.cdistance0)
		d = math.softapproach(d, target, 6 * dt, dymin = 0.001)
		self.cdistance = math.exp(d)
		if d == target:
			self.mode = self.tmode
			self.tmode = None
	elif self.mode == 1:
		self.cdistance = self.cdistance0
	
	self.cutdelay = math.approach(self.cutdelay, 0, dt)
	if self.cutdelay == 0:
		self.tcut += dt
	fshutter = 1 if self.cutting and self.cutdelay == 0 else 0
	self.fshutter = math.approach(self.fshutter, fshutter, dt)

def moonalpha():
	return math.fadebetween(math.log(self.cdistance), math.log(700), 0, math.log(1800), 1)


def perspective():
	glLoadIdentity()
	gluPerspective(5, pview.aspect, 100, 200 * world.R)

def perspectivestars():
	glLoadIdentity()
	d = 500 if self.fshutter else self.cdistance
#	gluPerspective(5, pview.aspect, d, d + 5000)
	gluPerspective(5, pview.aspect, 10, 10000)


def look():
	if self.fshutter > 0.5:
		camera, y, u, done = self.cutscene(self.tcut)
		if done:
			self.cutting = False
	else:
		dup, dforward = math.norm([2, -1], self.cdistance)
		camera = world.linsum(state.you.pos, 1, state.you.up, dup, state.you.forward, dforward)
		y = tuple(state.you.pos)
		u = tuple(state.you.up)
	gluLookAt(*camera, *y, *u)
	if self.fshutter not in (0, 1):
		f = 2 * min(self.fshutter, 1 - self.fshutter)
		glEnable(GL_SCISSOR_TEST)
		rect = pygame.Rect(0, 0, pview.w0, pview.h0 * (1 - f))
		rect.center = pview.center0
		glScissor(*pview.T(rect))

def cutto(cutscene, delay = 0):
	self.cutdelay = delay
	self.cutscene = cutscene
	self.cutting = True
	self.tcut = 0

