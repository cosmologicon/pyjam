from __future__ import division
import pygame, math

hillcache = {}
def hill(R, h):
	key = R, h
	if key in hillcache:
		return hillcache[key]
	img = pygame.Surface((2 * R, 2 * R)).convert_alpha()
	# TODO: numpy
	for px in range(2 * R):
		for py in range(2 * R):
			r = math.sqrt((px / R - 1) ** 2 + (py / R - 1) ** 2)
			f = 1 - math.smoothstep(r)
			a = int(255 * h * f)
			img.set_at((px, py), (255, 255, 255, a))
	hillcache[key] = img
	return img


if __name__ == "__main__":
	import random
	from . import mhack
	pygame.init()
	screen = pygame.display.set_mode((640, 480))
	screen.fill((0, 0, 0))
	for _ in range(20):
		img = hill(40, 0.5)
		screen.blit(img, (random.randint(200, 300), random.randint(200, 300)))
	lsurf = pygame.Surface(screen.get_size()).convert_alpha()
#	lsurf.fill((0, 0, 0, 0))
#	pygame.transform.threshold(screen, None, (255, 0, 0), (40, 40, 40), (10, 10, 10))
#	screen.fill((0, 0, 0))
#	screen.blit(lsurf, (0, 0))

	pygame.display.flip()
	while not any(event.type == pygame.KEYDOWN for event in pygame.event.get()):
		pass
	
