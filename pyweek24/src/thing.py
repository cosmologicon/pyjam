from __future__ import division
import pygame, math, random
from . import view, pview, ptext, enco, youstate, state, hill, settings
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
	# For objects that don't change x position or z, they're considered gone once they've completely
	# scrolled off the left of the screen.
	def xmax(self):
		return self.x
	def gone(self):
		x, y = view.toscreen(self.xmax(), 0, self.z)
		return x < -1

class Timer(enco.Component):
	def __init__(self):
		self.t = 0
	def setstate(self, t = 0, **args):
		self.t = t
	def think(self, dt):
		self.t += dt

class LinearMotion(enco.Component):
	def __init__(self):
		self.vx = 0
		self.vy = 0
	def setstate(self, vx, vy, **args):
		self.vx = vx
		self.vy = vy
	def think(self, dt):
		self.x += dt * self.vx
		self.y += dt * self.vy
	def recalibratemotion(self, X0, **args):
		# Reinterpret self.x and self.y and adjust accordingly.
		# Let the current (self.x, self.y) be the 0-plane position of self when view.X0 = X0.
		# Should probably only be called once on initialization.
		dt = (X0 - view.X0) / settings.speed - self.t
		x, y = view.from0planeatP0(self.x, self.y, self.z, (X0, 0))
		self.x = x - dt * self.vx
		self.y = y - dt * self.vy

class LinearSpan(enco.Component):
	def __init__(self):
		self.x1 = 0
		self.y1 = 0
	def setstate(self, x1, y1, **args):
		self.x1 = x1
		self.y1 = y1
		self.dx = self.x1 - self.x
		self.dy = self.y1 - self.y
		self.slope = self.dy / self.dx
		self.d = math.length((self.dx, self.dy))
		self.dhat = self.dhatx, self.dhaty = math.norm((self.dx, self.dy))
		self.scale = view.scale(self.z)
		self.d0 = self.d * self.scale
	def xmax(self):
		return self.x1

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

	def blockedat(self, a):
		p0 = view.to0(*self.along(a))
		return any(block.z > self.z and block.contains0(p0) for block in state.blocks)

	# Nearest position along this span in the 0 plane
	def pos0along(self, p0):
		f = self.fractionalong(p0)
		g = 1 - f
		return view.to0plane(g * self.x + f * self.x1, g * self.y + f * self.y1)

	# Any boards that begin exactly where this one ends (including in the same z-plane)
	# None if there is no such board.
	def handoff(self):
		return state.blefts.get((self.x1, self.y1, self.z))

class Polygonal(enco.Component):
	def __init__(self):
		self.ps = []
	def setstate(self, ps, **args):
		self.ps = ps
		n = len(self.ps)
		self.segments = [(self.ps[j], self.ps[(j + 1) % n]) for j in range(n)]
		xs, ys = zip(*ps)
		self._xmax = max(xs)
	def xmax(self):
		return self._xmax + self.x
	# Ray casting algorithm for point in polygon
	def contains0(self, p0):
		x0, y0 = p0
		x, y = view.from0(x0, y0, self.z)
		x -= self.x
		y -= self.y
		ncross = 0
		for (x0, y0), (x1, y1) in self.segments:
			dx0, dy0 = x0 - x, y0 - y
			dx1, dy1 = x1 - x, y1 - y
			if (dy0 >= 0) == (dy1 >= 0):
				continue
			xcross = (dx1 * dy0 - dx0 * dy1) / (dy0 - dy1)
			ncross += xcross < 0
		return ncross % 2 == 1

class RoundHitBox(enco.Component):
	def __init__(self):
		self.r = 10
	def setstate(self, r, **args):
		self.r = r
	def xmax(self):
		return self.x + 2 * self.r
	def hitsyou(self):
		R = self.r * view.scale(self.z) + state.you.r * view.scale(state.you.z)
		p0 = view.to0(self.x, self.y, self.z)
		pyou = view.to0(*state.you.center())
		return math.distance(p0, pyou) <= R
	

