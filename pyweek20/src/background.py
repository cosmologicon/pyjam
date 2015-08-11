from __future__ import division
import pygame, numpy, math
from pygame.locals import *
from src import window, state

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
	X = numpy.arctan2(dy, dx) - window.camera.X0
	y = numpy.sqrt(dx ** 2 + dy ** 2) + 10 * 0.001 * pygame.time.get_ticks()
	a = 60 + 15 * numpy.cos(X * 20) + 15 * numpy.cos(y * 0.2)
	
	arr = pygame.surfarray.pixels3d(surf)
	arr[:,:,0] = 0
	arr[:,:,1] = a
	arr[:,:,2] = 0
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
	

