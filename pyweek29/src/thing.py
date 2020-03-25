import pygame, math, random
from . import view, pview, state, sound, level, draw
from .pview import T

def collide(obj0, obj1):
	return (obj0.x, obj0.y) == (obj1.x, obj1.y)

def pickany(objs):
	objs = list(objs)
	return objs[0] if objs else None

class Lep:
	color = 255, 255, 255
	def __init__(self, pos):
		self.x, self.y = pos
		self.flyseed = random.random() * 1000
		self.charged = True
		self.nabbed = False
		self.tfly = 0
		self.xfly, self.yfly = random.uniform(-1, 1), random.uniform(-1, 1)
		self.vxfly, self.vyfly = random.uniform(-1, 1), random.uniform(-1, 1)
	def cannab(self):
		return False
	# Whether you're able to move away from this lep.
	def canmovefrom(self, d):
		return True
	def movefrom(self, d):
#		self.charged = False
		pass
	# Whether this lep prevents you from expending a leap in the given direction as you move away
	def canboost(self, d):
		return False
	# Called when you first enter this lep's space
	def encounter(self):
		pass
	# When you press a direction at this lep, what direction do you actually go?
	def adjustcombo(self, d):
		return d
	def nab(self):
		self.charged = False
		self.nabbed = True
		state.held = self
		state.leps.remove(self)
	def release(self, who):
		self.x = who.x
		self.y = who.y
		self.charged = False
		self.nabbed = False
		state.held = None
		state.leps.append(self)
	def think(self, dt):
		self.tfly -= dt
		if self.tfly <= 0:
			self.tfly = random.uniform(0.1, 0.3)
			self.vxfly = random.uniform(-1, 1) - math.clamp(self.xfly, -2, 2)
			self.vyfly = random.uniform(-1, 1) - math.clamp(self.yfly, -2, 2)
		self.xfly += 6 * dt * self.vxfly
		self.yfly += 6 * dt * self.vyfly
	def draw0(self, topos, zoom):
		dx, dy = 0.5, 0.5
		dx += 0.12 * self.xfly
		dy += 0.12 * self.yfly
		pos = topos((self.x + dx, self.y + dy))
		if self.nabbed:
			dx, dy = 0.8, 0.8
			pos = topos((state.you.x + dx, state.you.y + dy))
		r = T(0.1 * zoom)
		if self.charged:
			pygame.draw.circle(pview.screen, self.color, pos, r)
		else:
			pygame.draw.circle(pview.screen, self.color, pos, r, min(T(4), r))
	def drawarrow(self, topos, d):
		dx, dy = d
		R = math.R(math.atan2(-dx, dy))
		fs = (0, 0.5), (0.05, 0.35), (0, 0.4), (-0.05, 0.35)
		rfs = [R(f) for f in fs]
		ps = [topos((self.x + 0.5 + rfx, self.y + 0.5 + rfy)) for rfx, rfy in rfs]
		pygame.draw.polygon(pview.screen, self.color, ps)
	def draw(self):
		self.draw0(view.worldtoscreen, view.zoom)
	def drawmap(self):
		self.draw0(view.worldtomap, view.mapzoom())


# Lep is movable.
# When leaving the lep in a direction within ds, no movement is expended.
class FlowLep(Lep):
	color = 100, 100, 255
	def __init__(self, pos, ds):
		Lep.__init__(self, pos)
		self.ds = ds
	def cannab(self):
		return True
	def canboost(self, d):
		return self.charged and d in self.ds
	def draw0(self, topos, zoom):
		Lep.draw0(self, topos, zoom)
		if not self.nabbed:
			for d in self.ds:
				self.drawarrow(topos, d)

# Automatically moves you in a certain direction.
class SlingLep(Lep):
	color = 255, 50, 150
	def __init__(self, pos, ds):
		Lep.__init__(self, pos)
		self.ds = ds
	def canmovefrom(self, d):
		return d in self.ds
	def canboost(self, d):
		return self.charged and d in self.ds
	def draw0(self, topos, zoom):
		Lep.draw0(self, topos, zoom)
		if not self.nabbed:
			for d in self.ds:
				self.drawarrow(topos, d)

