import pygame
from . import ptext, pview, scene
from .pview import T

def control(cstate):
	if "click" in cstate.events:
		scene.pop()
	if "quit" in cstate.kdowns:
		scene.pop()
		scene.pop()

def think(dt):
	pass

def draw():
	from . import playscene
	playscene.draw()
	pview.fill((40, 40, 40, 200))
	ptext.draw("pause screen!", center = pview.center, fontsize = T(120), owidth = 1)
	ptext.draw("Click: resume\nEsc: to menu", center = T(640, 500), fontsize = T(80), owidth = 1)

