from functools import lru_cache, cache
import pygame, math
from . import pview, fuzz

def drawmask(mask, special_flags = 0):
	pview.screen.blit(mask, (0, 0), special_flags = special_flags)


@lru_cache(1)
def ssurf0(size):
	return pygame.Surface(size).convert_alpha()

def ssurf():
	return ssurf0(pview.size)

def drawlight():
	surf = ssurf()
	t = 0.001 * pygame.time.get_ticks() + 1000
	def S(omega0, omega1, *seed):
		return math.sin(fuzz.uniform(omega0, omega1, *seed) * t)
	def dx(*seed):
		return 30 * S(1, 1.5, 123, *seed) + 20 * S(2, 2.5, 234, *seed)
	def dalpha(*seed):
		return int(2 * S(3, 3.5, 345, *seed))
	def drawray(x0, x1, alpha):
		ps = [pview.T(p) for p in [(x0, 0), (x1, 0), (x1 - 200, 800), (x0 - 200, 800)]]
		pygame.draw.polygon(surf, (255, 255, 255, alpha), ps, 0)
	
	for j in range(6):
		surf.fill((255, 255, 255, 0))
		x0 = -200 + 1400 * (j * math.phi % 1)
		w = fuzz.uniform(200, 400, 876, j)
		drawray(x0 - w + dx(j, 1), x0 + w + dx(j, 2), 3 + dalpha(j, 3))
		drawmask(surf)


