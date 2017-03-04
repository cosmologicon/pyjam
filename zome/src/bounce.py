# Bouncing physics
from __future__ import division
import math, random
from . import settings


def getcollisions0(objs):
	for j in range(len(objs)):
		x1, y1, r1, m1 = objs[j]
		for i in range(j):
			x0, y0, r0, m0 = objs[i]
			if (x0 - x1) ** 2 + (y0 - y1) ** 2 < (r0 + r1) ** 2:
				yield i, j

def qcollide0(objs):
	collisions = set()
	for j, x1, y1, r1 in objs:
		for i, x0, y0, r0 in objs:
			if i >= j:
				continue
			if (x0 - x1) ** 2 + (y0 - y1) ** 2 < (r0 + r1) ** 2:
				collisions.add((i, j))
	return collisions

def qcollide(objs):
	if len(objs) < 10:
		return qcollide0(objs)
	rmax = max(r for j, x, y, r in objs)
	xmin = min(x - r for j, x, y, r in objs)
	xmax = max(x + r for j, x, y, r in objs)
	ymin = min(y - r for j, x, y, r in objs)
	ymax = max(y + r for j, x, y, r in objs)
	xr = xmax - xmin
	yr = ymax - ymin
	if xr > yr:
		xc = (xmin + xmax) / 2
		objs0 = [(j, x, y, r) for j, x, y, r in objs if x - r <= xc]
		objs1 = [(j, x, y, r) for j, x, y, r in objs if x + r >= xc]
	else:
		yc = (ymin + ymax) / 2
		objs0 = [(j, x, y, r) for j, x, y, r in objs if y - r <= yc]
		objs1 = [(j, x, y, r) for j, x, y, r in objs if y + r >= yc]
	if len(objs0) ** 2 + len(objs1) ** 2 > len(objs) ** 2:
		return qcollide0(objs)
	return qcollide(objs1) | qcollide(objs0)

def getcollisions(objs):
	if settings.n2collision:
		return getcollisions0(objs)
	return qcollide([(j, x, y, r) for j, (x, y, r, m) in enumerate(objs)])

def getbounce(objs, dt):
	ds = [[0, 0] for _ in objs]
	for i, j in getcollisions(objs):
		x0, y0, r0, m0 = objs[i]
		x1, y1, r1, m1 = objs[j]
		if (x0 - x1) ** 2 + (y0 - y1) ** 2 < (r0 + r1) ** 2:
			dx = x1 - x0
			dy = y1 - y0
			if dx == 0 and dy == 0:
				a = random.angle()
				dx = 1.0 * math.sin(a)
				dy = 1.0 * math.cos(a)
			d = math.sqrt(dx ** 2 + dy ** 2)
			f = math.clamp(20 * (r0 + r1 - d), 50, 200)
			dx *= dt / d * f
			dy *= dt / d * f
			da = math.sqrt(dx ** 2 + dy ** 2)
			if d + da > 1.001 * (r0 + r1):
				db = 1.001 * (r0 + r1) - d
				dx *= db / da
				dy *= db / da
			f0, f1 = (1, 0) if m1 > 100 * m0 else (0, 1) if m0 > 100 * m1 else (m1 / (m0 + m1), m0 / (m1 + m0))
#			f0, f1 = (m1 / (m0 + m1), m0 / (m1 + m0))
			ds[i][0] -= dx * f0
			ds[i][1] -= dy * f0
			ds[j][0] += dx * f1
			ds[j][1] += dy * f1
	return ds

def adjust(objs, dt):
	cspecs = [obj.getcollidespec() for obj in objs]
	for (dx, dy), obj in zip(getbounce(cspecs, dt), objs):
		obj.scootch(dx, dy)


if __name__ == "__main__":
	import pygame, random
	from . import mhack
	from .util import F
	pygame.init()
	screen = pygame.display.set_mode((1280, 960))

	balls = [[
		random.uniform(0, 1280),
		random.uniform(0, 960),
		random.uniform(20, 40),
	] for _ in range(100)]
	for ball in balls:
		ball.append(ball[-1])
	balls += [[
		random.uniform(0, 1280),
		random.uniform(0, 960),
		random.uniform(100, 120),
		10000,
	] for _ in range(20)]

	while not any(event.type == pygame.KEYDOWN for event in pygame.event.get()):
		screen.fill((0, 0, 0))
		t0 = pygame.time.get_ticks()
		ds = getbounce(balls, 0.01)
#		print(pygame.time.get_ticks() - t0)
		for ball, (dx, dy) in zip(balls, ds):
			ball[0] += dx
			ball[1] += dy
			x, y, r, m = ball
			p = int(x), int(y)
			r = int(r)
			pygame.draw.circle(screen, (255, 120, 0), p, r, 1)
			pygame.draw.circle(screen, (255, 120, 0), p, 1, 1)
		pygame.display.flip()
	
