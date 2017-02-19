import pygame
from . import ptext, state, view, state
from .util import F

def draw():
	box = pygame.Surface(F(50, 50)).convert_alpha()
	box.fill((80, 80, 80))
	box.fill((20, 20, 20), F(1, 1, 48, 48))
	ptext.draw("hp: %d" % state.hp, F(4, 4), surf = box, shadow = (1, 1), fontsize = F(14))
	view.screen.blit(box, F(3, 3))



