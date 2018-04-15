from __future__ import division
import pygame, math
from pygame.locals import *
from . import settings, view, pview, ptext, state

pygame.init()
pview.set_mode(settings.size0, settings.height,
	forceres = settings.forceres, fullscreen = settings.fullscreen)
pygame.display.set_caption(settings.gamename)
clock = pygame.time.Clock()
playing = True
state.load()
while playing:
	dt = min(clock.tick(settings.maxfps) * 0.001, 1 / settings.minfps)
	mposV = view.VconvertP(pygame.mouse.get_pos())
	pointedG = view.GnearesttileV(mposV)
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
			if state.canmoveto("X", pointedG):
				state.moveto("X", pointedG)
	pview.fill((0, 50, 120))
	ptext.draw(settings.gamename, center = pview.T(400, 100), color = "white", shade = 2,
		scolor = "black", shadow = (1, 1), angle = 10,
		fontsize = pview.T(120))
	for piece in state.getpieces():
		piece.think(dt)
	for color, pG in state.gettiles():
		if pG == pointedG and state.canmoveto("X", pointedG):
			color = "white"
		view.drawtile(color, pG)
	for piece in state.getpieces():
		piece.draw()
	if settings.DEBUG:
		ptext.draw("%.1ffps" % clock.get_fps(), bottomleft = pview.T(10, 710), fontsize = pview.T(25))
	pygame.display.flip()

