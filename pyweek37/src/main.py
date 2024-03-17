import pygame
from . import settings, view, control, pview, playscene

view.init()
playscene.init()
control.init()

clock = pygame.time.Clock()
dtaccum = 0
while not control.quit and pygame.K_ESCAPE not in control.kdowns:
	dt = min(0.001 * clock.tick(settings.maxfps), 1 / settings.minfps)
	control.think(dt)
	if pygame.K_F12 in control.kdowns: pview.screenshot()

	playscene.think(dt)
	playscene.draw()
	
	


