import pygame
from . import settings, view, pview, scene

view.init()
pygame.display.set_caption(settings.gamename)

clock = pygame.time.Clock()
playing = True
while playing:
	dt = 0.001 * min(clock.tick(settings.maxfps), 1 / settings.minfps)
	kdowns = set()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			playing = False
		if event.type == pygame.KEYDOWN:
			kdowns.add(event.key)

	if pygame.K_ESCAPE in kdowns:
		playing = False
	
	pview.fill((0, 0, 0))
	current = scene.top()
	if current:
		current.think(dt, kdowns)
		current.draw()

	if settings.DEBUG:
		pygame.display.set_caption("%s %.1ffps" % (settings.gamename, clock.get_fps()))
	pygame.display.flip()


