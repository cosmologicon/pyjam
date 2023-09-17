import pygame, os, math
from functools import lru_cache
from . import pview

@lru_cache(1000)
def getimg(imgname, scale, A):
	if scale != 1 or A != 0:
		img = getimg(imgname, 1, 0)
		return pygame.transform.rotozoom(img, A, scale)
	path = os.path.join("img", f"{imgname}.png")
	img = pygame.image.load(path).convert_alpha()
	return img
	

def loground(value, N):
	return math.exp(round(N * math.log(value)) / N)

def draw(imgname, pV, scale, A):
	scale = loground(scale, 20)
	A = round(math.degrees(-A) / 5) * 5
	img = getimg(imgname, scale, A)
	pview.screen.blit(img, img.get_rect(center = pV))

