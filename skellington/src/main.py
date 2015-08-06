import pygame
from pygame.locals import *
from src import settings, window

screen = pygame.display.set_mode(settings.windowsize, settings.displayflags)
pygame.display.set_caption(settings.gamename)
pygame.font.init()

clock = pygame.time.Clock()
playing = True
while playing:
	dt = 0.001 * clock.tick(settings.maxfps)
	for event in pygame.event.get():
		if event.type == QUIT:
			playing = False
		if event.type == KEYDOWN and event.key == K_ESCAPE:
			playing = False
	screen.fill((0, int(0.1 * pygame.time.get_ticks()) % 256, 0))
	screen.blit(pygame.font.Font(None, 40).render("Press Esc to quit", True, (255, 255, 255)), (0, 0))
	pygame.display.flip()

pygame.quit()
