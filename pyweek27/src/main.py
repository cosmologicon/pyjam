from __future__ import division
import pygame
from . import settings, control, scene, view, pview, ptext, playscene, background
from .pview import T

view.init()
playscene.init()

playing = True
clock = pygame.time.Clock()
taccum = 0
while playing:
	dt = 0.001 * clock.tick(settings.ups)
	taccum += dt
	controls = control.Controls()
	if controls.quit:
		playing = False
	if pygame.K_F10 in controls.kdowns:
		pview.toggle_fullscreen()
		background.clear()
	if pygame.K_F11 in controls.kdowns:
		pview.cycle_height(settings.heights)
		background.clear()
	if pygame.K_F12 in controls.kdowns:
		pview.screenshot()

	dt0 = 1 / settings.ups
	while taccum > 0.5 * dt0:
		playscene.think(dt0, controls)
		controls.clear()
		taccum -= dt0
	playscene.draw()

	if settings.DEBUG:
		text = "%.1fps" % clock.get_fps()
		ptext.draw(text, bottomleft = T(10, 710), fontsize = T(30))
	pygame.display.flip()

