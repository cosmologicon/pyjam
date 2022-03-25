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
#	room.addmirror(2, 0.5, 10)
#	room.addmirror(4, 0.7, 10)
#	room.addmirror(5, 0.7, 10)
	self.plates = [
		thing.Plate(0, (-5, 5), 2, 2.5),
	]
	self.room0 = room

def control(kdowns, dkx, dky):
	self.you.move(dkx, dky, self.room0)

def think(dt):
	pass

def looktree(room, plook, objs, Aset = None, lastjwall = None, maxdepth = 3):
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
		p1, p2 = room.getwall(jwall)
		robjs = [obj.reflect(p1, p2) for obj in objs]
		yield from looktree(rroom, plook, robjs, rAset, jwall, maxdepth - 1)
		yield rroom, rAset, robjs


def draw():
#	pview.fill((20, 20, 60))
	pview.screen.blit(graphics.backgroundimg(pview.size), (0, 0))
	graphics.timings.clear()
	plook = self.you.x, self.you.y
	objs = [self.you] + self.plates
	for room, Aset, objs in looktree(self.room0, plook, objs):
		mask = graphics.Mask()
		room.draw(mask.surf)
		for obj in objs:
			obj.draw(mask.surf)
#		youreflect = self.you.reflect(mirror)
#		youreflect.draw(mask.surf)
		mask.setmask(plook, Aset)
		mask.draw()
#		mirror.draw()
	self.room0.draw()
	for plate in self.plates:
		plate.draw()
	self.you.draw()
#	print(graphics.timings)
	




