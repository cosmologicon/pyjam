from __future__ import division
import pygame, math, random
from . import view, ptext, state, util
from . import scene, visitscene
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

class Lives(Component):
	def __init__(self):
		self.alive = True
		self.t = 0
	def setstate(self, **kw):
		if "alive" in kw: self.alive = kw["alive"]
		if "t" in kw: self.t = kw["t"]
	def think(self, dt):
		self.t += dt
	def die(self):
		self.alive = False

class LinearMotion(Component):
	def __init__(self):
		self.vx = 0
		self.vy = 0
	def setstate(self, **kw):
		if "vx" in kw: self.vx = kw["vx"]
		if "vy" in kw: self.vy = kw["vy"]
	def think(self, dt):
		self.x += dt * self.vx
		self.y += dt * self.vy

class MovesWithArrows(Component):
	def move(self, dx, dy):
		self.x += state.speed * dx
		self.y += state.speed * dy

class YouBound(Component):
	def __init__(self, omega, R):
		self.omega = omega
		self.R = R
	def think(self, dt):
		theta = self.omega * self.t
		self.x = state.you.x + self.R * math.cos(theta)
		self.y = state.you.y + self.R * math.sin(theta)

class FollowsScroll(Component):
	def think(self, dt):
		self.x += state.scrollspeed * dt

class Collides(Component):
	def __init__(self, r):
		self.r = r

class ConstrainToScreen(Component):
	def __init__(self, xmargin = 0, ymargin = 0):
		self.xmargin = xmargin
		self.ymargin = ymargin
	def think(self, dt):
		dxmax = 427 / view.Z - self.r - self.xmargin
		self.x = util.clamp(self.x, view.x0 - dxmax, view.x0 + dxmax)
		dymax = state.yrange - self.r - self.ymargin
		self.y = util.clamp(self.y, -dymax, dymax)

class DisappearsOffscreen(Component):
	def think(self, dt):
		vx = self.vx - state.scrollspeed
		x = self.x - view.x0
		xmax = 427 / view.Z + self.r + 10
		ymax = state.yrange + 10
		if x * vx > 0 and abs(x) > xmax:
			self.die()
		if self.y * self.vy > 0 and abs(self.y) > ymax:
			self.die()

class RoundhouseBullets(Component):
	def __init__(self):
		self.tbullet = 0
		self.dtbullet = 0.3
		self.nbullet = 20
		self.vbullet = 50
		self.jbullet = 0
	def think(self, dt):
		self.tbullet += dt
		while self.tbullet >= self.dtbullet:
			for jtheta in range(3):
				theta = (self.jbullet / self.nbullet + jtheta / 3) * math.tau
				dx, dy = math.cos(theta), math.sin(theta)
				r = self.r + 2
				bullet = BadBullet(
					x = self.x + r * dx,
					y = self.y + r * dy,
					vx = self.vx + self.vbullet * dx,
					vy = self.vy + self.vbullet * dy
				)
				state.badbullets.append(bullet)
			self.tbullet -= self.dtbullet
			self.jbullet += 1

class Visitable(Component):
	def setstate(self, **kw):
		if "name" in kw: self.name = kw["name"]
	def visit(self):
		if self.name in state.visited:
			return
		state.visited.add(self.name)
		scene.push(visitscene, self.name)
	def draw(self):
		if self.name in state.visited:
			return
		if self.t % 2 > 1.5:
			return
		pos = view.screenpos((self.x + self.r, self.y - self.r))
		ptext.draw("HELP!", center = pos, fontsize = F(30))

class DiesOnCollision(Component):
	def hit(self, target = None):
		self.die()

class HurtsOnCollision(Component):
	def __init__(self, damage = 1):
		self.damage = damage
	def setstate(self, **kw):
		if "damage" in kw: self.damage = kw["damage"]
	def hit(self, target = None):
		if target is not None:
			target.hurt(self.damage)

class DrawBox(Component):
	def __init__(self, boxname):
		self.boxname = boxname
	def draw(self):
		pos = view.screenpos((self.x, self.y))
		r = F(view.Z * self.r)
		pygame.draw.circle(view.screen, (120, 120, 120), pos, r)
		ptext.draw(self.boxname, center = pos, color = "white", fontsize = F(14))

class DrawFlash(Component):
	def __init__(self):
		self.dtflash = random.random()
	def draw(self):
		pos = view.screenpos((self.x, self.y))
		r = F(view.Z * self.r)
		color = (255, 120, 120) if (self.t + self.dtflash) * 5 % 1 > 0.5 else (255, 255, 0)
		pygame.draw.circle(view.screen, color, pos, r)

@WorldBound()
@Lives()
@MovesWithArrows()
@FollowsScroll()
@Collides(10)
@ConstrainToScreen(5, 5)
@DrawBox("you")
class You(object):
	def __init__(self, **kw):
		self.setstate(**kw)
	def hurt(self, damage):
		state.takedamage(damage)

@WorldBound()
@YouBound(5, 25)
@Lives()
@Collides(4)
@DrawBox("zap")
class Companion(object):
	def __init__(self, **kw):
		self.setstate(**kw)
	def hurt(self, damage):
		pass

@WorldBound()
@Lives()
@Collides(60)
@DrawBox("planet")
@Visitable()
class Planet(object):
	def __init__(self, **kw):
		self.setstate(**kw)
	def hurt(self, damage):
		pass

@WorldBound()
@Lives()
@Collides(3)
@LinearMotion()
@DiesOnCollision()
@HurtsOnCollision()
@DisappearsOffscreen()
@DrawFlash()
class BadBullet(object):
	def __init__(self, **kw):
		self.setstate(**kw)

@WorldBound()
@Lives()
@Collides(20)
@RoundhouseBullets()
@LinearMotion()
@DisappearsOffscreen()
@DrawBox("medusa")
class Medusa(object):
	def __init__(self, **kw):
		self.setstate(**kw)



