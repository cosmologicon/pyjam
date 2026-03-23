import pygame
from . import view, world

playing = True
mouseV = [0, 0]
mouseG = [0, 0]
cursor = None  # Star currently being pointed to, if any.

def think():
	global playing, mouseV, mouseG, cursor
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			playing = False
		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			playing = False
	mouseV = pygame.mouse.get_pos()
	mouseG = view.GconvertV(mouseV)
	nearest = min(world.stars, key = lambda star: star.distanceto(mouseG))
	if nearest.distanceto(mouseG) < 2:
		cursor = nearest
	else:
		cursor = None

