import pygame, math
from . import pview, control, settings, graphics

class self:
	pass

ctypes = ["import", "export", "tube"]

class FilterBox:
	def __init__(self, rectV, symbol, ctype):
		self.rectV = rectV
		self.symbol = symbol
		self.ctype = ctype
		self.selected = False
		self.keys = [(s, c)
			for s in (settings.colors if symbol is None else [symbol])
			for c in (ctypes if ctype is None else [ctype])
		]

	def draw(self):
		color = settings.colorcodes.get(self.symbol, (160, 160, 160))
		if not self.selected:
			color = math.imix(color, (0, 0, 0), 0.6)
		pygame.draw.rect(pview.screen, color, pview.T(self.rectV))
		if self.ctype is None:
			graphics.drawsymbolatD(self.symbol, pview.T(self.rectV.center), pview.T(50))

	def within(self, pD):
		return pview.T(self.rectV).collidepoint(pD)

def init():
	self.t = 0
	self.boxes = []
	for jcol, ctype in enumerate([None, "import", "export", "tube"]):
		for jrow, symbol in enumerate([None] + list(settings.colors)):
			if ctype is None and symbol is None: continue
			rect = pygame.Rect(20 + 34 * jcol, 20 + 54 * jrow, 30, 50)
			box = FilterBox(rect, symbol, ctype)
			self.boxes.append(box)
	self.selected = None
	self.f = { None: 1 }

def think(dt):
	self.t += dt
	self.active = self.selected
	for box in self.boxes:
		if box.within(control.posD):
			self.active = box
			if control.click:
				box.selected = not box.selected
				self.selected = box if box.selected else None
				control.click = False
	ftarget = 0 if self.active else 1
	if self.active:
		for key in self.active.keys:
			self.f[key] = self.f.get(key, self.f[None])
	df = 5 * dt
	self.f[None] = math.approach(self.f[None], ftarget, df)
	for key in list(self.f.keys()):
		if key is None: continue
		if self.active and key in self.active.keys:
			self.f[key] = math.approach(self.f[key], 1, df)
		else:
			self.f[key] = math.approach(self.f[key], ftarget, df)
			if self.f[key] == self.f[None]:
				del self.f[key]
	

# 0: disabled. 1: enabled.
def factor(symbol, ctype):
	return self.f.get((symbol, ctype), self.f[None])

def draw():
	for box in self.boxes:
		box.draw()

