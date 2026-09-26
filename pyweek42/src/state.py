import math
from . import graphics

you = None
hazards = []
spawners = []
salvos = []

room_rect = -8, -5, 16, 10

def room_bounds():
	x, y, w, h = room_rect
	return (x, x + w), (y, y + h)


def draw_room():
	x, y, w, h = room_rect
	graphics.drawrectG((x, y), (w, h), (0, 60, 60))

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
		self.charge = 0

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
def tfactor():
	if device.charging:
		return 1.3
	if device.discharging:
		return 0.7
	return 1
def youfactor():
	return 1 / tfactor() ** 2
def musicfactor():
	if device.charging:
		return 1.0
	if device.discharging:
		return 0.5
	return 0.7




