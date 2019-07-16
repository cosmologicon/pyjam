from __future__ import division
import pygame, math, random
tau = 2 * math.pi

ngrid = 64
N = { (x, y, z) : random.uniform(-1, 1) for x in range(ngrid) for y in range(ngrid) for z in range(ngrid) }
def noise(x, y, z):
	x %= ngrid
	y %= ngrid
	z %= ngrid
	ax, ay, az = int(x), int(y), int(z)
	fx, fy, fz = x - ax, y - ay, z - az
	t = 0
	for kx in (0, 1):
		for ky in (0, 1):
			for kz in (0, 1):
				jx = (ax + kx) % ngrid
				jy = (ay + ky) % ngrid
				jz = (az + kz) % ngrid
				t += N[(jx, jy, jz)] * (fx if kx else 1 - fx) * (fy if ky else 1 - fy) * (fz if kz else 1 - fz)
	return t

def fracnoise(x, y, z, n = 8):
	return 0 if n == 0 else noise(x, y, z) + 1 / 2 * fracnoise(x * 2 + 4.83, y * 2 + 5.93, z * 2 + 8.23, n - 1)

radius = 2
radius += 1
imgscale = 30

psize = int(2 * radius * imgscale)
screen = pygame.display.set_mode((psize, psize))

colors = [
	(-0.4, 0, 0, 50),
	(-0.1, 0, 0, 160),
	(0, 100, 100, 0),
	(0.1, 40, 100, 0),
	(0.4, 100, 50, 0),
	(0.6, 50, 50, 50),
]

colors = [
	(-0.4, 40, 0, 0),
	(0.4, 80, 0, 80),
]

colors = [
	(-0.4, 140, 140, 140),
	(-0.1, 0, 0, 100),
	(0.1, 140, 140, 140),
	(0.4, 0, 0, 100),
]

colors = [
	(-0.4, 40, 40, 40),
	(-0.1, 180, 180, 0),
	(0.1, 40, 40, 40),
	(0.4, 180, 180, 0),
]


colors.insert(0, (-999,) + colors[0][1:])
colors.append((999,) + colors[-1][1:])

def getcolor(a, d):
	for j in range(len(colors)):
		if colors[j][0] > a:
			f = (a - colors[j-1][0]) / (colors[j][0] - colors[j-1][0])
			return [d * (colors[j-1][k] * (1 - f) + colors[j][k] * f) for k in (1, 2, 3)] + [255]
	
img = pygame.Surface((psize, psize)).convert_alpha()
for px in range(psize):
	for py in range(psize):
		x = px / imgscale - radius
		y = py / imgscale - radius
		z2 = (radius - 1) ** 2 - x ** 2 - y ** 2
		if z2 < 0:
			img.set_at((px, py), (0, 0, 0, 0))
			continue
		z = math.sqrt(z2)
		n = fracnoise(2 * x, 2 * y, 2 * z, n = 6)
		d = min(max((x - y + z) * 0.2 + 0.5, 0), 1)
		img.set_at((px, py), map(int, getcolor(n, d)))

pygame.image.save(img, "data/planet-4.png")
screen.blit(img, (0, 0))
pygame.display.set_caption("done")
pygame.display.flip()
while not any(event.type in (pygame.KEYDOWN, pygame.QUIT) for event in pygame.event.get()):
	pass

