import pygame
from . import settings, view

settings.load()
view.init()

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
	
	dtaccum += dt
	dt0 = 1 / settings.maxfps
	while dtaccum > dt0:
		dtaccum -= dt0
		# think(dt0)

	view.clear()
	pygame.display.flip()


