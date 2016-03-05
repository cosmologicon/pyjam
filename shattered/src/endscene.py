from __future__ import division
import pygame, math, random
from . import settings, state, thing, background, window, gamedata, control, dialogue, quest, hud
from . import image, scene, mapscene, ptext, sound, thankscene
from .util import F

curtain = -1

def think(dt, estate):
	global curtain
	curtain = min(curtain + 6 * dt, 1)
	hud.clear()
	state.state.think(dt)
	window.think(dt)
	quest.think(dt)
	dialogue.think(dt)
	sound.playmusic(1, 1)
	if dialogue.tquiet > 1:
		scene.swap(thankscene)

def draw():
	background.draw()
	state.state.draw()
	g = int(200 + 50 * math.sin(1 + pygame.time.get_ticks() * 0.001))
	b = int(180 + 70 * math.sin(3 + pygame.time.get_ticks() * 0.0014))
	r = 80
	a = int(150 + 100 * math.sin(4 + pygame.time.get_ticks() * 0.0033))
	surf = window.screen.copy().convert_alpha()
	surf.fill((r, g, b, a))
	window.screen.blit(surf, (0, 0))
	dialogue.draw()

	if curtain <= 0:
		window.screen.fill((0, 0, 0))
	elif curtain < 1:
		h = int(window.sy / 2 * (1 - curtain))
		window.screen.fill((0, 0, 0), (0, 0, window.sx, h))
		window.screen.fill((0, 0, 0), (0, window.sy - h, window.sx, h))

