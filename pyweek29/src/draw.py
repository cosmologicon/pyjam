import pygame
from functools import lru_cache
from . import pview

@lru_cache(None)
def getimg(filename):
	return pygame.image.load("img/%s.png" % filename).convert_alpha()


specs = {
	"standing": ["backarm", "stand", "torso", "armdown"],
	"falling": ["backarm", "drop", "torso", "armup"],
}

@lru_cache(None)
def youimg0(spec):
	img = pygame.Surface((2020, 2052)).convert_alpha()
	img.fill((0, 0, 0, 0))
	for filename in specs[spec]:
		img.blit(getimg("you-%s" % filename), (0, 0))
	return img

@lru_cache(None)
def youimg(spec, scale, angle):
	img = youimg0(spec)
	if angle:
		img = pygame.transform.rotate(img, angle)
	size = pview.I([a * scale / 2000 for a in img.get_size()])
	return pygame.transform.smoothscale(img, size)

def you(spec, screenpos, scale, angle = 0):
	angle = int(round(angle)) % 360
	img = youimg(spec, scale, angle)
	rect = img.get_rect(center = screenpos)
	pview.screen.blit(img, rect)
	

