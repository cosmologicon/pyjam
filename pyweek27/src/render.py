from __future__ import division
import pygame, math
from . import maff, pview, ptext, view
from .pview import T, I

C15, S15 = math.CS(math.radians(15))
C30, S30 = math.CS(math.radians(30))

def arc0(r):
	return [(S, C) for C, S in [math.CS(math.radians(x), r) for x in range(0, 35, 5)]]


def drawlinesF(Fspot, pFs, color):
	pygame.draw.lines(pview.screen, color, False, T([view.BconvertF(Fspot, pF) for pF in pFs]))

def insector0(p):
	x, y = p
	return 0 <= x <= y / math.sqrt(3)

# Return a segment along the given segment within sector 0, or None if completely outside.
def cull(p0, p1):
	x0, y0 = p0
	x1, y1 = p1
	dx, dy = x1 - x0, y1 - y0
	ts = [0, 1]
	if (x0 > 0) != (x1 > 0) and abs(dx) > 0.001:
		ts.append(-x0 / dx)
	if (y0 > math.sqrt(3) * x0) != (y1 > math.sqrt(3) * x1):
		num = math.sqrt(3) * x0 - y0
		den = dy - math.sqrt(3) * dx
		if abs(den) > 0.001:
			ts.append(num / den)
	ts.sort()
	qs = [math.mix(p0, p1, t) for t in ts]
	segs = []
	for j in range(len(qs) - 1):
		q0, q1 = qs[j], qs[j+1]
		if insector0(math.mix(q0, q1, 0.5)):
			segs.append((q0, q1))
	return max(segs, key=lambda seg: math.distance(*seg)) if segs else None

def sector0(Fspot):
	color = pygame.Color("#444455")
	for j in range(1, 7):
		drawlinesF(Fspot, arc0(j / 6), color)
	drawlinesF(Fspot, [(S15/3, C15/3), (S15, C15)], color)
	color = pygame.Color("#9999aa")
	drawlinesF(Fspot, [(0, 1), (0, 0), (S30, C30)], color)

def sectors(Fspot):
	posB, BrF = Fspot
	color = pygame.Color("#9999aa")
	for j in range(1, 7):
		pygame.draw.circle(pview.screen, color, T(posB), T(BrF * j / 6), T(1))
	for a in (0, 60, 120):
		C, S = math.CS(math.radians(a))
		drawlinesF(Fspot, [(S, C), (-S, -C)], color)
	for C, S in math.CSround(6, 1, 1/2):
		drawlinesF(Fspot, [(S, C), (S/3, C/3)], color)
	for C, S in math.CSround(12, 1, 1/2):
		drawlinesF(Fspot, [(S, C), (2*S/3, 2*C/3)], color)

def anchor(Fspot, anchor, color):
	p = view.BconvertF(Fspot, anchor)
	pygame.draw.circle(pview.screen, pygame.Color("black"), T(p), T(10))
	pygame.draw.circle(pview.screen, pygame.Color(color), T(p), T(7))


# m = tan(60deg) = sqrt(3)
# A = 1/(1+m^2) [1-m^2, 2m, 2m, m^2 - 1] = 1/4 [-2, 2sqrt(3), 2sqrt(3), 2]
def R1(pos):
	x, y = pos
	m = math.sqrt(3)
	return (-x + m * y) / 2, (m * x + y) / 2
	
R2 = math.R(math.radians(-60))

def dim(color, amount=1):
	return ptext._applyshade(color, 0.2 * amount)

def sectorpoly(sectorimgs, ps0, color):
	s = sectorimgs[0].get_height()
	ps1 = [R1(p) for p in ps0]
	ps2 = [R2(p) for p in ps0]
	pygame.draw.polygon(sectorimgs[0], color, I([(x * s, (1 - y) * s) for x, y in ps0]))
	pygame.draw.polygon(sectorimgs[1], color, I([(x * s, (1 - y) * s) for x, y in ps1]))
	pygame.draw.polygon(sectorimgs[2], color, I([(x * s, (1 - y) * s) for x, y in ps2]))


if __name__ == "__main__":
	import random
	pview.set_mode((500, 500))
	Fspot = (250, 300), 50
	playing = True
	while playing:
		pview.fill((0, 0, 0))
		for _ in range(1):
			x0 = random.uniform(-5, 5)
			y0 = random.uniform(-5, 5)
			x1 = random.uniform(-5, 5)
			y1 = random.uniform(-5, 5)
			ps = (x0, y0), (x1, y1)
			drawlinesF(Fspot, ps, pygame.Color("#333333"))
			ps = cull(*ps)
			if ps is None:
				continue
			drawlinesF(Fspot, ps, pygame.Color("#aaaaaa"))
		sector0(Fspot)
		pygame.display.flip()
		while True:
			etypes = set(event.type for event in pygame.event.get())
			if pygame.KEYDOWN in etypes:
				break
			if pygame.QUIT in etypes:
				playing = False
				break


