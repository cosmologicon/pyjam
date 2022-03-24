import pygame, math
from functools import lru_cache
from . import view, pview, geometry

@lru_cache(10)
def sparesurf(name, size):
	return pygame.Surface(size).convert_alpha()


class Mask:
	maskheight = None
	def __init__(self):
		t0 = pygame.time.get_ticks()
		self.surf = sparesurf("msurf", pview.size)
		self.surf.fill((0, 0, 0, 0))
		if self.maskheight is None:
			self.mask = sparesurf("mask", pview.size)
		else:
			width = int(round(self.maskheight * pview.aspect))
			self.mask = sparesurf("mask", (width, self.maskheight))
		self.mask.fill((255, 255, 255, 0))
#		print("init", pygame.time.get_ticks() - t0)
		
	def setmask(self, plook, Aset):
		t0 = pygame.time.get_ticks()
		for Ainterval in Aset.intervals:
			ps = [
				plook,
				math.CS(Ainterval.A0, 1000, plook),
				math.CS(Ainterval.A1, 1000, plook),
			]
			ps = [view.screenpos(p) for p in ps]
			if self.mask.get_height() != pview.height:
				f = self.mask.get_height() / pview.height
				ps = [pview.I(f * x, f * y) for x, y in ps]
			pygame.draw.polygon(self.mask, (255, 255, 255, 255), ps)
#		print("setmask", pygame.time.get_ticks() - t0)

	def draw(self):
		t0 = pygame.time.get_ticks()
		if self.mask.get_height() != pview.height:
			self.mask = pygame.transform.scale(self.mask, pview.size, sparesurf("mask", pview.size))
		self.surf.blit(self.mask, (0, 0), None, pygame.BLEND_RGBA_MIN)
		pview.screen.blit(self.surf, (0, 0))
#		print("draw", pygame.time.get_ticks() - t0)
		
		

