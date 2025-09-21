import pygame
from . import settings, view, grid

class Control:
	def __init__(self):
		self.playing = True
		self.clock = pygame.time.Clock()
		self.dts = []
#		self.t0 = 0.001 * pygame.time.get_ticks()
		pygame.mouse.get_rel()

	def tick(self):
		dt = min(0.001 * self.clock.tick(settings.maxfps), 1 / settings.minfps)
		self.mposV = pygame.mouse.get_pos()
		self.mposP = view.PconvertV(self.mposV)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.playing = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				self.playing = False
			if event.type == pygame.MOUSEWHEEL:
				view.zoom(event.y, self.mposP)
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				self.onclick()
				
		button0, button1, button2 = pygame.mouse.get_pressed(3)
		dxV, dyV = pygame.mouse.get_rel()
		if button2:
			view.scootV((dxV, dyV))
		self.dts.append(dt)

	def Gsegment(self):
		return view.GnearestsegmentP(self.mposP)

	def onclick(self):
		segment = self.Gsegment()
		if grid.canaddsegment(segment):
			grid.addsegment(segment)

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
	return view.GnearestP(control.mposP)

def Gsegment():
	return control.Gsegment()

def infotext():
	fps = control.clock.get_fps()
	xP, yP = control.mposP
	xG, yG = Gcursor()
	return f"{fps:.1f}fps  P:[{xP:.1f},{yP:.1f}]  G:[{xG},{yG}]"


