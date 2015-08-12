from __future__ import division
import pygame, numpy, math, random
from pygame.locals import *
from src import window, state

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

surf = None
dsurf = None
def draw():
	global surf, dsurf
	factor = 20
	sx, sy = window.screen.get_size()
	sx = int(math.ceil(sx / factor))
	sy = int(math.ceil(sy / factor))
	dsx, dsy = sx * factor, sy * factor
	if surf is None or surf.get_size() != (sx, sy):
		surf = pygame.Surface((sx, sy)).convert()
		dsurf = pygame.Surface((dsx, dsy)).convert()
	a = numpy.zeros((sx, sy))
	dx = (numpy.arange(sx).reshape(sx, 1) - sx / 2) * factor / window.camera.R
	dy = (-numpy.arange(sy).reshape(1, sy) + sy / 2) * factor / window.camera.R + window.camera.y0
	x = (numpy.arctan2(dy, dx) - window.camera.X0) * (64 / math.tau) % 16
	y = (dx ** 2 + dy ** 2) ** 0.35 / 14 % 16
	z = 0.001 * pygame.time.get_ticks() / 4 % 16
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
	
	arr = pygame.surfarray.pixels3d(surf)
	arr[:,:,0] = 0
	arr[:,:,1] = 54 + 12 * g
	arr[:,:,2] = 30 - 8 * g
	del arr
	
	pygame.transform.smoothscale(surf, (dsx, dsy), dsurf)
	window.screen.blit(dsurf, (0, 0))

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
	

