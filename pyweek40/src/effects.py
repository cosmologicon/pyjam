import pygame, math
from . import view, ptext

class Info:
	def __init__(self, pP, text):
		self.pP = pP
		self.text = text
		self.t = 0
		self.T = 1
		self.f = 0
	
	def think(self, dt):
		self.t += dt
		self.f = self.t / self.T

	def draw(self):
		f = self.f ** 0.4
		pP = math.vtplus(self.pP, (0, 1), f)
		alpha = math.smoothinterp(f, 0.8, 1, 1, 0)
		ptext.draw(self.text, center = view.VconvertP(pP), fontsize = view.VscaleP(0.8),
			owidth = 1, alpha = alpha)


effects = []

def addinfoP(pP, text):
	effects.append(Info(pP, text))

def addinfoG(pG, text):
	addinfoP(view.PconvertG(pG), text)

def think(dt):
	for obj in effects:
		obj.think(dt)

def draw():
	for obj in effects:
		obj.draw()
	
