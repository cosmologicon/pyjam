import pygame, math
from . import view, pview, graphics, state
from .pview import T


def dist(obj0, obj1):
	x0, y0 = obj0.pos
	x1, y1 = obj1.pos
	return math.hypot(x1 - x0, y1 - y0)

class You:
	def __init__(self, pos):
		self.pos = pos
		self.v = 0, 0
		self.A = 0
		self.omega = 3
		self.t = 0
		self.aup = 4
		self.adrag = 2
		self.adown = 20
		self.vmax = 4

	def control(self, kdowns, kpressed):
		left = kpressed[pygame.K_LEFT]
		right = kpressed[pygame.K_RIGHT]
		up = kpressed[pygame.K_UP]
		down = kpressed[pygame.K_DOWN]
		self.controls = {
			"up": up and not down,
			"down": down and not up,
			"act": kpressed[pygame.K_SPACE],
			"dA": right - left,
		}

	def think(self, dt):
		self.t += dt
		self.on = self.controls["act"]			
		x, y = self.pos
		vx, vy = self.v
		A = math.dA(self.A + dt * self.omega * self.controls["dA"])
		C, S = math.CS(math.mixA(self.A, A, 0.5))
		if self.controls["up"]:
			vx += S * self.aup * dt
			vy += C * self.aup * dt
		else:
			a = self.adown if self.controls["down"] else self.adrag
			vx, vy = math.approach((vx, vy), (0, 0), dt * a)
		v = math.hypot(vx, vy)
		if v > self.vmax:
			vx *= self.vmax / v
			vy *= self.vmax / v
		vxavg, vyavg = math.mix(self.v, (vx, vy), 0.5)
		self.pos = x + dt * vxavg, y + dt * vyavg
		self.v = vx, vy
		self.A = A


	def draw(self):
		pV = view.VconvertG(self.pos)
		graphics.draw("ship", pV, pview.f * 0.3, self.A)
		if self.on:
			beam = Beam(self.pos, self.A, 0.5, 4, 0.15, 0.3)
			for DM in state.DMs:
				beam.occlude(DM)
			beam.draw()
		

class Stander:
	def __init__(self, pos, r):
		self.pos = pos
		self.r = r
		self.ffind = 0
		self.found = False

	def think(self, dt):
		if not self.found:
			ffind = 1 if dist(self, state.you) < self.r + 0.5 else 0
			self.ffind = math.approach(self.ffind, ffind, 0.3 * dt)
			if self.ffind == 1:
				self.found = True

	def draw(self):
		pV = view.VconvertG(self.pos)
		rV = T(view.VscaleG * self.r)
		color = (0, 100, 100) if self.found else (0, 0, 0)
		pygame.draw.circle(pview.screen, color, pV, rV)


def cutbeampath(w1, xB0, xB1, d1, fences):
	if not fences:
		return [(w1, xB0, d1), (w1, xB1, d1)]
	y, w, x0, x1 = fences[0]
	fences = fences[1:]
	if x1 <= xB0 or x0 >= xB1:
		return cutbeampath(w1, xB0, xB1, d1, fences)
	if x0 < xB0:
		left = [(w, xB0, y)]
	else:
		left = cutbeampath(w1, xB0, x0, d1, fences) + [(w, x0, y)]
	if x1 > xB1:
		right = [(w, xB1, y)]
	else:
		right = [(w, x1, y)] + cutbeampath(w1, x1, xB1, d1, fences)
	return left + right

def occludebeam(w0, w1, d0, d1, fences):
	path = cutbeampath(w1, -1, 1, d1, fences)
	return [(w0, 1, d0), (w0, -1, d0)] + path


class Beam:
	def __init__(self, p0, A, d0, d1, w0, w1):
		self.p0 = self.x0, self.y0 = p0
		self.A = A
		self.d0 = d0
		self.d1 = d1
		self.w0 = w0
		self.w1 = w1
		self.R = math.R(-self.A)
		self.Rinv = math.R(self.A)
		self.fences = []

	def occlude(self, obj):
		x, y = obj.pos
		xB, yB = self.Rinv((x - self.x0, y - self.y0))
		if not self.d0 <= yB <= self.d1:
			return
		w = math.interp(yB, self.d0, self.w0, self.d1, self.w1)
		if abs(xB) > w + obj.r:
			return
		self.fences.append((yB, w, (xB - obj.r) / w, (xB + obj.r) / w))

	def draw(self):
		self.fences.sort()
		dps = [self.R((w * dx, dy)) for w, dx, dy in occludebeam(self.w0, self.w1, self.d0, self.d1, self.fences)]
		pVs = [view.VconvertG((self.x0 + dx, self.y0 + dy)) for dx, dy in dps]
		pygame.draw.polygon(pview.screen, (255, 230, 200), pVs)

	def drawfences(self):
		for yB, w, xB0, xB1 in self.fences:
			dps = [self.R((w * xB, yB)) for xB in [xB0, xB1]]
			pVs = [view.VconvertG((self.x0 + dx, self.y0 + dy)) for dx, dy in dps]
			pygame.draw.line(pview.screen, (100, 100, 255), *pVs)




