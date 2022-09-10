import pygame, math

xV, yV = 0, 0

tdrag = 0.15
ddragV = 10

class self:
	pressed = False
	rpressed = False
	click = None
	rclick = False
	drag = None
	dragging = False
	drop = None
	

def init():
	pass

def now():
	return 0.001 * pygame.time.get_ticks()

def think(dt):
	global xV, yV, pV
	pV = xV, yV = pygame.mouse.get_pos()
	pressed, mpressed, rpressed = pygame.mouse.get_pressed()
	if pressed and not self.pressed:
		self.pdownV = pV
		self.tdown = now()
		self.dragging = False
		self.ddrug = False
	if rpressed and not self.rpressed:
		self.rclick = True
	if self.pressed:
		dt = now() - self.tdown
		if dt > tdrag:
			self.dragging = True
		d = math.distance(self.pdownV, pV)
		if d > ddragV:
			self.dragging = True
			self.ddrug = True
	if self.pressed and not pressed:
		if self.dragging:
			self.drop = dt, self.pdownV, pV
		else:
			self.click = pV
		self.dragging = False
	self.pressed = pressed
		

def getclick():
	ret = self.click
	self.click = None
	return ret

def getrclick():
	ret = self.rclick
	self.rclick = False
	return ret

def getdragging():
	return (now() - self.tdown, self.pdownV, (xV, yV), self.ddrug) if self.dragging else None

def getdrop():
	ret = self.drop
	self.drop = None
	return ret

