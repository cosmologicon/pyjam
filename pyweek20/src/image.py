from __future__ import division
import pygame, os.path, random, math
from pygame.locals import *
from src import window, ptext

cache = {}
def get(filename, s = None, angle = 0, alpha = 1):
	if filename == "slash":
		angle = int(round(angle / 5)) * 5 % 90
	else:
		angle = int(round(angle)) % 360
	alpha = int(round(alpha * 16)) / 16
	key = filename, s, angle, alpha
	if key in cache:
		return cache[key]
	if alpha != 1:
		img = get(filename, s, angle).copy()
		arr = pygame.surfarray.pixels_alpha(img)
		arr *= alpha
		del arr
	elif s is not None and angle == 0:
		img = get(filename)
		a = int(round(s))
		img = pygame.transform.smoothscale(img, (a, a))
	elif s is not None or angle != 0:
		img = get(filename)
		img = pygame.transform.rotozoom(img, angle, s / img.get_width())
	else:
		if "." not in filename:
			filename = filename + ".png"
		path = os.path.join("data", "img", filename)
		if os.path.exists(path):
			img = pygame.image.load(path)
			if filename.endswith(".png"):
				img = img.convert_alpha()
			else:
				img = img.convert()
		else:
			img = pygame.Surface((40, 40)).convert_alpha()
			img.fill((random.randint(100, 250), random.randint(100, 250), random.randint(100, 250), 80))
			ptext.drawbox(filename, img.get_rect(), surf = img, owidth = 1)
	cache[key] = img
	return img

def worlddraw(filename, X, y, r = 1, angle = 0, alpha = 1, rotate = True):
	px, py = window.screenpos(X, y)
	s = 2 * r * window.camera.R
	if not -s < px < window.sx + s or not -s < py < window.sy + s:
		return
	angle += math.degrees(window.camera.X0 - X)
	if not rotate:
		angle = 0
	img = get(filename, s, angle, alpha)
	window.screen.blit(img, img.get_rect(center = (px, py)))
	

