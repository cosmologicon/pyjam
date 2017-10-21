# thing module - entity defintions.

from __future__ import division
import pygame, math, random
from . import view, pview, ptext, enco, youstate, state, hill, settings
from .pview import T

def vmix(x, y, a):
	return tuple(math.mix(p, q, a) for p, q in zip(x, y))

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
	# scrolled off the left of the screen. Override this function with the rightmost x-coordinate of
	# an object.
	def xmax(self):
		return self.x
	# Has it scrolled off the left of the screen?
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

	# a is the fraction along this object: a = 0 is left edge, a = 1 is right edge.
	def along(self, a):
		return self.x + self.dx * a, self.y + self.dy * a, self.z

	# Is this object blocked by a block at a greater z value?
	def blockedat(self, a):
		p0 = view.to0(*self.along(a))
		return state.blockedat0(p0, self.z)

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
		d = math.distance(p0, pyou)
		if d > R:
			return False
		fR = state.you.r * view.scale(state.you.r) / R
		phit0 = vmix(p0, pyou, fR)
		return not state.blockedat0(phit0, self.z)

class HillSpec(enco.Component):
	def setstate(self, spec, color0 = (180, 100, 40), grasscolor = (40, 100, 40), **args):
		self.spec = tuple(tuple(tuple(p) for p in layer) for layer in spec)
		xs, ys = zip(*[p for layer in self.spec for p in layer])
		self._xmax = max(xs) + 3
		self.color0 = tuple(int(random.uniform(0.1, 0.3) * a) for a in color0)
		self.color1 = tuple(int(random.uniform(0.7, 1) * a) for a in color0)
		self.grasscolor = grasscolor
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
		hill.drawhill((self.x, self.y, self.z), self.spec, color0 = self.color0, color1 = self.color1, grasscolor = self.grasscolor)

class DrawYou(enco.Component):
	def __init__(self):
		self.r = 1.5
	def setstate(self, r = 1.5, **args):
		self.r = r
	def draw(self):
		px, py = self.screenpos()
		R = view.screenscale(self.r, self.z)
		# The rest is now handled by the drawyou module.
	def center(self):
		return self.x, self.y + self.r, self.z

# DrawBoard not used in the game - hills are drawn separately now.
class DrawBoard(enco.Component):
	def draw(self):
		pos0 = view.toscreen(self.x, self.y, self.z)
		pos1 = view.toscreen(self.x1, self.y1, self.z)
		pygame.draw.line(pview.screen, (255, 255, 0), pos0, pos1, T(3 * view.scale(self.z)))

# DrawShield not used in the game - hills are drawn separately now.
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

class LivesOnscreen(enco.Component):
	def alive(self):
		return not self.gone()

class DrawText(enco.Component):
	def setstate(self, text, fontsize = 3, fontname = None, color = None, shadow = None, angle = 0, **args):
		self.text = text
		self.fontname = fontname
		self.fontsize = fontsize
		self.color = color
		self.shadow = shadow
		self.angle = angle
	def draw(self):
		p = view.toscreen(self.x, self.y, self.z)
		ptext.draw(self.text,
			center = view.toscreen(self.x, self.y, self.z),
			fontsize = view.screenscale(self.fontsize, self.z),
			fontname = self.fontname,
			lineheight = 0.8,
			color = self.color,
			shadow = self.shadow,
			angle = self.angle
		)
	def xmax(self):
		return self.x + 0.5 * self.fontsize * len(self.text)

class DrawArrow(enco.Component):
	def setstate(self, right = False, left = False, **args):
		self.right = right
		self.left = left
		self.angle = random.uniform(-15, 15)
	def draw(self):
		x0, y0 = self.screenpos()
		C, S = math.CS(math.radians(self.angle))
		# TODO: maff.R
		color = 140, 140, 180
		if self.right:
			dxys = [(1, 5), (6, 0), (1, -5)]
			dxys = [(C * dx + S * dy, -S * dx + C * dy) for dx, dy in dxys]
			ps = [view.toscreen(self.x + dx, self.y + dy, self.z) for dx, dy in dxys]
			pygame.draw.polygon(pview.screen, color, ps)
		if self.left:
			dxys = [(-1, 5), (-6, 0), (-1, -5)]
			dxys = [(C * dx + S * dy, -S * dx + C * dy) for dx, dy in dxys]
			ps = [view.toscreen(self.x + dx, self.y + dy, self.z) for dx, dy in dxys]
			pygame.draw.polygon(pview.screen, color, ps)
	def xmax(self):
		return self.x + 4


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
@LivesOnscreen()
class Sign(object):
	def __init__(self, **args):
		self.setstate(**args)
	def think(self, dt):
		pass

@WorldBound()
@DrawArrow()
@LivesOnscreen()
class Arrow(object):
	def __init__(self, **args):
		self.setstate(**args)
	def think(self, dt):
		pass

