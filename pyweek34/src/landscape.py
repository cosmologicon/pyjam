import pygame
from functools import lru_cache
from . import maff

cache = lru_cache(None)

@cache
def anchor(ix, iy, d):
	return maff.fuzzrange(-1, 1, ix, iy, d)
def level(x, y, d, wrap = 16):
	ix, fx = divmod(x, 1)
	iy, fy = divmod(y, 1)
	ix %= wrap
	iy %= wrap
	jx = (ix + 1) % wrap
	jy = (iy + 1) % wrap
	return maff.mix(
		maff.mix(anchor(ix, iy, d), anchor(jx, iy, d), fx),
		maff.mix(anchor(ix, jy, d), anchor(jx, jy, d), fx),
		fy)
def noise(x, y):
	S, C = 0.6 * 2, 0.8 * 2
	a = 0
	f = 1
	for d in range(6):
		a += f * level(x, y, d)
		x, y = C * x + S * y, -S * x + C * y
		f *= 0.7
	return a


class Hmap:
	def __init__(self, size):
		self.size = size
		self.surf = pygame.Surface(size).convert_alpha()
		self.ready = False
		self.progress = 0
		self.ocean = pygame.Surface(size).convert_alpha()
	def killtime(self):
		if self.ready:
			return
		w, h = self.size
		y = self.progress
		for x in range(w):
			m = noise(0.005 * x, 0.005 * y)
			c = int(maff.interp(m, -2, 50, 2, 150))
			self.surf.set_at((x, y), (c, 0, 0, 255))
		self.progress += 1
		self.ready = self.progress == h
	def complete(self):
		while not self.ready:
			self.killtime()
	def getocean(self, depth):
		mask = pygame.mask.from_threshold(self.surf, (0, 0, 0, 255), (depth, 255, 255, 255))
		return mask.to_surface(self.ocean, setcolor = (0, 20, 60, 255), unsetcolor = (0, 0, 0, 0))


queue = []
def killtime(dt):
	tend = pygame.time.get_ticks() + 1000 * dt
	while queue and pygame.time.get_ticks() < tend:
		queue[0].killtime()
		if queue[0].ready:
			queue.pop(0)

if __name__ == "__main__":
	from . import settings, view, pview
#	settings.size0 = 500, 500
	view.init()
	hmap = Hmap(settings.size0)
	queue.append(hmap)
	clock = pygame.time.Clock()
	while not any(event.type in (pygame.KEYDOWN, pygame.QUIT) for event in pygame.event.get()):
		dt = clock.tick(60) * 0.001
		killtime(dt)
		pview.fill((0, 0, 0))
		pview.screen.blit(hmap.surf, (0, 0))
		depth = maff.imix(50, 150, maff.cycle(0.001 * pygame.time.get_ticks() / 40))
		pview.screen.blit(hmap.getocean(depth), (0, 0))
		pygame.display.flip()
		pygame.display.set_caption("%.1ffps" % clock.get_fps())


