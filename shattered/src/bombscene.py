import pygame, math
from . import ptext, window, sound, scene, playscene
from .util import F

def onpush():
	global t
	t = 0
	sound.play("bomb")

def think(dt, estate):
	global t
	t += dt
	if t > 4:
		scene.swap(playscene)

def draw():
	window.screen.fill((100, 50, 0))
	g = int(200 + 50 * math.sin(1 + pygame.time.get_ticks() * 0.001))
	b = int(180 + 70 * math.sin(3 + pygame.time.get_ticks() * 0.0014))
	r = 80
	a = int(150 + 100 * math.sin(4 + pygame.time.get_ticks() * 0.0033))
	surf = window.screen.copy().convert_alpha()
	surf.fill((r, g, b, a))
	window.screen.blit(surf, (0, 0))


