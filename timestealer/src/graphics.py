import pygame, os
from functools import cache, lru_cache
from . import pview, view
from .pview import T

@cache
def baseimg(fname):
	return pygame.image.load(os.path.join("img", f"{fname}.png")).convert_alpha()

@lru_cache(10000)
def img0(fname, scale = 1, angle = 0, mask = None):
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

def drawimgG(fname, posG, scaleG, angle = 0, mask = None):
	drawimgB(fname, view.BconvertG(posG), view.BscaleG(scaleG), angle, mask)

def drawcircleB(posB, rB, color = (255, 255, 255)):
	pygame.draw.circle(pview.screen, color, T(posB), T(rB), 1)

def drawcircleG(posG, rG, color = (255, 255, 255)):
	drawcircleB(view.BconvertG(posG), view.BscaleG(rG), color)

def drawrectG(posG, sizeG, color = (255, 255, 255), fill = False):
	wG, hG = sizeG
	sizeB = view.BscaleG(wG), view.BscaleG(hG)
	rect = pygame.Rect(T(view.BconvertG(posG)), sizeB)
	pygame.draw.rect(pview.screen, color, rect, (0 if fill else T(1)))

