import pygame, math, random
from . import pview, grid, view, state, ptext, graphics
from .pview import T

def drawcircleat(pH, rG, color):
	xG, yG = grid.GconvertH(pH)
	xV, yV = view.VconvertG((xG, yG))
	r = T(view.VscaleG * rG)
	h = T(view.VscaleG * rG * 0.6)
	pygame.draw.circle(pview.screen, color, (xV, yV - h), r)


class You:
	def __init__(self, pH):
		self.pH = pH
		self.t = 0
		self.fmove = 0
		self.fnab = 0
		self.tonab = []

	def think(self, dt):
		self.t += dt
		if self.fmove:
			self.fmove = math.approach(self.fmove, 0, dt * 4 * len(self.pH) ** -0.4)
		if self.fnab and not self.fmove:
			self.fnab = math.approach(self.fnab, 0, dt * 2)
			if self.fnab == 0:
				self.tonab.pop()
				if self.tonab:
					self.fnab = 1

	def draw0(self):
		drawcircleat(self.pH, 0.4, (255, 200, 40))

	def draw(self):
		if self.fmove:
			a = (1 - self.fmove) * (len(self.movepath) - 1)
			n, k = divmod(a, 1)
			n = int(n)
			pG = math.mix(self.movepath[n], self.movepath[n+1], k)
		else:
			pG = grid.GconvertH(self.pH)
		zG = math.mix(0.7, 1, math.cycle(self.t / 4))
		pV = view.VconvertG(pG, zG = zG)
		scale = 0.004 * view.VscaleG * pview.f
		graphics.draw("token", pV, scale)
		for jgoal, goal in enumerate(self.tonab):
			f = self.fnab if jgoal == len(self.tonab) - 1 else 1
			goal.drawnab(self.pH, f)

	def drawghost(self, pH):
		zG = 0.7
		pV = view.VconvertG(grid.GconvertH(pH), zG = zG)
		scale = 0.004 * view.VscaleG * pview.f
		graphics.draw("token", pV, scale, alpha = 0.4)

	def canclaim(self, goal):
		return grid.distanceH(self.pH, goal.pH) <= 1

	def claim(self, goal):
		state.goals.remove(goal)
		self.tonab.append(goal)
		self.fnab = 1

	def canplaceat(self, pH):
		return state.grid0.samecomponent(self.pH, pH) and pH not in state.grid0.goals
	
	def placeat(self, pH):
		pH0 = self.pH
		self.pH = pH
		if pH != pH0:
			self.fmove = 1
			self.movepath = [grid.GconvertH(p) for p in state.grid0.getpath(pH0, pH)]
			state.advanceturn()

class Obstacle:
	def __init__(self, pH):
		self.pH = pH
		self.reset()
		self.fmove = 0
		self.t = 0

	def think(self, dt):
		self.t += dt
		if self.fmove:
			self.fmove = math.approach(self.fmove, 0, dt * 4)

	def reset(self):
		self.ready = True

	def draw0(self):
		color = (255, 255, 255) if self.ready else (128, 128, 128)
		drawcircleat(self.pH, 0.3, color)
		pV = view.VconvertG(grid.GconvertH(self.pH))
		ptext.draw(self.name, center = pV, fontsize = T(view.VscaleG * 0.2), owidth = 0.5)

	def draw(self):
		if self.fmove > 0:
			pH = math.mix(self.pH, self.movepH, self.fmove)
			zG = 2.5 * self.fmove * (1 - self.fmove)
		else:
			pH = self.pH
			zG = 0
		pV = view.VconvertG(grid.GconvertH(pH), zG = zG)
		scale = 0.007 * view.VscaleG * pview.f
		shade = 1 if self.ready else 0.4
		graphics.draw(self.name, pV, scale, shade = shade)

	def drawghost(self, pH):
		pV = view.VconvertG(grid.GconvertH(pH))
		scale = 0.007 * view.VscaleG * pview.f
		graphics.draw(self.name, pV, scale, alpha = 0.6)

	def canplaceat(self, pH):
		return pH in state.grid0.open and self.legalmove(pH)
	
	def placeat(self, pH):
		if pH != self.pH:
			self.fmove = 1
			self.movepH = self.pH
			self.ready = False
		self.pH = pH

class Pawn(Obstacle):
	name = "pawn"
	def legalmove(self, pH):
		return grid.distanceH(self.pH, pH) <= 1


