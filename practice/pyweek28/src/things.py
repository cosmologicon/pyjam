import pygame, math, random, time
from . import view, pview, ptext, state
from .pview import T

def collide(obj0, obj1):
	return math.distance(obj0.p, obj1.p) < obj0.r + obj1.r


class Balloon:
	def __init__(self, p):
		self.p = p
		self.v = 0, 0
		self.r = 1
		self.hurt = 0
		self.color = [(255, 200, 100), (255, 0, 0)]

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
		if self.hurt == 1 and time.time() - self.hurt_time > .5:
			self.hurt = 0
		pygame.draw.circle(pview.screen, self.color[self.hurt], p, T(r))
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



class Meteor:
	def __init__(self, p, v):
		self.p = p
		self.v = v
		self.r = 0.4
		self.alive = True
		self.color = tuple(random.randint(0,255) for _ in range(3))

	def think(self, dt):
		x, y = self.p
		vx, vy = self.v
		x += dt * vx
		y += dt * vy
		self.p = x, y
		# TODO: play a sound effect on hurt or collect
		if collide(self, state.balloon):
			state.hurt()
			state.balloon.hurt = 1
			state.balloon.hurt_time = time.time()
			self.alive = False
		elif collide(self, state.castle):
			state.collect()
			self.alive = False
		w, h = pview.width0 / view.zoom, pview.height0 / view.zoom
		if y < view.y0 - 0.6 * h:
			self.alive = False

	def draw(self):
		p = view.worldtoscreen(self.p)
		r = self.r * view.zoom
		pygame.draw.circle(pview.screen, self.color, p, T(r))

def randommeteor():
	w, h = pview.width0 / view.zoom, pview.height0 / view.zoom
	x = view.x0 + 0.7 * w * random.uniform(-1, 1)
	y = view.y0 + 0.6 * h
	vx = random.uniform(-1, 1)
	vy = random.uniform(-5, -4)
	return Meteor((x, y), (vx, vy))
