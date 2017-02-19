from __future__ import division
import pygame, os, datetime
from pygame.locals import *
from . import settings, view, ptext, background
from . import scene, playscene
from .util import F

pygame.init()
view.init()
background.init()

scene.push(playscene)

clock = pygame.time.Clock()
while scene.stack:
	dt = min(clock.tick(settings.maxfps) * 0.001, 1 / settings.minfps)
	top = scene.stack[-1]
	kdowns = set()
	for event in pygame.event.get():
		if event.type == QUIT:
			scene.quit()
		if event.type == KEYDOWN:
			kdowns.add(event.key)
	kpressed = pygame.key.get_pressed()

	top.think(dt, kdowns, kpressed)
	top.draw()
	if settings.DEBUG:
		text = "%.1ffps" % clock.get_fps()
		ptext.draw(text, bottomleft = F(5, 475), fontsize = F(18), color = "white", owidth = 1)
	pygame.display.flip()

	if K_ESCAPE in kdowns:
		scene.quit()
	if K_F11 in kdowns:
		settings.fullscreen = not settings.fullscreen
		view.init()
	if K_F12 in kdowns:
		if not os.path.exists(settings.screenshotdir):
			os.makedirs(settings.screenshotdir)
		t = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
		path = os.path.join(settings.screenshotdir, "screenshot-%s.png" % t)
		pygame.image.save(view.screen, path)

pygame.quit()



