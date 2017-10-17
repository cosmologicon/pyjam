# Procedural hill graphics

from __future__ import division, print_function
import pygame, random, math
from . import view, pview

# TODO: add to maff
def vmix(x, y, a):
	return tuple(math.mix(p, q, a) for p, q in zip(x, y))

def splitlayer(layer, n = 20):
	if len(layer) == 1:
		return [(j / n, layer[0]) for j in range(n+1)]
	ds = [math.distance(layer[j], layer[j+1]) for j in range(len(layer) - 1)]
	D = sum(ds)
	dfs = [0]
	for d in ds:
		dfs.append(dfs[-1] + d / D)
	splits = [(df, pos) for df, pos in zip(dfs, layer)]
	while len(splits) < n + 1:
		f = random.random()
		j = max(j for j, df in enumerate(dfs[:-1]) if df <= f)
		pos = vmix(layer[j], layer[j+1], f - dfs[j])
		splits.append((f, pos))
	return sorted(splits)
	

def splitspec(layers, n = 100):
	nlayer = len(layers)
	slayers = [splitlayer(layer, n) for layer in layers]
	scatter = 0.2 * n ** -0.5
	for jlayer in range(nlayer - 1):
		top = slayers[jlayer]
		bottom = slayers[jlayer + 1]
		for j in range(n):
			f0, top0 = top[j]
			f1, top1 = top[j+1]
			f2, bottom0 = bottom[j]
			f3, bottom1 = bottom[j+1]
			f = (f0 + f1 + f2 + f3) / 4 + random.uniform(-1, 1) * scatter
			yield f, top0, top1, bottom0, bottom1

def getsurf(spec, z):
	ps = [p for layer in spec for p in layer]
	ps = [view.screenoffset(x, y, z) for x, y in ps]
	xs, ys = zip(*ps)
	x0, y0 = min(xs), min(ys)
	ps = [(x - x0, y - y0) for x, y in ps]
	xs, ys = zip(*ps)
	surf = pygame.Surface((max(xs), max(ys))).convert_alpha()
	surf.fill((40, 40, 40, 255))
	for split in splitspec(spec):
		f, top0, top1, bottom0, bottom1 = split
		rps = bottom0, top0, top1, bottom1
		rps = [view.screenoffset(x, y, z) for x, y in rps]
		rps = [(x - x0, y - y0) for x, y in rps]
		color = int(80 + 60 * f), int(40 + 30 * f), 0
		pygame.draw.polygon(surf, color, rps)
#		pygame.draw.line(surf, (255, 255, 0), rps[1], rps[2], 5)
 	return surf, (x0, y0)

def drawhill(p, spec):
	x, y, z = p
	surf, (dx, dy) = getsurf(spec, z)
	px, py = view.toscreen(x, y, z)
	pview.screen.blit(surf, (px + dx, py + dy))

if __name__ == "__main__":
	from . import maff
	view.init()
	pview.toggle_fullscreen()
	drawhill((0, 0, 0), [
		((-10, 10), (-5, 12), (5, 13), (15, 12)),
		((-8, 0), (-3, -1), (7, -1), (15, 2)),
		((-8, -12), (13, -14)),
		((-20, -50), (20, -50)),
	])
	drawhill((30, 0, 0), [
		((-10, 10), (-5, 12), (5, 13), (15, 12)),
		((-5, 3), (11, 6)),
		((5, 0),),
	])
	drawhill((-30, 0, 0), [
		((0, 25),),
		((3, 10), (6, 11)),
		((0, 0), (3, 0)),
		((-6, -10), (-2, -12)),
		((-7, -30), (-1, -30)),
	])
	pygame.display.flip()
	while not any(event.type == pygame.KEYDOWN for event in pygame.event.get()):
		pass


