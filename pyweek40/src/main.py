import pygame
from . import ptext
from . import settings, view, play
from .pview import T

view.init()


playing = True
clock = pygame.time.Clock()
while playing:
	dt = min(0.001 * clock.tick(settings.maxfps), 1 / settings.minfps)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			playing = False
		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			playing = False
	
	play.think(dt)
	play.draw()
	ptext.draw(f"{clock.get_fps():.1f}fps", bottomleft = T(10, 790), fontsize = T(30))
	pygame.display.flip()




