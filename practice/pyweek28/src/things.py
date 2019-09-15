import pygame, math
from . import view, pview, ptext, state
from .pview import T

class Balloon:
	def __init__(self, p):
		self.p = p
		self.v = 0, 0
		self.r = 1

	def move(self, dx, dy):
		# TODO: a small amount of acceleration/deceleration here rather than going right to full speed.
		self.v = state.speed * dx, state.speed * dy

	def think(self, dt):
		x, y = self.p
		vx, vy = self.v
		x += dt * vx
		y += dt * vy
		self.p = x, y

	def draw(self):
		p = view.worldtoscreen(self.p)
		r = self.r * view.zoom
		pygame.draw.circle(pview.screen, (255, 200, 100), p, T(r))
		ptext.draw("balloon", center = p, fontsize = T(18), owidth = 1)

class Castle:
	def __init__(self, p):
		self.p = p
		self.v = 0, 0
		self.r = 1

	def think(self, dt):
		x, y = self.p
		vx, vy = self.v
		x += dt * vx
		y += dt * vy
		self.p = x, y

		# Gravity
		vy -= 50 * dt
		# Friction
		f = math.exp(-1 * dt)
		vx *= f
		vy *= f
		def vecminus(v0, v1):
			return v0[0] - v1[0], v0[1] - v1[1]
		# Position of the castle relative to the balloon
		dx, dy = vecminus(self.p, state.balloon.p)
		d = math.length((dx, dy))
		if d > state.stringlength:
			# The castle gets pulled back by the string.
			# Model this as a highly inelastic collision in the reference frame of the balloon.
			rv = vecminus(self.v, state.balloon.v)
			# Velocity projected onto the offset is the radial component of the velocity.
			proj = math.dot(rv, (dx, dy)) / d
			pvx, pvy = math.norm((dx, dy), proj)
			if proj > 0:
				# 1 = completely inelastic, 2 = completely elastic
				f = 1.2
				vx -= f * pvx
				vy -= f * pvy
			# Constrain position to be within the radius.
			self.p = math.mix(state.balloon.p, self.p, state.stringlength / d)
		self.v = vx, vy

	def draw(self):
		p = view.worldtoscreen(self.p)
		s = T(2 * self.r * view.zoom)
		rect = pygame.Rect(0, 0, s, s)
		rect.center = p
		pygame.draw.rect(pview.screen, (100, 100, 100), rect)
		ptext.draw("castle", center = p, fontsize = T(18), owidth = 1)

