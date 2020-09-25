import math
from . import state, world, view, enco


class Quest(enco.Component):
	goal = None
	def __init__(self):
		self.progress = 0
		self.done = False
		self.t = 0
		self.tstep = 0
	def think(self, dt):
		self.t += dt
		self.tstep += dt
	def advance(self):
		self.progress += 1
		self.tstep = 0
		if self.goal is not None and self.progress >= self.goal:
			self.finish()

	def finish(self):
		self.done = True
	def objective(self):
		return None


@Quest()
class HitAllQuest:
	def __init__(self):
		self.hit = set()
		self.goal = 6
	
	def think(self, dt):
		iname = state.iname()
		if iname is not None and iname not in self.hit:
			self.hit.add(iname)
			self.advance()

	def finish(self):
		view.cutto(trunkscene, 2)
		quests.append(PlantQuest())

	def objective(self):
		return "Visit all 6 islands (%d/6 done)" % len(self.hit)

def trunkscene(tcut):
	island = state.getisland("Zodiac")
	if tcut >= 1:
		island.grow()
	if tcut >= 3.5:
		island.bloom()
	y = world.times(island.up, world.R + 0)
	C, S = math.CS(0.5 * tcut, 300)
	camera = world.linsum(y, 1, island.up, 500, island.forward, C, island.left, S)
	u = island.up
	done = tcut > 6
	return camera, y, u, done


@Quest()
class PlantQuest:
	def __init__(self):
		self.firstseed = False
		self.goal = 7
		self.seed = None

	def advance(self):
		view.self.cdtarget = [640, 640, 640, 640, 720, 900, 1200, 1200][self.progress]

	def think(self, dt):
		from . import thing
		iname = state.iname()
		if self.progress == 0:
			if iname == "Zodiac" and not view.pendingcutscene():
				if self.tstep > 1:
					self.advance()
					view.cutto(self.getseedscene)
			else:
				self.tstep = 0
		if self.progress == 1:
			if iname not in (None, "Zodiac"):
				if self.tstep > 0.5:
					self.dropto = iname
					self.firstdrop = False
					self.advance()
					view.cutto(self.dropseedscene)
			else:
				self.tstep = 0
		if self.progress >= 2:
			if self.seed is not None and not self.seed.alive:
				self.seed = None
				self.advance()
			island = state.getisland(iname)
			if self.seed is None and iname is not None and island.ktree == 1:
				self.seed = thing.Seed(state.getisland("Zodiac"))
				state.effects.append(self.seed)

	def finish(self):
		quests.append(WaterQuest())

	def getseedscene(self, tcut):
		from . import thing
		island = state.getisland("Zodiac")
		if tcut > 2 and not self.firstseed:
			self.seed = thing.Seed(island)
			self.seed.autodrop = False
			state.effects.append(self.seed)
			self.firstseed = True
		y = world.times(island.up, world.R + 0)
		C, S = math.CS(0.1 * tcut, 300)
		camera = world.linsum(y, 1, island.up, 500, island.forward, C, island.left, S)
		u = island.up
		done = tcut > 4
		return camera, y, u, done

	def dropseedscene(self, tcut):
		from . import thing
		island = state.getisland(self.dropto)
		if tcut > 2 and not self.firstdrop:
			self.seed.dropto(island)
			self.firstdrop = True
		y = world.times(island.up, world.R + 0)
		C, S = math.CS(-0.1 * tcut, 300)
		camera = world.linsum(y, 1, island.up, 500, island.forward, C, island.left, S)
		u = island.up
		done = tcut > 6
		return camera, y, u, done

	def objective(self):
		done = max(self.progress - 2, 0)
		return "Bring seeds from Zodiac Island to the other 5 islands (%d/5 done)" % done

@Quest()
class WaterQuest:
	def __init__(self):
		self.bloomed = set(["Zodiac"])
		self.goal = 6

	def think(self, dt):
		from . import thing
		if self.progress == 0:
			state.moonrod = thing.Moonrod(spot = world.oct0)
			state.moonrod.h = -20
			self.trodsplash = 0
			view.cutto(self.moonrodscene, 1)
			self.advance()
		else:
			for island in state.islands:
				if island.name not in self.bloomed and island.bloomed:
					self.bloomed.add(island.name)
					self.advance()

	def moonrodscene(self, tcut):
		from . import thing
		rod = state.moonrod
		rod.h = math.fadebetween(tcut, 0, -20, 4, 5)
		state.tide = math.fadebetween(tcut, 0, 0, 4, 5)
		while tcut > self.trodsplash:
			spot = rod.forward, rod.left, rod.up
			state.effects.append(thing.Splash(spot, [0, 0, 0]))
			self.trodsplash += 0.1

		y = world.times(rod.up, world.R + 10)
		C, S = math.CS(0.1 * tcut, 300)
		camera = world.linsum(y, 1, rod.up, 500, rod.forward, C, rod.left, S)
		u = rod.up
		done = tcut > 5
		return camera, y, u, done

	def objective(self):
		done = max(self.progress, 1)
		return "Bring the Tidal Stone to each island to raise the water level. Release the stone near the island, and splash water onto the island's tree. (%d/6 done)" % done

	def finish(self):
		quests.append(DiscQuest())

@Quest()
class DiscQuest:
	def __init__(self):
		self.goal = 2
		self.disc = None
		self.disc3 = None

	def think(self, dt):
		if self.progress == 0 and not view.pendingcutscene():
			view.cutto(self.discscene, 1)
			self.advance()
		if self.progress == 1 and self.tstep > 2 and not view.pendingcutscene():
			if self.disc.touched():
				view.cutto(self.disc3scene)
				self.advance()

	def discscene(self, tcut):
		from . import thing
		if self.disc is None:
			self.disc = thing.Disc(world.oct0, "white")
			state.effects.append(self.disc)
		y = world.times(self.disc.up, world.R)
		across, up = math.CS(math.fadebetween(tcut, 0, 0.2, 6, 1.6), 500)
		C, S = math.CS(1 * tcut, across)
		camera = world.linsum(y, 1, self.disc.up, up, self.disc.forward, C, self.disc.left, S)
		u = self.disc.up
		done = tcut > 5
		return camera, y, u, done

	def disc3scene(self, tcut):
		from . import thing
		if self.disc3 is None:
			self.disc3 = [
				thing.Disc(world.oct1, "red"),
				thing.Disc(world.oct2, "yellow"),
				thing.Disc(world.oct3, "blue"),
			]
			for disc in self.disc3:
				state.effects.append(disc)
		f, l, u = world.oct0
		y = world.times(u, -50)
		u = world.neg(u)
		C, S = math.CS(1 * tcut, 1600)
		camera = world.linsum(y, 1, u, 300, f, C, l, S)
		done = tcut > 8
		return camera, y, u, done

	def objective(self):
		return "The water is low enough to expose the portal. Park your boat at the portal."
		return "Bring the Tidal Stone to the opposite side from the portal, to lower the water level at the portal."

	def finish(self):
		print("done")


quests = []

def init():
	quests.append(HitAllQuest())
#	quests.append(DiscQuest())

def think(dt):
	for quest in quests:
		quest.think(dt)
	quests[:] = [q for q in quests if not q.done]

def objectives():
	objs = [q.objective() for q in quests]
	return reversed([obj for obj in objs if obj])

def skip():
	if quests:
		quests[-1].finish()

def pourwater(up):
	for island in state.islands:
		if not island.bloomed and state.tideat(island.up) > 4:
			d = world.R * math.length(world.minus(island.up, up))
			if d < 10:
				island.bloom()

