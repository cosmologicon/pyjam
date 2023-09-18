import pygame, math
from . import maff

# https://en.wikipedia.org/wiki/Regular_dodecahedron#Cartesian_coordinates
vertices = [
	(x, y, z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)
] + [
	(0, a, b) for a in (-math.phi, math.phi) for b in (-math.Phi, math.Phi)
] + [
	(b, 0, a) for a in (-math.phi, math.phi) for b in (-math.Phi, math.Phi)
] + [
	(a, b, 0) for a in (-math.phi, math.phi) for b in (-math.Phi, math.Phi)
]

def dist(p0, p1):
	x0, y0, z0 = p0
	x1, y1, z1 = p1
	return math.hypot(x1 - x0, y1 - y0, z1 - z0)

def adj(p0, p1):
	s = math.sqrt(5) - 1
	return abs(dist(p0, p1) - s) < 0.001

edges = [(j, k) for j, v0 in enumerate(vertices) for k, v1 in enumerate(vertices) if j < k and adj(v0, v1)]

S = 200
pygame.init()
screen = pygame.display.set_mode((2 * S, 2 * S))

def aV(aG):
	return int(aG * S * 0.5)
def pV(pG):
	x, y = pG
	return int(S + S * x * 0.5), int(S + S * y * 0.5)

color = 100, 255, 255

theta = 0
def T(p):
	x, y, z = p
	y, z = math.R(0.4, (y, z))
	x, y = math.R(theta, (x, y))
	z, x = math.R(0.8, (z, x))
	y, z = math.R(0.9, (y, z))
	x, y = math.R(1.0, (x, y))
	return x, y, z


def draw():
	img = pygame.Surface((2 * S, 2 * S)).convert_alpha()
	img.fill((0, 0, 0, 0))
	coms = [(0, pygame.draw.circle, ((0, 0, 0), pV((0, 0)), aV(1.6)))]
	for x, y, z in vertices:
		x, y, z = T((x, y, z))
		com = z, pygame.draw.circle, (color, pV((x, y)), aV(0.12))
		coms.append(com)
	for j, k in edges:
		x0, y0, z0 = T(vertices[j])
		x1, y1, z1 = T(vertices[k])
		z = math.mix(z0, z1, 0.5)
		com = z, pygame.draw.line, (color, pV((x0, y0)), pV((x1, y1)), aV(0.06))
		coms.append(com)

	coms.sort(key = lambda com: com[0])
	for z, com, args in coms:
		com(img, *args)
	return img

Nframe = 40
for j in range(Nframe):
	theta = math.tau * j / Nframe
	pygame.image.save(draw(), f"img/cage/frame-{j:02d}.png")

while not pygame.event.get(pygame.KEYDOWN, pump=True):
	theta = 0.001 * pygame.time.get_ticks()
	screen.fill((10, 10, 10))
	screen.blit(draw(), (0, 0))
	pygame.display.flip()



