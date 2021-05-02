import pygame, math, random
from . import view, pview, state, sound, level, draw, settings, ptext
from .pview import T

def collide(obj0, obj1):
	return (obj0.x, obj0.y) == (obj1.x, obj1.y)

def pickany(objs):
	objs = list(objs)
	return objs[0] if objs else None

class GuideGlow:
	def __init__(self, who):
		self.who = who
		self.lights = []
		self.t = 0
	def think(self, dt):
		self.t += dt
		if 0.06 * random.random() < dt:
			t = self.t + 0.5
			x0 = self.who.x + 0.5 + 0.12 * self.who.xfly
			y0 = self.who.y + 0.5 + 0.12 * self.who.yfly
			dx, dy = random.uniform(-0.2, 0.2), random.uniform(-0.2, 0.2)
			color = math.imix(self.who.color, (255, 255, 255), random.uniform(0, 1))
			self.lights.append((t, x0 + dx, y0 + dy, color))
		self.lights = [light for light in self.lights if light[0] > self.t]
	def draw(self):
		for t, x, y, color in self.lights:
			f = math.clamp((t - self.t) / 0.5, 0, 1)
			if f > 0:
				pos = view.worldtoscreen((x, y))
				pygame.draw.circle(pview.screen, color, pos, T(f * 8))

class Lep:
	color = 255, 255, 255
	def __init__(self, pos):
		self.x, self.y = pos
		self.flyseed = random.random() * 1000
		self.charged = True
		self.guidable = False
		self.tfly = 0
		self.xfly, self.yfly = random.uniform(-1, 1), random.uniform(-1, 1)
		self.vxfly, self.vyfly = random.uniform(-1, 1), random.uniform(-1, 1)
		self.tflap = random.uniform(0, 100)
		self.aseen = False
		self.ds = []  # Not used to restrict movement unless canmovefrom is overriden.
		self.glow = None
	# Whether you're able to move away from this lep.
	def canmovefrom(self, d):
		return d in self.ds
	def movefrom(self, d):
#		self.charged = False
		pass
	# Whether this lep prevents you from expending a leap in the given direction as you move away
	def canboost(self, d):
		return self.charged and d in self.ds
	# Called when you first enter this lep's space
	def encounter(self):
		self.aseen = True
	# When you press a direction at this lep, what direction do you actually go?
	def adjustcombo(self, d):
		return d
	def guide(self):
#		self.charged = False
		state.guided = self
		state.leps.remove(self)
	def release(self, who):
		self.x = who.x
		self.y = who.y
