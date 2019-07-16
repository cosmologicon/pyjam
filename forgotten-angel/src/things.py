from __future__ import division
import math, random, pygame
import vista, img, settings, weapon, state, effects

class Planet(object):
	radius = 2
	imgname = "planet-0"
	burns = False
	showsup = True

	def __init__(self, pos):
		self.x, self.y = pos
		self.angle = 0
		self.surveyed = False
		self.tsurvey = 0
		self.value = random.choice([10, 10, 10, 15, 15, 20])
		self.imgname = "planet-%d" % random.choice((0,1,2,3))

	def think(self, dt):
		pass

	def nearyou(self):
		dx, dy = self.x - state.state.you.x, self.y - state.state.you.y
		return math.sqrt(dx ** 2 + dy ** 2) < 0.7 * self.radius

	def draw(self):
		if not vista.isvisible((self.x, self.y), self.radius):
			return
		img.worlddraw(self.imgname, (self.x, self.y), angle = self.angle, scale = 1)


class Sun(object):
	radius = 8
	burns = True
	showsup = True

	def __init__(self, pos):
		self.x, self.y = pos
		self.surveyed = False
		self.collapsed = False
		self.tsurvey = 0
		self.value = 50

	def think(self, dt):
		pass

	def nearyou(self):
		dx, dy = self.x - state.state.you.x, self.y - state.state.you.y
		return math.sqrt(dx ** 2 + dy ** 2) < 0.7 * self.radius

	def draw(self):
		if not vista.isvisible((self.x, self.y), self.radius):
			return
		imgname = ("antisun-%s" if self.collapsed else "sun-%s") % self.radius
		img.worlddraw(imgname, (self.x, self.y), scale = 1)

