import pygame
from . import view, world, thing

playing = True
mouseV = [0, 0]
mouseG = [0, 0]
cursor = None  # Star currently being pointed to, if any.
anchor = None  # Star selected

def think(dt):
	global playing, mouseV, mouseG, cursor, anchor
	ldown = False
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			playing = False
		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			playing = False
		if event.type == pygame.KEYDOWN and event.key == pygame.K_F10:
			view.change_res()
		if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
			view.toggle_fullscreen()
		if event.type == pygame.KEYDOWN and event.key == pygame.K_F12:
			view.screenshot()
		if event.type == pygame.KEYDOWN and event.key == pygame.K_F2:
			world.advance()
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			ldown = True
	mouseV = pygame.mouse.get_pos()
	mouseG = view.GconvertV(mouseV)
	nearest = min(world.stars, key = lambda star: star.distanceto(mouseG))
	if nearest.distanceto(mouseG) < 2:
		cursor = nearest
	else:
		cursor = None
	if ldown:
		if cursor is None:
			anchor = None
		elif cursor is anchor:
			anchor = None
		elif cursor is not None and anchor is None:
			anchor = cursor
		elif cursor is not None and anchor is not None:
			link0 = anchor.haslinkto(cursor)
			if link0 is not None:
				link0.unplace()
			else:
				link = thing.Link(anchor, cursor)
				world.placelink(link)
			anchor = None

