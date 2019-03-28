from __future__ import division
import pygame
from . import settings, control, scene, view, pview, ptext, playscene, background, menuscene
from .pview import T

pview.SCREENSHOT_DIRECTORY = "screenshot"
view.init()
if playscene.canload() and not settings.reset:
	scene.push(menuscene)
	scene.push(playscene)
	playscene.load()
else:
	scene.push(menuscene)

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

	current = scene.top()
	if current is None:
		break
	dt0 = 1 / settings.ups
	while taccum > 0.5 * dt0:
		current.think(dt0, controls)
		controls.clear()
		taccum -= dt0
	current.draw()

	if settings.DEBUG:
		text = "%.1fps %s" % (clock.get_fps(), pygame.mouse.get_pos())
		ptext.draw(text, bottomleft = T(10, 710), fontsize = T(30), owidth = 1.2)
	pygame.display.flip()

