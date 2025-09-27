import pygame, math, random
from . import view, ptext, pview
from .pview import T

class Info:
	def __init__(self, pP, text):
		self.pP = pP
		self.text = text
		self.t = 0
		self.T = 1
		self.f = 0
		self.alive = True
	
	def think(self, dt):
		self.t += dt
		self.f = math.clamp(self.t / self.T, 0, 1)
		self.alive = self.f < 1

	def draw(self):
		f = self.f ** 0.4
		pP = math.vtplus(self.pP, (0, 1), f)
		alpha = math.smoothinterp(f, 0.8, 1, 1, 0)
		ptext.draw(self.text, center = view.VconvertP(pP), fontsize = view.VscaleP(0.8),
			owidth = 1, alpha = alpha)

def gaussian2d(mu = (0, 0), sigma = 1):
	x, y = mu
	return random.gauss(x, sigma), random.gauss(y, sigma)

class Bubble:
	def __init__(self, pP, vP0 = 0.8):
		self.vP = gaussian2d(sigma = vP0)
		self.pP = math.vtplus(pP, self.vP, 0.2)
		self.t = 0
		self.T = random.uniform(0.5, 1)
		self.f = 0
		a = random.uniform(0, 1)
		self.rP = math.mix(0.04, 0.1, a)
		self.terminalvP = 0, math.mix(3, 1.5, a)
		self.alive = True
		
	def think(self, dt):
		self.t += dt
		self.f = self.t / self.T
		self.vP = math.approach(self.vP, self.terminalvP, 10 * dt)
		self.pP = math.vtplus(self.pP, self.vP, dt)
		self.alive = self.f < 1

	def draw(self):
		if not self.alive: return
		pV = view.VconvertP(self.pP)
		rV = view.VscaleP(self.rP)
		pygame.draw.circle(pview.screen, (80, 80, 120), pV, rV, T(1))

class Burst:
	def __init__(self, pP, size = 10):
		self.pP = pP
		self.size = size
		self.bubbles = [Bubble(pP) for _ in range(size)]

	def think(self, dt):
		for obj in self.bubbles:
			obj.think(dt)
		self.alive = any(obj.alive for obj in self.bubbles)
	
	def draw(self):
		for obj in self.bubbles:
			obj.draw()


effects = []

def addinfoP(pP, text):
	effects.append(Info(pP, text))

def addinfoG(pG, text):
	addinfoP(view.PconvertG(pG), text)

def addburstP(pP, size = 10):
	effects.append(Burst(pP, size))

def addburstG(pG, size = 10):
	addburstP(view.PconvertG(pG), size)

def addburstsegment(segment):
	for a in (0, 0.25, 0.5, 0.75, 1):
		addburstG(math.mix(segment.p, segment.parent.p, a), 10)

def addburststructure(structure):
	for p in structure.ps + [structure.pbase]:
		addburstG(p, 30)

def addbreathbubbleP(pP):
	effects.append(Bubble(pP, 0))

def think(dt):
	global effects
	for obj in effects:
		obj.think(dt)
	effects = [obj for obj in effects if obj.alive]

def draw():
	for obj in effects:
		obj.draw()
	
