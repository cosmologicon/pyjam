import pygame
from . import enco

class WorldBound(enco.Component):
	def __init__(self):
		self.pos = pygame.math.Vector3(0, 0, 0)

class Faces(enco.Component):
	def __init__(self):
		self.face = pygame.math.Vector3(0, 1, 0)


@WorldBound()
@Faces()
class You():
	pass

