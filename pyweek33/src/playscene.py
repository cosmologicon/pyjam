import pygame, math
from . import pview, thing, geometry, graphics, sound, ptext
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
	self.caption = "This statue's eyes seem to gaze in all directions. What all does it see?"

	self.cmirror = None
	self.held = None
	self.lheld = False
	self.lwithin = False
	self.t = 0
	
	self.winning = False
	self.twin = 0


def control(kdowns, dkx, dky):
	self.you.move(dkx, dky, self.room0)
	p = self.you.x, self.you.y
	self.cmirror = None
	self.lwithin = False
	if self.winning:
		return
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
	self.t += dt
	if self.winning:
		self.twin += dt

def done():
	return self.twin >= 2


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
		robjs[0].setvisible(plook, rAset, rroom, jwall)
		yield from looktree(rroom, plook, robjs, rAset, jwall, maxdepth - 1)
		yield jwall, rroom, rAset, robjs


def tallyplates(you, plates):
	if not you.visible:
		return
	p = you.x, you.y
	for plate in plates:
		if math.distance(p, (plate.x, plate.y)) < plate.r:
			self.tally[plate.jplate] += 1


def draw():
	pview.screen.blit(graphics.backgroundimg(pview.size), (0, 0))
	a = math.fadebetween(self.t, 2, 0, 2.5, 1)
	ptext.draw(self.caption, center = T(200, 600), fontsize = T(32), width = T(320),
		shade = 1, owidth = 1, alpha = a)
	graphics.timings.clear()
	self.tally = { plate.jplate: 0 for plate in self.plates }
	plook = (self.looker.x, self.looker.y) if not self.lheld else (self.you.x, self.you.y)
	objs = [self.you] + self.plates
	for jwall, room, Aset, objs in looktree(self.room0, plook, objs):
		mask = graphics.Mask()
		room.draw(surf = mask.surf)
		ryou = objs.pop(0)
		for obj in objs:
			obj.draw(mask.surf)
		if ryou.visible:
			ryou.draw(mask.surf)
			tallyplates(ryou, objs)
#		youreflect = self.you.reflect(mirror)
#		youreflect.draw(mask.surf)
		mask.setmask(plook, Aset)
		mask.exclude(plook, room.poly, jwall)
		mask.draw()
#		mirror.draw()
	mask = graphics.LookerMask()
	self.room0.draw(cmirror = self.cmirror, surf = mask.surf)
	for plate in self.plates:
		plate.draw(surf = mask.surf)
	if not self.lheld:
		self.looker.draw(surf = mask.surf)
	self.you.setvisible(plook, None, self.room0, None)
	tallyplates(self.you, self.plates)
	for plate in self.plates:
		plate.tally = self.tally[plate.jplate]
		if not plate.done and plate.tally == plate.n:
			plate.done = True
			sound.play("done")
	self.you.draw(surf = mask.surf)
	mask.setmask(plook, self.room0.poly)
	mask.draw()
	if all(plate.done for plate in self.plates):
		self.winning = True
		sound.play("win")
	if self.twin > 0:
		a = math.imix(0, 255, math.fadebetween(self.twin, 1, 0, 1.5, 1))
		pview.fill((50, 50, 100, a))
#	print(graphics.timings)
	