class Goal:
	def __init__(self, pH):
		self.pH = pH

	def draw0(self):
		drawcircleat(self.pH, 0.3, (100, 255, 100))

	def draw(self):
		pV0 = view.VconvertG(grid.GconvertH(self.pH))
		scale = 0.007 * view.VscaleG * pview.f
		graphics.draw("pedestal", pV0, scale)
		a = math.cycle(0.001 * pygame.time.get_ticks() + math.fuzz(1, *self.pH))
		mask = math.imix((100, 255, 100), (120, 120, 255), a)
		tcycle = math.fuzzrange(2, 3, 2, *self.pH)
		a = math.cycle(0.001 * pygame.time.get_ticks() / tcycle + math.fuzz(3, *self.pH))
		pV1 = view.VconvertG(grid.GconvertH(self.pH), zG = math.mix(1, 1.2, a))
		graphics.draw("goal", pV1, scale = scale, mask = mask)

	def drawnab(self, pH, f):
		pV0 = view.VconvertG(grid.GconvertH(self.pH))
		scale = 0.007 * view.VscaleG * pview.f
		graphics.draw("pedestal", pV0, scale, alpha = f)
		pG = grid.GconvertH(math.mix(pH, self.pH, f))
		zG = 1 + 3 * f * (1 - f)
		pV = view.VconvertG(pG, zG = zG)
		mask = (100, 255, 100)
		graphics.draw("goal", pV, scale = scale, mask = mask)
		


class Light:
	def __init__(self, pH, dirHs):
		self.pH = pH
		self.dirHs = dirHs
		self.hitsyou = False

	def illuminate(self):
		self.dlights = []
		self.hitsyou = False
		for dxH, dyH in self.dirHs:
			dlight = 0
			xH, yH = self.pH
			while True:
				xH, yH = xH + dxH, yH + dyH
				dlight += 1
				if (xH, yH) == state.you.pH:
					dlight += 0.1
					self.hitsyou = True
					break
				if (xH, yH) not in state.grid0.cells:
					dlight -= 0.25
					break
				if (xH, yH) not in state.grid0.open or (xH, yH) in state.grid0.goals:
					break
				state.grid0.illuminate((xH, yH))
			self.dlights.append(dlight)

	def draw0(self):
		xG, yG = grid.GconvertH(self.pH)
		xV, yV = view.VconvertG((xG, yG))
		r = T(view.VscaleG * 0.3)
		h = T(view.VscaleG * 0.2)
		pygame.draw.circle(pview.screen, (240, 120, 120), (xV, yV - h), r)
		xH0, yH0 = self.pH
		for dxH, dyH in self.dirHs:
			xH, yH = self.pH
			n = 0
			while True:
				xH, yH = xH + dxH, yH + dyH
				if (xH, yH) not in state.grid0.open:
					break
				n += 1
			if n > 0:
				pH0 = xH0 + dxH * 0.5, yH0 + dyH * 0.5
				pH1 = xH0 + dxH * (n + 0.5), yH0 + dyH * (n + 0.5)
				xV0, yV0 = view.VconvertG(grid.GconvertH(pH0))
				xV1, yV1 = view.VconvertG(grid.GconvertH(pH1))
				pygame.draw.line(pview.screen, (255, 160, 160),
					(xV0, yV0 - h), (xV1, yV1 - h), T(view.VscaleG * 0.1))

	def draw(self):
		xH, yH = self.pH
		h = T(view.VscaleG * 0.2)
		for (dxH, dyH), dlight in zip(self.dirHs, self.dlights):
			xH0 = xH + 0.25 * dxH
			yH0 = yH + 0.25 * dyH
			xH1 = xH + (dlight - 0.25) * dxH
			yH1 = yH + (dlight - 0.25) * dyH
			xV0, yV0 = view.VconvertG(grid.GconvertH((xH0, yH0)))
			xV1, yV1 = view.VconvertG(grid.GconvertH((xH1, yH1)))
			yV0 -= h
			yV1 -= h
			for _ in range(4):
				angle = random.uniform(0, 360)
				scale, alpha = random.choice([(1, 0.8), (1.2, 0.5), (1.4, 0.3)])
				scale *= view.VscaleG * pview.f * 0.003
				color = (255, 255, 100)
				graphics.draw("splash", (xV1, yV1), scale, alpha = alpha,
					mask = color, angle = angle)
			colors = [
				(255, 255, 100),
				(255, 255, 150),
				(255, 255, 200),
			]
			ws = [
				random.uniform(0.18, 0.20),
				random.uniform(0.13, 0.16),
				random.uniform(0.09, 0.12),
			]
			for color, w in zip(colors, ws):
				pygame.draw.line(pview.screen, color,
					(xV0, yV0), (xV1, yV1), T(view.VscaleG * w))
	


