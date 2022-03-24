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
	room.addmirror(2, 0.5, 10)
	room.addmirror(4, 0.7, 10)
	room.addmirror(5, 0.7, 10)
	self.room0 = room

def control(kdowns, dkx, dky):
	self.you.move(dkx, dky, self.room0)

def think(dt):
	pass

def looktree(room, plook, Aset = None, lastjwall = None, maxdepth = 3):
	if maxdepth <= 0:
		return
	for jwall in range(room.nwall()):
		if jwall == lastjwall:
			continue
		rAset = room.Asetthrough(plook, jwall)
		if Aset is not None:
			rAset = rAset.intersection(Aset)
		if rAset.empty():
			continue
		rroom = room.reflect(jwall)
		yield from looktree(rroom, plook, rAset, jwall, maxdepth - 1)
		yield rroom, rAset
		

def draw():
	pview.fill((20, 20, 60))
	graphics.timings.clear()
	plook = self.you.x, self.you.y
	for room, Aset in looktree(self.room0, plook):
		mask = graphics.Mask()
		room.draw(mask.surf)
#		youreflect = self.you.reflect(mirror)
#		youreflect.draw(mask.surf)
		mask.setmask(plook, Aset)
		mask.draw()
#		mirror.draw()
	self.room0.draw()
	self.you.draw()
#	print(graphics.timings)
	