#		self.charged = False
		state.guided = None
		state.leps.append(self)
	def think(self, dt):
		if self.guidable and not self.glow:
			self.glow = GuideGlow(self)
		if self.glow:
			self.glow.think(dt)
		if self in state.goals:
			speed = 10 * math.exp(-0.3 * (state.goals.index(self) + 1))
			seekpos = state.you.x, state.you.y + 0.2
			self.x, self.y = math.softapproach((self.x, self.y), seekpos, speed * dt)
		elif self is state.guided:
			seekpos = state.you.x, state.you.y + 0.2
			self.x, self.y = math.softapproach((self.x, self.y), seekpos, 10 * dt)
		self.tflap += dt
		self.tfly -= dt
		if self.tfly <= 0:
			self.tfly = random.uniform(0.1, 0.3)
			self.vxfly = random.uniform(-1, 1) - math.clamp(self.xfly, -2, 2)
			self.vyfly = random.uniform(-1, 1) - math.clamp(self.yfly, -2, 2)
		self.xfly += 6 * dt * self.vxfly
		self.yfly += 6 * dt * self.vyfly
	def drawsymbol(self, pos, scale):
		if not settings.colormode:
			return
		color = math.imix(self.color, (255, 255, 255), 0.5)
		ptext.draw(self.symbol, center = pos, color = color, fontname = "Bevan",
			fontsize = T(scale * 0.12), owidth = 1, shade = 1)
	def draw0(self, topos, zoom):
		dx, dy = 0.5, 0.5
		dx += 0.12 * self.xfly
		dy += 0.12 * self.yfly
		pos = topos((self.x + dx, self.y + dy))
		vfactor = 1 if self.vyfly < 0 else -1
		vfactor = 1.6 * math.sin(self.tflap * 20)
		flip = self.vxfly < 0
		angle = (-1 if flip else 1) * (20 + 5 * math.clamp(self.vyfly, -2, 2))
		scale = T(1.4 * view.zoom)
		draw.lep(pos, scale, angle, flip, vfactor, colormask = self.color)
		if self in state.leps:
			if self.glow:
				self.glow.draw()
			self.drawsymbol(topos((self.x + 0.5, self.y + 0.5)), scale)
	def drawarrow(self, d, dist = 0.32):
		if not self.aseen:
			return
		dx, dy = math.norm(d)
		pos = self.x + 0.5 + dist * dx, self.y + 0.5 + dist * dy
		alpha = 1 if (self.x, self.y) == (state.you.x, state.you.y) else 0.25
		scale = 0.38 * pview.f * view.zoom
		draw.arrow(view.worldtoscreen(pos), scale, d, self.color, self.tflap, alpha)
	def drawarrows(self):
		if self is not state.guided:
			for d in self.ds:
				self.drawarrow(d)
	def draw(self):
		self.draw0(view.worldtoscreen, view.zoom)
	def drawmap(self):
		pos = view.worldtomap((self.x + 0.5, self.y + 0.5))
		scale = 3.0 * pview.f * view.mapzoom()
		owidth = 2 if self.glow else 0
		if self.glow and pygame.time.get_ticks() * 0.001 % 0.5 < 0.1:
			scale *= 1.1
		draw.drawimg("lep-icon", pos, scale, colormask = self.color, owidth = owidth)
		self.drawsymbol(pos, scale)
	def drawarrowmap(self, d, dist = 0.32):
		if not self.aseen:
			return
		dx, dy = math.norm(d)
		pos = self.x + 0.5 + dist * dx, self.y + 0.5 + dist * dy
		scale = 0.4 * pview.f * view.mapzoom()
		draw.arrow(view.worldtomap(pos), scale, (dx, dy), self.color, 1, 1, 1)
	def drawarrowsmap(self):
		if self is not state.guided:
			for d in self.ds:
				self.drawarrowmap(d)
	def draweditor(self):
		pos = view.worldtoscreen((self.x + 0.5, self.y + 0.5))
		pygame.draw.circle(pview.screen, self.color, pos, T(12))
		if self.guidable:
			pygame.draw.circle(pview.screen, self.color, pos, T(20), T(4))
		for d in self.ds:
			dx, dy = math.norm(d)
			dpos = view.worldtoscreen((self.x + 0.5 + 0.4 * dx, self.y + 0.5 + 0.4 * dy))
			pygame.draw.line(pview.screen, self.color, pos, dpos, T(4))
	def drawguided(self, mcenter):
		scale = 600 * pview.f
		draw.drawimg("lep-icon", T(mcenter), scale, colormask = self.color, owidth = 2)
		self.drawsymbol(T(mcenter), scale)
		self.drawguidedarrows(mcenter)
	def drawguidedarrow(self, mcenter, d, dist = 0.32):
		if not self.aseen:
			return
		dx, dy = math.norm(d)
		x0, y0 = mcenter
		pos = T(x0 + 50 * dx, y0 - 50 * dy)
		scale = 80 * pview.f
		draw.arrow(pos, scale, (dx, dy), self.color, self.tflap, 1)
	def drawguidedarrows(self, mcenter):
		for d in self.ds:
			self.drawguidedarrow(mcenter, d)


# Lep is movable.
# May only leave the lep in the given direction.
class FlowLep(Lep):
	color = 100, 100, 255
	symbol = "O"
	def __init__(self, pos, ds):
		Lep.__init__(self, pos)
		self.ds = ds
	def draw0(self, topos, zoom):
		Lep.draw0(self, topos, zoom)
		self.drawarrows()

# Rotates along with all other SpinLeps
class SpinLep(Lep):
	color = 40, 255, 40
	symbol = "X"
	ds0 = (0, 1), (1, 0), (0, -1), (-1, 0)
	ds1 = (1, 1), (1, -1), (-1, 1), (-1, -1)
	def __init__(self, pos):
		Lep.__init__(self, pos)
	def think(self, dt):
		Lep.think(self, dt)
		self.ds = self.ds0 if state.jspin % 2 == 0 else self.ds1
	def movefrom(self, d):
		Lep.movefrom(self, d)
		state.jspin += 1
	def draw0(self, topos, zoom):
		Lep.draw0(self, topos, zoom)
		self.drawarrows()

