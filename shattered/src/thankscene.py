from __future__ import division
import pygame, math, random
from . import settings, state, thing, background, window, gamedata, control, dialogue, quest, hud
from . import image, scene, mapscene, ptext, sound
from .util import F

t = 0
def think(dt, estate):
	global t
	t += dt

def draw():
	window.screen.fill((0, 0, 0))
	alpha = min(max(255 * (1 - 0.5 * t), 0), 255)
	surf = window.screen.copy().convert_alpha()
	surf.fill((255, 255, 255, alpha))
	window.screen.blit(surf, (0, 0))
	ptext.draw("Thank you for playing!", fontsize = F(75), fontname = "Oswald", color = "white",
		midbottom = (854 / 2, 480 / 2))
	for j, ship in enumerate(state.state.team):
		image.draw("avatar-%s" % ship.letter, F((-2.5 + j) * 100 + 854 / 2, 360), size = F(90))
	if len(state.state.team) < 6:
		image.draw("avatar-???", F((-2.5 + 5) * 100 + 854 / 2, 360), size = F(90))
		
