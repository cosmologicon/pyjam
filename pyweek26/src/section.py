# A section of the sewer

import math, pygame
from OpenGL.GL import *
from . import graphics

# A circular section without a current
# In this section the left and right arrow keys rotate you
class Pool():
	def __init__(self, pos, r):
		self.pos = pos
		self.r = r
		self.connections = []
		self.toturn = 0
	def move(self, you, dt, dx, dy, turn):
		if turn:
			you.heading += self.toturn
			self.toturn = math.tau / 2
		you.heading += 2 * dt * dx
		if self.toturn:
			toturn = math.softapproach(self.toturn, 0, 10 * dt, dymin = 0.01)
			you.heading += self.toturn - toturn
			self.toturn = toturn
		speed = 10 if dy > 0 else -3 if dy < 0 else 0
		v = pygame.math.Vector3(0, speed, 0).rotate_z(math.degrees(-you.heading))
		you.v = pygame.math.Vector3(math.approach(you.v, v, 50 * dt))

	def flow(self, dt, obj):
		# Very gentle flow toward the center
		v = (self.pos - obj.pos) / 10
		if v.length() > 1:
			v = v.normalize()
		obj.pos += dt * v
	def handoff(self, obj):
		d = (obj.pos - self.pos).length()
		if d > self.r - 1 and self.connections:
			path = min(self.connections, key = lambda c: c.dcenter(obj.pos))
			if path.dcenter(obj.pos) < 1:
				obj.section = path
				obj.upstream = self is path.pool1
				self.toturn = 0
	def draw(self):
		glPushMatrix()
		glColor4f(0, 0, 1, 0.3)
		glTranslate(*self.pos)
		glBegin(GL_POLYGON)
		for x, y in math.CSround(round(10 * self.r), r = self.r):
			glVertex(x, y, 0)
		glEnd()
		# Fixed barriers
		glColor4f(0.8, 0.8, 0.8, 1)
		for x, y in math.CSround(round(2 * self.r), r = self.r):
			glPushMatrix()
			glTranslate(x, y, 0)
			graphics.drawsphere(0.2)
			glPopMatrix()
		glPopMatrix()

class Connector():
	def __init__(self, pool0, pool1, rate = 10, width = 4):
		self.pool0 = pool0
		self.pool1 = pool1
		self.rate = rate
		self.width = width
		pool0.connections.append(self)
		pool1.connections.append(self)
		d = self.pool1.pos - self.pool0.pos
		self.face = d.normalize()
		self.length = d.length()
		self.angle = math.atan2(self.face.x, self.face.y)
	# Distance to the section center line, in units of the width.
	def dcenter(self, pos):
		p = pos - self.pool0.pos
		proj = p.dot(self.face) * self.face
		return (p - proj).length() / self.width
	def move(self, you, dt, dx, dy, turn):
		if turn:
			you.upstream = not you.upstream
		v = pygame.math.Vector3(5 * dx, 10 + 12 * dy, 0).rotate_z(math.degrees(-self.angle))
		if you.upstream:
			v *= -1
		you.v = pygame.math.Vector3(math.approach(you.v, v, 50 * dt))

		heading = self.angle + (math.tau / 2 if you.upstream else 0)
		you.heading = math.anglesoftapproach(you.heading, heading, 10 * dt, dymin = 0.01)

	def flow(self, dt, obj):
		v = self.face * self.rate
		obj.pos += dt * v
	def handoff(self, obj):
		for pool in (self.pool0, self.pool1):
			if (obj.pos - pool.pos).length() < pool.r - 2:
				obj.section = pool
	def draw(self):
		glPushMatrix()
		glColor4f(0, 0, 1, 0.3)
		glTranslate(*self.pool0.pos)
		glRotate(math.degrees(-self.angle), 0, 0, 1)
		glBegin(GL_QUADS)
		for dx, dy in [(-1, 0), (-1, 1), (1, 1), (1, 0)]:
			glVertex(dx * self.width, dy * self.length, 0)
		glEnd()
		glColor4f(0.8, 0.8, 0.8, 1)
		n = round(self.length / 4)
		for jball in range(n+1):
			y = jball / n * self.length
			if math.length([self.width, y]) < self.pool0.r:
				continue
			if math.length([self.width, self.length - y]) < self.pool1.r:
				continue
			for x in (-self.width, self.width):
				glPushMatrix()
				glTranslate(x, y, 0)
				graphics.drawsphere(0.3)
				glPopMatrix()
		glPopMatrix()