# Doubles your movement
class BoostLep(Lep):
	color = 255, 128, 0
	symbol = "2"
	def __init__(self, pos, ds, n = 2):
		Lep.__init__(self, pos)
		self.ds = ds
		self.n = n
	def adjustcombo(self, d):
		dx, dy = d
		return dx * self.n, dy * self.n
	def draw0(self, topos, zoom):
		Lep.draw0(self, topos, zoom)
		self.drawarrows()
	def drawarrows(self):
		if self is not state.guided:
			for d in self.ds:
				self.drawarrow(d, 0.42)
			for d in self.ds:
				self.drawarrow(d, 0.3)
	def drawarrowsmap(self):
		if self is not state.guided:
			for d in self.ds:
				self.drawarrowmap(d, 0.42)
			for d in self.ds:
				self.drawarrowmap(d, 0.3)
	def drawguidedarrows(self, mcenter):
		for d in self.ds:
			self.drawguidedarrow(mcenter, d, 0.42)
		for d in self.ds:
			self.drawguidedarrow(mcenter, d, 0.3)

# Only lets you go straight through
class ContinueLep(Lep):
	symbol = "<>"
	color = 255, 0, 255
	def think(self, dt):
		Lep.think(self, dt)
		if state.you.lastdx or state.you.lastdy:
			self.ds = [(math.sign(state.you.lastdx), math.sign(state.you.lastdy))]
	def draw0(self, topos, zoom):
		Lep.draw0(self, topos, zoom)
		self.drawarrows()

# Refills the leaps
class ChargeLep(Lep):
	color = 200, 0, 255
	def canmovefrom(self, d):
		return True
	def canboost(self, d):
		return False
	def encounter(self):
		sound.play("recharge")
		state.recharge()

# Reach the goal leps to complete the stage.
class GoalLep(Lep):
	color = 255, 255, 0
	symbol = "!!"
	def __init__(self, pos):
		Lep.__init__(self, pos)
		self.glow = GuideGlow(self)
	def canmovefrom(self, d):
		return True
	def canboost(self, d):
		return False
	def encounter(self):
		if self in state.leps:
			state.goals.append(self)
			state.leps.remove(self)
			level.checkpoint()
			sound.play("goal")


