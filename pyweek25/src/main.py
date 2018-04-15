import pygame
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
	pview.fill((0, 50, 120))
	ptext.draw(settings.gamename, center = pview.T(400, 100), color = "white", shade = 2,
		scolor = "black", shadow = (1, 1), angle = 10,
		fontsize = pview.T(120))
	for color, pG in state.gettiles():
		view.drawtile(color, pG)
	for name, color, pG in state.getpieces():
		view.drawpiece(name, color, pG)
	pygame.display.flip()

