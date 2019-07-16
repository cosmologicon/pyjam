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

radius = 8
radius += 1
imgscale = 30

psize = int(2 * radius * imgscale)
screen = pygame.display.set_mode((psize, psize))

def getcolor(a):
	if a < 0.3:
		a = (a - 0) / 0.3
		return 255, 0, 0, a * 0.5 * 255
	if a < 0.6:
		a = (a - 0.3) / 0.3
		return 255, a * 255, 0, (a * 0.5 + 0.5) * 255
	else:
		a = (a - 0.6) / 0.4
		return 255, 255, a * 255, 255
	

img = pygame.Surface((psize, psize)).convert_alpha()
for px in range(psize):
	for py in range(psize):
		x = px / imgscale - radius
		y = py / imgscale - radius
		r = math.sqrt(x**2 + y**2)
		theta = math.atan2(x, y)
		n = 1 * fracnoise(r * 1, theta / tau * ngrid, 0.5, n = 5)
		a = min(max(radius - r - n - 1, 0), 1)
		img.set_at((px, py), map(int, getcolor(a)))

pygame.image.save(img, "data/sun.png")
screen.blit(img, (0, 0))
pygame.display.set_caption("done")
pygame.display.flip()
while not any(event.type in (pygame.KEYDOWN, pygame.QUIT) for event in pygame.event.get()):
	pass

