import pygame
from pygame.locals import *
from src import settings, window, ptext
from src.scenes import play
from src.window import F

ptext.FONT_NAME_TEMPLATE = "data/%s.ttf"
pygame.mixer.init()
window.init()
play.init()

clock = pygame.time.Clock()
playing = True
while playing:
	dt = 0.001 * clock.tick(settings.maxfps)
	events = list(pygame.event.get())
	for event in events:
		if event.type == QUIT:
			playing = False
		if event.type == KEYDOWN and event.key == K_ESCAPE:
			playing = False
	play.think(dt, events)
	play.draw()
	ptext.draw("%.1ffps" % clock.get_fps(), fontname = "Oregano", fontsize = F(32),
		bottomright = window.screen.get_rect().bottomright, color = "white")
	pygame.display.flip()

pygame.quit()
