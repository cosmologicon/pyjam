from __future__ import division
import pygame, math
from . import view, pview, ptext
from .pview import T
from .enco import Component

class WorldBound(Component):
	def __init__(self, xG = 0, yG = 0, zG = 0):
		self.xG = xG
		self.yG = yG
		self.zG = zG
	def pG(self):
		return self.xG, self.yG, self.zG
	def pV(self):
		return view.VconvertG(self.pG())

class ArcMove(Component):
	def __init__(self, tmove = 0.25):
		self.tmove = tmove
		self.pGlast = None
		self.movet = 0
	def think(self, dt):
		if self.pGlast is None:
			self.pGlast = self.pG()
		if self.pGlast != self.pG():
			self.movet += dt
			if self.movet >= self.tmove:
				self.pGlast = self.pG()
				self.movet = 0
	def pdrawG(self):
		if self.pGlast == self.pG():
			return self.pG()
		f = math.clamp(self.movet / self.tmove, 0, 1)
		xG, yG, zG = math.mix(self.pGlast, self.pG(), f)
		zG += 0.8 * f * (1 - f)
		return xG, yG, zG
	def pdrawV(self):
		return view.VconvertG(self.pdrawG())

class DrawPiece(Component):
	def __init__(self, name = "", color = ""):
		self.name = name
		self.color = color
	def draw(self):
		xV, yV = self.pdrawV()
		S = view.S
		ps = [T(xV + S * a, yV + S * b) for a, b in
			[(0.25, 0), (-0.25, 0), (-0.15, -0.6), (0.15, -0.6)]]
		pygame.draw.polygon(pview.screen, pygame.Color(self.color), ps)
		pygame.draw.lines(pview.screen, pygame.Color("black"), True, ps, T(0.05 * S))
		ptext.draw(self.name, center = T(xV, yV - S * 0.25), fontsize = T(0.35 * S),
			color = "white", ocolor = "black", owidth = 1)

@WorldBound()
class Thing(object):
	def __init__(self, **kw):
		for k, v in kw.items():
			setattr(self, k, v)
	def __lt__(self, other):
		return view.sortkeyG(self.pG()) < view.sortkeyG(other.pG())

@ArcMove()
@DrawPiece()
class Piece(Thing):
	pass

