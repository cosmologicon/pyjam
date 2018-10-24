from __future__ import division
import datetime, math
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from . import settings, state, graphics

screen = None

# Hack to allow some "global" variables in this method.
class self:
	camera = pygame.math.Vector3(0, 0, 0)
	vantage = pygame.math.Vector3(1, 0, 0)
	# Countdown timer of how long the camera should lag in catching up to the player
	tosnap = 0

def init():
	global screen
	flags = pygame.DOUBLEBUF | pygame.OPENGL
	if settings.fullscreen:
		flags |= pygame.FULLSCREEN
	screen = pygame.display.set_mode(settings.resolution, flags)

def clear(color = (0, 0, 0, 1)):
	glClearColor(*color)
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

def addsnap(dt):
	self.tosnap += dt

def think(dt):
	self.tosnap = max(self.tosnap - dt, 0)
	camera = 1 * state.you.pos
	vantage = camera - 20 * state.you.face + pygame.math.Vector3(0, 0, 16)
	if self.tosnap:
		# f is approximately dt / self.tosnap for large values of self.tosnap
		# rapidly approaches 1 as self.tosnap goes to 0
		f = 1 - math.exp(-dt / self.tosnap)
		self.camera += f * (camera - self.camera)
		self.vantage += f * (vantage - self.vantage)
	else:
		self.camera = camera
		self.vantage = vantage

# Set up camera perspective and settings for drawing game entities
def look():
	
	# cycle animation variables
	graphics.animation.cycle()
	
	# TODO: get lighting working
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()

	# TODO: probably don't need to center the player character
	# can we put it 3/4 of the way down the window?
	w, h = screen.get_size()
	fov = 45
	gluPerspective(fov, w / h, 0.1, 1000.0)
	args = list(self.vantage) + list(self.camera) + [0, 0, 1]
	gluLookAt(*args)
	
	#glEnable(GL_BLEND)
	# TODO: get water transparency working
	#glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	
	glMatrixMode(GL_MODELVIEW)
	glEnable(GL_DEPTH_TEST)
	glDepthMask(GL_TRUE)
	
	# TODO: cull faces
	# TODO: need to swap cull direction when drawing tunnel so that the top won't be drawn


def screenshot():
	# TODO: get screenshot working
	filename = datetime.datetime.now().strftime("screenshot-%Y%m%d%H%M%S.png")
	w, h = screen.get_size()
	data = glReadPixels(0, 0, w, h, GL_RGBA, GL_UNSIGNED_BYTE)
	surf = pygame.Surface((w, h)).convert_alpha()
	arr = pygame.surfarray.pixels3d(surf)

