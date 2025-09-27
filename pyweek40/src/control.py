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
	
	def draw(self):
		if not self.active:
			return
		boxV = view.VconvertS(self.boxS)
		color = (140, 140, 140) if self.selected else (60, 60, 60)
		pygame.draw.rect(pview.screen, color, boxV)
		ptext.draw(self.text, fontsize = T(40), center = boxV.center, owidth = 1)
		

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

	def clickbutton(self, button):
		if button.selected:
			button.selected = False
			self.tool = None
		else:
			button.selected = True
			self.tool = button.text

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
		Button("residence1", pygame.Rect(500, 600, 100, 100), True),
		Button("vending1", pygame.Rect(800, 600, 100, 100), True),
	]

def tick():
	control.tick()

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


