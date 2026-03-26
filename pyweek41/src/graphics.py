import pygame, math, random
from functools import cache, lru_cache
from . import pview, fuzz

@cache
def img0(fname):
	return pygame.image.load(f"img/{fname}.png").convert_alpha()

@cache
def scaledimg(imgname, size):
	img = img0(imgname)
	if size == img.get_size():
		return img
	return pygame.transform.smoothscale(img, size)

def drawbackground():
	pview.screen.blit(scaledimg("background", pview.size), (0, 0))

@cache
def sparklers(size):
	w, h = size
	N = int(round(0.001 * w * h))
	ret = []
	for n in range(N):
		x = fuzz.randint(0, w - 1, 1.234, n, w, h)
		y = fuzz.randint(0, h - 1, 1.345, n, w, h)
		c = fuzz.randint(40, 80, 1.456, n, w, h)
		ret.append((x, y, c))
	return ret

@lru_cache(1)
def sparklerimg(size):
	img = pygame.Surface(size).convert_alpha()
	img.fill((0, 0, 0, 0))
	for x, y, c in sparklers(size):
		img.set_at((x, y), (c, c, c))
	return img

def drawsparkle():
	if True:
		pview.screen.blit(sparklerimg(pview.size), (0, 0))
		ps = sparklers(pview.size)
		for n in range(len(ps) // 60):
			x, y, c = random.choice(ps)
			c = int(c * random.uniform(1.2, 1.8))
			pview.screen.set_at((x, y), (c, c, c))
	elif False:
		for y in range(pview.h):
			x = int(fuzz.uniform(0, pview.w, 0.432, y))
			c = int(fuzz.uniform(0, 80, 0.543, y) * random.uniform(0.6, 1.5))
			pview.screen.set_at((x, y), (c, c, c))
	else:
		for n in range(int(0.0001 * pview.area)):
			x = random.randint(0, pview.w)
			y = random.randint(0, pview.h)
			c = random.randint(40, 120)
			pview.screen.set_at((x, y), (c, c, c))

def drawtreeline():
	pview.screen.blit(scaledimg("treeline", pview.size), (0, 0))

@lru_cache(1)
def backimg(size, sky):
	img = scaledimg("background", size).copy()
	dark = img.copy()
	dark.fill((0, 0, 0, math.interpI(sky, 3, 255, 6, 0)))
	img.blit(dark, (0, 0))
	img.blit(sparklerimg(size), (0, 0))
	return img

def drawback(sky):
	pview.screen.blit(backimg(pview.size, sky), (0, 0))
	drawsparkle()
	alpha = math.interpI(sky, 1, 255, 6, 0)
	pview.fill((40, 40, 90, alpha))



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
	

