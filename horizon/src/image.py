from __future__ import division
import pygame, os.path, random, math
from pygame.locals import *
from src import window, ptext, settings

cache = {}
def get(filename, s = None, angle = 0, alpha = 1):
	aresolution, asymmetry = settings.angleresolution, 1
	if filename == "slash-red":
		aresolution = 15
		asymmetry = 4
	elif filename == "payload":
		asymmetry = 5
	elif filename == "qtarget":
		asymmetry = 2
	elif filename == "cursor":
		asymmetry = 4
	
	angle = int(round(angle / aresolution)) * aresolution % (360 / asymmetry)
	alpha = int(int(round(alpha * settings.alpharesolution)) * 255 / settings.alpharesolution)
	key = filename, s, angle, alpha
	if key in cache:
		return cache[key]
	if alpha != 255:
		img = get(filename, s, angle).copy()
		img.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
	elif s is not None and angle == 0:
		img = get(filename)
		a = int(round(s))
		img = pygame.transform.smoothscale(img, (a, a))
	elif settings.smoothrotozoom and angle != 0 and s is not None:
		img = get(filename)
		w0 = img.get_width()
		img = pygame.transform.rotate(img, angle)
		a = int(round(s * img.get_width() / w0))
		img = pygame.transform.smoothscale(img, (a, a))
	elif s is not None or angle != 0:
		img = get(filename)
		zoom = 1 if s is None else s / img.get_width()
		img = pygame.transform.rotozoom(img, angle, zoom)
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
	if settings.DEBUG:
		imgx, imgy = img.get_size()
		cache["total"] = cache.get("total", 0) + imgx * imgy
		dataline = "%d %d %s %s\n" % (len(cache), cache["total"], key, img.get_size())
		open("debug-image-data.txt", "a").write(dataline)
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
	

