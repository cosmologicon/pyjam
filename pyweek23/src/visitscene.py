import pygame
from pygame.locals import *
from . import ptext, view, scene
from .util import F

class self:
	pass

def init(name):
	self.name = name
	
def think(dt, kdowns, kpressed):
	if K_SPACE in kdowns:
		scene.pop()

def draw():
	view.screen.fill((0, 40, 100))
	ptext.draw("Visiting: " + self.name, midtop = F(427, 10),
		fontsize = F(40), shadow = (1, 1))
	ptext.draw("Space to leave", midbottom = F(427, 470),
		fontsize = F(40), shadow = (1, 1))

