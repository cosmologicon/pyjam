import pygame, datetime, os.path
from pygame.locals import *
from src import settings, thing, window, ptext, state
from src.window import F
from src.scenes import play

window.init()
pygame.display.set_caption(settings.gamename)
play.init()

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
	kpressed = pygame.key.get_pressed()
	play.think(dt, events, kpressed)
	play.draw()
	if settings.DEBUG:
		ptext.draw("%.1ffps" % clock.get_fps(), fontsize = F(36), owidth = 2,
			bottomright = (window.sx - F(10), window.sy - F(10)))
		ptext.draw("%.4f, %.1f" % (state.you.X, state.you.y), fontsize = F(36), owidth = 2,
			bottomright = (window.sx - F(10), window.sy - F(50)))
	pygame.display.flip()

pygame.quit()

