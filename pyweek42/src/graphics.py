import pygame, os
from functools import cache, lru_cache
from . import pview
from .pview import T

@cache
def baseimg(fname):
	return pygame.image.load(os.path.join("img", f"{fname}.png")).convert_alpha()

@cache
def img0(fname, scale = 1, angle = 0, mask = None):
	print(fname, scale, angle, mask)
	if scale != 1 or angle != 0:
		return pygame.transform.rotozoom(img0(fname, mask = mask), angle, scale)
	if mask is not None:
		return applymask(img0, mask)
	return baseimg(fname)

Qangle = 10
def img(fname, scale = 1, angle = 0, mask = None):
	# Quantize scale?
	angle = int(round(angle / Qangle) * Qangle) % 360
	return img0(fname, scale, angle, mask)

def drawimgB(fname, posB, scaleB, angle = 0, mask = None):
	scale = scaleB * pview.f
	surf = img(fname, scale, angle, mask)
	pview.screen.blit(surf, surf.get_rect(center = T(posB)))

def drawcircleB(posB, rB, color = (255, 255, 255)):
	pygame.draw.circle(pview.screen, color, T(posB), T(rB), 1)



