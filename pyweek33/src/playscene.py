import pygame
from . import pview, thing, geometry, graphics
from .pview import T

class self:
	pass

def init():
	self.you = thing.You((0, 0))
	room = thing.Room([(16, -9), (16, 0), (0, 9), (-16, 9), (-16, -0), (0, -9)])
	self.rooms = [room]
	self.mirrors = [
		thing.Mirror((16, 0), (16, -9)),
		thing.Mirror((16, 0), (0, 9)),
		thing.Mirror((-16, 9), (-16, 0)),
		thing.Mirror((0, -9), (16, -9)),
	]

def control(kdowns, dkx, dky):
	self.you.move(dkx, dky, self.rooms[0])

def think(dt):
	pass

def draw():
	pview.fill((20, 20, 60))
	p0 = self.you.x, self.you.y
	for mirror in self.mirrors:
		mask = graphics.Mask()
		for room in self.rooms:
			roomreflect = room.reflect(mirror)
			roomreflect.draw(mask.surf)
		youreflect = self.you.reflect(mirror)
		youreflect.draw(mask.surf)
		mask.setmask(self.you, mirror)
		mask.draw()
		mirror.draw()
	for room in self.rooms:
		room.draw()
	self.you.draw()
	




