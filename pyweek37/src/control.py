import pygame

def init():
	global posD, kdowns, quit, click, rclick
	posD = [0, 0]
	kdowns = []
	quit = False
	click = False
	rclick = False

def think(dt):
	global posD, kdowns, quit, click, rclick
	posD = pygame.mouse.get_pos()
	kdowns = []
	quit = False
	click = False
	rclick = False
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit = True
		if event.type == pygame.KEYDOWN:
			kdowns.append(event.key)
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			click = True
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
			rclick = True


