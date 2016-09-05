import pygame, random, math
from . import blob, view
from .util import F

def init():
	global motes
	motes = [(
		random.uniform(0, 1000000),
		random.uniform(0, 1000000),
		random.uniform(-10, 10),
		random.uniform(-10, 10),
		random.uniform(2, 4),
		random.choice([20, 30, 40, 50]),
	) for _ in range(200)]


def draw():
	t = pygame.time.get_ticks() * 0.001
	vZ = math.sqrt(view.Z)
	nmote = min(int(math.ceil(len(motes) / vZ ** 2)), len(motes))
	for x, y, vx, vy, z, r in motes[:nmote]:
		x += vx * t - view.x0
		y += vy * t - view.y0
		x *= z
		y *= z
		px, py = F([
			854 / 2 + vZ * (z * (x + vx * t + 2 * view.x0)),
			480 / 2 - vZ * (z * (y + vy * t + 2 * view.y0)),
		])
		r = F(vZ * r)
		px = (px + 2 * r) % (view.sx + 4 * r) - 2 * r
		py = (py + 2 * r) % (view.sy + 4 * r) - 2 * r
		img = blob.mote(r, 0.01)
		view.screen.blit(img, (px, py), None, pygame.BLEND_SUB)


