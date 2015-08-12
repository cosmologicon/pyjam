from __future__ import division
import pygame, datetime, os.path
from pygame.locals import *
from src import settings, thing, window, ptext, state, background, scene
from src.window import F
from src.scenes import play, intro, title

window.init()
pygame.display.set_caption(settings.gamename)
pygame.mixer.init()
background.init()

lastscene = None
scene.current = intro

clock = pygame.time.Clock()
playing = True
while playing:
	dt = clock.tick(settings.maxfps) * 0.001
	events = list(pygame.event.get())
	for event in events:
		if event.type == QUIT:
			playing = False
		if event.type == KEYDOWN and event.key == K_ESCAPE:
			playing = False
		if event.type == KEYDOWN and event.key == K_F11:
			settings.fullscreen = not settings.fullscreen
			window.init()
		if event.type == KEYDOWN and event.key == K_F12:
			fname = datetime.datetime.now().strftime("screenshot-%Y%m%d%H%M%S.png")
			pygame.image.save(window.screen, os.path.join("screenshots", fname))
		if settings.DEBUG and event.type == KEYDOWN and event.key == K_F3:
			settings.drawbackground = not settings.drawbackground
		if settings.DEBUG and event.type == KEYDOWN and event.key == K_F2:
			print("ships %d" % len(state.ships))
			print("objs %d" % len(state.objs))
			print("hazards %d" % len(state.hazards))
	kpressed = pygame.key.get_pressed()
	if scene.current is not lastscene:
		scene.current.init()
		lastscene = scene.current
	s = scene.current
	s.think(dt, events, kpressed)
	s.draw()
	if settings.DEBUG:
		ptext.draw("%.4f, %.1f" % (state.you.X, state.you.y), fontsize = F(36),
			bottomright = (window.sx - F(10), window.sy - F(50)), cache = False)
		ptext.draw("%.1ffps" % clock.get_fps(), fontsize = F(36),
			bottomright = (window.sx - F(10), window.sy - F(10)), cache = False)
	pygame.display.flip()

pygame.quit()

