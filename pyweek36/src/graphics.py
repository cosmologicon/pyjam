import pygame, os, math
from functools import lru_cache
from . import pview, view
from .pview import T

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
	A = round(math.degrees(A) / 5) * 5
	img = getimg(imgname, scale, A)
	pview.screen.blit(img, img.get_rect(center = pV))

@lru_cache(20)
def glow(s, seed = 0, color = None):
	if s != 40:
		return pygame.transform.scale(glow(40, seed, color), (2 * s, 2 * s))
	if color is not None:
		img0 = glow(s, seed)
		img = img0.copy()
		img.fill(color)
		img.blit(img0, (0, 0), special_flags = pygame.BLEND_RGBA_MULT)
		return img
	img = pygame.Surface((2 * s, 2 * s)).convert_alpha()
	ps = [(p - s + 0.5) / s for p in range(2 * s)]
	for px, x in enumerate(ps):
		for py, y in enumerate(ps):
			r = math.hypot(x, y)
			f = math.fuzzrange(0.8, 1, px, py, seed)
			alpha = math.clamp(int(round(255 * f * (1 - r ** 4))), 0, 255)
			img.set_at((px, py), (255, 255, 255, alpha))
	return img

@lru_cache(1)
def getstars(N):
	stars = []
	for j in range(N):
		x = math.fuzzrange(0, 100000, j, 123)
		y = math.fuzzrange(0, 100000, j, 234)
		z = math.mix(0.2, 1.0, j / N)
		color = math.imix((0, 0, 0), (255, 255, 255), z)
		stars.append((x, y, z, color))
	return stars

def drawstars():
	density = 0.001
	N = int(pview.area * density)
	for x, y, z, color in getstars(N):
		px = int(-view.VscaleG * view.xG0 * z + x) % pview.w
		py = int(view.VscaleG * view.yG0 * z + y) % pview.h
		pview.screen.set_at((px, py), color)

@lru_cache(10)
def getnebula(s = 40):
	if s != 40:
		return pygame.transform.smoothscale(getnebula(40), (s, s))
	img = pygame.Surface((s, s)).convert_alpha()
	for px in range(s):
		for py in range(s):
			alpha = int(math.fuzzrange(0, 3, px, py))
			img.set_at((px, py), (255, 255, 255, alpha))
	return img

def tilerange(s, p0, pmin, pmax):
	j0 = int((pmin - p0) // s)
	j1 = int((pmax - p0) // s) + 1
	return [p0 + j * s for j in range(j0, j1)]

def drawnebula():
	for jz in range(3):
		z = 0.2 * math.Phi ** jz
		s = T(view.VscaleG * 20 * z)
		px0 = int(round(-pview.f * view.VscaleG * z * view.xG0 + math.fuzzrange(0, s, jz, 1.3)))
		py0 = int(round(pview.f * view.VscaleG * z * view.yG0 + math.fuzzrange(0, s, jz, 1.4)))
		img = getnebula(s)
		for px in tilerange(s, px0, 0, pview.w):
			for py in tilerange(s, py0, 0, pview.h):
				pview.screen.blit(img, (px, py))


