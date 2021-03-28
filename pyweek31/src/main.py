import pygame
from . import settings, state, view
from . import playscene

view.init()
playscene.init()

playing = True
clock = pygame.time.Clock()
dtaccum = 0
while playing:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			playing = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				playing = False
	kpressed = pygame.key.get_pressed()
	mposV = pygame.mouse.get_pos()
	playscene.control(mposV)

	dt = min(0.001 * clock.tick(settings.maxfps), 1 / settings.minfps)
	if settings.DEBUG and kpressed[pygame.K_F1]:
		dt *= 5
	dtaccum += dt
	
	dt0 = 1 / settings.maxfps
	while dtaccum >= dt0:
		playscene.think(dt0)
		dtaccum -= dt0
	
	view.clear()
	playscene.draw()
	pygame.display.flip()
	
	if settings.DEBUG:
		xG, yG = view.GconvertV(mposV)
		pygame.display.set_caption("%s | %.1ffps | %.2f %.2f" % (settings.gamename, clock.get_fps(), xG, yG))

