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

	def draw0(self):
		drawcircleat(self.pH, 0.4, (255, 200, 40))

	def drawghost(self, pH):
		drawcircleat(pH, 0.4, (60, 60, 60))

	def canclaim(self, goal):
		return grid.distanceH(self.pH, goal.pH) <= 1

	def canplaceat(self, pH):
		return state.grid0.samecomponent(self.pH, pH)
	
	def placeat(self, pH):
		moving = pH != self.pH
		self.pH = pH
		if moving:
			state.advanceturn()

class Obstacle:
	def __init__(self, pH):
		self.pH = pH
		self.reset()

	def reset(self):
		self.ready = True

	def draw0(self):
		color = (255, 255, 255) if self.ready else (128, 128, 128)
		drawcircleat(self.pH, 0.3, color)
		pV = view.VconvertG(grid.GconvertH(self.pH))
		ptext.draw(self.name, center = pV, fontsize = T(view.VscaleG * 0.2), owidth = 0.5)

	def draw(self):
		pV = view.VconvertG(grid.GconvertH(self.pH))
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
		xV, yV = view.VconvertG(grid.GconvertH(self.pH))
		scale = 0.007 * view.VscaleG * pview.f
		graphics.draw("pedestal", (xV, yV), scale)
		a = math.cycle(0.001 * pygame.time.get_ticks() + math.fuzz(1, *self.pH))
		mask = math.imix((100, 255, 100), (120, 120, 255), a)
		tcycle = math.fuzzrange(2, 3, 2, *self.pH)
		a = math.cycle(0.001 * pygame.time.get_ticks() / tcycle + math.fuzz(3, *self.pH))
		hV = int(round(pview.f * view.VscaleG * math.mix(1, 1.2, a)))
		graphics.draw("goal", (xV, yV - hV), scale = scale, mask = mask)


class Light:
	def __init__(self, pH, dirHs):
		self.pH = pH
		self.dirHs = dirHs

	def illuminate(self):
		self.dlights = []
		for dxH, dyH in self.dirHs:
			dlight = 0
			xH, yH = self.pH
			while True:
				xH, yH = xH + dxH, yH + dyH
				dlight += 1
				if (xH, yH) not in state.grid0.cells:
					dlight -= 0.25
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
	


