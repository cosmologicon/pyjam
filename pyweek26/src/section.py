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
	def move(self, you, dt, dx, dy, turn):
		you.heading += 2 * dt * dx
		speed = 10 if dy > 0 else -3 if dy < 0 else 0
		v = pygame.math.Vector3(0, speed, 0).rotate_z(math.degrees(-you.heading))
		you.v = pygame.math.Vector3(math.approach(you.v, v, 50 * dt))

	def flow(self, dt, obj):
		# Very gentle flow toward the center
		v = (self.pos - obj.pos) / 10
		if v.length() > 1:
			v = v.normalize()
		obj.pos += dt * v
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

"""
		if turn:
			self.upstream = not self.upstream
		vx = 5 * dx
		vy = 10 + 12 * dy
		if not self.upstream:
			vx *= -1
			vy *= -1
		self.v.x = math.approach(self.v.x, vx, 50 * dt)
		self.v.y = math.approach(self.v.y, vy, 50 * dt)
"""
