from __future__ import division
import pygame, math, random
from . import view, pview, ptext, tile
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
	def pdrawG(self):
		return self.pG()
	def pdrawV(self):
		return view.VconvertG(self.pdrawG())

class Timered(Component):
	def __init__(self, t = 0):
		self.t = t
	def think(self, dt):
		self.t += dt

class TileBound(Component):
	def ptileG(self):
		from . import state
		tile = state.grid[(self.xG, self.yG)]
		xG, yG, zG = tile.pdrawG()
		return xG, yG, zG + self.zG
	def pdrawG(self):
		return self.ptileG()

class VerticalShift(Component):
	def __init__(self, zshiftG = 0):
		self.zshiftG = zshiftG
	def pshiftG(self):
		xG, yG, zG = self.pG()
		return xG, yG, zG + self.zshiftG
	def pdrawG(self):
		return self.pshiftG()

class Sway(Component):
	def __init__(self, Asway = 0.1, Tsway = 1):
		self.Asway = Asway
		self.Tsway = Tsway
		self.swayphase = -1
	def think(self, dt):
		if self.swayphase == -1:
			self.swayphase = random.random()
	def sway(self):
		return self.Asway * math.sin(math.tau * (self.t / self.Tsway + self.swayphase))

class FlyUp(Component):
	def __init__(self, tfly = 1):
		self.tfly = tfly
		self.flydelay = -1
	def think(self, dt):
		if self.flydelay == -1:
			self.flydelay = random.random() * 0.3
	def dzfly(self):
		f = math.clamp(self.t / self.tfly - self.flydelay, 0.0001, 1)
		return -1/f - f + 2

class Joltable(Component):
	def __init__(self):
		self.Ajolt = 0
		self.jdelay = 0
		self.tjolt = 0
	def jolt(self, jdelay):
		self.jdelay = jdelay
	def think(self, dt):
		if self.jdelay > 0:
			self.Ajolt = 0
			self.tjolt = 0
			self.jdelay -= dt
			if self.jdelay <= 0:
				self.jdelay = 0
				self.Ajolt = 40
				self.tjolt = 0
		else:
			self.tjolt += dt
			self.Ajolt = math.softapproach(self.Ajolt, 0, 10 * dt)
	def dzjolt(self, dz):
		dzj = self.Ajolt * math.sin(self.tjolt * 20)
		f = min(math.exp(-self.tjolt), 0.05 * self.tjolt)
		return math.mix(dz, dzj, f)
		

class TiledArcMove(Component):
	def __init__(self, tmove = 0.25):
		self.tmove = tmove
		self.pGlast = None
		self.ptileGlast = None
		self.movet = 0
	def think(self, dt):
		if self.pGlast is None:
			self.pGlast = self.pG()
			self.ptileGlast = self.ptileG()
		if self.pGlast != self.pG():
			self.movet += dt
			if self.movet >= self.tmove:
				self.pGlast = self.pG()
				self.movet = 0
		else:
			self.ptileGlast = self.ptileG()
	def pdrawG(self):
		if self.pGlast == self.pG():
			return self.ptileG()
		f = math.clamp(self.movet / self.tmove, 0, 1)
		xG, yG, zG = math.mix(self.ptileGlast, self.ptileG(), f)
		zG += 0.8 * f * (1 - f)
		return xG, yG, zG

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

class DrawPart(Component):
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

class DrawTile(Component):
	def __init__(self, name = "", color = ""):
		self.name = name
		self.color = color
	def draw(self):
		S = view.S
		pV = view.VconvertG(self.pshiftG())
		tile.draw(self.color, pV, 0.94 * S)


class DrawImpact(Component):
	def __init__(self, turn = None):
		self.turn = turn
	def turnsleft(self):
		from . import state
		return self.turn - state.turn()
	def draw(self):
		xG, yG, zG = self.pdrawG()
		pV0 = self.pdrawV()
		pV1 = view.VconvertG((xG, yG, zG + 1))
		color = 100, 0, 100
		pygame.draw.line(pview.screen, color, pV0, pV1, T(5))
		label = str(self.turnsleft())
		ptext.draw(label, center = pV1, color = "white", ocolor = color, owidth = 3, fontsize = T(40), shade = 2)

class Thing(object):
	def __init__(self, pG = None, **kw):
		for k, v in kw.items():
			setattr(self, k, v)
		if pG is not None:
			self.xG, self.yG, self.zG = view.ifzG(pG)
		self.think(0)
	def __lt__(self, other):
		return view.sortkeyG(self.pG()) < view.sortkeyG(other.pG())
	def think(self, dt):
		pass

@WorldBound()
@Timered()
@TileBound()
@TiledArcMove()
@DrawPiece()
class Piece(Thing):
	pass

@WorldBound()
@Timered()
@DrawPart()
@TileBound()
class Part(Thing):
	pass

@WorldBound()
@Timered()
@DrawImpact()
@TileBound()
class Impact(Thing):
	pass

@WorldBound()
@Timered()
@DrawTile()
@VerticalShift()
@Sway(0.03, 3)
@FlyUp(0.6)
@Joltable()
class Tile(Thing):
	def think(self, dt):
		Thing.think(self, dt)
		self.zshiftG = self.dzjolt(self.sway()) + self.dzfly()


