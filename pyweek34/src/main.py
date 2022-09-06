import pygame
from . import pview, ptext
from . import settings, view, play
from .pview import T

view.init()

clock = pygame.time.Clock()
playing = True
while playing:
	dt = min(0.001 * clock.tick(settings.maxfps), 1 / settings.minfps)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			playing = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				playing = False
			if event.key == pygame.K_F10:
				pview.cycle_height(settings.heights)
			if event.key == pygame.K_F11:
				pview.toggle_fullscreen()
			if event.key == pygame.K_F12:
				pview.screenshot()

	pview.fill((60, 20, 0))
	
	if settings.DEBUG:
		ptext.draw(f"{clock.get_fps():.1f}fps", bottomleft = pview.bottomleft, owidth = 1,
			fontsize = T(26))
	pygame.display.flip()


