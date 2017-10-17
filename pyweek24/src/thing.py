from __future__ import division
import pygame, math
from . import view, pview, enco, youstate, state
from .pview import T

class WorldBound(enco.Component):
	def __init__(self):
		self.x = 0
		self.y = 0
		self.z = 0
	def setstate(self, x, y, z, **args):
		self.x = x
		self.y = y
		self.z = z
	def screenpos(self):
		return view.toscreen(self.x, self.y, self.z)

class LinearSpan(enco.Component):
	def __init__(self):
		self.x1 = 0
		self.y1 = 0
	def setstate(self, x1, y1, **args):
		self.x1 = x1
		self.y1 = y1
		self.dx = self.x1 - self.x
		self.dy = self.y1 - self.y
		self.d = math.length((self.dx, self.dy))
		self.dhat = self.dhatx, self.dhaty = math.norm((self.dx, self.dy))
		self.scale = view.scale(self.z)
		self.d0 = self.d * self.scale
	# (a, b) in cross coordinates. 
	def crosspos(self, p0):
		x, y = p0
		x0, y0 = view.to0plane(self.x, self.y, self.z)
		cx, cy = x - x0, y - y0
		a = math.dot((cx, cy), self.dhat) / self.d0
		b = self.dhatx * cy - self.dhaty * cx
		return a, b

	def along(self, a):
		return self.x + self.dx * a, self.y + self.dy * a, self.z

	# Nearest position along this span in the 0 plane
	def pos0along(self, p0):
		f = self.fractionalong(p0)
		g = 1 - f
		return view.to0plane(g * self.x + f * self.x1, g * self.y + f * self.y1)


class DrawYou(enco.Component):
	def draw(self):
		px, py = self.screenpos()
		R = T(10)
		pygame.draw.circle(pview.screen, (255, 0, 255), (px, py - R), R, T(1))
		pygame.draw.circle(pview.screen, (255, 200, 255), (px, py), T(3), 0)

class DrawBoard(enco.Component):
	def draw(self):
		pos0 = view.toscreen(self.x, self.y, self.z)
		pos1 = view.toscreen(self.x1, self.y1, self.z)
		pygame.draw.line(pview.screen, (255, 255, 0), pos0, pos1, T(3 * view.scale(self.z)))

@WorldBound()
@DrawYou()
@youstate.YouStates()
class You(object):
	def __init__(self, **args):
		self.setstate(**args)

@WorldBound()
@LinearSpan()
@DrawBoard()
class Board(object):
	def __init__(self, **args):
		self.setstate(**args)
		self.name = "%f,%f,%f,%f,%f" % (self.x, self.y, self.x1, self.y1, self.z)
	def think(self, dt):
		pass

