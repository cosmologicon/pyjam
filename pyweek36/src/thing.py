import pygame, math, random
from . import view, pview, graphics, state, enco, ptext, perform, settings, sound
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
	def isactive(self, T):
		v = self.v + 20
		return view.beyondminimap(self) < T * v

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
	def vmax(self):
		return self.aup()
	def omega(self):
		return [2.5, 3, 4, 6, 8][state.techlevel["engine"]]
	def aup(self):
		return [3, 4, 5.5, 8, 12][state.techlevel["engine"]]
	def adown(self):
		return 10
	def adrag(self):
		level = state.techlevel["drag"]
		return ([0, 0.5, 1, 2, 10][level] if level >= 0 else 1) * self.aup()

class TakesDamage(enco.Component):
	def __init__(self):
		self.finvul = 0
	def think(self, dt):
		if self.finvul or self.driveon:
			if any(DM.collides(self) for DM in state.DMtracker.active):
				self.finvul = 1
			else:
				self.finvul = math.approach(self.finvul, 0, 0.5 * dt)
		else:
			for DM in state.DMtracker.active:
				if DM.collides(self):
					from . import progress
					progress.takedamage(DM.dhp)
					self.finvul = 1
					break
	def invulframe(self):
		if state.hp <= 0:
			return True
		if not self.finvul:
			return False
		N = 10 if self.finvul < 0.5 else 5
		return (self.t * N) % 1 > 0.5

class LaunchCages(enco.Component):
	def think(self, dt):
		if self.cageunlocked() and state.charge["gravnet"] < 1:
			state.charge["gravnet"] = math.approach(state.charge["gravnet"], 1, self.cagechargerate() * dt)
		if self.controls["gravnet"] and self.cageunlocked():
			if self.canlaunchcage():
				self.launchcage()
			else:
				pass
	def cagechargerate(self):
		return [0.25, 0.5, 1, 2, 4][state.techlevel["gravnet"]]
	def cageunlocked(self):
		return state.techlevel["gravnet"] >= 0
	def canlaunchcage(self):
		return state.charge["gravnet"] == 1
	def launchcage(self):
		state.shots.append(Cage(self.pos, self.A))
		dA = 0.08
		if state.techlevel["gravnet"] >= 3:
			state.shots.append(Cage(self.pos, self.A + dA))
			state.shots.append(Cage(self.pos, self.A - dA))
		if state.techlevel["gravnet"] >= 4:
			state.shots.append(Cage(self.pos, self.A + 2 * dA))
			state.shots.append(Cage(self.pos, self.A - 2 * dA))
		state.charge["gravnet"] = 0


class ShineBeam(enco.Component):
	def __init__(self):
		self.beamon = False
		self.tbeam = 0
	def onhome(self):
		self.tbeam = 0
		self.beamon = False
	def turnbeamoff(self):
		self.tbeam = 0
		self.beamon = False
	def turnbeamon(self):
		if state.energy >= 1:
			from . import progress
			progress.useenergy(1)
			self.tbeam = 0
			self.beamon = True
			sound.play("beam")
		else:
			sound.play("lowcharge")
	def beamunlocked(self):
		return state.techlevel["beam"] >= 0
	def think(self, dt):
		if not self.beamunlocked():
			return
		if self.beamon:
			self.tbeam += dt
		if self.beamon and self.controls["stop"]:
			self.turnbeamoff()
		if self.controls["beam"]:
			self.turnbeamon()
	def launchcage(self):
		if self.beamon:
			self.turnbeamoff()
	def drawbeam(self):
		if not self.beamon:
			return
		perform.start("beam")

		d0 = 0.5
		d1 = [4, 6, 8, 10, 14][state.techlevel["beam"]]
		w0 = [0.03, 0.05, 0.07, 0.03, 0.05][state.techlevel["beam"]]
		w1 = w0 * d1 / d0
		alphamax = [0.2, 0.3, 0.4, 0.4, 0.5][state.techlevel["beam"]]
		falpha = math.interp(self.tbeam, 0, 0, 2, alphamax)
		beams = [Beam(self.pos, self.A, d0, d1, w0, w1, falpha)]
		if state.techlevel["beam"] >= 3:
			for dA in (-1, 1):
				pos = math.CS(self.A + dA * math.tau / 4, 0.5, self.pos)
				beams.append(Beam(pos, self.A + 0.1 * dA, d0 - 0.3, d1 - 0.3, w0, w1, falpha))
		for beam in beams:
			for DM in state.DMtracker.active:
				beam.occlude(DM)
			for spot in state.spots:
				beam.occlude(spot)
			beam.draw()
		perform.stop("beam")

