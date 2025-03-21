from __future__ import division
import pygame, random, math, numpy
from . import window, settings, ptext, util, state
from .util import F, debug

tilesize = 40
tiles = {}

#T = 20

reveallog = []


worldmaps = {}
mapimg = None
maskimg = None
watermask = None
cloudimgs = []
def init():
	global mapimg, maskimg, watermask
	mapimg = pygame.image.load("data/map.png").convert()
	watermask = pygame.mask.from_threshold(pygame.image.load("data/watermask.png"), (255, 255, 255), (127, 127, 127))
	maskimg = mapimg.convert_alpha()
	maskimg.fill(settings.shadecolor + (255,))
	cloudimgs.append(pygame.image.load("data/clouds-0.png").convert())
	cloudimgs.append(pygame.image.load("data/clouds-1.png").convert())
	for img in cloudimgs:
		img.set_alpha(20)

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
landsize = 0
def getland(ntile):
	global landsize
	key = ntile, util.f, window.Z
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
	landsize += 4 * surf.get_width() * surf.get_height()
	if landsize > 100 << 20:  # 100 MB
		landsize = 0
		debug("reducing land usage")
		land.clear()
	debug("background land size:", len(land))
	return surf


unmasks = {}
def reveal(x, y, r, update = True):
	reveallog.append((x, y, r))
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
	x0, y0 = maskimg.get_width() // 2 + int(x) - R, maskimg.get_height() // 2 - int(y) - R
	x1, y1 = x0 + 2 * R, y0 + 2 * R
	if x0 < 0:
		unmask = unmask[-x0:,:]
		x0 = 0
	if x1 > 2048:
		unmask = unmask[:-(x1-2048),:]
		x1 = 2048
	if y0 < 0:
		unmask = unmask[:,-y0:]
		y0 = 0
	if y1 > 2048:
		unmask = unmask[:,:-(y1-2048)]
		y1 = 2048
	arr[x0:x1,y0:y1] = numpy.maximum(arr[x0:x1,y0:y1] - unmask, 0)
	del arr
	if not update:
		return

	X0 = int(math.floor((x - R - 1) / tilesize))
	X1 = int(math.ceil((x + R + 1) / tilesize))
	Y0 = int(math.floor((y - R - 1) / tilesize))
	Y1 = int(math.ceil((y + R + 1) / tilesize))
	for key in list(tiles):
		X, Y = key
		if X0 <= X <= X1 and Y0 <= Y <= Y1:
			del tiles[key]
	for key in list(land):
		(X, Y), f, Z = key
		if X0 <= X <= X1 and Y0 <= Y <= Y1:
			del land[key]
	worldmaps.clear()
	minimaps.clear()

def revealall():
	reveallog[:] = [None]
	maskimg.fill(settings.shadecolor + (0,))
	tiles.clear()
	land.clear()
	worldmaps.clear()
	minimaps.clear()

def getstate():
	return reveallog

def setstate(reveals):
	maskimg.fill(settings.shadecolor + (255,))
	del reveallog[:]
	if None in reveals:
		revealall()
	else:
		for x, y, r in reveals:
			reveal(x, y, r, update = False)
	tiles.clear()
	land.clear()
	worldmaps.clear()
	minimaps.clear()
	


