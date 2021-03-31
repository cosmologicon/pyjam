import pygame
from . import ptext, pview, scene
from .pview import T

def control(cstate):
	if "click" in cstate.events:
		scene.pop()
	if "quit" in cstate.kdowns:
		scene.pop()

def think(dt):
	pass

def draw():
	from . import playscene
	playscene.draw()
	pview.fill((40, 40, 40, 200))
	ptext.draw("help screen!", center = pview.center, fontsize = T(120), owidth = 1)

