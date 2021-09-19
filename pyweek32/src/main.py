import pygame
from . import settings, view, playscene

settings.load()
view.init()
playscene.init()

playing = True
clock = pygame.time.Clock()
dtaccum = 0
while playing:
	dt = min(0.001 * clock.tick(settings.maxfps), 1 / settings.minfps)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			playing = False
		if settings.DEBUG and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			playing = False
		if event.type == pygame.KEYDOWN and event.key == pygame.K_F10:
			view.resize()
		if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
			view.toggle_fullscreen()
		if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
			pview.toggle_fullscreen()
	kpressed = pygame.key.get_pressed()

	
	dtaccum += dt
	dt0 = 1 / settings.maxfps
	while dtaccum > dt0:
		dtaccum -= dt0
		playscene.think(dt0, kpressed)

	view.clear()
	playscene.draw()
	pygame.display.flip()


