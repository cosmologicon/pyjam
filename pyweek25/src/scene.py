import math, pygame, random
from . import state, view, pview, settings, ptext, progress, space, hud, cstate, pathfind, program, sound, tile, dialog
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
		"level1": (-50, 200),
		"level2": (50, 300),
		"level3": (-50, 400),
		"level4": (50, 500),
		"level5": (-50, 600),
	}
	color0 = {
		0: (120, 120, 120),
		1: (0, 0, 255),
		2: (255, 0, 0),
		3: (200, 0, 200),
	}
	color1 = {
		0: (200, 200, 200),
		1: (120, 120, 255),
		2: (255, 120, 120),
		3: (255, 120, 255),
	}
	def init(self):
		self.act = int(max(level[3] for level in progress.unlocked))
		self.targets = {}
		for level in sorted(progress.unlocked):
			act = int(level[3])
			jlevel = level[5:]
			x0 = pview.w0 / (self.act + 2) * (act + 1)
			xV, yV = self.lspotpVs[jlevel]
			self.targets[level] = x0 + xV, yV
		self.target = None
	def think(self, dt, control):
		self.target = None
		for target, pV in self.targets.items():
			if math.distance(pV, control.mposV) < 50:
				self.target = target
		if control.down and self.target is not None:
			progress.select(self.target)
			push(Wipe(play, self.target))
		space.killtime(0.01)
	def draw(self):
		for act in range(self.act + 1):
			x0 = pview.w0 / (self.act + 2) * (act + 0.5 if act else 0)
			pview.fill(self.color0[act], T(x0, 0, pview.w0, pview.h0))
			if act:
				pygame.draw.line(pview.screen, (255, 255, 255), T(x0, 0), T(x0, pview.h0), T(6))
		for target, pV in self.targets.items():
			color = (self.color1 if target == self.target else self.color0)[int(target[3])]
			img = tile.getimg("button", T(100), color)
			pview.screen.blit(img, img.get_rect(center = T(pV)))
			ptext.draw(target, center = T(pV), fontsize = T(30), owidth = 1.5, ocolor = "black",
				color = "white", fontname = "Londrina")
		if self.target is not None:
			ptext.draw(self.target, midtop = pview.midtop, fontsize = T(120),
				owidth = 1.5, ocolor = "black", shade = 2)
select = Select()

class Play(object):
	def init(self):
		self.act = int(progress.current[3])
		if self.act == 0:
			self.turnorder = "XZ"
		elif self.act == 1:
			self.turnorder = "XYZ"
		state.load()
		pathfind.clear()
		self.players = ["X"]
		cstate.pointedG = None
		cstate.cursor = None
		hud.controls = ["Reset", "Undo", "Give up"]
		if settings.DEBUG:
			hud.controls += ["Win"]
		self.turn = "X"
		self.tthink = 0
		self.scolor = (0, 0, 0)
		self.checkeddialog = False
	def think(self, dt, control):
		if not self.checkeddialog:
			if progress.shouldtalk():
				push(Dialog())
			self.checkeddialog = True

		if self.turn in self.players and state.alive(self.turn):
			cstate.cursor = hud.getpointed(control.mposV)
			cstate.pointedG = view.GnearesttileV(control.mposV) if cstate.cursor is None else None
		else:
			cstate.cursor = None
			cstate.pointedG = None
		if control.down and cstate.cursor:
			if cstate.cursor == "Give up":
				self.lose()
			if cstate.cursor == "Reset":
				push(Wipe(play))
			if cstate.cursor == "Undo":
				state.popstate()
			if cstate.cursor == "Win":
				self.win()
		if control.down and cstate.pointedG:
			if state.canclaimpart(self.turn, cstate.pointedG):
				state.pushstate()
				state.claimpart(self.turn, cstate.pointedG)
				self.nextturn()
			elif state.canmoveto(self.turn, cstate.pointedG):
				state.pushstate()
				state.moveto(self.turn, cstate.pointedG)
				self.nextturn()
			elif state.canclaimtile(self.turn, cstate.pointedG):
				state.pushstate()
				state.claimtile(self.turn, cstate.pointedG)
				self.nextturn()
			else:
				sound.play("no")
		if self.turn in self.players and not state.alive(self.turn):
			self.lose()
		if state.won(self.players):
			self.win()
		elif not state.canwin(self.players) and self.turn in self.players:
			self.lose()
		if self.turn not in self.players:
			self.tthink += dt
			if self.tthink > 1:
				self.move()
			elif self.turn == "Z" and not any(impact.turnsleft() == 0 for impact in state.meteors.values()):
				self.nextturn()
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
		self.turn = self.turnorder[(self.turnorder.index(self.turn) + 1) % len(self.turnorder)]
		self.tthink = 0
	def move(self):
		if self.turn == "Y":
			if state.alive("Y"):
				togo = program.move()
				if state.canclaimpart("Y", togo):
					state.claimpart("Y", togo)
				elif state.canclaimtile("Y", togo):
					state.claimtile("Y", togo)
				elif state.canmoveto("Y", togo):
					state.moveto("Y", togo)
			self.nextturn()
		elif self.turn == "Z":
			todestroy = [impact for impact in state.meteors.values() if impact.turnsleft() == 0]
			if todestroy:
				impact = random.choice(todestroy)
				state.destroy((impact.xG, impact.yG))
				self.tthink = 0
			else:
				self.nextturn()
	def win(self):
		# progress.unlock...
		push(Wipe(select, "Level complete"))
	def lose(self):
		push(Wipe(select, "Level failed"))
	def draw(self):
		space.draw(pview.I(self.scolor), (40, 40, 40))
		ptext.draw(settings.gamename, center = pview.T(400, 100), color = "white", shade = 2,
			scolor = "black", shadow = (1, 1), angle = 10, fontname = "Londrina",
			fontsize = pview.T(120))
		for tile in state.gettiles():
			tile.draw()
		for obj in state.getboardobjs():
			obj.draw()
		hud.draw()
play = Play()


class Wipe(object):
	def __init__(self, nextscene, message = None):
		self.nextscene = nextscene
		self.message = message
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
		if self.message is not None:
			alpha = math.clamp(3 * self.t / self.T, 0, 1)
			ptext.draw(self.message, center = pview.center, fontsize = T(150),
				owidth = 2, ocolor = "black", color = "yellow", shade = 2,
				fontname = "Londrina",
				alpha = alpha)

class Dialog(object):
	def __init__(self):
		pass
	def init(self):
		self.texts = dialog.texts[progress.current]
		self.current = None
		progress.seen.add(progress.current)
		progress.save()
		self.t = 0
	def think(self, dt, control):
		if self.current is None and self.t > 0.25:
			if not self.texts:
				scenes.pop()
				return
			self.current = self.texts.pop(0)
			self.t = 0
		self.t += dt
		if control.down:
			self.current = None
		space.killtime(0.01)
	def draw(self):
		if self is not top():
			return
		scenes[-2].draw()
		play.draw()
		pview.fill((0, 0, 0, 200))
		if not self.current:
			return
		who, text = self.current
		color = 255, 0, 0
		img = tile.getimg(who, T(250), color)
		textcolor = 255, 128, 128
		pview.screen.blit(img, T(80, 480))
		ptext.draw(text, T(400, 500), width = T(700), fontname = "CuteFont", fontsize = T(60),
			owidth = 2, ocolor = "black", lineheight = 0.7,
			color = textcolor, shade = 1.5)

