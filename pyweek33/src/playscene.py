import pygame, math
from . import pview, thing, geometry, graphics, sound, ptext, view, leveldata
from .pview import T

class self:
	pass

def init(level):
	self.level = level
	data = leveldata.data[self.level]
	
	view.camera.zoom = data["zoom"]
	self.you = thing.You(data["youpos"])
	self.looker = thing.Looker(data["lookpos"])
	self.room0 = thing.Room(data["roomps"])
	for jwall, f, w in data["mirrors"]:
		self.room0.addmirror(jwall, f, w)
	self.plates = []
	for jplate, (p, n) in enumerate(data["plates"]):
		self.plates.append(thing.Plate(jplate, p, n, 2.4))
	self.caption = data["caption"]
	self.tip = data["tip"]

	self.cmirror = None
	self.held = None
	self.lheld = False
	self.lwithin = False
	self.t = 0
	self.winning = False
	self.twin = 0
	self.ttip = 0
	self.stepping = False
	self.jplate = None


def control(kdowns, dkx, dky, ktip):
	self.you.move(dkx, dky, self.room0)
	p = self.you.x, self.you.y
	self.cmirror = None
	self.lwithin = False
	if ktip:
		self.ttip += ktip
	else:
		self.ttip = 0
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
			for plate in self.plates:
				plate.done = False
	else:
		self.cmirror = self.room0.mirrorwithin(p, 3)
		if "act" in kdowns:
			if self.cmirror is not None:
				self.held = self.room0.popmirror(self.cmirror)
				self.cmirror = None
				sound.play("grab")
				for plate in self.plates:
					plate.done = False
	self.jplate = None
	stepping = any(math.distance(p, (plate.x, plate.y)) < plate.r for plate in self.plates)
	if stepping != self.stepping:
		sound.play("stepon" if stepping else "stepoff")
		self.stepping = stepping
	if stepping and not self.lheld and not self.held:
		self.jplate, plate = [(jplate, plate) for jplate, plate in enumerate(self.plates)
			if math.distance(p, (plate.x, plate.y)) < plate.r][0]
		if "act" in kdowns and not plate.done:
			if plate.tally == plate.n:
				plate.done = True
				sound.play("done")
			else:
				sound.play("cantdone")


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
	view.camera.x0 = self.you.x
	view.camera.y0 = self.you.y
	pview.screen.blit(graphics.backgroundimg(pview.size), (0, 0))
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
	self.you.draw(surf = mask.surf)
	mask.setmask(plook, self.room0.poly)
	mask.draw()

	za = (1 - view.camera.zoomout) ** 2
	a = math.fadebetween(self.t, 2, 0, 2.5, 1) * za
	ptext.draw(self.caption, midbottom = T(240, 680), fontsize = T(26), width = T(400),
		fontname = "Fondamento", shade = 1, owidth = 1, alpha = a, lineheight = 0.86)
	text = f"Stage {self.level}" if self.level < 8 else "The End"
	ptext.draw(text, topleft = T(10, 10), fontsize = T(36),
		fontname = "Fondamento", shade = 1, owidth = 1, alpha = za)
	if self.ttip > 0:
		a = math.fadebetween(self.ttip, 0.5, 0, 1, 1) * za
		ptext.draw(self.tip, midtop = T(640, 10), fontsize = T(40), width = T(800),
			fontname = "PatuaOne", shade = 1, owidth = 1, alpha = a)
	text = []
	if self.level < 3:
		text.append("Arrow keys or WASD: move")
	if self.level < 4:
		text.append("Space: grab or drop")
	text.append("1: previous level")
	text.append("2: next level")
	text.append("Hold Shift: tip")
	text.append("Hold Ctrl: zoom out")
	text.append("Esc: quit")
	ptext.draw("\n".join(text), fontsize = T(26), owidth = 1, fontname = "PatuaOne",
		bottomright = T(1270, 710), alpha = za)

	instruction = None
	if self.lheld:
		instruction = "Space: place statue"
	elif self.held:
		instruction = "Space: place mirror"
	elif self.jplate is not None and not self.plates[self.jplate].done:
		instruction = "Space: activate plate"
	elif self.lwithin:
		instruction = "Space: take statue"
	elif self.cmirror is not None:
		instruction = "Space: take mirror"
	if instruction is not None:
		ptext.draw(instruction, fontsize = T(42), owidth = 1, fontname = "PatuaOne",
			shade = 1, color = (200, 200, 255), center = T(640, 620), alpha = za)

	if all(plate.done for plate in self.plates):
		self.winning = True
		sound.play("win")
	if self.twin > 0:
		a = math.imix(0, 255, math.fadebetween(self.twin, 1, 0, 1.5, 1))
		pview.fill((50, 50, 100, a))
#	print(graphics.timings)
	




