import math
from . import graphics, stage

current_stage = 1
tstage = 0
you = None
hazards = []
spawners = []
salvos = []
won = False
health = 3

def load_stage():
	global tstage
	tstage = 0
	del hazards[:]
	del spawners[:]
	del salvos[:]
	from . import thing
	for t, stype in stage.stages[current_stage]["salvos"]:
		flipH, flipV = False, False
		if stype.startswith("H"):
			flipH = True
			stype = stype[1:]
		if stype.startswith("V"):
			flipV = True
			stype = stype[1:]
		sclass = {
			"top5": thing.TopSalvo5,
			"x": thing.XSalvo,
			"sweepr": thing.SweepSalvoR,
			"sweepd": thing.SweepSalvoD,
			"rlr": thing.SalvoRLR,
			"mega": thing.MegaSalvo,
			"z": thing.SalvoZ,
			"edges": thing.SalvoEdges,
		}[stype]
		salvos.append(sclass(t, flipH, flipV))
	print(salvos)

def advance():
	global current_stage, tstage, won, health
	current_stage += 1
	health = math.approach(health, 3, 1)
	if current_stage in stage.stages:
		load_stage()
	else:
		won = True

def think(dt):
	global tstage
	tstage += dt
	if tstage >= stage.stages[current_stage]["t"]:
		advance()
		
def hurt():
	global health
	health -= 1

room_rect = -8, -5, 16, 10


def room_bounds():
	x, y, w, h = room_rect
	return (x, x + w), (y, y + h)


def draw_room():
	x, y, w, h = room_rect
	graphics.drawrectG((x, y), (w, h), (10, 30, 30), fill = True)

def constrain_to_room(pos, r = 0):
	x, y = pos
	(x0, x1), (y0, y1) = room_bounds()
	return math.clamp(x, x0 + r, x1 - r), math.clamp(y, y0 + r, y1 - r)


class Device:
	tcharge = 3
	tdischarge = 2
	def __init__(self):
		self.charging = False
		self.discharging = False
		self.charge = 1

	def can_activate(self):
		return not self.charging and not self.discharging

	def activate(self):
		if not self.can_activate(): return False
		if self.charge == 0:
			self.charging = True
		else:
			self.discharging = True

	def think(self, dt):
		if self.charging:
			self.charge = math.approach(self.charge, 1, dt / self.tcharge)
			if self.charge == 1:
				self.charging = False
		if self.discharging:
			self.charge = math.approach(self.charge, 0, dt / self.tdischarge)
			if self.charge == 0:
				self.discharging = False
device = Device()

def activate():
	device.activate()
def deactivate():
	device.charge = 0
	device.charging = False
	device.discharging = False
def tfactor():
	if device.charging:
		return 1
	if device.discharging:
		return 0.4
	return 0.7
def youfactor():
	if device.charging:
		return 0.8
	if device.discharging:
		return 1.6
	return 1.2
def musicfactor():
	if device.charging:
		return 1.0
	if device.discharging:
		return 0.5
	return 0.7




