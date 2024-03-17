import pygame
from . import control, pview


def init():
	pass

def think(dt):
	pass

def draw():
	pview.fill((0, 0, 12))
	pygame.draw.circle(pview.screen, (255, 200, 128), control.pos, 3)
	pygame.display.flip()

