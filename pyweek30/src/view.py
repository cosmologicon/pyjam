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
	glClearColor(*world.times(state.color0, 0.4), 1)
#	glClearColor(0, 0, 0, 1)
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)



class s:
	mode = 1
	tmode = None
	tswap = 0
	jdistance = 0
	cdistance = 640
	cdistance0 = 640
	cdistance1 = 2600
	cdtarget = 640
	
	tcut = 0
	fshutter = 0
	cutscene = None
	cutting = False
	cutdelay = 0
	oncut = None
	
	shake = 0
	numcuts = 0
self = s()


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
	self.cdistance0 = math.softapproach(self.cdistance0, self.cdtarget, 0.2 * dt, dymin = 0.001)
	if self.tmode is not None:
		target = 1 if self.tmode == 3 else 0
		self.jdistance = math.softapproach(self.jdistance, target, 6 * dt, dymin = 0.001)
		if self.jdistance == target:
			self.mode = self.tmode
			self.tmode = None
	self.cdistance = math.exp(math.fadebetween(self.jdistance, 0, math.log(self.cdistance0), 1, math.log(self.cdistance1)))
	
	self.cutdelay = math.approach(self.cutdelay, 0, dt)
	if self.cutdelay == 0:
		self.tcut += dt
	fshutter = 1 if self.cutting and self.cutdelay == 0 else 0
	self.fshutter = math.approach(self.fshutter, fshutter, dt * math.exp(0.1 * self.numcuts))
	if fshutter == 1 and self.fshutter > 0.5 and self.oncut:
		self.oncut()
		self.oncut = None

def moonalpha():
	d = math.dot(state.rmoon, state.you.up)
	alpha0 = math.fadebetween(d, 0.4, 1, 0.9, 0.7)
	alpha = alpha0 * self.jdistance
	if self.fshutter > 0.5:
		camera, y, u, done = self.cutscene(self.tcut)
		if math.distance(camera, y) < 1000:
			return min(alpha, 1 - self.fshutter)
		
	return alpha


def perspective():
	glLoadIdentity()
	gluPerspective(5, pview.aspect, 100, 200 * world.R)

def perspectivestars():
	glLoadIdentity()
	if self.fshutter > 0.5:
		camera, y, u, done = self.cutscene(self.tcut)
		d = math.length(camera)
	else:
		d = self.cdistance
	gluPerspective(5, pview.aspect, d, d + 5000)
#	gluPerspective(5, pview.aspect, 10, 10000)


def look():
	from . import graphics
	if self.fshutter > 0.5:
		camera, y, u, done = self.cutscene(self.tcut)
		if done:
			self.cutting = False
	else:
		dup, dforward = math.norm([2, -1], self.cdistance)
		camera = world.linsum(state.you.pos, 1, state.you.up, dup, state.you.forward, dforward)
		y = tuple(state.you.pos)
		y = world.linsum(y, 1, graphics.shake(0.001 * pygame.time.get_ticks()), self.shake)
		u = tuple(state.you.up)
	gluLookAt(*camera, *y, *u)

def cutto(cutscene, delay = 0, oncut = None):
	self.numcuts += 1
	self.cutdelay = delay
	self.cutscene = cutscene
	self.cutting = True
	self.oncut = oncut
	self.tcut = 0

def overcut():
	if self.fshutter not in (0, 1):
		f = 2 * min(self.fshutter, 1 - self.fshutter)
		glEnable(GL_SCISSOR_TEST)
		glClearColor(0, 0, 0, 1)
		rect = pygame.Rect(0, 0, pview.w, int(pview.h * f))
		rect.top = 0
		glScissor(*rect)
		glClear(GL_COLOR_BUFFER_BIT)
		rect.bottom = pview.h
		glScissor(*rect)
		glClear(GL_COLOR_BUFFER_BIT)
		glDisable(GL_SCISSOR_TEST)

