import pygame
from . import settings, window, ptext
from .util import F

window.init()
clock = pygame.time.Clock()
playing = True
while playing:
	dt = 0.001 * clock.tick(settings.maxfps)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			playing = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_F11:
				window.togglefullscreen()
			if event.key == pygame.K_F12:
				window.screenshot()
			if event.key == pygame.K_ESCAPE:
				playing = False

	window.screen.fill((0, 0, 0))
	if settings.DEBUG:
		ptext.draw("%.1ffps" % clock.get_fps(), bottomright = F(844, 470), fontsize = F(24))
	pygame.display.flip()

pygame.quit()

