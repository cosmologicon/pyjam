import pygame, math
from . import view, pview, geometry

class Mask:
	surf = None
	mask = None
	def __init__(self):
		t0 = pygame.time.get_ticks()
		if self.surf is None:
			Mask.surf = pygame.Surface(pview.size).convert_alpha()
		self.surf.fill((0, 0, 0, 0))
		if self.mask is None:
			Mask.mask = pygame.Surface(pview.size).convert_alpha()
		self.mask.fill((255, 255, 255, 0))
#		print("init", pygame.time.get_ticks() - t0)
		
	def setmask(self, viewer, mirror):
		t0 = pygame.time.get_ticks()
		viewpos = viewer.x, viewer.y
		ps = [view.screenpos(p) for p in geometry.viewfield(viewpos, mirror.p1, mirror.p2)]
		pygame.draw.polygon(self.mask, (255, 255, 255, 255), ps)
#		print("setmask", pygame.time.get_ticks() - t0)

	def draw(self):
		t0 = pygame.time.get_ticks()
		self.surf.blit(self.mask, (0, 0), None, pygame.BLEND_RGBA_MIN)
		pview.screen.blit(self.surf, (0, 0))
#		print("draw", pygame.time.get_ticks() - t0)
		
		

