import pygame, math, random
from . import view, pview, graphics, state, enco, ptext, perform
from .pview import T


def pdist(p0, p1):
	x0, y0 = p0
	x1, y1 = p1
	return math.hypot(x1 - x0, y1 - y0)

def dvec(p0, p1):
	x0, y0 = p0
	x1, y1 = p1
	return x1 - x0, y1 - y0

def dist(obj0, obj1):
	return pdist(obj0.pos, obj1.pos)

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

# Set pos and r in game coordinates in constructor.
class WorldBound(enco.Component):
	boxcolor = 255, 255, 255
	def pV(self):
		return view.VconvertG(self.pos)
	def rV(self):
		return T(view.VscaleG * self.r)
	def drawbox(self, color=None):
		pygame.draw.circle(pview.screen, (color or self.boxcolor), self.pV(), self.rV(), 1)


class HasVelocity(enco.Component):
	def think(self, dt):
		x, y = self.pos
		vx, vy = self.v
		self.pos = x + vx * dt, y + vy * dt


class ShotPath(enco.Component):
	def __init__(self, D, d0):
		self.D = D
		self.d0 = d0

	def think(self, dt):
		f = 0.5 * self.f * (3 - self.f ** 2)
		d = math.mix(self.d0, self.D, f)
		self.pos = math.CS(self.A, d, self.pos0)

class Engines(enco.Component):
	def aup(self):
		return [3, 4, 5.5, 8, 12][state.techlevel["engine"]]
	def adown(self):
		return 10
	def adrag(self):
		level = state.techlevel["drag"]
		return ([0, 0.5, 1, 2, 10][level] if level >= 0 else 1) * self.aup()

class LaunchCages(enco.Component):
	def think(self, dt):
		if self.cageunlocked() and state.charge["gravnet"] < 1:
			state.charge["gravnet"] = math.approach(state.charge["gravnet"], 1, self.cagechargerate() * dt)
		if self.controls["act"] and self.cageunlocked():
			if self.canlaunchcage():
				self.launchcage()
			else:
				pass
	def cagechargerate(self):
		return [0.5, 1, 2, 10][state.techlevel["gravnet"]]
	def cageunlocked(self):
		return state.techlevel["gravnet"] >= 0
	def canlaunchcage(self):
		return state.charge["gravnet"] == 1
	def launchgage(self):
		state.shots.append(Cage(self.pos, self.A))
		state.charge["gravnet"] = 0

@KeepsTime()
@WorldBound()
@Engines()
@LaunchCages()
class You:
	def __init__(self, pos):
		self.pos = pos
		self.v = 0, 0
		self.A = 0
		self.r = 1
		self.omega = 3
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
	
	def leave(self, obj):
		self.v = 2, 0
		self.A = 0
		self.pos = math.CS(self.A, 5, obj.pos)

	def think(self, dt):
		x, y = self.pos
		vx, vy = self.v
		A = math.dA(self.A + dt * self.omega * self.controls["dA"])
		if self.controls["up"]:
			vx, vy = math.CS(math.mixA(self.A, A, 0.5), self.aup() * dt, (vx, vy))
		else:
			a = self.adown() if self.controls["down"] else self.adrag()
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
		graphics.drawG("ship", self.pV(), 0.003, self.A)
		self.drawbeam()

	def drawglow(self):
		pV = view.VconvertG(math.CS(self.A, 1.4, self.pos))
		glow = graphics.glow(T(view.VscaleG * 1.0), seed = random.randint(0, 9), color = (100, 50, 0, 100))
		pview.screen.blit(glow, glow.get_rect(center = self.pV()))


	def drawbeam(self):
		perform.start("beam")
		beam = Beam(self.pos, self.A, 0.5, 10, 0.15, 1)
		for DM in state.DMs:
			beam.occlude(DM)
		beam.draw()
		perform.stop("beam")

class Findable(enco.Component):
	def __init__(self, xp = 1):
		self.xp = xp
		self.found = False

	def find(self):
		self.found = True
		self.onfound()
	
	def onfound(self):
		state.xp += self.xp


class DrawCage(enco.Component):
	def __init__(self):
		self.omegaspin = None
	def drawcage(self):
		if self.omegaspin is None:
			self.omegaspin = random.uniform(0.8, 2.5) * random.choice([-1, 1])
		if not view.isvisible(self):
			return
		pV = view.VconvertG(self.pos)
		rV = T(view.VscaleG * self.r)
		graphics.drawcageG(self.t * self.omegaspin, pV, 0.0065 * self.r, 0)


