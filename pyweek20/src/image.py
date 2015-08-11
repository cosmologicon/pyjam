from __future__ import division
import pygame, os.path, random, math
from pygame.locals import *
from src import window, ptext

cache = {}
def get(filename, s = 1, angle = 0):
	angle = int(round(angle)) % 360
	key = filename, s, angle
	if key in cache:
		return cache[key]
	if s == 1 and angle == 0:
		path = os.path.join("data", "img", filename + ".png")
		if os.path.exists(path):
			img = pygame.image.load(filename).convert_alpha()
		else:
			img = pygame.Surface((40, 40)).convert_alpha()
			img.fill((random.randint(100, 250), random.randint(100, 250), random.randint(100, 250), 80))
			ptext.drawbox(filename, img.get_rect(), surf = img, owidth = 1)
	else:
		img = get(filename)
		img = pygame.transform.rotozoom(img, angle, s / img.get_width())
	cache[key] = img
	return img

def worlddraw(filename, X, y, r = 1, angle = 0):
	px, py = window.screenpos(X, y)
	s = 2 * r * window.cameraR
	if not -s < px < window.sx + s or not -s < py < window.sy + s:
		return
	angle += math.degrees(window.cameraX0 - X)
	img = get(filename, s)
	window.screen.blit(img, img.get_rect(center = (px, py)))
	

