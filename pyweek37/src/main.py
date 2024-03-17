import pygame
from . import settings, view, control, pview, playscene

view.init()
playscene.init()
control.init()

clock = pygame.time.Clock()
dtaccum = 0
while not control.quit:
	dt = min(0.001 * clock.tick(settings.maxfps), 1 / settings.minfps)
	control.think(dt)

	playscene.think(dt)
	playscene.draw()
	
	


