import pygame, math, random
from . import view, pview, graphics, state, enco
from .pview import T


def dist(obj0, obj1):
	x0, y0 = obj0.pos
	x1, y1 = obj1.pos
	return math.hypot(x1 - x0, y1 - y0)

def overlaps(obj0, obj1):
	return dist(obj0, obj1) <= obj0.r + obj1.r

class KeepsTime(enco.Component):
	def __init__(self):
		self.t = 0
	def think(self, dt):
		self.t += dt

class Lifetime(enco.Component):
	def __init__(self, T):
		self.T = T
		self.alive = True
	def think(self, dt):
		self.f = math.clamp(self.t / self.T, 0, 1)
		if self.f == 1:
			self.alive = False

class HasVelocity(enco.Component):
	def think(self, dt):
		x, y = self.pos
		vx, vy = self.v
		self.pos = x + vx * dt, y + vy * dt

@KeepsTime()
class You:
	def __init__(self, pos):
		self.pos = pos
		self.v = 0, 0
		self.A = 0
		self.omega = 3
		self.aup = 4
		self.adrag = 2
		self.adown = 20
		self.vmax = 4
		self.on = False

	def control(self, kdowns, kpressed):
		left = kpressed[pygame.K_LEFT]
		right = kpressed[pygame.K_RIGHT]
		up = kpressed[pygame.K_UP]
		down = kpressed[pygame.K_DOWN]
		self.controls = {
			"up": up and not down,
			"down": down and not up,
			"acting": kpressed[pygame.K_SPACE],
			"dA": left - right,
			"act": pygame.K_SPACE in kdowns,
		}

	def think(self, dt):
		x, y = self.pos
		vx, vy = self.v
		A = math.dA(self.A + dt * self.omega * self.controls["dA"])
		if self.controls["up"]:
			vx, vy = math.CS(math.mixA(self.A, A, 0.5), self.aup * dt, (vx, vy))
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
		if self.controls["act"]:
			state.pulses.append(Pulse(self.pos))


	def draw(self):
		pV = view.VconvertG(self.pos)
		graphics.draw("ship", pV, pview.f * 0.3, self.A)
		if self.on:
			beam = Beam(self.pos, self.A, 0.5, 4, 0.15, 0.3)
			for DM in state.DMs:
				beam.occlude(DM)
			beam.draw()

class Findable(enco.Component):
	def __init__(self, Tfind):
		self.Tfind = Tfind
		self.ffind = 0
		self.found = False

	def think(self, dt):
		if not self.found:
			ffind = 1 if dist(self, state.you) < self.r + 0.5 else 0
			self.ffind = math.approach(self.ffind, ffind, dt / self.Tfind)
			if self.ffind == 1:
				self.found = True

	def draw(self):
		pV = view.VconvertG(self.pos)
		rV = T(view.VscaleG * self.r)
		color = (0, 100, 100) if self.found else (0, 0, 0)
		pygame.draw.circle(pview.screen, color, pV, rV)
		
@Findable(3)
class Stander:
	def __init__(self, pos, r):
		self.pos = pos
		self.r = r

@Findable(3)
@KeepsTime()
class Orbiter:
	def __init__(self, pos0, A0, omega, Rorbit, r):
		self.pos0 = pos0
		self.r = r
		self.A0 = A0
		self.omega = omega
		self.Rorbit = Rorbit
		self.setpos()
	
	def think(self, dt):
		self.setpos()
	
	def setpos(self):
		self.A = self.A0 + self.omega * self.t
		dy, dx = math.CS(self.A, self.Rorbit)
		x0, y0 = self.pos0
		self.pos = x0 + dx, y0 + dy



def cutbeampath(w1, yB0, yB1, d1, fences):
	if not fences:
		return [(d1, w1 * yB0), (d1, w1 * yB1)]
	x, w, y0, y1 = fences[0]
	fences = fences[1:]
	if y1 <= yB0 or y0 >= yB1:
		return cutbeampath(w1, yB0, yB1, d1, fences)
	if y0 < yB0:
		bottom = [(x, w * yB0)]
	else:
		bottom = cutbeampath(w1, yB0, y0, d1, fences) + [(x, w * y0)]
	if y1 > yB1:
		top = [(x, w * yB1)]
	else:
		top = [(x, w * y1)] + cutbeampath(w1, y1, yB1, d1, fences)
	return bottom + top