# Rotates along with all other SpinLeps
class SpinLep(Lep):
	color = 40, 255, 40
	def __init__(self, pos):
		Lep.__init__(self, pos)
	def ds(self):
		ds0 = (0, 1), (1, 0), (0, -1), (-1, 0)
		ds1 = (1, 1), (1, -1), (-1, 1), (-1, -1)
		return ds0 if state.jspin % 2 == 0 else ds1
	def canboost(self, d):
		return self.charged and d in self.ds()
	def movefrom(self, d):
		Lep.movefrom(self, d)
		state.jspin += 1
	def draw0(self, topos, zoom):
		Lep.draw0(self, topos, zoom)
		if not self.nabbed:
			for d in self.ds():
				self.drawarrow(topos, d)

# Doubles your movement
class BoostLep(Lep):
	color = 255, 128, 0
	def __init__(self, pos, n = 2):
		Lep.__init__(self, pos)
		self.n = n
	def adjustcombo(self, d):
		dx, dy = d
		return dx * self.n, dy * self.n

# Refills the leaps
class ChargeLep(Lep):
	color = 200, 0, 255
	def encounter(self):
		sound.play("recharge")
		state.recharge()

# Reach the goal leps to complete the stage.
class GoalLep(Lep):
	color = 255, 255, 0
	def __init__(self, pos):
		Lep.__init__(self, pos)
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
			if currentlep and not currentlep.cannab():
				sound.play("no")
			else:
				if state.held:
					state.held.release(self)
				if currentlep:
					currentlep.nab()
					sound.play("nab")
	def combo(self, d):
		if self.state in ("falling", "rebounding"):
			return
		currentlep = pickany(lep for lep in state.leps if collide(state.you, lep))
		if currentlep:
			if not currentlep.canmovefrom(d):
				sound.play("no")
				return
			d = currentlep.adjustcombo(d)
		dx, dy = d
		if not 0 <= self.x + dx < state.w:
			sound.play("no")
			return
		if not 0 <= self.y + dy:
			sound.play("no")
			return
		dleap = 1
		if currentlep and currentlep.canboost(d):
			dleap -= 1
			currentlep.movefrom(d)
		if state.leaps - dleap < 0:
			sound.play("no")
			return

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
			dx = int("right" in keys) - int("left" in keys)
			dy = int("up" in keys) - int("down" in keys)
			if dx or dy:
				self.combo((dx, dy))
	def canmove(self):
		if state.leaps:
			return True
		currentlep = pickany(lep for lep in state.leps if collide(self, lep))
		ds = [(x, y) for x in (-1, 0, 1) for y in (-1, 0, 1) if x or y]
		if currentlep and any(currentlep.canboost(d) for d in ds):
			return True
		return False
	def think(self, dt):
		self.tmove += dt
		if self.state == "jumping":
			self.thang += dt
			thang = state.thang if self.canmove() else state.thang0
			if self.thang >= thang:
				self.state = "falling"
				self.vy = 8
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
			return "falling", 0
		if self.state == "jumping" and not self.canmove():
			angle = (1 if self.facingright else -1) * 8 * self.lastdy
			return "falling", angle
		if self.state in ("jumping", "rebounding"):
			angle = (1 if self.facingright else -1) * 15 * self.lastdy
			if self.jjumpspec < 0.2:
				return "leap0", angle
			elif self.jjumpspec < 0.4:
				return "leap1", angle
			elif self.jjumpspec < 0.6:
				return "leap2", angle
			elif self.jjumpspec < 0.8:
				return "leap3", angle
			else:
				return "leap4", angle
	def draw(self):
		spec, angle = self.drawspec()
		scale = T(1.3 * view.zoom)
		for j in (3, 2, 1, 0):
			seed = self.tmove + 100 * j + self.x + 100 * self.y
			alpha = math.clamp((1 - 0.2 * j) * (1 - self.tmove), 0, 1)
			factor = 5 * math.exp(-0.5 * j)
			f = math.clamp(factor * self.tmove ** 0.5, 0, 1)
			px, py = math.mix((self.x - self.lastdx, self.y - self.lastdy), (self.x, self.y), f)
			pos = view.worldtoscreen((px + 0.5, py + 0.5))
			if j == 0:
				draw.you(spec, pos, scale, angle, self.facingright)
			else:
				if alpha < 0:
					continue
				draw.you(spec, pos, scale, angle, self.facingright, seed, alpha)


	def drawmap(self):
		pos = view.worldtomap((self.x + 0.5, self.y + 0.5))
		r = T(0.25 * view.mapzoom())
		pygame.draw.circle(pview.screen, (200, 180, 40), pos, r, T(4))



