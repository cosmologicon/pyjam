import pygame
from . import view, ptext, state, util
from .enco import Component
from .util import F

# Positive x is right
# Positive y is down

# positive rotational motion is clockwise
# angle of 0 is right
# angle of tau/4 is down

class WorldBound(Component):
	def setstate(self, **kw):
		if "x" in kw: self.x = kw["x"]
		if "y" in kw: self.y = kw["y"]

class MovesWithArrows(Component):
	def move(self, dx, dy):
		self.x += state.speed * dx
		self.y += state.speed * dy

class FollowsScroll(Component):
	def think(self, dt):
		self.x += state.scrollspeed * dt

class Collides(Component):
	def __init__(self, r):
		self.r = r

class ConstrainHorizontal(Component):
	def __init__(self, xmargin = 0):
		self.xmargin = xmargin
	def think(self, dt):
		dxmax = 427 / view.Z - self.r - self.xmargin
		self.x = util.clamp(self.x, view.x0 - dxmax, view.x0 + dxmax)

class DrawBox(Component):
	def __init__(self, boxname):
		self.boxname = boxname
	def draw(self):
		pos = view.screenpos((self.x, self.y))
		r = F(view.Z * self.r)
		pygame.draw.circle(view.screen, (120, 120, 120), pos, r)
		ptext.draw(self.boxname, center = pos, color = "white", fontsize = F(14))

@WorldBound()
@MovesWithArrows()
@FollowsScroll()
@Collides(10)
@ConstrainHorizontal(5)
@DrawBox("you")
class You(object):
	def __init__(self, **kw):
		self.setstate(**kw)


