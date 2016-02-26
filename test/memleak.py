# Pygame program with a memory leak

import pygame
from src import ptext

ptext.AUTO_CLEAN = False

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Leaking memory... press any key to quit")

n = 0
while not any(event.type in (pygame.QUIT, pygame.KEYDOWN) for event in pygame.event.get()):
	screen.fill((0, 60, 0))
	ptext.getsurf("abcdefghijklmn" + str(n), fontsize = 50)
	n += 1
	s = "Approx. memory\nusage: %dMB" % (ptext._surf_size_total >> 20)
	ptext.draw(s, fontsize = 60, center = screen.get_rect().center)
	pygame.display.flip()

