import math, pygame
from . import state, view, pview, settings, ptext, progress, space
from .pview import T

scenes = []
def push(s):
	scenes.append(s)
	s.init()
def swap(s):
	if scenes:
		scenes.pop()
	push(s)
def top():
	return scenes[-1] if scenes else None

class Select(object):
	lspotpVs = {
		"level1": (300, 400),
		"level2": (500, 200),
	}
	actdVs = {
		"x": (-45, 10),
		"y": (45, 10),
		"xy": (0, 30),
	}
	def init(self):
		self.lspots = sorted(level.split(".")[0] for level in progress.unlocked)
		self.targets = sorted(progress.unlocked)
	def targetpV(self, target):
		lspot, act = target.split(".")
		xV, yV = self.lspotpVs[lspot]
		dxV, dyV = self.actdVs[act]
		return xV + dxV, yV + dyV
	def think(self, dt, control):
		self.target = None
		for target in self.targets:
			pV = self.targetpV(target)
			if math.distance(pV, control.mposV) < 20:
				self.target = target
		if control.down and self.target is not None:
			push(Wipe(play))
		space.killtime(0.01)
	def draw(self):
		pview.fill((0, 50, 120))
		for lspot in self.lspots:
			xV, yV = self.lspotpVs[lspot]
			pygame.draw.circle(pview.screen, (0, 0, 0), T(xV, yV), T(50))
			ps = [T(xV + dx, yV + dy) for dx, dy in [math.CS(j / 40 * math.tau, 43) for j in range(10, 31)]]
			pygame.draw.polygon(pview.screen, (0, 0, 160), ps)
			ps = [T(xV + dx, yV + dy) for dx, dy in [math.CS(j / 40 * math.tau, 43) for j in range(30, 51)]]
			pygame.draw.polygon(pview.screen, (120, 0, 0), ps)
		for target in self.targets:
			color = (255, 255, 255) if target == self.target else (0, 0, 0)
			pV = self.targetpV(target)
			pygame.draw.circle(pview.screen, color, T(pV), T(20))
			pygame.draw.circle(pview.screen, (60, 60, 60), T(pV), T(16))
select = Select()

class Play(object):
	def init(self):
		state.load()
		self.player = "X"
		self.pointedG = None
	def think(self, dt, control):
		self.pointedG = view.GnearesttileV(control.mposV)
		if control.down and self.pointedG:
			if state.canmoveto(self.player, self.pointedG):
				state.moveto(self.player, self.pointedG)
		for piece in state.getpieces():
			piece.think(dt)
		space.killtime(0.01)
	def draw(self):
		space.draw((40, 40, 255), (40, 40, 40))
		ptext.draw(settings.gamename, center = pview.T(400, 100), color = "white", shade = 2,
			scolor = "black", shadow = (1, 1), angle = 10,
			fontsize = pview.T(120))
		for color, pG in state.gettiles():
			if pG == self.pointedG and state.canmoveto(self.player, self.pointedG):
				color = "white"
			view.drawtile(color, pG)
		for piece in state.getpieces():
			piece.draw()
play = Play()


class Wipe(object):
	def __init__(self, nextscene):
		self.nextscene = nextscene
	def init(self):
		self.t = 0
		self.T = 0.6
		self.starting = True
	def think(self, dt, control):
		if self.starting:
			self.t += dt
			if self.t >= self.T:
				self.t = self.T
				self.starting = False
				scenes[-2] = self.nextscene
				self.nextscene.init()
		else:
			self.t -= dt
			if self.t <= 0:
				scenes.pop()
		space.killtime(0.01)
	def draw(self):
		if self is not top():
			return
		scenes[-2].draw()
		x = int(round(1.2 * self.t / self.T * pview.w))
		if x <= 0:
			return
		ys = [int(round(j * pview.h / 6)) for j in range(7)]
		for j in range(6):
			x0 = 0 if j % 2 == self.starting else pview.w - x
			pview.screen.fill((0, 0, 0), (x0, ys[j], x, ys[j+1] - ys[j]))