class DrawDM(enco.Component):
	def draw(self):
		if self.found:
			self.drawcage()
#			pygame.draw.circle(pview.screen, (255, 255, 255), pV, rV, 1)
		else:
			pV = view.VconvertG(self.pos)
			rV = T(view.VscaleG * self.r)
			color = (0, 100, 100) if self.found else (0, 0, 0)
			pygame.draw.circle(pview.screen, color, pV, rV)

class Unfindable(enco.Component):
	def __init__(self):
		self.found = False

	def find(self):
		pass

class LinePart:
	def __init__(self, pos0, pos1, v):
		self.pos0 = pos0
		self.pos1 = pos1
		self.v = v
		self.d = pdist(pos0, pos1)
		self.T = self.d / v
	def pos(self, t):
		return math.mix(self.pos0, self.pos1, t / self.T)

def joinparts(part0, part1, v):
	return LinePart(part0.pos(part0.T), part1.pos(0), v)


# v > 0 counterclockwise, v < 0 clockwise
class CirclePart:
	def __init__(self, center, Rorbit, v, Aoff, A0 = 0, A1 = math.tau):
		self.center = center
		self.Rorbit = Rorbit
		self.omega = v / Rorbit
		self.Aoff = Aoff
		self.A0 = A0
		self.A1 = A1
		self.T = (A1 - A0) * Rorbit / abs(v)
	def pos(self, t):
		theta = self.A0 + self.Aoff + t * self.omega
		return math.CS(theta, self.Rorbit, self.center)

class WavePart:
	def __init__(self, pos0, pos1, v, amp, Nwave, neg):
		self.pos0 = pos0
		self.pos1 = pos1
		self.v = v
		self.amp = amp
		self.Nwave = Nwave
		self.neg = neg
		self.d = pdist(pos0, pos1)
		self.T = self.d / v
		x0, y0 = pos0
		x1, y1 = pos1
		self.px, self.py = x1 - x0, y1 - y0
		self.qx, self.qy = math.norm((-self.px, self.py), amp)
		if neg:
			self.qx, self.qy = -self.qx, -self.qy
	def pos(self, t):
		f = t / self.T
		x, y = math.mix(self.pos0, self.pos1, f)
		C = math.cos(f * math.tau / 2 * self.Nwave)
		x += C * self.qx
		y += C * self.qy
		return x, y
		
class FollowsPath(enco.Component):
	def __init__(self):
		self.jpath = 0
		self.tpath = 0
	def think(self, dt):
		self.tpath += -dt if self.reverse else dt
		self.setpos()
	def jumprandom(self):
		T = sum(path.T for path in self.paths)
		self.tpath += random.uniform(0, T) * (-1 if self.reverse else 1)
	def setpos(self):
		if self.reverse:
			while self.tpath < 0:
				self.jpath = (self.jpath - 1) % len(self.paths)
				self.tpath += self.paths[self.jpath].T
		else:
			while self.tpath >= self.paths[self.jpath].T:
				self.tpath -= self.paths[self.jpath].T
				self.jpath = (self.jpath + 1) % len(self.paths)
		self.pos = self.paths[self.jpath].pos(self.tpath)
#	def draw(self):
#		self.drawpath()

	def drawpath(self):
		ps = []
		for path in self.paths:
			ps += [path.pos(t) for t in range(int(path.T))] + [path.pos(path.T)]
		pVs = [view.VconvertG(p) for p in ps]
		pygame.draw.lines(pview.screen, (255, 255, 255), False, pVs, 1)


@WorldBound()
@Findable(1)
@KeepsTime()
@FollowsPath()
@DrawCage()
@DrawDM()
class Visitor:
	def __init__(self, pos0, pos1, Nstay, Rorbit, v, reverse=False):
		self.r = 0.4
		self.pos0 = pos0
		self.pos1 = pos1
		self.Nstay = Nstay
		self.Rorbit = Rorbit
		self.v = v
		self.reverse = reverse
#		self.Nwave = int(round(pdist(pos0, pos1) / (3 * self.Rorbit)))
		dx, dy = dvec(pos1, pos0)
		Aoff = math.atan2(dy, dx)
		backpath = CirclePart(pos0, Rorbit, v, Aoff, -math.tau/4, math.tau * (1/4 + Nstay))
		frontpath = CirclePart(pos1, Rorbit, v, Aoff, math.tau/4, math.tau * 3/4)
		self.paths = [
			backpath,
			joinparts(backpath, frontpath, v),
			frontpath,
			joinparts(frontpath, backpath, v),
		]
		self.setpos()
		self.found = False
		self.jumprandom()

