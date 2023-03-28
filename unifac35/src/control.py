import pygame
from . import view

click = False
release = False
mposV = None
mposG = None
misdown = False

def think(dt):
	global mposV, mposG, click, release, misdown
	mposV = pygame.mouse.get_pos()
	mposG = view.GconvertV(mposV)
	mdown = pygame.mouse.get_pressed()[0]
	if mdown and not misdown:
		click = True
	elif misdown and not mdown:
		release = True
	misdown = mdown

def getstate():
	global click, release
	state = mposV, mposG, click, release
	click = False
	release = False
	return state

