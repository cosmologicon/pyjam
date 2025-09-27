import pygame, math
from . import pview
from . import settings, view, grid, state, effects

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
				self.tool = "office"
			if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
				self.tool = "spire"
			if event.type == pygame.KEYDOWN and event.key == pygame.K_4:
				grid.spawnshopper()
				
		button0, button1, button2 = pygame.mouse.get_pressed(3)
		dxV, dyV = pygame.mouse.get_rel()
		if button2:
			view.scootV((dxV, dyV))
		self.dts.append(dt)

	def onclick(self):
		segment = self.Gsegment
		p0, p1 = segment
		if self.tool is None:
			if state.canspend("segment") and grid.canaddsegment(segment):
				obj = grid.addsegment(segment)
				state.spend("segment")
				effects.addburstsegment(obj)
		if self.tool == "remove":
			grid.removeat(self.Gcursor)
		if self.tool in ["office", "spire"]:
			grid.addstructure(self.tool, p0)
			state.spend(self.tool)
		

def init():
	global control
	control = Control()

def tick():
	control.tick()

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