class ShootRing(enco.Component):
	def __init__(self):
		self.tring = 0
	def onhome(self):
		self.tring = 0
	def ringunlocked(self):
		return state.techlevel["ring"] >= 0
	def think(self, dt):
		if not self.ringunlocked():
			return
		if self.controls["ring"]:
			if state.energy >= 1:
				from . import progress
				progress.useenergy(1)
				state.pulses.append(Ring(self))
				sound.play("ring")
			else:
				sound.play("lowcharge")

class HasGlow(enco.Component):
	def __init__(self):
		self.glowon = False
		self.tglow = 0
	def onhome(self):
		self.tglow = 0
		self.glowon = False
	def turnglowoff(self):
		self.tglow = 0
		self.glowon = False
	def turnglowon(self):
		if state.energy >= 1:
			from . import progress
			progress.useenergy(1)
			self.tglow = 0
			self.glowon = True
			sound.play("glow")
		else:
			sound.play("lowcharge")
	def glowunlocked(self):
		return state.techlevel["glow"] >= 0
	def think(self, dt):
		if not self.glowunlocked():
			return
		if self.glowon:
			self.tglow += dt
		if self.glowon and self.controls["stop"]:
			self.turnglowoff()
		if self.controls["glow"]:
			self.turnglowon()
	def launchcage(self):
		if self.glowon:
			self.turnglowoff()
	def drawglow(self):
		if not self.glowon:
			return
		omega = [1, 1, 1.5, 2, 3][state.techlevel["glow"]]
		R0 = [2.5, 2.5, 3.5, 5, 5][state.techlevel["glow"]]
		r = [2, 2, 3, 4.5, 4.5][state.techlevel["glow"]]
		N = [1, 2, 2, 3, 4][state.techlevel["glow"]]
		A = omega * self.tglow
		R = math.smoothinterp(self.tglow, 0, 0, 1, R0)
		for j in range(N):
			pV = view.VconvertG(math.CS(A + j / N * math.tau, R, self.pos))
			glow = graphics.glow(T(view.VscaleG * r), seed = random.randint(0, 9), color = (100, 50, 0, 100))
			pview.screen.blit(glow, glow.get_rect(center = pV))


class Hyperdrive(enco.Component):
	def __init__(self):
		self.driveon = False
		self.tdrive = 0
	def onhome(self):
		self.tdrive = 0
		self.driveon = False
	def turndriveoff(self):
		self.tdrive = 0
		self.driveon = False
		sound.play("driveoff")
	def turndriveon(self):
		if state.energy >= 1:
			from . import progress
			progress.useenergy(1)
			self.tdrive = 0
			self.driveon = True
			sound.play("drive")
		else:
			sound.play("lowcharge")
	def driveunlocked(self):
		return state.techlevel["drive"] >= 0
	def think(self, dt):
		if not self.driveunlocked():
			return
		if self.driveon:
			self.tdrive += dt
		if self.driveon and self.controls["stop"]:
			self.turndriveoff()
		if self.controls["drive"]:
			self.turndriveon()
	def launchcage(self):
		if self.driveon:
			self.turndriveoff()
	def draw(self):
		if not self.driveon:
			return
		for j in range(T(view.VscaleG * 0.05)):
			pG = math.CS(random.uniform(0, math.tau), random.uniform(0, 0.1), self.pos)
			pV = view.VconvertG(pG)
			rV = T(view.VscaleG * 1)
			color = math.imix((0, 0, 50), (100, 100, 255), random.uniform(0.5, 0.6))
			pygame.draw.circle(pview.screen, color, pV, rV, 1)
			
			


