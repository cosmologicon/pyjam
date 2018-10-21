import pygame, math
from . import enco

class WorldBound(enco.Component):
	def __init__(self):
		self.pos = pygame.math.Vector3(0, 0, 0)

class Lives(enco.Component):
	def __init__(self):
		self.t = 0
	def think(self, dt):
		self.t += dt

class Faces(enco.Component):
	def __init__(self):
		self.face = pygame.math.Vector3(0, 1, 0)

class MovesWithArrows(enco.Component):
	def __init__(self):
		self.v = pygame.math.Vector3(0, 0, 0)
		self.Tswim = 0  # Animation timer for swimming
	def move(self, dt, dx, dy):
		self.v.x = math.approach(self.v.x, 5 * dx, 10)
		self.v.y = math.approach(self.v.y, 5 + 5 * dy, 10)
		self.pos += dt * self.v
		self.pos.x += 5 * dt * dx
		self.pos.y += 5 * dt * dy
	def think(self, dt):
		# Swim faster if you're going forward.
		f = math.smoothfadebetween(self.v.y, 0, 0.5, 10, 3)
		self.Tswim += dt * f

@WorldBound()
@Lives()
@Faces()
@MovesWithArrows()
class You():
	pass

