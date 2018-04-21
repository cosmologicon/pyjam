import math, pygame, random
from . import state, view, pview, settings, ptext, progress, space, hud, cstate, pathfind, program, sound, tile, dialog, level
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
		"level1": (-50, 230),
		"level2": (50, 330),
		"level3": (-50, 430),
		"level5": (50, 530),
#		"level5": (-50, 600),
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
		sound.playmusic("space-in-time")
		self.act = int(max(level[3] for level in progress.unlocked))
		self.targets = {}
		for level in sorted(progress.unlocked):
			act = int(level[3])
			jlevel = level[5:]
			x0 = pview.w0 / (self.act + 1) * (act + 0.5)
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
			push(Wipe(play, level.name(self.target)))
			sound.play("reset")
		space.killtime(0.01)
	def draw(self):
		for act in range(self.act + 1):
			x0 = pview.w0 / (self.act + 1) * act
			pview.fill(self.color0[act], T(x0, 0, pview.w0, pview.h0))
			if act:
				pygame.draw.line(pview.screen, (255, 255, 255), T(x0, 0), T(x0, pview.h0), T(6))
		for target, pV in self.targets.items():
			color = (self.color1 if target == self.target else self.color0)[int(target[3])]
			img = tile.getimg("button", T(100), color)
			pview.screen.blit(img, img.get_rect(center = T(pV)))
			ptext.draw(level.name(target), center = T(pV), fontsize = T(30), owidth = 1.5, ocolor = "black",
				color = "white", fontname = "Londrina")
		ptext.draw(settings.gamename, midtop = pview.midtop, fontsize = T(140),
			owidth = 1.5, ocolor = "black", shade = 2, fontname = "Passion")
		if progress.done():
			ptext.draw("Thank you for playing", midbottom = pview.midbottom, fontsize = T(100),
				owidth = 1.5, ocolor = "black", shade = 2, fontname = "Passion")
		else:
			ptext.draw("by team Universe Factory", midbottom = pview.midbottom, fontsize = T(60),
				owidth = 1.5, ocolor = "black", shade = 2, fontname = "Passion")
		if len(progress.unlocked) < 5:
			ptext.draw("F10: change resolution\nF11: fullscreen", bottomright = pview.bottomright, fontsize = T(26),
				color = "#aaaaff", owidth = 1.5, ocolor = "black", shade = 1, fontname = "Passion")
			
select = Select()

class Play(object):
	def init(self):
		self.act = int(progress.current[3])
		sound.playmusic("magic-forest" if self.act in (0, 1, 2) else "metaphysik")
		if self.act == 0:
			self.turnorder = "XZ"
			self.players = ["X"]
		elif self.act == 1:
			self.turnorder = "XYZ"
			self.players = ["X"]
		elif self.act == 2:
			self.turnorder = "YXZ"
			self.players = ["Y"]
		elif self.act == 3:
			self.turnorder = "XYZ"
			self.players = ["X", "Y"]
		state.load()
		pathfind.clear()
		cstate.pointedG = None
		cstate.cursor = None
		hud.controls = ["Reset", "Undo", "Give up"]
		if settings.DEBUG:
			hud.controls += ["Win"]
		self.turn = self.turnorder[0]
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
				sound.play("reset")
			if cstate.cursor == "Undo":
				state.popstate()
				sound.play("undo")
			if cstate.cursor == "Win":
				self.win()
		if control.down and cstate.pointedG:
			topush = self.turn == self.turnorder[0]
			if state.canclaimpart(self.turn, cstate.pointedG):
				if topush:
					state.pushstate()
				state.claimpart(self.turn, cstate.pointedG)
				self.nextturn()
				sound.play("claimpart")
			elif state.canmoveto(self.turn, cstate.pointedG):
				if topush:
					state.pushstate()
				state.moveto(self.turn, cstate.pointedG)
				self.nextturn()
				sound.play("move")
			elif state.canclaimtile(self.turn, cstate.pointedG):
				if topush:
					state.pushstate()
				state.claimtile(self.turn, cstate.pointedG)
				self.nextturn()
				sound.play("claimtile")
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
		if self.turn in ["X", "Y"]:
			if state.alive(self.turn):
				togo = program.move()
				if state.canclaimpart(self.turn, togo):
					state.claimpart(self.turn, togo)
					sound.play("claimpart")
				elif state.canclaimtile(self.turn, togo):
					state.claimtile(self.turn, togo)
					sound.play("claimtile")
				elif state.canmoveto(self.turn, togo):
					state.moveto(self.turn, togo)
					sound.play("move")
			self.nextturn()
		elif self.turn == "Z":
			todestroy = [impact for impact in state.meteors.values() if impact.turnsleft() == 0]
			if todestroy:
				impact = random.choice(todestroy)
				state.destroy((impact.xG, impact.yG))
				self.tthink = 0
				sound.play("destroy")
			else:
				self.nextturn()
	def win(self):
		progress.win()
		push(Wipe(select, "Level complete"))
		sound.play("win")
	def lose(self):
		push(Wipe(select, "Level failed"))
		sound.play("lose")
	def draw(self):
		space.draw(pview.I(self.scolor), (40, 40, 40))
		ptext.draw(level.name(progress.current), center = pview.T(pview.centerx0, 100),
			color = "white", shade = 2,
			owidth = 2, ocolor = "black", fontname = "Passion",
			fontsize = pview.T(120))
		for tile in state.gettiles():
			tile.draw()
		for obj in state.getboardobjs():
			obj.draw()
		hud.draw(self.players)
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
		if who == "X":
			color = 0, 0, 255
			textcolor = 128, 128, 255
			size = 250
			fontname = "CuteFont"
			fontsize = 60
		elif who == "Y":
			color = 255, 0, 0
			textcolor = 255, 128, 128
			size = 200
			fontname = "Kirang"
			fontsize = 48
		img = tile.getimg(who, T(size), color)
		pview.screen.blit(img, img.get_rect(center = T(180, 600)))
		ptext.draw(text, T(400, 500), width = T(700), fontname = fontname, fontsize = T(fontsize),
			owidth = 2, ocolor = "black", lineheight = 0.7,
			color = textcolor, shade = 1.5)

