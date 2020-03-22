import pygame, math
from . import view, pview, state, sound
from .pview import T

def collide(obj0, obj1):
	return (obj0.x, obj0.y) == (obj1.x, obj1.y)

def pickany(objs):
	objs = list(objs)
	return objs[0] if objs else None

class Lep:
	color = 255, 255, 255
	movable = False
	def __init__(self, pos):
		self.x, self.y = pos
		self.charged = True
		self.nabbed = False
	def cannab(self):
		return False
	# Whether you're able to move away from this lep.
	def canmovefrom(self, d):
		return True
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
	def draw0(self, topos, zoom):
		dx, dy = 0.5, 0.5
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
	movable = True
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

# Doubles your movement
class BoostLep(Lep):
	color = 255, 128, 0
	def __init__(self, pos, n = 2):
		Lep.__init__(self, pos)
		self.n = n
	def adjustcombo(self, d):
		dx, dy = d
		return dx * self.n, dy * self.n

# Reach the goal lep to complete the stage.
class GoalLep(Lep):
	color = 255, 255, 0
	def __init__(self, pos):
		Lep.__init__(self, pos)
	def encounter(self):
		if self.charged:
			self.charged = False
			state.ngoal += 1


class You:
	def __init__(self):
		self.x, self.y = 0, 0
		self.state = "grounded"
		state.leaps = state.maxleaps
		self.thang = 0
		self.vy = 0
	def jumpmeter(self):
		if self.state == "grounded":
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
		if self.state == "falling":
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
		dleap = 1
		if currentlep and currentlep.canboost(d):
			dleap -= 1
			currentlep.charged = False
		if state.leaps - dleap < 0:
			sound.play("no")
			return

		self.x += dx
		self.y += dy
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
	def drawmap(self):
		pos = view.worldtomap((self.x + 0.5, self.y + 0.5))
		r = T(0.25 * view.mapzoom())
		pygame.draw.circle(pview.screen, (200, 180, 40), pos, r, T(4))