def occludebeam(w0, w1, d0, d1, fences):
	path = cutbeampath(w1, -1, 1, d1, fences)
	return [(d0, w0), (d0, -w0)] + path


class Beam:
	def __init__(self, p0, A, d0, d1, w0, w1):
		self.p0 = self.x0, self.y0 = p0
		self.A = A
		self.d0 = d0
		self.d1 = d1
		self.w0 = w0
		self.w1 = w1
		self.R = math.R(self.A)
		self.Rinv = math.R(-self.A)
		self.fences = []

	def occlude(self, obj):
		x, y = obj.pos
		xB, yB = self.Rinv((x - self.x0, y - self.y0))
		if not self.d0 <= xB <= self.d1:
			return
		w = math.interp(xB, self.d0, self.w0, self.d1, self.w1)
		if abs(yB) > w + obj.r:
			return
		self.fences.append((xB, w, (yB - obj.r) / w, (yB + obj.r) / w))

	def draw(self):
		self.fences.sort()
		dps = [self.R((dx, dy)) for dx, dy in occludebeam(self.w0, self.w1, self.d0, self.d1, self.fences)]
		pVs = [view.VconvertG((self.x0 + dx, self.y0 + dy)) for dx, dy in dps]
		pygame.draw.polygon(pview.screen, (255, 230, 200), pVs)
		#self.drawfences()

	def drawfences(self):
		for xB, w, yB0, yB1 in self.fences:
			dps = [self.R((xB, w * yB)) for yB in [yB0, yB1]]
			pVs = [view.VconvertG((self.x0 + dx, self.y0 + dy)) for dx, dy in dps]
			pygame.draw.line(pview.screen, (100, 100, 255), *pVs)


@KeepsTime()
@Lifetime(3)
@HasVelocity()
class Tracer:
	def __init__(self, origin, A, d, v):
		self.origin = origin
		self.pos = math.CS(A, d, origin)
		self.v = math.CS(A, v)
		self.r = 0.05

	def think(self, dt):
		for DM in state.DMs:
			if overlaps(DM, self):
				self.alive = False

	def draw(self):
		pV = view.VconvertG(self.pos)
		rV = T(view.VscaleG * self.r)
		color = (255, 200, 100)
		pygame.draw.circle(pview.screen, color, pV, rV)


@KeepsTime()
class Tspawner:
	def __init__(self, pos):
		self.pos = pos
		self.Tspawn = 0.01
		self.jspawn = 0
		
	def think(self, dt):
		while self.t > self.Tspawn * self.jspawn:
			state.tracers.append(Tracer(self.pos, self.jspawn * math.phyllo, 1, 3))
			self.jspawn += 1


@KeepsTime()
@Lifetime(2)
class Pulse:
	def __init__(self, origin):
		self.origin = origin
		self.w = 0.6
		self.v = 2
		self.ps = []
		self.rmax = 0
		self.j0 = 0

	def think(self, dt):
		self.R = self.v * self.t
		self.R0 = self.R - self.w
		self.R1 = self.R + self.w
		while self.rmax < self.R1:
			A = random.uniform(0, math.tau)
			x, y = math.CS(A, self.rmax, self.origin)
			d = random.uniform(0, self.w)
			self.ps.append((self.rmax - d, self.rmax + d, x, y))
			self.rmax += 0.001
		while self.ps[self.j0][0] < self.R0:
			self.j0 += 1

	def draw(self):
		for j in range(self.j0, len(self.ps)):
			Rmin, Rmax, x, y = self.ps[j]
			if not Rmin < self.R < Rmax:
				continue
			if any(math.hypot(DM.pos[0] - x, DM.pos[1] - y) < DM.r for DM in state.DMs):
				continue
			pV = view.VconvertG((x, y))
			pview.screen.set_at(pV, (100, 100, 255))


