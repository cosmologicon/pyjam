import pygame, math
from . import view, pview, state, sound
from .pview import T

def collide(obj0, obj1):
	return (obj0.x, obj0.y) == (obj1.x, obj1.y)

class Lep:
	def __init__(self, pos):
		self.x, self.y = pos
		self.charged = True
		self.color = 255, 255, 255
		self.nabbed = False
	def expend(self):
		self.charged = False
		state.leaps = min(state.leaps + 1, state.maxleaps)
		sound.play("recharge")
	def nab(self):
		self.charged = False
		self.nabbed = True
		state.held = self
	def release(self, who):
		self.x = who.x
		self.y = who.y
		self.charged = False
		self.nabbed = False
		state.held = None
	def draw(self):
		dx, dy = 0.5, 0.5
		pos = view.worldtoscreen((self.x + dx, self.y + dy))
		if self.nabbed:
			dx, dy = 0.8, 0.8
			pos = view.worldtoscreen((state.you.x + dx, state.you.y + dy))
		r = T(0.1 * view.zoom)
		if self.charged:
			pygame.draw.circle(pview.screen, self.color, pos, r)
		else:
			pygame.draw.circle(pview.screen, self.color, pos, r, T(4))

class You:
	def __init__(self):
		self.x, self.y = 0, 0
		self.state = "grounded"
		state.leaps = state.maxleaps
		self.thang = 0
		self.vy = 0
	def control(self, kdowns):
		print(kdowns)
		if pygame.K_SPACE in kdowns:
			print(self.state)
			if self.state == "jumping":
				lepshere = [lep for lep in state.leps if collide(self, lep)]
				if state.held:
					state.held.release(self)
				if lepshere:
					lepshere[0].nab()
					sound.play("nab")
				print(lepshere, state.held)
		dx = int(pygame.K_RIGHT in kdowns) - int(pygame.K_LEFT in kdowns)
		dy = int(pygame.K_UP in kdowns) - int(pygame.K_DOWN in kdowns)
		if not dx and not dy:
			return
		if self.state == "falling":
			return
		if not 0 <= self.x + dx < state.w:
			sound.play("no")
			return
		if self.state == "jumping" and state.leaps == 0:
			sound.play("no")
			return
		self.x += dx
		self.y += dy
		if self.state == "grounded":
			dy = max(dy, 0)
			if dy > 0:
				self.state = "jumping"
				self.thang = 0
				state.leaps -= 1
		elif self.state == "jumping":
			state.leaps -= 1
			self.thang = 0
		for lep in state.leps:
			if lep.charged and (self.x, self.y) == (lep.x, lep.y):
				lep.expend()
	def think(self, dt):
		if self.state == "jumping":
			self.thang = math.approach(self.thang, state.thang, dt)
			if self.thang == state.thang:
				self.state = "falling"
				self.vy = 8
		elif self.state == "falling":
			self.vy += 40 * dt
			self.y -= self.vy * dt
			if self.y <= 0:
				self.y = 0
				self.state = "grounded"
				state.leaps = state.maxleaps
				for lep in state.leps:
					lep.charged = True
	def draw(self):
		pos = view.worldtoscreen((self.x + 0.5, self.y + 0.5))
		r = T(0.25 * view.zoom)
		pygame.draw.circle(pview.screen, (200, 180, 40), pos, r, T(4))