class DrawRock(enco.Component):
	def draw(self):
		pV = view.VconvertG(self.pos)
		rV = T(view.VscaleG * self.r)
		color = (80, 80, 80)
		pygame.draw.circle(pview.screen, color, pV, rV)

@KeepsTime()
@FollowsPath()
@DrawRock()
@Unfindable()
class CircleRock:
	def __init__(self, center, Rorbit, v, r, reverse = False):
		self.paths = [CirclePart(center, Rorbit, v, 0)]
		self.reverse = reverse
		self.r = r
		self.setpos()
		self.jumprandom()


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
		self.blockers = []

	def occlude(self, obj):
		x, y = obj.pos
		xB, yB = self.Rinv((x - self.x0, y - self.y0))
		if not self.d0 <= xB <= self.d1:
			return
		w = math.interp(xB, self.d0, self.w0, self.d1, self.w1)
		if abs(yB) > w + obj.r:
			return
		self.fences.append((xB, w, (yB - obj.r) / w, (yB + obj.r) / w))
		self.blockers.append(obj)

	def draw(self):
		self.fences.sort()
#		dps = [(self.d0, self.w0), (self.d0, -self.w0), (self.d1, -self.w1), (self.d1, self.w1)]
#		dps = [self.R((dx, dy)) for dx, dy in dps]
		polys = []
#		for alpha0, fw in [(40, 1), (50, 0.8), (60, 0.6)]:
		for alpha0, fw in [(40, 1)]:
			alpha = int(alpha0 * random.uniform(1, 1.1))
			dps = [self.R((dx, dy)) for dx, dy in occludebeam(self.w0 * fw, self.w1 * fw, self.d0, self.d1, self.fences)]
			pVs = [view.VconvertG((self.x0 + dx, self.y0 + dy)) for dx, dy in dps]
			polys.append((alpha, pVs))
		xs = [x for alpha, pVs in polys for x, y in pVs]
		ys = [y for alpha, pVs in polys for x, y in pVs]
		xVmin = max(min(xs), 0)
		xVmax = min(max(xs), pview.w)
		yVmin = max(min(ys), 0)
		yVmax = min(max(ys), pview.h)
		w, h = xVmax - xVmin, yVmax - yVmin
		surf = pygame.Surface((w, h)).convert_alpha()
		surf.fill((255, 255, 50, 0))
		for alpha, pVs in polys:
			pVs = [(xV - xVmin, yV - yVmin) for xV, yV in pVs]
			pygame.draw.polygon(surf, (255, 255, 50, alpha), pVs)
		for obj in self.blockers:
			xV, yV = obj.pV()
			pygame.draw.circle(surf, (255, 255, 50, 0), (xV - xVmin, yV - yVmin), obj.rV())
		fade = graphics.fadeimg(T(view.VscaleG * self.d1))
		xV0, yV0 = view.VconvertG((self.x0, self.y0))
		center = xV0 - xVmin, yV0 - yVmin
		surf.blit(fade, fade.get_rect(center = center), special_flags = pygame.BLEND_RGBA_MULT)
		pview.screen.blit(surf, (xVmin, yVmin))
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
@Lifetime(0.5)
@ShotPath(7, 0.6)
@DrawCage()
class Cage:
	def __init__(self, pos0, A):
		self.pos0 = pos0
		self.A = A
		self.pos = math.CS(A, self.d0, pos0)
		self.r = 0.2

	def think(self, dt):
		for DM in state.DMs:
			if not DM.found and overlaps(DM, self):
				DM.find()
				self.alive = False

	def draw(self):
		self.drawcage()


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


@WorldBound()
class Spot:
	def __init__(self, pos):
		self.pos = pos
		self.r = 2

	def think(self, dt):
		pass

	def nnear(self):
		DMs = [DM for DM in state.DMs if dist(self, DM) < 25]
		return sum(not DM.found for DM in DMs), sum(DM.found for DM in DMs)

	def draw(self):
		if not view.isvisible(self):
			return
		pygame.draw.circle(pview.screen, (30, 50, 70), self.pV(), self.rV())
		if state.techlevel["count"] > 0:
			nunfound, nfound = self.nnear()
			text = f"{nfound} : {nunfound}"
			ptext.draw(text, center = self.pV(), color = "#7f7fff", owidth = 1, fontsize = T(view.VscaleG * 1))