def revealed(x, y):
	mx, my = maskimg.get_size()
	px = int(round(mx // 2 + x))
	py = int(round(my // 2 - y))
	if not 0 <= px < mx or not 0 <= py < my:
		return False
	r, g, b, a = maskimg.get_at((px, py))
	return a < 200

def island(x, y):
	mx, my = maskimg.get_size()
	px = int(round(mx // 2 + x))
	py = int(round(my // 2 - y))
	if not 0 <= px < mx or not 0 <= py < my:
		return False
	return watermask.get_at((px, py))

clouds = {}
def getcloud(layer):
	key = layer, util.f, window.Z
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
#	window.screen.blit(getshade(), (0, 0))

def drawclouds():
	fcloud = 1.6
	t = 0.001 * pygame.time.get_ticks()
	for layer in [0, 1]:
		vx = [3, -2][layer]
		vy = [3, 2][layer]
		cloud = getcloud(layer)
		cx, cy = cloud.get_size()
		x0s = [-(int((fcloud * window.x0 + vx * t) * util.f * window.Z) % cx)]
		y0s = [-(int((fcloud * -window.y0 + vy * t) * util.f * window.Z * window.fy) % cy)]
		while x0s[-1] + cx < window.sx:
			x0s.append(x0s[-1] + cx)
		while y0s[-1] + cy < window.sy:
			y0s.append(y0s[-1] + cy)
		for x0 in x0s:
			for y0 in y0s:
				window.screen.blit(cloud, (x0, y0))

def minimaprect():
	rect = pygame.Rect(F(0, 0, 140, 140))
	rect.bottomright = F(854 - 8, 480 - 8)
	return rect

minimaps = {}
minishades = {}
def drawminimap():
	from . import control
	K = settings.minimapscale
	key = util.f
	if key not in minimaps:
		surf = mapimg.copy()
		surf.blit(maskimg, (0, 0))
		s = F(surf.get_width() * K)
		minimaps[key] = pygame.transform.smoothscale(surf, (s, s))
		minishades[key] = pygame.Surface(minimaprect().size).convert_alpha()
		minishades[key].fill((20, 20, 20, 200))
	surf = pygame.Surface(minimaprect().size).convert_alpha()
	surf.fill((0, 0, 0))
	x = (surf.get_width() - minimaps[key].get_width()) // 2 - F(window.x0 * K)
	y = (surf.get_height() - minimaps[key].get_height()) // 2 + F(window.y0 * K)
	surf.blit(minimaps[key], (x, y))
	surf.blit(minishades[key], (0, 0))
	objs = []
	for ship in state.state.team:
		color = (255, 0, 255) if control.isselected(ship) and pygame.time.get_ticks() * 0.001 % 1 > 0.3 else (200, 200, 200)
		objs.append([ship.x, ship.y, 3, color])
	for building in state.state.buildings:
		if building.revealed() and building.mapr is not None and building.getcolor() is not None:
			color = (255, 255, 0)
			objs.append([building.x, building.y, building.mapr, building.getcolor()])
	for x, y, r, color in objs:
		px = surf.get_width() // 2 + F((x - window.x0) * K)
		py = surf.get_height() // 2 - F((y - window.y0) * K)
		pygame.draw.circle(surf, color, (px, py), F(r))
	pygame.draw.rect(surf, (120, 120, 120), surf.get_rect(), F(2))
	window.screen.blit(surf, minimaprect())


def drawmap():
	from . import control, image
	size = window.sx, window.sy
	if size not in worldmaps:
		surf = mapimg.copy()
		surf.blit(maskimg, (0, 0))
		worldmaps[size] = pygame.transform.smoothscale(surf, size)
	window.screen.blit(worldmaps[size], (0, 0))
	ptext.draw(settings.gamename.replace(" ", "\n"), topleft = F(10, 10), color = "yellow",
		gcolor = "orange",
		fontsize = F(48), fontname = "SansitaOne")
	for ship in state.state.team:
		px = int((ship.x + 1024) / 2048 * window.sx)
		py = int((-ship.y + 1024) / 2048 * window.sy)
		if pygame.time.get_ticks() * 0.001 % 1 < 0.3:
			color = (255, 0, 255) if control.isselected(ship) else (200, 200, 200)
			pygame.draw.circle(window.screen, color, (px, py), F(2))
		else:
			image.draw("avatar-%s" % ship.letter, (px, py), size = F(20))
	for building in state.state.buildings:
		if not building.revealed():
			continue
		color = building.getcolor()
		r = building.mapr
		if color is None or r is None:
			continue
		px = int((building.x + 1024) / 2048 * window.sx)
		py = int((-building.y + 1024) / 2048 * window.sy)
		pygame.draw.circle(window.screen, color, (px, py), F(r))


