import pygame, random, math, util
from . import window

tilesize = 20
tiles = {}
T = 40

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
	tiles[ntile] = randomtile()
	return tiles[ntile]

land = {}
def getland(ntile):
	key = ntile, util.f
	if key in land:
		return land[key]
	tile = gettile(ntile)
	w = int(math.ceil(window.Z * T))
	h = int(math.ceil(window.Z * T * window.fy))
	surf = pygame.transform.smoothscale(tile, (w, h))
	land[key] = surf
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


