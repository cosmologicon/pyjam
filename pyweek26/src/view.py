import pygame
from OpenGL.GL import *
from . import settings

screen = None

def init():
	global screen
	screen = pygame.display.set_mode(settings.resolution, pygame.DOUBLEBUF | pygame.OPENGL)

def clear(color = (0, 0, 0, 1)):
	glClearColor(*color)
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

