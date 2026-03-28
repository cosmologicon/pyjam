import pygame, math, random
from functools import cache, lru_cache
from . import pview, fuzz, geometry

@cache
def img0(fname):
	return pygame.image.load(f"img/{fname}.png").convert_alpha()

@cache
def scaledimg(imgname, size):
	img = img0(imgname)
	if size == img.get_size():
		return img
	return pygame.transform.smoothscale(img, size)

def mask(img, color):
	img = img.copy()
	msurf = img.copy()
	msurf.fill(color)
	img.blit(msurf, (0, 0), special_flags = pygame.BLEND_RGBA_MULT)
	return img

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
	pview.fill((70, 60, 120, alpha))

def coverstars(sky):
	alpha = math.interpI(sky, 1, 128, 3, 0)
	pview.fill((70, 60, 120, alpha))


Fstar = 4

@cache
def starimg0(r, color, n):
	if color != (255, 255, 255):
		return mask(starimg0(r, (255, 255, 255), n), color)
	s0 = int(math.ceil(r))
	if s0 != 100:
		return pygame.transform.smoothscale(starimg0(100, (255, 255, 255), n), (2 * s0, 2 * s0))
	s = r * Fstar
	img = pygame.Surface((2 * s, 2 * s)).convert_alpha()
	img.fill((0, 0, 0, 0))
	limg = img.copy()
	for l in range(40):
		limg.fill((0, 0, 0, 0))
		ps = [math.I(math.CS(random.uniform(0, math.tau), r = random.uniform(0, s), center = (s, s))) for _ in range(3)]
		mcolor = (255, 255, 255) if random.random() > 0.5 else (0, 0, 0)
		lcolor = math.mixI(color, mcolor, random.uniform(0, 0.5))
		acolor = list(lcolor) + [30]
		pygame.draw.polygon(limg, acolor, ps)
		img.blit(limg, (0, 0))
#	pygame.draw.circle(img, color, (s, s), s)
	return pygame.transform.smoothscale(img, (2 * s0, 2 * s0))

def roundcolor(color):
	return tuple(math.clamp(int(round(c / 4)) * 4, 0, 255) for c in color)

maxn = 0
def starimg(r, color):
	global maxn
	r = round(r * Fstar) / Fstar
	color = roundcolor(color)
	n = random.randint(0, maxn)
	if n == maxn and maxn < 29:
		maxn += 1
	return starimg0(r, color, n)

def drawat(img, pV):
	pview.screen.blit(img, dest = img.get_rect(center = pV))

# rV can be non-integer
def drawstarV(pV, rV, color0):
	color = math.interpI(random.uniform(0, 0.2), 0, color0, 1, (0, 0, 0))
	drawat(starimg(rV, color), pV)

def drawlinkV(pV0, pV1, wV, color0):
	dx, dy = math.I(math.norm(geometry.vminus(pV1, pV0), wV))
	dp = -dy, dx
	ps = [geometry.vplus(pV0, dp), geometry.vplus(pV1, dp),
		geometry.vminus(pV1, dp), geometry.vminus(pV0, dp)]
	pygame.draw.polygon(pview.screen, color0, ps, 0)





