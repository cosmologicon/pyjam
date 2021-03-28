import pygame
from . import settings, state, view

view.init()

playing = True
clock = pygame.time.Clock()
dtaccum = 0
while playing:
	dt = min(0.001 * clock.tick(settings.maxfps), 1 / settings.minfps)
	dtaccum += dt
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			playing = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				playing = False
	
	dt0 = 1 / settings.maxfps
	while dtaccum >= dt0:
		state.think(dt0)
		dtaccum -= dt0
	
	view.clear()
	state.draw()
	pygame.display.flip()
	
	if settings.DEBUG:
		pygame.display.set_caption("%s | %.1ffps" % (settings.gamename, clock.get_fps()))

