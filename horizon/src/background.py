from __future__ import division
import pygame, numpy, math, random
from pygame.locals import *
from src import window, state, settings

def rgrad():
	x, y, z = random.gauss(0, 1), random.gauss(0, 1), random.gauss(0, 1)
	d = math.sqrt(x ** 2 + y ** 2 + z ** 2)
	return x / d, y / d, z / d
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
gradz = numpy.reshape(
	[grad[(x % 16, y % 16, z % 16)][2]
	for x in range(17) for y in range(17) for z in range(17)],
	(17, 17, 17))

flowt = 0
washt = 0
def think(dt, fflow = 1):
	global washt
	if washt:
		washt = max(washt - dt, 0)
	flow(dt * fflow)
def flow(dt):
	global flowt
	flowt += dt

# Returns two Surfaces, one exactly scalefactor times larger than the other, with the larger
# Surface at least as large as size.
def getsurfs(size, scalefactor = None, _cache={}):
	key = size, scalefactor
	if key in _cache:
		return _cache[key]
	sx, sy = size
	if scalefactor is None:
		msurf = pygame.Surface((sx, sy)).convert_alpha()
		dsurf = None
	else:
		sx = int(math.ceil(sx / scalefactor))
		sy = int(math.ceil(sy / scalefactor))
		msurf = pygame.Surface((sx, sy)).convert_alpha()
		dsurf = pygame.Surface((sx * scalefactor, sy * scalefactor)).convert_alpha()
	_cache[key] = msurf, dsurf
	return msurf, dsurf

# Get the surface on which the horizon line is drawn.
# Radius of the horizon is in units of the screen width.
def gethsurf(size, radius, _cache={}):
	key = size, radius
	if key in _cache:
		return _cache[key]
	hx, hy = size
	hsurf = pygame.Surface(size).convert_alpha()
	dx = (numpy.arange(hx).reshape(hx, 1) - hx / 2) / hx
	dy = (-numpy.arange(hy).reshape(1, hy) + hy / 2) / hx
	y = (dx ** 2 + (dy + radius) ** 2) ** 0.5 / radius - 1
	arr = pygame.surfarray.pixels3d(hsurf)
	arr[:,:,0] = 255 * numpy.exp(numpy.minimum(100 * y, -2400 * y))
	arr[:,:,1] = 255 * numpy.exp(numpy.minimum(0, -2400 * y))
	arr[:,:,2] = 255 * numpy.exp(numpy.minimum(100 * y, -2400 * y))
	del arr
	arr = pygame.surfarray.pixels_alpha(hsurf)
	arr[:,:] = 255 * numpy.exp(numpy.minimum(0, 300 * y))
	del arr
	_cache[key] = hsurf
	return hsurf

def getgrid(size, X0, y0, R):
	sx, sy = size
	dx = (numpy.arange(sx).reshape(sx, 1) - sx / 2) / R
	dy = (-numpy.arange(sy).reshape(1, sy) + sy / 2) / R + y0
	x = (numpy.arctan2(dy, dx) - X0) / math.tau
	y = (dx ** 2 + dy ** 2) ** 0.5
	return x, y

def getnoise(x, y, z):
	x %= 16
	y %= 16
	z %= 16
	nx, ny, nz = x.astype(int), y.astype(int), int(z)
	fx, fy, fz = x % 1, y % 1, z % 1
	ax = (3 - 2 * fx) * fx ** 2
	ay = (3 - 2 * fy) * fy ** 2
	az = (3 - 2 * fz) * fz ** 2
	gx, gy, gz = fx - 1, fy - 1, fz - 1
	bx, by, bz = 1 - ax, 1 - ay, 1 - az
	g = x * 0
	for dx in (0, 1):
		for dy in (0, 1):
			axy = (ax if dx else bx) * (ay if dy else by)
			for dz in (0, 1):
				g += (
					gradx[nx + dx, ny + dy, nz + dz] * (gx if dx else fx) +
					grady[nx + dx, ny + dy, nz + dz] * (gy if dy else fy) +
					gradz[nx + dx, ny + dy, nz + dz] * (gz if dz else fz)
				) * (axy * (az if dz else bz))
	return g * 4


def draw(factor = None, camera = None, hradius = None):
	if factor is None:
		factor = settings.backgroundfactor
	if camera is None:
		camera = window.camera
	sx, sy = window.screen.get_size()
	msurf, dsurf = getsurfs((sx, sy), factor)
	msx, msy = msurf.get_size()
	dsx, dsy = dsurf.get_size()

	gx, gy = getgrid((msx, msy), camera.X0, camera.y0, camera.R / factor)
	gz = flowt / 10
	g = getnoise(gx * 64, gy / 14, gz)
	c = numpy.exp(-numpy.maximum(0, gy - state.Rcore) * 0.05)
	c2 = (1 - c)
	arr = pygame.surfarray.pixels3d(msurf)
	arr[:,:,0] = c * 255
	arr[:,:,1] = c * 255 + c2 * (54 + 12 * g)
	arr[:,:,2] = c * 255 + c2 * (30 - 8 * g)
	del arr
#	pygame.surfarray.pixels_alpha(surf)[:,:] = 255 * (y0 < state.R)
	
	pygame.transform.smoothscale(msurf, (dsx, dsy), dsurf)
	window.screen.blit(dsurf, (0, 0))
	y = int((camera.y0 - state.R) * camera.R)
	if y > -sy and hradius != -1:
		if hradius is None:
			hradius = state.R * camera.R / sx
		hsurf = gethsurf((sx, sy), hradius)
		window.screen.blit(hsurf, (0, y))
	if y > 0:
		window.screen.fill((0, 0, 0), (0, 0, sx, y))


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
	surf, _ = getsurfs(window.screen.get_size())
	surf.fill((255, 255, 255, int(255 * alpha)))
	window.screen.blit(surf, (0, 0))

def init():
	getsurfs(window.screen.get_size(), settings.backgroundfactor)
	gethsurf(window.screen.get_size(), 6)
	window.screen.fill((0, 0, 0))

