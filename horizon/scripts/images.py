from __future__ import division
import pygame, math, random

s = 200

screen = pygame.display.set_mode((s, s))
timg = pygame.Surface((s, s)).convert_alpha()
simg = pygame.Surface((s, s)).convert_alpha()
himg = pygame.Surface((s, s)).convert_alpha()
eimg = pygame.Surface((s, s)).convert_alpha()
cimg = pygame.Surface((s, s)).convert_alpha()
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
		
		timg.set_at((px, py), (c, c, c, a))

		c1, c2, c3 = [random.choice([0, 255]) for _ in range(3)]
		ye = y * 2
		re = math.sqrt(x ** 2 + ye ** 2)
		a = int(120 * (3 - 2 * (1-re)) * (1-re)**2) if re < 1 else 0
		eimg.set_at((px, py), (c1, c2, c3, a))


		c = 200
		p = min(math.sqrt((x - x0) ** 2 + (y - y0) ** 2) for x0 in (-1, 1) for y0 in (-1, 1))
		a = min(max(int(300 * (p - 1)), 0), 255)
		simg.set_at((px, py), (c, c, c, a))

		c = 100
		a = int(min(10 + 10 * math.exp(3 * (r - 1)), 10 * math.exp(-20 * (r - 1))))
		himg.set_at((px, py), (c, c, c, a))

		

screen.fill((0, 100, 0))
screen.blit(himg, (0, 0))
pygame.display.flip()
pygame.image.save(timg, "data/img/tremor.png")
pygame.image.save(simg, "data/img/slash.png")
pygame.image.save(himg, "data/img/shield.png")
pygame.image.save(eimg, "data/img/teleport.png")

colors = [
	("white", 1, 1, 1),
	("red", 1, 0.4, 0.4),
	("green", 0.4, 1, 0.4),
	("blue", 0.4, 0.4, 1),
	("yellow", 1, 1, 0.1),
	("purple", 1, 0.1, 1),
	("orange", 1, 0.6, 0.4),
]
for cname, r, g, b in colors:
	img = timg.copy()
	arr = pygame.surfarray.pixels3d(img)
	arr[:,:,0] *= r
	arr[:,:,1] *= g
	arr[:,:,2] *= b
	del arr
	pygame.image.save(img, "data/img/tremor-%s.png" % cname)

colors = [
	("white", 1, 1, 1),
	("red", 1, 0, 0),
	("green", 0, 1, 0),
	("blue", 0, 0, 1),
	("yellow", 0.8, 0.8, 0),
	("purple", 0.8, 0, 0.8),
	("orange", 0.8, 0.4, 0),
	("gray", 0.4, 0.4, 0.4),
	("black", 0, 0, 0),
]
for cname, r, g, b in colors:
	img = simg.copy()
	arr = pygame.surfarray.pixels3d(img)
	arr[:,:,0] *= r
	arr[:,:,1] *= g
	arr[:,:,2] *= b
	del arr
	pygame.image.save(img, "data/img/slash-%s.png" % cname)



