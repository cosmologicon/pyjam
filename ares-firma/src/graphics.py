import pygame, math
from functools import lru_cache
from . import pview
cache = lru_cache

@cache
def sunimg(rV, f):
	if rV != 400:
		return pygame.transform.smoothscale(sunimg(400, f), (2 * rV, 2 * rV))
	img = pygame.Surface((2 * rV, 2 * rV)).convert_alpha()
	img.fill((255, 255, 0, 0))
	color = (255, 255, 0, 48)
	pygame.draw.circle(img, color, (rV, rV), int(round(0.6 * rV)))
	p0s = [(0, 1), (0.3, 0.7), (-0.3, 0.7)]
	for jtheta in range(7):
		theta = (jtheta + f) * math.tau / 7
		R = math.R(theta)
		ps = [R(p) for p in p0s]
		ps = [(int(round((x + 1) * rV)), int(round((y + 1) * rV))) for x, y in ps]
		pygame.draw.polygon(img, color, ps)
	return img

@cache
def arrowimg(rV, theta):
	if theta != 0:
		return pygame.transform.rotozoom(arrowimg(100, 0), theta, rV / 100)
	elif rV != 100:
		return pygame.transform.smoothscale(arrowimg(100, 0), (2 * rV, 2 * rV))
	img = pygame.Surface((2 * rV, 2 * rV)).convert_alpha()
	img.fill((255, 255, 0, 0))
	color = (255, 255, 0, 48)
	pygame.draw.circle(img, color, (rV, rV), int(round(0.6 * rV)))


def sun(rV, f):
	return sunimg(int(round(rV)), int(f * 20) % 20 / 20)

def drawat(img, pV):
	pview.screen.blit(img, img.get_rect(center = pV))
	
