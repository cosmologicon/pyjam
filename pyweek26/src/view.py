from __future__ import division
import datetime
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from . import settings, state

screen = None

def init():
	global screen
	screen = pygame.display.set_mode(settings.resolution, pygame.DOUBLEBUF | pygame.OPENGL)

def clear(color = (0, 0, 0, 1)):
	glClearColor(*color)
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

def look():
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()

	# TODO: probably don't need to center the player character
	# can we put it 3/4 of the way down the window?
	w, h = screen.get_size()
	fov = 45
	gluPerspective(fov, w / h, 0.001, 1000.0)
	camera = state.you.pos - 10 * state.you.face + pygame.math.Vector3(0, 0, 5)
	gluLookAt(*camera, *state.you.pos, 0, 0, 1)
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


def screenshot():
	# TODO: get this working
	filename = datetime.datetime.now().strftime("screenshot-%Y%m%d%H%M%S.png")
	w, h = screen.get_size()
	data = glReadPixels(0, 0, w, h, GL_RGBA, GL_UNSIGNED_BYTE)
	surf = pygame.Surface((w, h)).convert_alpha()
	arr = pygame.surfarray.pixels3d(surf)

