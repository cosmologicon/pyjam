import pygame
from . import pview, thing
from .pview import T

class self:
	pass

def init():
	self.you = thing.You((0, 0))
	room = thing.Room([(16, -9), (16, 0), (0, 9), (-16, 9), (-16, -0), (0, -9)])
	mirror = thing.Mirror((16, 0), (0, 9))
	self.rooms = [room, room.reflect(mirror)]
	self.mirrors = [mirror]

def control(kdowns, dkx, dky):
	self.you.move(dkx, dky, self.rooms[0])

def think(dt):
	pass

def draw():
	pview.fill((20, 20, 60))
	for room in self.rooms:
		room.draw()
	for mirror in self.mirrors:
		mirror.draw()
		self.you.reflect(mirror).draw()
	self.you.draw()
	




