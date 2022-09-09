import pygame, math
from . import pview, maff
from . import landscape, control

class self:
	dmap = None

def init():
	self.dmap = landscape.Dmap((10, 10))
	self.t = 0

def think(dt):
	self.t += dt
	xP, yP = control.xV / 120, control.yV / 120
	self.dmap.drain(xP, yP, 1.5, 0.5 * dt)

def draw():
	pview.fill((0, 0, 0))
	surf = self.dmap.tosurf()
	surf = pygame.transform.smoothscale(surf, (1200, 1200))
	pview.screen.blit(surf, (0, 0))

