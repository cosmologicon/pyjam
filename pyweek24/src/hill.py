# Procedural hill graphics

from __future__ import division, print_function
import pygame, random, math
from . import view, pview
from .pview import T

surfs = {}
tick = { None: 0 }

def countusage(key):
	tick[key] = tick[None]
	tick[None] += 1

# TODO: add to maff
def vmix(x, y, a):
	return tuple(math.mix(p, q, a) for p, q in zip(x, y))
def colormix(x, y, a):
	return tuple(int(math.clamp(math.mix(p, q, a), 0, 255)) for p, q in zip(x, y))

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
	

def splitspec(layers, n = 20):
	n = max(n, max(len(layer) for layer in layers))
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

def grasspos(layer, thickness, margin = 5):
	for j in range(len(layer) - 1):
		p0 = layer[j]
		p1 = layer[j + 1]
		d = math.distance(p0, p1)
		n = int(d * thickness)
		for j in range(n + 1):
			x, y = vmix(p0, p1, j / n)
			df = min(math.distance((x, y), layer[0]), math.distance((x, y), layer[-1])) / margin
			df = min(df, 1)
			f = random.random() ** 2.5
			yield 1 - f, x, y - 5 * df * f

def getsurf(spec, z, color0 = (40, 20, 0), color1 = (150, 70, 0)):
	key = spec, z, color0, color1, pview.f
	if key in surfs:
		countusage(key)
		return surfs[key]
	s = view.scale(z)
	ps = [p for layer in spec for p in layer]
	ps = [view.screenoffset(x, y, z) for x, y in ps]
	xs, ys = zip(*ps)
	margin = T(6 * s)
	x0, y0 = min(xs) - margin, min(ys) - margin
	ps = [(x - x0, y - y0) for x, y in ps]
	xs, ys = zip(*ps)
	surf = pygame.Surface((max(xs) + margin, max(ys) + margin)).convert_alpha()
	surf.fill((0, 0, 0, 0))
#	surf.fill((40, 40, 40, 255))
	for split in splitspec(spec, 10):
		f, top0, top1, bottom0, bottom1 = split
		rps = bottom0, top0, top1, bottom1
		rps = [view.screenoffset(x, y, z) for x, y in rps]
		rps = [(x - x0, y - y0) for x, y in rps]
		color = colormix(color0, color1, f)
		pygame.draw.polygon(surf, color, rps)
#		pygame.draw.line(surf, (255, 255, 0), rps[1], rps[2], 5)
	for nsplit in (5, 6, 7, 8, 9):
		subsurf = pygame.Surface(surf.get_size()).convert_alpha()
		subsurf.fill((0, 0, 0, 0))
		for split in splitspec(spec, nsplit):
			f, top0, top1, bottom0, bottom1 = split
			rps = bottom0, top0, top1, bottom1
			rps = [view.screenoffset(x, y, z) for x, y in rps]
			rps = [(x - x0, y - y0) for x, y in rps]
			color = colormix(color0, color1, f)
			pygame.draw.polygon(subsurf, color, rps)
		pygame.surfarray.pixels_alpha(subsurf)[:,:] //= 3
		surf.blit(subsurf, (0, 0))

	thickness = 20
	for f, cx, cy in sorted(grasspos(spec[0], thickness)):
		f += random.uniform(-0.2, 0.2)
		color = 20 + 20 * f, 50 + 50 * f, 20 + 20 * f
		r = random.uniform(3, 6) * s
		cx, cy = view.screenoffset(cx, cy, z)
		pygame.draw.circle(surf, color, (int(cx) - x0, int(cy) - y0), T(r))
	surfs[key] = surf, (x0, y0)
	countusage(key)
 	return surfs[key]

def drawhill(p, spec):
	x, y, z = p
	surf, (dx, dy) = getsurf(spec, z)
	px, py = view.toscreen(x, y, z)
	pview.screen.blit(surf, (px + dx, py + dy))


specs = {
	"island": (
		((-10, 1), (-5, 3), (5, 3), (10, 1)),
		((-7, -3), (0, -5), (7, -3)),
		((0, -7),),
	),
	"oval": (
		((-10, 11), (-5, 15), (0, 16), (5, 16), (10, 11)),
		((-15, 0), (-12, 2), (-4, 3), (4, 1), (8, -2), (10, -5)),
		((-20, -15), (0, -15), (9, -17)),
		((-25, -30), (8, -30)),
	),
	"level": (
		((-10, 0), (10, 0)),
		((-10, -10), (11, -12)),
		((-12, -30), (11, -30)),
	),
	"widelevel": (
		((-50, 0), (50, 0)),
		((-50.2, -10), (49.6, -9)),
		((-51.0, -20), (50, -21)),
		((-53, -30), (51.5, -30)),
	),
	"incline": (
		((-10, -2), (-5, -1.5), (5, 1.5), (10, 2)),
		((-10, -10), (11, -12)),
		((-12, -30), (11, -30)),
	),
	"tower": (
		((-5, 0), (-4, 0.5), (-2, 1), (2, 1), (4, 0.5), (5, 0)),
		((-1, -5), (0, -4.5), (2.5, -4.5)),
		((0, -9), (2, -8.4)),
		((1, -15), (2.5, -14.5)),
		((5, -30), (5.5, -30)),
	),
	"towerup": (
		((-5, 0), (-4, 1), (-2, 2.5), (2, 4), (4, 5), (5, 5.2)),
		((-1, -5), (0, -4.5), (2.5, -4.5)),
		((0, -9), (2, -8.4)),
		((1, -15), (2.5, -14.5)),
		((5, -30), (5.5, -30)),
	),
}
def getspec(h):
	fx = math.exp(h["sx"] * 0.125) * (-1 if h["xflip"] else 1)
	fy = math.exp(h["sy"] * 0.125)
	return tuple(
		tuple((x * fx, y * fy) for x, y in (reversed(layer) if h["xflip"] else layer))
		for layer in specs[h["specname"]]
	)


if __name__ == "__main__":
	from . import maff
	view.init()
#	pview.toggle_fullscreen()
	drawhill((0, 0, 0), (
		((-10, 10), (-5, 12), (5, 13), (15, 12)),
		((-8, 0), (-3, -1), (7, -1), (15, 2)),
		((-8, -12), (13, -14)),
		((-20, -50), (20, -50)),
	))
	drawhill((30, 0, 0), (
		((-10, 10), (-5, 12), (5, 13), (15, 12)),
		((-5, 3), (11, 6)),
		((5, 0),),
	))
	drawhill((0, -15, 15), (
		((-10, 10), (-5, 12), (5, 13), (15, 12)),
		((-5, 3), (11, 6)),
		((5, 0),),
	))
	drawhill((-30, 0, 0), (
		((0, 25),),
		((3, 10), (6, 11)),
		((0, 0), (3, 0)),
		((-6, -10), (-2, -12)),
		((-7, -30), (-1, -30)),
	))
	pygame.display.flip()
	while not any(event.type == pygame.KEYDOWN for event in pygame.event.get()):
		pass


