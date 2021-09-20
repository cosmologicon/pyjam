import random, math
from . import pview, view
from .pview import T

stars = []
def drawstars():
	Nstars = math.ceil(0.003 * pview.area)
	if len(stars) != Nstars:
		del stars[:]
		for jstar in range(Nstars):
			x = random.uniform(0, 1000000)
			y = random.uniform(0, 1000000)
			z = math.mix(0.2, 0.5, jstar / Nstars)
			color0 = 200, random.uniform(200, 255), random.uniform(200, 255)
			a = math.mix(0.2, 1, (jstar / Nstars) ** 4)
			color = math.imix((0, 0, 0), color0, a)
			stars.append((x, y, z, color))
	for x, y, z, color in stars:
		px = T((x - z * view.x0) * 40) % pview.w
		py = T(-(y - z * view.y0) * 40) % pview.h
		pview.screen.set_at((px, py), color)
	

