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
			a = int(255 * math.clamp(h * f, 0, 1))
			img.set_at((px, py), (255, 255, 255, a))
	hillcache[key] = img
	return img

def tocell(surf):
	osurf = surf.copy()
	osurf.fill((0, 50, 50, 255))
	a = pygame.surfarray.pixels_alpha(surf)
	arr = pygame.surfarray.pixels3d(osurf)
	arr[a > 100, 1:3] = 0
	arr[a > 150, 1:3] = 120
	return osurf


if __name__ == "__main__":
	import random
	from . import mhack
	pygame.init()
	screen = pygame.display.set_mode((1280, 960))
	blobs = [(
		random.uniform(0, math.tau),  # theta0
		random.uniform(0.3, 0.5) * random.choice([-1, 1]),  # dtheta
		random.uniform(0, math.tau),  # phi0
		random.uniform(0.1, 0.2) * random.choice([-1, 1]),  # dphi
		random.randrange(50, 51), # r
		random.uniform(0.3, 0.8), # h
	) for _ in range(30)]
	surf = pygame.Surface((640, 480)).convert_alpha()
	while not any(event.type == pygame.KEYDOWN for event in pygame.event.get()):
		surf.fill((0, 0, 0, 0))
		img = hill(100, 2)
		surf.blit(img, img.get_rect(center = (320, 240)))
		for theta0, dtheta, phi0, dphi, r, h in blobs:
			theta = theta0 + dtheta * pygame.time.get_ticks() * 0.001
			phi = phi0 + dphi * pygame.time.get_ticks() * 0.001
			R = 70 + 10 * math.sin(phi)
			x, y = 320 + R * math.cos(theta), 240 + R * math.sin(theta)
			img = hill(r, h)
			surf.blit(img, img.get_rect(centerx = int(x), centery = int(y)))
		t0 = pygame.time.get_ticks()
		screen.blit(pygame.transform.smoothscale(tocell(surf), screen.get_size()), (0, 0))
#		print pygame.time.get_ticks() - t0

		pygame.display.flip()
	
