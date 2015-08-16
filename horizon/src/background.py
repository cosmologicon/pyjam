from __future__ import division
import pygame, numpy, math, random
from pygame.locals import *
from src import window, state, settings

def rgrad():
	x, y = random.gauss(0, 1), random.gauss(0, 1)
	d = math.sqrt(x ** 2 + y ** 2)
	return x / d, y / d
grad = {
	(x, y, z): rgrad()
	for x in range(16) for y in range(16) for z in range(16)
}
gradx = numpy.reshape(
	[grad[(x % 16, y % 16, z % 16)][0]
	for x in range(17) for y in range(17) for z in range(17)],
	(17, 17, 17))
grady = numpy.reshape(
	[grad[(x % 16, y % 16, z % 16)][1]
	for x in range(17) for y in range(17) for z in range(17)],
	(17, 17, 17))

flowt = 0
washt = 0
def think(dt):
	global flowt, washt
	dt *= 6 / (1 + 5 * state.you.y / state.R)
	flowt += dt
	if washt:
		washt = max(washt - dt, 0)

surf = None
dsurf = None
hsurf = None
def draw(factor = None):
	global surf, dsurf, hsurf
	if factor is None:
		factor = settings.backgroundfactor
	sx, sy = window.screen.get_size()
	sx = int(math.ceil(sx / factor))
	sy = int(math.ceil(sy / factor))
	dsx, dsy = sx * factor, sy * factor
	if surf is None or surf.get_size() != (sx, sy):
		surf = pygame.Surface((sx, sy)).convert_alpha()
		dsurf = pygame.Surface((dsx, dsy)).convert_alpha()
		hx, hy = window.screen.get_size()
		hsurf = pygame.Surface((hx, hy)).convert_alpha()
		R = window.screen.get_height() / settings.logicalscreensize
		dx = (numpy.arange(hx).reshape(hx, 1) - hx / 2) / R
		dy = (-numpy.arange(hy).reshape(1, hy) + hy / 2) / R + state.R
		y = (dx ** 2 + dy ** 2) ** 0.5 - state.R
		arr = pygame.surfarray.pixels3d(hsurf)
		arr[:,:,0] = 255 * numpy.exp(numpy.minimum(y, -12 * y))
		arr[:,:,1] = 255 * numpy.exp(numpy.minimum(0, -12 * y))
		arr[:,:,2] = 255 * numpy.exp(numpy.minimum(y, -12 * y))
		del arr
		arr = pygame.surfarray.pixels_alpha(hsurf)
		arr[:,:] = 255 * numpy.minimum(1, numpy.exp(0.2 * y))
		del arr
	a = numpy.zeros((sx, sy))
	dx = (numpy.arange(sx).reshape(sx, 1) - sx / 2) * factor / window.camera.R
	dy = (-numpy.arange(sy).reshape(1, sy) + sy / 2) * factor / window.camera.R + window.camera.y0
	x = (numpy.arctan2(dy, dx) - window.camera.X0) * (64 / math.tau) % 16
	y0 = (dx ** 2 + dy ** 2) ** 0.5
	y = y0 / 14 % 16
	z = flowt / 4 % 16
	nx, ny, nz = x.astype(int), y.astype(int), int(z)
	fx, fy, fz = x % 1, y % 1, z % 1
	ax = (3 - 2 * fx) * fx ** 2
	ay = (3 - 2 * fy) * fy ** 2
	az = (3 - 2 * fz) * fz ** 2
	gx, gy, gz = 1 - fx, 1 - fy, 1 - fz
	bx, by, bz = 1 - ax, 1 - ay, 1 - az
	g = x * 0
	for dx in (0, 1):
		for dy in (0, 1):
			axy = (ax if dx else bx) * (ay if dy else by)
			for dz in (0, 1):
				g += (
					gradx[nx + dx, ny + dy, nz + dz] * (fx if dx else gx) +
					grady[nx + dx, ny + dy, nz + dz] * (fy if dy else gy)
				) * (axy * (az if dz else bz))
	
	c = numpy.exp(-numpy.maximum(0, y0 / 15 - 2))
	c2 = (1 - c)
	arr = pygame.surfarray.pixels3d(surf)
	arr[:,:,0] = c * 255
	arr[:,:,1] = c * 255 + c2 * (54 + 12 * g)
	arr[:,:,2] = c * 255 + c2 * (30 - 8 * g)
	del arr
#	pygame.surfarray.pixels_alpha(surf)[:,:] = 255 * (y0 < state.R)
	
	pygame.transform.smoothscale(surf, (dsx, dsy), dsurf)
	window.screen.blit(dsurf, (0, 0))
	y = int((window.camera.y0 - state.R) * window.camera.R)
	if y > -hsurf.get_height():
		window.screen.blit(hsurf, (0, y))
	if y > 0:
		window.screen.fill((0, 0, 0), (0, 0, hsurf.get_width(), y))


fsurf = None
dfsurf = None
def drawfilament():
	global fsurf, dfsurf
	factor = 5
	sx, sy = window.screen.get_size()
	sx = int(math.ceil(sx / factor))
	sy = int(math.ceil(sy / factor))
	dsx, dsy = sx * factor, sy * factor
	if fsurf is None or fsurf.get_size() != (sx, sy):
		fsurf = pygame.Surface((sx, sy)).convert_alpha()
		dfsurf = pygame.Surface((dsx, dsy)).convert_alpha()
	fsurf.fill((0, 0, 0, 0))
	for filament in state.filaments:
		filament.draw(fsurf, factor)
	pygame.transform.smoothscale(fsurf, (dsx, dsy), dfsurf)
	window.screen.blit(dfsurf, (0, 0))
	
def drawfilament():
	for filament in state.filaments:
		ps = [window.screenpos(X, y) for X, y in filament.ladderps]
		pygame.draw.lines(window.screen, (255, 255, 0), False, ps, 3)

stars = [
	(random.uniform(0.2, 1), random.uniform(0, 100000), random.uniform(0, 100000))
	for _ in range(10000)
]
def drawstars():
	dstars = stars[:int(window.sx * window.sy / 1000)]
	t = window.sy * 0.3 * flowt
	for f, x, y in dstars:
		px = int(x) % window.sx
		py = int(y - t * f) % window.sy
		c = int(255 * f)
		window.screen.set_at((px, py), (c, c, c))

def wash():
	global washt
	washt = 1
def drawwash():
	if not washt:
		return
	alpha = washt
	dsurf.fill((255, 255, 255, int(255 * alpha)))
	window.screen.blit(dsurf, (0, 0))

def init():
	draw()
	window.screen.fill((0, 0, 0))

