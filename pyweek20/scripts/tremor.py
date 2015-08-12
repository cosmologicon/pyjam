from __future__ import division
import pygame, math

s = 200

screen = pygame.display.set_mode((s, s))
img = pygame.Surface((s, s)).convert_alpha()
tau = 2 * math.pi

for px in range(s):
	for py in range(s):
		x = 2 * px / s - 1
		y = 2 * py / s - 1
		
		r = math.sqrt(x ** 2 + y ** 2)
		theta = math.atan2(x, y)

		if r > 1 or r < 1/3:
			a = 0
		else:
			a = (r - 1/3) ** 2 * (1 - r) ** 2

		c = math.sin(theta * 4)

		c = int(128 + 120 * c)
		a = int(2000 * a)

		c = 100
		a = int(120 * (3 - 2 * (1-r)) * (1-r)**2) if r < 1 else 0
		
		img.set_at((px, py), (c, c, c, a))

screen.fill((0, 100, 0))
screen.blit(img, (0, 0))
pygame.display.flip()
pygame.image.save(img, "data/img/tremor.png")


