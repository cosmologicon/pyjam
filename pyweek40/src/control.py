import pygame, math
from . import pview
from . import settings, view, grid, state, effects, ptext, graphics
from .pview import T

class Button:
	def __init__(self, text, boxS, active = False):
		self.boxS = boxS
		self.text = text
		self.active = active
		self.selected = False

	def withinV(self, pV):
		return view.VconvertS(self.boxS).collidepoint(pV)

	def afford(self):
		return state.getcost(self.text)
	
	def draw(self):
		if not self.active:
			return
		boxV = view.VconvertS(self.boxS)
		color = (60, 60, 60)
		if self.selected:
			color = math.imix(color, (255, 255, 255), 0.5)
		if not self.afford():
			color = math.imix(color, (0, 0, 0), 0.5)
		pygame.draw.rect(pview.screen, color, boxV)
		ptext.draw(self.text, fontsize = T(40), center = boxV.center, owidth = 1)


class GrowButton(Button):
	def __init__(self, boxS):
		Button.__init__(self, "pop: 0", boxS, active = True)

	def afford(self):
		return state.cangrow()

	def draw(self):
		self.text = f"pop: {state.getpop()}"
		Button.draw(self)

selectorsegments = {
	"residence1": ((-3, 0), (-3, 1)),
	"residence2": ((-6, 0), (-6, 1)),
	"residence3": ((-10, 0), (-10, 1)),
	"vending1": ((3, 0), (4, 1)),
	"vending2": ((6, 0), (7, 1)),
	"vending3": ((10, 0), (11, 1)),
}

class Selector:
	def __init__(self, stype):
		self.stype = stype
		self.segment = selectorsegments[stype]
		p0, p1 = self.segment
		node0 = grid.Node(p0)
		self.parent = grid.Node(p1, node0)
		self.structure = grid.stypes[stype](self.parent)
		self.structure.place(inert = True)
		self.selected = False
	
	def draw(self):
		graphics.drawsegment(*self.segment)
		self.structure.draw(glow = self.selected)

	def withinG(self, pG):
		return pG == self.structure.pbase or pG in self.structure.ps

class Control:
	def __init__(self):
		self.playing = True
		self.clock = pygame.time.Clock()
		self.dts = []
#		self.t0 = 0.001 * pygame.time.get_ticks()
		self.tool = None
		pygame.mouse.get_rel()
		self.Gcursor = (0, 0)
		self.Gsegment = (0, 0), (0, 1)
		self.selectors = [
			Selector("residence1"),
			Selector("vending1"),
			Selector("residence2"),
			Selector("vending2"),
			Selector("residence3"),
			Selector("vending3"),
		]

	def tick(self):
		dt = min(0.001 * self.clock.tick(settings.maxfps), 1 / settings.minfps)
		self.mposV = pygame.mouse.get_pos()
		self.mposP = view.PconvertV(self.mposV)
		self.Gcursor = view.GnearestP(self.mposP)
		self.Gsegment = view.GnearestsegmentP(self.mposP)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.playing = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				self.playing = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_F10:
				pview.cycle_heights(settings.heights)
			if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
				pview.toggle_fullscreen()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_F12:
				pview.screenshot()
			if event.type == pygame.MOUSEWHEEL:
				view.zoom(event.y, self.mposP)
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				self.onclick()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
				state.grow()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
				self.tool = "remove"
			if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
				self.tool = None
			if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
				self.tool = "residence1"
			if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
				self.tool = "vending1"
				
		button0, button1, button2 = pygame.mouse.get_pressed(3)
		dxV, dyV = pygame.mouse.get_rel()
		if button2:
			view.scootV((dxV, dyV))
		self.dts.append(dt)

	def onclick(self):
		for button in buttons:
			if button.active and button.withinV(self.mposV):
				self.clickbutton(button)
				return
		for selector in self.selectors:
			if selector.withinG(self.Gcursor):
				self.clickselector(selector)
				return
		segment = self.Gsegment
		p0, p1 = segment
		if self.tool is None:
			if state.canspend("segment") and grid.canaddsegment(segment):
				obj = grid.addsegment(segment)
				state.spend("segment")
				effects.addburstsegment(obj)
		if self.tool == "remove":
			grid.removeat(self.Gcursor)
		if self.tool in ["office", "spire", "residence1", "vending1"]:
			if state.canspend(self.tool) and grid.canaddstructure(self.tool, self.Gcursor):
				obj = grid.addstructure(self.tool, self.Gcursor)
				effects.addburststructure(obj)
				state.spend(self.tool)
				self.tool = None
				for button in buttons:
					button.selected = False
				for selector in self.selectors:
					selector.selected = False

	def clickbutton(self, button):
		if button.selected:
			for button in buttons:
				button.selected = False
			self.tool = None
		else:
			for button in buttons:
				button.selected = False
			button.selected = True
			self.tool = button.text

	def clickselector(self, selector):
		isselected = selector.selected
		for obj in self.selectors:
			obj.selected = False
		self.tool = None
		if not isselected:
			selector.selected = True
			self.tool = selector.stype

	def drawcursor(self):
		if self.tool is None:
#			parent = grid.canextend(self.Gcursor)
#			print(self.Gcursor, parent)
			if grid.canaddsegment(self.Gsegment):
				shade = (255, 255, 255, 140) if grid.canaddsegment(self.Gsegment) else (255, 50, 50, 140)
				graphics.drawsegment(*self.Gsegment, shade = shade)
		elif self.tool == "remove":
			pass
		elif self.tool.startswith("residence") or self.tool.startswith("vending"):
			parent = grid.canextend(self.Gcursor)
			if parent:
				obj = grid.structurefrom(self.tool, parent)
				shade = (255, 255, 255, 140) if grid.canaddstructure(self.tool, self.Gcursor) else (255, 50, 50, 140)
				obj.draw(shade = shade)

def init():
	global control, buttons
	control = Control()
	buttons = [
#		Button("residence1", pygame.Rect(500, 600, 100, 100), True),
#		Button("vending1", pygame.Rect(800, 600, 100, 100), True),
#		GrowButton(pygame.Rect(100, 600, 100, 100)),
	]

def tick():
	control.tick()

def drawselectors():
	for obj in control.selectors:
		obj.draw()

def drawhud():
	for obj in buttons:
		obj.draw()

def drawcursor():
	control.drawcursor()

def playing():
	return control.playing

def dts():
	yield from control.dts
	control.dts = []

def Gcursor():
	return control.Gcursor

def Gsegment():
	return control.Gsegment

def infotext():
	fps = control.clock.get_fps()
	xP, yP = control.mposP
	xG, yG = Gcursor()
	return "\n".join([
		f"Tab: grow (${state.growcost()})",
		f"1: segment",
		f"2: office",
		f"3: spire",
		f"4: spawn shopper",
		f"Money: ${state.money}",
		f"F10: change screen size",
		f"F11: toggle fullscreen",
		f"{fps:.1f}fps  P:[{xP:.1f},{yP:.1f}]  G:[{xG},{yG}]  tool:{control.tool}"
	])


