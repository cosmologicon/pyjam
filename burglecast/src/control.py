import pygame, math
from . import view

click = False
release = False
drop = False
mposV = None
mposG = None
dragging = False

misdown = False
clickpV0 = None
clickt0 = None

def think(dt):
	global mposV, mposG, click, release, drop, misdown, dragging, clickpV0, clickt0
	mposV = pygame.mouse.get_pos()
	mposG = view.GconvertV(mposV)
	mdown = pygame.mouse.get_pressed()[0]
	if mdown and not misdown:
		click = True
		clickpV0 = mposV
		clickt0 = pygame.time.get_ticks() * 0.001
	elif misdown and not mdown:
		release = True
		if dragging:
			drop = True
		dragging = False
	misdown = mdown
	if misdown and not dragging:
		t = pygame.time.get_ticks() * 0.001
		if math.distance(clickpV0, mposV) >= 4 or t - clickt0 >= 0.3:
			dragging = True

def getstate():
	global click, release, drop
	state = mposV, mposG, click, release, drop
	click = False
	release = False
	drop = False
	return state

