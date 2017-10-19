from __future__ import division, print_function
import pygame
from . import settings, view, pview, ptext
from . import scene, playscene
from .pview import T

view.init()
scene.set(playscene)

clock = pygame.time.Clock()
playing = True
while playing:
	dt = 0.001 * clock.tick(settings.maxfps)
	dt = min(dt, 1 / settings.minfps)

	kdowns = []
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			kdowns.append(event.key)
		if event.type == pygame.QUIT:
			playing = False
	
	kpressed = pygame.key.get_pressed()

	currentscene = scene.current
	if not currentscene:
		break

	currentscene.think(dt, kdowns, kpressed)

	if pygame.K_F11 in kdowns:
		pview.toggle_fullscreen()
	currentscene.draw()
	if settings.DEBUG:
		text = "X0 = %.1f\n%.1ffps" % (view.X0, clock.get_fps())
		ptext.draw(text, bottomleft = T(10, 470), fontsize = T(16))

	if pygame.K_F12 in kdowns:
		pview.screenshot()

	pygame.display.flip()
	if pygame.K_ESCAPE in kdowns:
		playing = False

