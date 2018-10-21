from __future__ import division
import datetime
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from . import settings, state

screen = None

def init():
	global screen
	flags = pygame.DOUBLEBUF | pygame.OPENGL
	if settings.fullscreen:
		flags |= pygame.FULLSCREEN
	screen = pygame.display.set_mode(settings.resolution, flags)

def clear(color = (0, 0, 0, 1)):
	glClearColor(*color)
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

# Set up camera perspective and settings for drawing game entities
def look():
	# TODO: get lighting working
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()

	# TODO: probably don't need to center the player character
	# can we put it 3/4 of the way down the window?
	w, h = screen.get_size()
	fov = 45
	gluPerspective(fov, w / h, 0.001, 1000.0)
	camera = state.you.pos - 20 * state.you.face + pygame.math.Vector3(0, 0, 16)
	args = list(camera) + list(state.you.pos) + [0, 0, 1]
	gluLookAt(*args)
	glEnable(GL_BLEND)
	# TODO: get water transparency working
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	glEnable(GL_DEPTH_TEST)
	# TODO: cull faces
	# TODO: need to swap cull direction when drawing tunnel so that the top won't be drawn


def screenshot():
	# TODO: get screenshot working
	filename = datetime.datetime.now().strftime("screenshot-%Y%m%d%H%M%S.png")
	w, h = screen.get_size()
	data = glReadPixels(0, 0, w, h, GL_RGBA, GL_UNSIGNED_BYTE)
	surf = pygame.Surface((w, h)).convert_alpha()
	arr = pygame.surfarray.pixels3d(surf)

