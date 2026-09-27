# B (baseline) coordinates: baseline pixels. +x is right. +y is down. (0, 0) is upper left of screen.
# G (game) coordinates. +x is right. +y is down.

import pygame
from . import settings, pview

def init():
	pview.set_mode(size0 = settings.size0, height = settings.height, fullscreen = settings.fullscreen, forceres = settings.forceres)
	pygame.display.set_caption(settings.gamename)

class camera:
	xG0 = 0
	yG0 = 0
	zoom = 40  # baseline pixels per game unit

def BscaleG(rG):
	return rG * camera.zoom

def BconvertG(pG):
	xG, yG = pG
	xB = pview.centerx0 + BscaleG(xG - camera.xG0)
	yB = pview.centery0 + BscaleG(yG - camera.yG0)
	return xB, yB






