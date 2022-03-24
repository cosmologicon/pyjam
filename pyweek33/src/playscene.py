import pygame
from . import pview, thing, geometry, graphics
from .pview import T

class self:
	pass

def init():
	self.you = thing.You((0, 0))
	room = thing.Room([(16, -9), (16, 0), (0, 9), (-16, 9), (-16, -0), (0, -9)])
	room.addmirror(0, 0.5, 4)
	room.addmirror(1, 0.5, 10)
	self.room0 = room

def control(kdowns, dkx, dky):
	self.you.move(dkx, dky, self.room0)

def think(dt):
	pass

def draw():
	pview.fill((20, 20, 60))
	plook = self.you.x, self.you.y
	for jwall in range(self.room0.nwall()):
		Aset = self.room0.Asetthrough(plook, jwall)
		if Aset.empty():
			continue
		mask = graphics.Mask()
		room = self.room0.reflect(jwall)
		room.draw(mask.surf)
#		youreflect = self.you.reflect(mirror)
#		youreflect.draw(mask.surf)
		mask.setmask(plook, Aset)
		mask.draw()
#		mirror.draw()
	self.room0.draw()
	self.you.draw()
	




