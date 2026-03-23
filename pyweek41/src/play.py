from . import world, thing
from . import fuzz


def randomstar(*seed):
	x = fuzz.uniform(-40, 40, 0.123, *seed)
	y = fuzz.uniform(-20, 20, 0.234, *seed)
	mag = fuzz.random(0.345) ** 0.2 * 6
	return thing.Star((x, y), mag)

def init():
	world.stars = [randomstar(j) for j in range(100)]

def think():
	pass

def draw():
	for star in world.stars:
		star.draw()

