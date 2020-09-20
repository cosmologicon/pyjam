import pygame
from OpenGL.GL import *
from . import settings, pview

pview.WINDOW_FLAGS = pygame.DOUBLEBUF | pygame.OPENGL
pview.FULLSCREEN_FLAGS |= pygame.OPENGL

def init():
	pview.set_mode(settings.size0, settings.height, fullscreen=settings.fullscreen)
	pygame.display.set_caption(settings.gamename)
	glClearColor(0.1, 0.1, 0.1, 1)


def clear():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


