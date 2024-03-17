import pygame

def init():
	global pos, kdowns, quit
	pos = [0, 0]
	kdowns = []
	quit = False

def think(dt):
	global pos, kdowns, quit
	pos = pygame.mouse.get_pos()
	kdowns = []
	quit = False
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit = True
		if event.type == pygame.KEYDOWN:
			kdowns.append(event.key)
	