class You:
	def __init__(self):
		self.x, self.y = 0, 0
		self.state = "grounded"
		state.leaps = state.maxleaps
		self.thang = 0
		self.vy = 0
		self.trebound = 0
		# Animations
		self.facingright = True
		self.jumpspec = 0
		self.lastdx = 0
		self.lastdy = 0
		self.tmove = 10
	def jumpmeter(self):
		if self.state in ("grounded", "rebounding"):
			return 1
		if self.state == "falling":
			return 0
		if self.state == "jumping":
			return 1 - self.thang / state.thang
	def act(self):
		currentlep = pickany(lep for lep in state.leps if collide(self, lep))
		if self.state == "jumping":
			if currentlep and not currentlep.guidable:
				sound.play("no")
			else:
				if state.guided:
					state.guided.release(self)
					if not currentlep:
						sound.play("release")
				if currentlep:
					currentlep.guide()
					sound.play("guide")
	def combo(self, d):
		if self.state in ("falling", "rebounding"):
			return
		currentlep = pickany(lep for lep in state.leps if collide(state.you, lep))
		if currentlep:
			if not currentlep.canmovefrom(d):
				sound.play("no")
				if not settings.forgive:
					self.fall()
				return
		dleap = 1
		if currentlep and currentlep.canboost(d):
			dleap -= 1
		if state.leaps - dleap < 0:
			sound.play("no")
			if not settings.forgive:
				self.fall()
			return
		if currentlep:
			d = currentlep.adjustcombo(d)
		dx, dy = d
		if not 0 <= self.x + dx < state.w:
			sound.play("no")
			return
		if not 0 <= self.y + dy:
			sound.play("no")
			return
		# Actually move
		sound.play("jump")
		if currentlep:
			currentlep.movefrom(d)

		self.x += dx
		self.y += dy
		self.tmove = 0
		self.jjumpspec = random.random()
		self.lastdx = dx
		self.lastdy = dy
		if dx:
			self.facingright = dx > 0
		if self.state == "grounded":
			dy = max(dy, 0)
			if dy > 0:
				self.state = "jumping"
				self.thang = 0
				state.leaps -= dleap
		elif self.state == "jumping":
			state.leaps -= dleap
			self.thang = 0
		for lep in state.leps:
			if collide(state.you, lep):
				lep.encounter()

	
	def control(self, keys):
		if "act" in keys:
			self.act()
		if "combo" in keys:
			if ("left" in keys and "right" in keys) or ("up" in keys and "down" in keys):
				self.fall()
			else:
				dx = int("right" in keys) - int("left" in keys)
				dy = int("up" in keys) - int("down" in keys)
				if dx or dy:
					self.combo((dx, dy))
	# Whether there are any legal moves you can make. If not, go ahead and fall.
	def canmove(self):
		if state.leaps or state.guided:
			return True
		currentlep = pickany(lep for lep in state.leps if collide(self, lep))
		if currentlep and currentlep.guidable:
			return True
		ds = [(x, y) for x in (-1, 0, 1) for y in (-1, 0, 1) if x or y]
		if currentlep and any(currentlep.canboost(d) for d in ds):
			return True
		return False
	def fall(self):
		self.state = "falling"
		self.vy = 8
	def think(self, dt):
		self.tmove += dt
		if self.state == "jumping":
			self.thang += dt
			thang = state.thang if self.canmove() else state.thang0
			if self.thang >= thang:
				self.fall()
		elif self.state == "falling":
			self.vy += 40 * dt
			self.y -= self.vy * dt
			if state.yfloor > 0:
				if self.y < state.yfloor - 2:
					self.state = "rebounding"
					self.trebound = 0
					self.x = state.xfloor
					self.y = state.yfloor - 2
			else:
				if self.y <= 0:
					self.y = 0
					self.state = "grounded"
					state.recharge()
					state.rechargeleps()
		elif self.state == "rebounding":
			self.trebound += dt
			if self.trebound > 1:
				self.x = state.xfloor
				self.y = state.yfloor
				sound.play("rebound")
				state.recharge()
				state.rechargeleps()
				self.state = "jumping"
				self.thang = 0
				self.tmove = 0
				self.lastdx, self.lastdy = 0, 2
	def drawspec(self):
		if self.state == "grounded":
			return "standing", 0
		if self.state == "falling":
			angle = (1 if self.facingright else -1) * 8 * self.lastdy
			return "falling", angle
		if self.state == "jumping" and not self.canmove():
			angle = (1 if self.facingright else -1) * 8 * self.lastdy
			return "falling", angle
		if self.state in ("jumping", "rebounding"):
			angle = 14 * math.sign(self.lastdy) * (2 - (self.lastdx != 0))
			angle *= (1 if self.facingright else -1)
			return "pose", angle
	def draw(self):
		spec, angle = self.drawspec()
		scale = T(1.3 * view.zoom)
		pose0 = 5 + 2 * self.x + 3 * self.y + (self.x + 2) * (self.y + 2) + 3 * self.facingright
		pose0 %= 8
		for j in ((0,) if settings.noshadow else (2, 1, 0)):
			alpha = math.clamp((1 - 0.2 * j) * (1 - self.tmove), 0, 1)
			if j and alpha < 0:
				continue
			pose = (pose0 + 3 * j) % 8
			seed = 100 * pose + 17
			factor = [5, 2, 1][j]
			f = math.clamp(factor * self.tmove, 0, 1)
			px, py = math.mix((self.x - self.lastdx, self.y - self.lastdy), (self.x, self.y), f)
			pos = view.worldtoscreen((px + 0.5, py + 0.5))
			drawspec = spec if spec != "pose" and j == 0 else "pose-horiz-%d" % pose
			if j == 0:
				draw.you(drawspec, pos, scale, angle, self.facingright, owidth=2)
			else:
				draw.you(drawspec, pos, scale, angle, self.facingright, seed, alpha, owidth=2)

	def drawmap(self):
		pos = view.worldtomap((self.x + 0.5, self.y + 0.5))
		scale = 3.0 * pview.f * view.mapzoom()
		draw.drawimg("token", pos, scale, flip = not self.facingright)



