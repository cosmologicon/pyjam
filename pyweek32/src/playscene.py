import pygame, math, bisect
from . import view, pview, graphics
from .pview import T

class self:
	speed = 10
	length = 40
	numlinks = 96


def init():
	self.t = 0
	self.d = 0
	self.ps = [(0, (0, 0))]
	self.theta = 0  # 0 = north, tau/4 = east

def think(dt, kpressed):
	self.t += dt
	dkx = (1 if kpressed[pygame.K_RIGHT] else 0) - (1 if kpressed[pygame.K_LEFT] else 0)
	dky = (1 if kpressed[pygame.K_UP] else 0) - (1 if kpressed[pygame.K_DOWN] else 0)
	if False:
		self.theta += 6 * dt * dkx % math.tau
	else:
		if dkx or dky:
			target = math.atan2(dkx, dky)
			theta = (self.theta - target + math.tau / 2) % math.tau + target - math.tau / 2
			self.theta = math.approach(theta, target, 6 * dt)
			
	d0, (x0, y0) = self.ps[-1]
	self.d += dt * self.speed
	dy, dx = math.CS(self.theta, self.speed * dt)
	x, y = x0 + dx, y0 + dy
	self.ps.append((self.d, (x, y)))
	while self.ps[0][0] < self.d - self.length:
		self.ps.pop(0)
	
	view.x0, view.y0 = math.softapproach((view.x0, view.y0), (x, y), 4 * dt, dymin=0.001)

def interp(x, xys):
	j = bisect.bisect(xys, (x,))
	if j == 0: return xys[0][1]
	if j >= len(xys): return xys[-1][1]
	return math.fadebetween(x, *xys[j-1], *xys[j])


def draw():
	graphics.drawstars()
	for k in range(self.numlinks):
		d = self.d - self.length * k / self.numlinks
		pos = view.screenpos(interp(d, self.ps))
		size = T(view.scale * (0.3 if k == 0 else 0.2 * 0.99 ** k))
		color = [(120, 255, 120), (255, 255, 0)][k % 2]
		color = math.imix(color, (120, 255, 120), k / 120)
		pygame.draw.circle(pview.screen, color, pos, size)


