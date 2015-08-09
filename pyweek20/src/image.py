import pygame, os.path
from pygame.locals import *
from src import window, ptext

cache = {}
def get(filename):
	key = filename
	if key in cache:
		return cache[key]
	path = os.path.join("data", "img", filename + ".png")
	if os.path.exists(path):
		img = pygame.image.load(filename).convert_alpha()
	else:
		img = pygame.Surface((40, 40)).convert_alpha()
		img.fill((255, 255, 255, 40))
		ptext.drawbox(filename, img.get_rect(), surf = img, owidth = 1)
	cache[key] = img
	return img
		
	

