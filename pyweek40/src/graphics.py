from functools import lru_cache, cache
import pygame, math
from . import pview, fuzz
from .pview import T


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
		return int(2 * S(0.3, 0.4, 345, *seed) + S(0.2, 0.3, 456, *seed))
	rskew = int(0.1 * pview.h)
	def drawray(x0, x1, alpha):
		ps = [(x0 + rskew, 0), (x1 + rskew, 0), (x1 - rskew, pview.h), (x0 - rskew, pview.h)]
		ps = [pview.T(p) for p in ps]
		pygame.draw.polygon(surf, (255, 255, 255, alpha), ps, 0)
	
	w0, w1 = T(600, 1000)
	x0min, x0max = -w1, pview.w + w1
	for j in range(10):
		surf.fill((255, 255, 255, 0))
		x0 = math.imix(x0min, x0max, j * math.phi % 1) + dx(j, 0)
		w = fuzz.uniform(w0, w1, 876, j)
		drawray(x0 - w + dx(j, 1), x0 + w + dx(j, 2), 4 + dalpha(j, 3))
		drawmask(surf)


