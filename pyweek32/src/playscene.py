import pygame, math, bisect
from . import view, pview
from .pview import T

class self:
	speed = 10
	length = 10
	numlinks = 24


def init():
	self.t = 0
	self.d = 0
	self.ps = [(0, (0, 0))]
	self.theta = 0  # 0 = north, tau/4 = east

def think(dt, kpressed):
	self.t += dt
	dkx = (1 if kpressed[pygame.K_RIGHT] else 0) - (1 if kpressed[pygame.K_LEFT] else 0)
	self.theta += 6 * dt * dkx % math.tau
	d0, (x0, y0) = self.ps[-1]
	self.d += dt * self.speed
	dy, dx = math.CS(self.theta, self.speed * dt)
	x, y = x0 + dx, y0 + dy
	self.ps.append((self.d, (x, y)))
	while self.ps[0][0] < self.d - self.length:
		self.ps.pop(0)

def interp(x, xys):
	j = bisect.bisect(xys, (x,))
	if j == 0: return xys[0][1]
	if j >= len(xys): return xys[-1][1]
	return math.fadebetween(x, *xys[j-1], *xys[j])


def draw():
	for k in range(self.numlinks):
		d = self.d - self.length * k / self.numlinks
		x, y = interp(d, self.ps)
		pos = T(640 + view.scale * x, 360 - view.scale * y)
		size = T(view.scale * 0.2 * 0.95 ** k)
		pygame.draw.circle(pview.screen, (255, 255, 255), pos, size)

