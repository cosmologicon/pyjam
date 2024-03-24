import pygame, math
from collections import defaultdict
from . import settings

class self:
	pass

def init():
	global posD, kdowns, kpressed, quit, click, mclick, rclick, dwheel
	global dragD, dragfrom, mdragD, rdragD
	posD = (0, 0)
	kdowns = []
	kpressed = defaultdict(bool)
	quit = False
	click = False
	mclick = False
	dragD = (0, 0)
	dragfrom = None  # On the frame when dragging begins, p0
	mdragD = (0, 0)
	rdragD = (0, 0)
	rclick = False
	dwheel = 0
	self.current = None
	self.tcurrent = None
	self.p0current = None
	self.pcurrent = None
	self.dragging = False
	self.borked = False

def think(dt):
	global posD, kdowns, kpressed, quit, click, mclick, rclick, dwheel
	global dragD, dragfrom, mdragD, rdragD
	posD = pygame.mouse.get_pos()
	kdowns = []
	quit = False
	click = False
	mclick = False
	rclick = False
	dwheel = 0
	dragD = (0, 0)
	dragfrom = None
	mdragD = (0, 0)
	rdragD = (0, 0)
	if self.borked and not any(pygame.mouse.get_pressed()):
		self.borked = False
	if self.current and not self.dragging and not self.borked:
		dt = 0.001 * (pygame.time.get_ticks() - self.tcurrent)
		dmove = math.distance(posD, self.p0current)
		if dt > 0.5 or dmove > 5:
			self.dragging = True
			dragfrom = self.p0current
	if self.dragging:
		x0, y0 = self.pcurrent
		x1, y1 = posD
		self.pcurrent = posD
		if self.current == 1:
			dragD = x1 - x0, y1 - y0
		elif self.current == 2:
			mdragD = x1 - x0, y1 - y0
		elif self.current == 3:
			rdragD = x1 - x0, y1 - y0
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit = True
		if event.type == pygame.KEYDOWN:
			kdowns.append(event.key)
		if event.type == pygame.MOUSEBUTTONDOWN and event.button in (1, 2, 3) and not self.borked:
			if self.current is not None:
				self.current = None
				self.borked = True
			else:
				self.current = event.button
				self.tcurrent = pygame.time.get_ticks()
				self.p0current = posD
				self.pcurrent = posD
				self.dragging = False
		if event.type == pygame.MOUSEWHEEL:
			dwheel += event.y
		if event.type == pygame.MOUSEBUTTONUP and event.button in (1, 2, 3):
			if event.button == self.current:
				dt = 0.001 * (pygame.time.get_ticks() - self.tcurrent)
				dmove = math.distance(posD, self.p0current)
				if not self.dragging:
					if event.button == 1: click = True
					if event.button == 2: mclick = True
					if event.button == 3: rclick = True
			self.current = None
	pressed = pygame.key.get_pressed()
	kpressed = {}
	for keyname, codes in settings.keys.items():
		if any(code in kdowns for code in codes):
			kdowns.append(keyname)
		kpressed[keyname] = any(pressed[code] for code in codes)

