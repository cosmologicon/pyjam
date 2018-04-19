import math, pygame, random
from . import state, view, pview, settings, ptext, progress, space, hud
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
		self.target = None
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
		self.cursor = None
		hud.controls = ["Reset", "Undo", "Give up"]
		if settings.DEBUG:
			hud.controls += ["Win"]
		self.turn = "X"
		self.tthink = 0
		self.scolor = (0, 0, 0)
	def think(self, dt, control):
		if self.turn == self.player:
			self.cursor = hud.getpointed(control.mposV)
			self.pointedG = view.GnearesttileV(control.mposV) if self.cursor is None else None
		else:
			self.cursor = None
			self.pointedG = None
		if control.down and self.cursor:
			if self.cursor == "Give up":
				push(Wipe(select))
			if self.cursor == "Reset":
				state.resetstate()
			if self.cursor == "Undo":
				state.popstate()
		if control.down and self.pointedG:
			if state.canmoveto(self.player, self.pointedG):
				state.pushstate()
				state.moveto(self.player, self.pointedG)
				self.nextturn()
		if self.turn != self.player:
			self.tthink += dt
			if self.tthink > 1:
				self.move()
		for obj in state.getthinkers():
			obj.think(dt)
		space.killtime(0.01)
		scolor = {
			"X": (80, 80, 255),
			"Y": (200, 40, 40),
			"Z": (0, 0, 0),
		}[self.turn]
		self.scolor = math.approach(self.scolor, scolor, 300 * dt)
	def nextturn(self):
		turnorder = "XYZ"
		self.turn = turnorder[(turnorder.index(self.turn) + 1) % len(turnorder)]
		self.tthink = 0
	def move(self):
		if self.turn == "Y":
			while True:
				tile = random.choice(list(state.grid))
				if state.canmoveto(self.turn, tile):
					state.moveto(self.turn, tile)
					break
			self.nextturn()
		elif self.turn == "Z":
			todestroy = [impact for impact in state.meteors.values() if impact.turnsleft() == 0]
			if todestroy:
				impact = random.choice(todestroy)
				state.destroy((impact.xG, impact.yG))
				self.tthink = 0
			else:
				self.nextturn()
	def draw(self):
		space.draw(pview.I(self.scolor), (40, 40, 40))
		ptext.draw(settings.gamename, center = pview.T(400, 100), color = "white", shade = 2,
			scolor = "black", shadow = (1, 1), angle = 10,
			fontsize = pview.T(120))
		for tile in state.gettiles():
			tile.draw()
		for obj in state.getboardobjs():
			obj.draw()
		hud.draw(cursor = self.cursor)
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

