import pygame, math
from functools import cache
from . import pview

Fstar = 8

@cache
def starimg0(r, color):
	s0 = int(math.ceil(r))
	s = r * Fstar
	img = pygame.Surface((2 * s, 2 * s)).convert_alpha()
	img.fill((0, 0, 0, 0))
	pygame.draw.circle(img, color, (s, s), s)
	return pygame.transform.smoothscale(img, (s0, s0))

def starimg(r, color):
	r = round(r * Fstar) / Fstar
	return starimg0(r, color)

def drawat(img, pV):
	pview.screen.blit(img, dest = img.get_rect(center = pV))

# rV can be non-integer
def drawstarV(pV, rV, color):
	drawat(starimg(rV, color), pV)
	

