from __future__ import division
import pygame, random, math, util, numpy
from . import window, settings
from .util import F, debug

tilesize = 20
tiles = {}

#T = 20

mapimg = None
maskimg = None
cloudimgs = []
def init():
	global mapimg, maskimg
	mapimg = pygame.image.load("data/map.png").convert()
	maskimg = mapimg.convert_alpha()
	maskimg.fill(settings.shadecolor + (255,))
	cloudimgs.append(pygame.image.load("data/clouds-0.png").convert_alpha())

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
	surf = pygame.Surface((tilesize + 2 * d, tilesize + 2 * d)).convert_alpha()
	surf.fill((0, 0, 0))
	mx, my = mapimg.get_size()
	px, py = mx // 2 + X * tilesize - d, my // 2 - (Y + 1) * tilesize - d
	surf.blit(mapimg, (-px, -py))
	surf.blit(maskimg, (-px, -py))
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
	# Note: the -1 in the following equations was hard come by. I should do a writeup on it.
	w0 = F(math.ceil(window.Z * (tile.get_width() - 1)))
	h0 = F(math.ceil(window.Z * window.fy * (tile.get_height() - 1)))
	surf0 = pygame.transform.smoothscale(tile, (w0, h0))
	w = F(math.ceil(window.Z * tilesize)) + 1
	h = F(math.ceil(window.Z * tilesize * window.fy)) + 1
	surf = pygame.Surface((w, h)).convert()
	surf.blit(surf0, ((w - w0) // 2, (h - h0) // 2))
	land[key] = surf
	debug("background land size:", len(land))
	return surf


unmasks = {}
def reveal(x, y, r):
	R = r + 2
	if r not in unmasks:
		unmasks[r] = numpy.zeros(shape = (2 * R, 2 * R)).astype(numpy.int16)
		for ax in range(2*R):
			for ay in range(2*R):
				d = math.sqrt((ax - R) ** 2 + (ay - R) ** 2)
				a = min(max(int(100 * math.exp(r - d)), 0), 255)
				unmasks[r][ax,ay] = a
	unmask = unmasks[r]
	arr = pygame.surfarray.pixels_alpha(maskimg)
	ax, ay = maskimg.get_width() // 2 + int(x) - R, maskimg.get_height() // 2 - int(y) - R
	arr[ax:ax+2*R,ay:ay+2*R] = numpy.maximum(arr[ax:ax+2*R,ay:ay+2*R] - unmask, 0)
	del arr

	X0 = int(math.floor((x - R - 1) / tilesize))
	X1 = int(math.ceil((x + R + 1) / tilesize))
	Y0 = int(math.floor((y - R - 1) / tilesize))
	Y1 = int(math.ceil((y + R + 1) / tilesize))
	for key in list(tiles):
		X, Y = key
		if X0 <= X <= X1 and Y0 <= Y <= Y1:
			del tiles[key]
	for key in list(land):
		(X, Y), f = key
		if X0 <= X <= X1 and Y0 <= Y <= Y1:
			del land[key]

def revealed(x, y):
	mx, my = maskimg.get_size()
	px = int(round(mx // 2 + x))
	py = int(round(my // 2 - y))
	if not 0 <= px < mx or not 0 <= py < my:
		return False
	r, g, b, a = maskimg.get_at((px, py))
	return a < 200


clouds = {}
def getcloud(layer):
	key = layer, util.f
	if key in clouds:
		return clouds[key]
	w = F(math.ceil(window.Z * 50))
	h = F(math.ceil(window.Z * 50 * window.fy))
	surf = pygame.transform.smoothscale(cloudimgs[0], (w, h))
	clouds[key] = surf
	debug("background cloud size:", len(clouds))
	return clouds[key]




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
	X0 = int(math.floor(x0 / tilesize))
	Y0 = int(math.floor(y0 / tilesize))
	X1 = int(math.ceil(x1 / tilesize))
	Y1 = int(math.ceil(y1 / tilesize))

	for X in range(X0, X1):
		for Y in range(Y0, Y1):
			surf = getland((X, Y))
			pos = window.worldtoscreen(X * tilesize - 0.5, (Y + 1) * tilesize + 0.5, 0)
			window.screen.blit(surf, pos)
	window.screen.blit(getshade(), (0, 0))

def drawclouds():
	window.screen.blit(getcloud(0), (0, 0))

