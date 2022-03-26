import pygame, math
from . import pview, thing, geometry, graphics, sound
from .pview import T

class self:
	pass

def init():
	self.you = thing.You((3, 0))
	self.looker = thing.Looker((0, 3))
	room = thing.Room([(16, -9), (16, 9), (-16, 9), (-16, 0), (0, 0), (0, -9)])
	room.addmirror(0, 0.5, 4)
	room.addmirror(1, 0.5, 10)
	self.plates = [
		thing.Plate(0, (-5, 5), 2, 2.5),
	]
	self.room0 = room
	self.cmirror = None
	self.held = None
	self.lheld = False
	self.lwithin = False

def control(kdowns, dkx, dky):
	self.you.move(dkx, dky, self.room0)
	p = self.you.x, self.you.y
	self.cmirror = None
	self.lwithin = False
	if self.lheld:
		if "act" in kdowns:
			self.looker.x, self.looker.y = p
			self.lheld = False
			sound.play("put")
	elif self.held:
		if "act" in kdowns:
			spot, d = self.room0.spotwithin(p, self.held, 3)
			if spot is None:
				sound.play("cantput")
			else:
				self.room0.addmirror(*spot)
				self.held = None
				sound.play("put")
	elif math.distance(p, (self.looker.x, self.looker.y)) < 3:
		self.lwithin = True
		if "act" in kdowns:
			self.lheld = True
			sound.play("grab")
	else:
		self.cmirror = self.room0.mirrorwithin(p, 3)
		if "act" in kdowns:
			if self.cmirror is not None:
				self.held = self.room0.popmirror(self.cmirror)
				self.cmirror = None
				sound.play("grab")

def think(dt):
	p = self.you.x, self.you.y


def looktree(room, plook, objs, Aset = None, lastjwall = None, maxdepth = 3):
	if maxdepth <= 0:
		return
	for jwall in range(room.nwall()):
		if jwall == lastjwall:
			continue
		rAset = room.Asetthrough(plook, jwall, lastjwall)
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
	pview.screen.blit(graphics.backgroundimg(pview.size), (0, 0))
	graphics.timings.clear()
	plook = (self.looker.x, self.looker.y) if not self.lheld else (self.you.x, self.you.y)
	objs = [self.you] + self.plates
	for room, Aset, objs in looktree(self.room0, plook, objs):
		mask = graphics.Mask()
		room.draw(surf = mask.surf)
		for obj in objs:
			obj.draw(mask.surf)
#		youreflect = self.you.reflect(mirror)
#		youreflect.draw(mask.surf)
		mask.setmask(plook, Aset)
		mask.draw()
#		mirror.draw()
	mask = graphics.LookerMask()
	self.room0.draw(cmirror = self.cmirror, surf = mask.surf)
	for plate in self.plates:
		plate.draw(surf = mask.surf)
	if not self.lheld:
		self.looker.draw(surf = mask.surf)
	self.you.draw(surf = mask.surf)
	mask.setmask(plook, self.room0.poly)
	mask.draw()
#	print(graphics.timings)
	




