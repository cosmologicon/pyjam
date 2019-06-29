from __future__ import division
import pygame, math
from pygame.locals import *
from . import sound, settings, view, pview, ptext, state, scene

ptext.FONT_NAME_TEMPLATE = "fonts/%s.ttf"
pygame.init()
pview.set_mode(settings.size0, settings.height,
	forceres = settings.forceres, fullscreen = settings.fullscreen)
pygame.display.set_caption(settings.gamename)
clock = pygame.time.Clock()
playing = True
scene.push(scene.select)
while playing:
	dt = min(clock.tick(settings.maxfps) * 0.001, 1 / settings.minfps)
	class control:
		down = False
		mposV = view.VconvertP(pygame.mouse.get_pos())
	for event in pygame.event.get():
		if event.type == QUIT:
			playing = False
		if event.type == KEYDOWN and event.key == K_ESCAPE:
			playing = False
		if event.type == KEYDOWN and event.key == K_F10:
			pview.cycle_height(settings.heights)
		if event.type == KEYDOWN and event.key == K_F11:
			pview.toggle_fullscreen()
		if event.type == KEYDOWN and event.key == K_F12:
			pview.screenshot()
		if event.type == MOUSEBUTTONDOWN:
			control.down = True
	currentscene = scene.top()
	if not currentscene:
		playing = False
		continue
	currentscene.think(dt, control)
	currentscene.draw()
	if settings.DEBUG:
		ptext.draw("%.1ffps" % clock.get_fps(), bottomleft = pview.T(10, 710), fontsize = pview.T(25))
	pygame.display.flip()