@KeepsTime()
@WorldBound()
@Engines()
@TakesDamage()
@LaunchCages()
@ShineBeam()
@ShootRing()
@HasGlow()
@Hyperdrive()
class You:
	def __init__(self, pos):
		self.pos = pos
		self.v = 0, 0
		self.A = 0
		self.r = 0.6
		self.on = False
		self.flean = 0

	def control(self, kdowns, kpressed, mdowns):
		keys = set(kname for kname, kcodes in settings.keys.items() if any(kpressed[kcode] for kcode in kcodes))
		self.controls = {
			"thrust": "thrust" in keys,
			"stop": "stop" in keys,
			"dA": ("left" in keys) - ("right" in keys),
			"gravnet": bool(set(settings.keys["gravnet"]) & set(kdowns)),
			"beam": bool(set(settings.keys["beam"]) & set(kdowns)),
			"ring": bool(set(settings.keys["ring"]) & set(kdowns)),
			"glow": bool(set(settings.keys["glow"]) & set(kdowns)),
			"drive": bool(set(settings.keys["drive"]) & set(kdowns)),
		}
	
	def leave(self, obj):
		self.v = 2, 0
		self.A = 0
		self.pos = math.CS(self.A, obj.r + self.r + 0.5, obj.pos)

	def think(self, dt):
		if not state.hp:
			return
		x, y = self.pos
		v = self.v
		fAdrive = 2 if self.driveon else 1
		A = math.dA(self.A + dt * self.omega() * self.controls["dA"] * fAdrive)
		fdrive = 6 if self.driveon else 1
		if self.controls["thrust"]:
			v = math.CS(math.mixA(self.A, A, 0.5), self.aup() * dt * fdrive, v)
		else:
			v = math.approach(v, (0, 0), self.adrag() * dt * fdrive)
		v = math.vclamp(v, self.vmax() * fdrive)
		vxavg, vyavg = math.mix(self.v, v, 0.5)
		self.pos = x + dt * vxavg, y + dt * vyavg
		self.v = v
		self.A = A
		self.flean = math.approach(self.flean, -self.controls["dA"], 4 * dt)

	def draw(self):
		if not self.invulframe():
			graphics.drawshipG(self.pV(), 0.008 * self.r, self.A, self.flean)


class Findable(enco.Component):
	def __init__(self, xp = 1):
		self.xp = xp
		self.found = False

	def isunfound(self):
		return not self.found

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
	def __init__(self):
		self.tring = 0
	def ringcharge(self, t):
		self.tring = t
	def think(self, dt):
		self.tring = math.approach(self.tring, 0, dt)
	def draw(self):
		if self.found:
			self.drawcage()
		else:
			pygame.draw.circle(pview.screen, (0, 0, 0), self.pV(), self.rV())
			if self.tring > 0:
				color = math.imix((0, 0, 0), (255, 255, 100), math.interp(self.tring, 0, 0, 1, 1))
				pygame.draw.circle(pview.screen, color, self.pV(), self.rV(), T(2))
				
	def mapcolor(self):
		return (0, 200, 200) if self.found else None

class Unfindable(enco.Component):
	def __init__(self):
		self.found = False

	def isunfound(self):
		return False

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
		self.tpath += math.fuzzrange(0, T, *self.pos) * (-1 if self.reverse else 1)
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


class DamagesYou(enco.Component):
	dhp = 1
	def collides(self, obj):
		return overlaps(self, obj)
	
class DoesntDamageYou(enco.Component):
	def collides(self, obj):
		return False

@WorldBound()
@Findable(1)
@KeepsTime()
@FollowsPath()
@DoesntDamageYou()
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
	def mapcolor(self):
		return None



@WorldBound()
@KeepsTime()
@DamagesYou()
@FollowsPath()
@DrawRock()
@Unfindable()
class CircleRock:
	def __init__(self, center, Rorbit, v, r, reverse = False):
		self.paths = [CirclePart(center, Rorbit, v, 0)]
		self.reverse = reverse
		self.r = r
		self.v = v
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
	def __init__(self, p0, A, d0, d1, w0, w1, falpha=1):
		self.p0 = self.x0, self.y0 = p0
		self.A = A
		self.d0 = d0
		self.d1 = d1
		self.w0 = w0
		self.w1 = w1
		self.falpha = falpha
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
		for alpha0, fw in [(100, 1)]:
			alpha = int(self.falpha * alpha0 * random.uniform(1, 1.1))
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
		rect = fade.get_rect(center = center)
		w, h = surf.get_size()
		surf.blit(fade, rect, special_flags = pygame.BLEND_RGBA_MULT)
		if rect.x > 0:
			surf.fill((255, 255, 50, 0), (0, 0, rect.x, h))
		if rect.y > 0:
			surf.fill((255, 255, 50, 0), (0, 0, w, rect.y))
		if rect.right < w:
			surf.fill((255, 255, 50, 0), (rect.right, 0, w - rect.right, h))
		if rect.bottom < h:
			surf.fill((255, 255, 50, 0), (0, rect.bottom, w, h - rect.bottom))
			
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
		for DM in state.DMtracker.active:
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
		self.d0 = state.you.r
		self.D = [4, 5, 7, 10, 12][state.techlevel["gravnet"]]
		self.T = [0.7, 0.6, 0.5, 0.4, 0.3][state.techlevel["gravnet"]]

	def think(self, dt):
		for DM in state.DMtracker.active:
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
			if any(math.hypot(DM.pos[0] - x, DM.pos[1] - y) < DM.r for DM in state.DMtracker.active):
				continue
			pV = view.VconvertG((x, y))
			pview.screen.set_at(pV, (100, 100, 255))

