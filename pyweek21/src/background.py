from __future__ import division
import pygame, random, math, util
from . import window, settings
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
	d = 2
	X, Y = ntile
	surf = pygame.Surface((tilesize + 2 * d, tilesize + 2 * d)).convert()
	surf.fill((0, 0, 0))
	mx, my = mapimg.get_size()
	px, py = mx // 2 + X * tilesize - d, my // 2 - Y * tilesize - d
	surf.blit(mapimg, (-px, -py))
#	pygame.draw.line(surf, (255, 0, 0), (0, 0), (22, 22))
#	pygame.draw.line(surf, (0, 255, 0), (2, 0), (2, 22))
#	fuzz = randomtile()
#	fuzz.set_alpha(100)
#	surf.blit(fuzz, (0, 0))
	tiles[ntile] = surf
	debug("background tile size:", len(tiles))
	return surf

land = {}
def getland(ntile):
	key = ntile, util.f
	if key in land:
		return land[key]
	tile = gettile(ntile)
	w0 = F(math.ceil(window.Z * T * tile.get_width() / tilesize))
	h0 = F(math.ceil(window.Z * T * window.fy * tile.get_height() / tilesize))
	surf0 = pygame.transform.smoothscale(tile, (w0, h0))
	w = F(math.ceil(window.Z * T))
	h = F(math.ceil(window.Z * T * window.fy))
	print tile.get_size(), w0, h0, w, h, ((w - w0) // 2), ((h - h0) // 2)
	surf = pygame.Surface((w, h)).convert()
	surf.blit(surf0, ((w - w0) // 2, (h - h0) // 2))
	land[key] = surf
	debug("background land size:", len(land))
	return surf

shade = {}
def getshade():
	key = window.sx, window.sy
	if key in shade:
		return shade[key]
	img0 = pygame.Surface((1, 255)).convert_alpha()
	r, g, b = settings.shadecolor
	for y in range(img0.get_height()):
		img0.set_at((0, img0.get_height() - 1 - y), (r, g, b, y))
	surf = pygame.transform.smoothscale(img0, key)
	shade[key] = surf
	debug("background shade size:", len(shade))
	return shade[key]


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
	window.screen.blit(getshade(), (0, 0))


