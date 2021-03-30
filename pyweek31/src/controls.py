import pygame, math
from . import settings, view

class state:
	# Starting time for the mouse down
	lt0 = None
	rt0 = None
	lpV0 = None
	rpV0 = None
	lpV = None
	rpV = None
	ldragging = False
	rdragging = False
	tlast = None

class ControlState:
	def __init__(self):
		self.t = 0.001 * pygame.time.get_ticks()
		self.dt = self.t - state.tlast if state.tlast is not None else 0.0
		state.tlast = self.t

		self.kpressed = pygame.key.get_pressed()
		self.mposV = pygame.mouse.get_pos()
		self.dragstart = None
		self.dragdV = None
		self.rdragdV = None
		self.scroll = 0

		self.events = set()
		self.kdowns = set()
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				for name, keycodes in settings.keys.items():
					if event.key in keycodes:
						self.kdowns.add(name)
			if event.type == pygame.QUIT:
				self.events.add("quit")
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					self.events.add("down")
					state.lt0 = self.t
					state.lpV0 = self.mposV
					state.lpV = self.mposV
					state.ldragging = False
				if event.button == 3:
					self.events.add("rdown")
					state.rt0 = self.t
					state.rpV0 = self.mposV
					state.rpV = self.mposV
					state.rdragging = False
				if event.button == 4:
					self.scroll += 1
				if event.button == 5:
					self.scroll -= 1
			if event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					self.events.add("up")
					if not state.ldragging:
						self.events.add("click")
					state.lt0 = None
				if event.button == 3:
					self.events.add("rup")
					if not state.rdragging:
						self.events.add("rclick")
					state.lt0 = None
		if state.lt0 is not None:
			if self.t - state.lt0 > 0.3 or math.distance(self.mposV, state.lpV0) > 10:
				state.ldragging = True
			if state.ldragging:
				self.dragdV = view.vecadd(self.mposV, state.lpV, -1)
				state.lpV = self.mposV
		if state.rt0 is not None:
			if self.t - state.rt0 > 0.3 or math.distance(self.mposV, state.rpV0) > 10:
				state.rdragging = True
			if state.rdragging:
				self.rdragdV = view.vecadd(self.mposV, state.rpV, -1)
				state.rpV = self.mposV



