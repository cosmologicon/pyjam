import pygame, math
from . import view, pview, graphics
from .pview import T

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
			x, y = self.pos
			dy, dx = math.CS(self.A, 4)
			pV1 = view.VconvertG((x + dx, y + dy))
			rV = T(view.VscaleG * 0.03)
			pygame.draw.line(pview.screen, (255, 230, 200), pV, pV1, rV)
			
		

class Stander:
	def __init__(self, pos, r):
		self.pos = pos
		self.r = r

	def draw(self):
		pV = view.VconvertG(self.pos)
		rV = T(view.VscaleG * self.r)
		pygame.draw.circle(pview.screen, (0, 0, 0), pV, rV)

