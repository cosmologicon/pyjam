import pygame, math
from . import pview, ptext, control, settings, graphics, state, sound
from .pview import T

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

	def getactive(self):
		return True

	def draw(self):
		ocolor = settings.getcolor(self.symbol)
		if not self.selected:
			ocolor = math.imix(ocolor, (0, 0, 0), 0.6)
		color = math.imix(ocolor, (0, 0, 0), 0.6)
		pygame.draw.rect(pview.screen, color, pview.T(self.rectV), border_radius = T(5))
		pygame.draw.rect(pview.screen, ocolor, pview.T(self.rectV), border_radius = T(5), width = T(3))
		if self.ctype is None:
			graphics.drawsymbolatD(self.symbol, pview.T(self.rectV.center), pview.T(35),
				immediate = True)

	def within(self, pD):
		return pview.T(self.rectV).collidepoint(pD)

	def onhover(self, selfobj):
		selfobj.active = self

	def onclick(self, selfobj):
		self.selected = not self.selected
		selfobj.selected = self if self.selected else None
		control.click = False
		for box in selfobj.boxes:
			if box is not self:
				box.selected = False

class Button:
	def __init__(self, rectV):
		self.rectV = rectV
		self.borderV = 10
		self.fontsizeV = self.rectV.height * 0.6
		self.text = ""

	def gettext(self):
		return self.text

	def getactive(self):
		return True

	def draw(self):
		color0 = 60, 60, 120
		color1 = 128, 128, 255
		if not self.getactive():
			color0 = math.imix(color0, (0, 0, 0), 0.8)
			color1 = math.imix(color0, (0, 0, 0), 0.8)
		pygame.draw.rect(pview.screen, color0, T(self.rectV), border_radius = T(self.borderV))
		pygame.draw.rect(pview.screen, color1, T(self.rectV), border_radius = T(self.borderV),
			width = T(3))
		text = self.gettext()
		ptext.draw(text, center = T(self.rectV).center, fontsize = T(self.fontsizeV),
			fontname = "BebasNeue", color = color1, shade = 0.3, shadow = (0.3, 0.3))

	def within(self, pD):
		return pview.T(self.rectV).collidepoint(pD)

	def onhover(self, selfobj):
		pass

	def onclick(self, selfobj):
		pass

class OptionBox(Button):
	def __init__(self, rectV, optname, text):
		Button.__init__(self, rectV)
		self.optname = optname
		self.text = text
		self.opts = ["off", "dim", "on"]

	def gettext(self):
		return f"{self.text}: {self.getopt()}"

	def getopt(self):
		return getattr(settings, self.optname)

	def setopt(self, value):
		return setattr(settings, self.optname, value)

	def onclick(self, selfobj):
		self.setopt(state.cycle_opts(self.getopt(), self.opts))
		settings.save()

class ReverseButton(Button):
	def __init__(self, rectV):
		Button.__init__(self, rectV)
		self.text = "Reverse conduit"
	
	def getactive(self):
		return isinstance(control.selected, state.Tube)
	
	def onclick(self, selfobj):
		control.selected.flip()

class ToggleButton(Button):
	def __init__(self, rectV):
		Button.__init__(self, rectV)
		self.text = "Change resource"

	def getactive(self):
		return isinstance(control.selected, state.Tube)
	
	def onclick(self, selfobj):
		control.selected.togglecarry()

class TrashButton(Button):
	def __init__(self, rectV):
		Button.__init__(self, rectV)
		self.text = "Remove Conduit"
	
	def getactive(self):
		return isinstance(control.selected, state.Tube)
	
	def onclick(self, selfobj):
		state.removetube(control.selected)
		control.selected = None


def init():
	self.t = 0
	self.boxes = []
	if False:
		for jcol, ctype in enumerate([None, "import", "export", "tube"]):
			for jrow, symbol in enumerate([None] + list(settings.colors)):
				if ctype is None and symbol is None: continue
				rect = pygame.Rect(25 + 34 * jcol, 50 + 54 * jrow, 30, 50)
				box = FilterBox(rect, symbol, ctype)
				self.boxes.append(box)
	for jrow, symbol in enumerate(list(settings.colors)):
		rect = pygame.Rect(20, 60 + 54 * jrow, 80, 50)
		box = FilterBox(rect, symbol, None)
		self.boxes.append(box)
	texts = ["Met demand", "Claimed supply"]
	optnames = ["showdemand", "showsupply"]
	rectV = pygame.Rect(0, 0, 180, 40)
	rectV.center = 110, 480
	dy = 50
	self.boxes.append(ReverseButton(rectV))
	rectV = rectV.move(0, dy)
	self.boxes.append(ToggleButton(rectV))
	rectV = rectV.move(0, dy)
	self.boxes.append(TrashButton(rectV))
	rectV = rectV.move(0, dy)
	for text, optname in zip(texts, optnames):
		self.boxes.append(OptionBox(rectV, optname, text))
		rectV = rectV.move(0, dy)
	self.selected = None
	self.f = { None: 1 }
	self.lastsave = 0  # No idea why I'm tracking this here. It has to be somewhere.

def think(dt):
	self.t += dt
	self.active = self.selected
	for box in self.boxes:
		if box.within(control.posD):
			box.onhover(self)
			if control.click:
				if box.getactive():
					box.onclick(self)
					control.click = False
					sound.play("click")
				else:
					sound.play("no")
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
	if self.lastsave + settings.autosave_seconds < self.t:
		state.save()
		self.lastsave = self.t
	

# 0: disabled. 1: enabled.
def factor(symbol, ctype):
	return self.f.get((symbol, ctype), self.f[None])

def draw():
	ptext.draw("Hover or click to highlight", midtop = T(60, 10), width = T(100),
		fontname = "BebasNeue", fontsize = T(18),
		owidth = 1, shade = 1)
	for box in self.boxes:
		box.draw()