class HillSpec(enco.Component):
	def setstate(self, spec, **args):
		self.spec = tuple(tuple(tuple(p) for p in layer) for layer in spec)
		xs, ys = zip(*[p for layer in self.spec for p in layer])
		self._xmax = max(xs) + 3
		self.color0 = (random.uniform(30, 50), random.uniform(20, 40), random.uniform(0, 20))
		self.color1 = (random.uniform(100, 180), random.uniform(50, 100), random.uniform(0, 50))
	def xmax(self):
		return self._xmax + self.x
	def hilltopend(self):
		x, y = self.spec[0][-1]
		return self.x + x, self.y + y
	def boards(self):
		layer = self.spec[0]
		n = len(layer)
		if n == 1:
			return
		for j in range(n-1):
			x, y = layer[j]
			x1, y1 = layer[j+1]
			yield Board(
				x = x + self.x, y = y + self.y,
				x1 = x1 + self.x, y1 = y1 + self.y,
				z = self.z)
	def block(self):
		midlayers = self.spec[1:-1]
		ps = (list(self.spec[0]) + [layer[-1] for layer in midlayers] +
			list(reversed(self.spec[-1])) + [layer[0] for layer in reversed(midlayers)])
		return Block(x = self.x, y = self.y, ps = ps, z = self.z)
	def draw(self):
		hill.drawhill((self.x, self.y, self.z), self.spec, color0 = self.color0, color1 = self.color1)

class DrawYou(enco.Component):
	def __init__(self):
		self.r = 1.5
	def setstate(self, r = 1.5, **args):
		self.r = r
	def draw(self):
		px, py = self.screenpos()
		R = view.screenscale(self.r, self.z)
		pygame.draw.circle(pview.screen, (255, 0, 255), (px, py - R), R, T(1))
		pygame.draw.circle(pview.screen, (255, 200, 255), (px, py), T(3), 0)
	def center(self):
		return self.x, self.y + self.r, self.z

class DrawBoard(enco.Component):
	def draw(self):
		pos0 = view.toscreen(self.x, self.y, self.z)
		pos1 = view.toscreen(self.x1, self.y1, self.z)
		pygame.draw.line(pview.screen, (255, 255, 0), pos0, pos1, T(3 * view.scale(self.z)))

class DrawShield(enco.Component):
	def setstate(self, scolor = None, **args):
		self.scolor = scolor
		if self.scolor is None:
			self.scolor = [random.randint(100, 200) for _ in "rgb"]
	def draw(self):
		ps = [view.toscreen(self.x + dx, self.y + dy, self.z) for dx, dy in self.ps]
		pygame.draw.polygon(pview.screen, self.scolor, ps)

def colormix(x, y, a):
	return tuple(int(math.clamp(math.mix(p, q, a), 0, 255)) for p, q in zip(x, y))

class RoundFlashing(enco.Component):
	def draw(self):
		color = colormix((255, 200, 0), (180, 90, 0), math.sin(2 * self.t * math.tau) ** 2)
		r = view.screenscale(self.r, self.z)
		pygame.draw.circle(pview.screen, color, self.screenpos(), r)

class DrawText(enco.Component):
	def setstate(self, text, fontsize = 3, color = None, ocolor = None, owidth = 0, angle = 0, **args):
		self.text = text
		self.fontsize = fontsize
		self.color = color
		self.ocolor = ocolor
		self.owidth = owidth
		self.angle = angle
	def draw(self):
		p = view.toscreen(self.x, self.y, self.z)
		ptext.draw(self.text,
			center = view.toscreen(self.x, self.y, self.z),
			fontsize = view.screenscale(self.fontsize, self.z),
			color = self.color,
			ocolor = self.ocolor,
			owidth = self.owidth,
			angle = self.angle
		)
	def xmax(self):
		return self.x + 0.5 * self.fontsize * len(self.text)
	def alive(self):
		return not self.gone()
		

@WorldBound()
@Timer()
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
		self.name = (self.x, self.y, self.x1, self.y1, self.z)
	def think(self, dt):
		pass

@WorldBound()
@Polygonal()
@DrawShield()
class Block(object):
	def __init__(self, **args):
		self.setstate(**args)
	def think(self, dt):
		pass

@WorldBound()
@HillSpec()
class Hill(object):
	def __init__(self, **args):
		self.setstate(**args)
	def think(self, dt):
		pass

@WorldBound()
@Timer()
@LinearMotion()
@RoundHitBox()
@RoundFlashing()
class Hazard(object):
	def __init__(self, **args):
		self.setstate(**args)
		self.recalibratemotion(**args)

@WorldBound()
@DrawText()
class Sign(object):
	def __init__(self, **args):
		self.setstate(**args)
	def think(self, dt):
		pass

