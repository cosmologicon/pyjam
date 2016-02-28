import pygame, random, math, util
from . import window
from .util import F, debug

tilesize = 20
tiles = {}
T = 20

mapimg = None
def init():
	global mapimg
	mapimg = pygame.image.load("/tmp/map.png").convert()


def randomtile():
	surf = pygame.Surface((tilesize, tilesize)).convert()
	for x in range(tilesize):
		for y in range(tilesize):
			r = random.randint(40, 60)
			g = random.randint(40, 60)
			b = random.randint(40, 60)
			surf.set_at((x, y), (r, g, b))
	return surf

def gettile(ntile):
	if ntile in tiles:
		return tiles[ntile]
	X, Y = ntile
	surf = pygame.Surface((tilesize, tilesize)).convert()
	surf.fill((0, 0, 0))
	mx, my = mapimg.get_size()
	px, py = mx // 2 + X * tilesize, my // 2 - Y * tilesize
	surf.blit(mapimg, (-px, -py))
	fuzz = randomtile()
	fuzz.set_alpha(100)
	surf.blit(fuzz, (0, 0))
	tiles[ntile] = surf
	debug("background tile size %d" % len(tiles))
	return surf

land = {}
def getland(ntile):
	key = ntile, util.f
	if key in land:
		return land[key]
	tile = gettile(ntile)
	w = F(math.ceil(window.Z * T))
	h = F(math.ceil(window.Z * T * window.fy))
	surf = pygame.transform.smoothscale(tile, (w, h))
	land[key] = surf
	debug("background land size %d" % len(land))
	return surf

def draw():
	x0, y0 = window.screentoworld(0, window.sy)
	x1, y1 = window.screentoworld(window.sx, 0)
	X0 = int(math.floor(x0 / T))
	Y0 = int(math.floor(y0 / T))
	X1 = int(math.ceil(x1 / T))
	Y1 = int(math.ceil(y1 / T))

	for X in range(X0, X1):
		for Y in range(Y0, Y1):
			surf = getland((X, Y))
			pos = window.worldtoscreen(X * T, (Y + 1) * T, 0)
			window.screen.blit(surf, pos)