@WorldBound()
@KeepsTime()
@Lifetime(2)
class Ring:
	def __init__(self, origin):
		self.origin = origin
		self.pos = origin.pos
		self.R = [5, 7, 9, 12, 16][state.techlevel["ring"]]
		self.T = [1, 1, 1, 1, 1][state.techlevel["ring"]]
		self.df = [0.05, 0.1, 0.15, 0.2, 0.25][state.techlevel["ring"]]
		self.power = [0.5, 1, 3, 8, 20][state.techlevel["ring"]]
		self.charged = []

	def think(self, dt):
		r = self.ringr(self.f)
		for DM in state.DMtracker.active:
			if dist(self.origin, DM) < r and DM not in self.charged:
				DM.ringcharge(self.power)
				self.charged.append(DM)

	def ringr(self, f):
		return self.R * f ** 0.5 if f > 0 else 0

	def draw(self):
		rV0 = T(view.VscaleG * self.ringr(self.f))
		rV1 = T(view.VscaleG * self.ringr(self.f - self.df))
		w = 0 if rV1 <= 0 else rV0 - rV1
		color = math.imix((255, 255, 0), (0, 0, 0), self.f)
		pygame.draw.circle(pview.screen, color, self.origin.pV(), rV0, w)


class TracksNear(enco.Component):
	def nnear(self, countall = False):
		DMs = state.DMs if countall else state.DMtracker.active
		DMs = [DM for DM in DMs if dist(self, DM) < settings.countradius]
		return sum(not DM.found for DM in DMs), sum(DM.found for DM in DMs)
	def nunfound(self, countall = False):
		DMs = state.DMs if countall else state.DMtracker.active
		DMs = [DM for DM in DMs if dist(self, DM) < settings.countradius]
		return sum(DM.isunfound() for DM in DMs)
	def nfound(self):
		return self.nnear()[1]

@WorldBound()
@KeepsTime()
@TracksNear()
class Home:
	def __init__(self, pos):
		self.pos = pos
		self.r = 2

	def draw(self):
		if not view.isvisible(self):
			return
		A = math.tau / 8 * (self.t * 0.1 % 1)
		graphics.drawG("starbase", self.pV(), 0.006 * self.r, A, dA = 0.5)
		if state.techlevel["count"] > 0:
			text = f"{self.nunfound()}"
			ptext.draw(text, center = self.pV(), color = "#7f7fff", shade = 1, owidth = 0.5, fontsize = T(view.VscaleG * 2))


@WorldBound()
@KeepsTime()
@TracksNear()
class Spot:
	def __init__(self, pos):
		self.pos = pos
		self.r = 1
		self.unlocked = False
		self.funlock = 0

	def think(self, dt):
		if not self.unlocked and view.isvisible(self) and state.techlevel["count"] > 0 and self.nfound() >= 3:
			from . import quest
			self.unlocked = True
			quest.marquee.append("New Counter deployed.")
			quest.marquee.append("+10 XP")
			state.xp += 10
			self.funlock = 0
		if self.unlocked:
			self.funlock = math.approach(self.funlock, 1, 0.5 * dt)

	def draw(self):
		if not view.isvisible(self) or not self.unlocked:
			return
		A = math.tau / 8 * (self.t % 1)
		graphics.drawG("starbase", self.pV(), 0.006 * self.r, A, dA = 5)
		if state.techlevel["count"] > 0:
			text = f"{self.nunfound()}"
			ptext.draw(text, center = self.pV(), color = "#7f7fff", shade = 1, owidth = 0.5, fontsize = T(view.VscaleG * 1))



