import random
from . import view

stars = []
def init():
	stars.extend([
		(random.uniform(0, 1000000), random.uniform(0, 1000000), random.uniform(0.2, 0.8))
		for _ in range(10000)
	])

def draw():
	view.screen.fill((0, 0, 0))
	N = min(len(stars), int(view.sx * view.sy * 0.001))
	for x, y, z in stars[:N]:
		px = int((x - view.x0) * z % view.sx)
		py = int((y - view.y0) * z % view.sy)
		color = 255, 255, 255
		view.screen.set_at((px, py), color)

