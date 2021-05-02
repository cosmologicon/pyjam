from OpenGL.GL import *
from OpenGL.GLU import *
import math, random
from . import state, world, view, enco, sound, graphics, thing, settings, ptextgl
from .pview import T


class Quest(enco.Component):
	goal = None
	shownames = False
	showtab = False
	cantab = True
	ending = False
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
	def controlinfo(self):
		return None
	def objective(self):
		return None
	def color0(self):
		return None
#	def drawend(self):
#		pass
	def titlealpha(self):
		return 0

@Quest()
class HitAllQuest:
	shownames = True
	cantab = False
	def __init__(self):
		self.hit = set()
		self.goal = 6
		sound.playmusic(1, 0)

	def advance(self):
		sound.playmusic(1, 0.7 * (self.progress / self.goal) ** 2)
	
	def think(self, dt):
		iname = state.iname()
		if iname is not None and iname not in self.hit:
			self.hit.add(iname)
			sound.play("tree%d" % len(self.hit))
			self.advance()

	def finish(self):
		view.cutto(trunkscene, 1)
		quests.append(PlantQuest())

	def controlinfo(self):
		if self.progress < 2:
			return "Arrow keys: move"

	def objective(self):
		return "Visit all 6 islands (%d/6 done)" % len(self.hit)

	def titlealpha(self):
		return math.dsmoothfade(self.t, 15, 22, 0.5)

def trunkscene(tcut):
	island = state.getisland("Zodiac")
	if tcut >= 1 and not island.grown:
		island.grow()
		sound.play("find1")
	if tcut >= 3.5 and not island.bloomed:
		island.bloom()
		sound.play("whirr")
	y = world.times(island.up, world.R + 0)
	C, S = math.CS(0.5 * tcut, 300)
	camera = world.linsum(y, 1, island.up, 500, island.forward, C, island.left, S)
	u = island.up
	done = tcut > 6
	return camera, y, u, done


@Quest()
class PlantQuest:
	shownames = True
	cantab = False
	def __init__(self):
		self.firstseed = False
		self.goal = 7
		self.seed = None
		view.self.cdtarget = 640
		sound.playmusic(1, 0.7)

	def advance(self):
		view.self.cdtarget = [640, 640, 640, 640, 720, 900, 1200, 1200][self.progress]

	def think(self, dt):
		iname = state.iname()
		if self.progress == 0:
			if iname == "Zodiac" and not view.pendingcutscene():
				if self.tstep > 1:
					self.advance()
					view.cutto(getseedscene, args=(self,))
					sound.play("find2")
			else:
				self.tstep = 0
		if self.progress == 1:
			if iname not in (None, "Zodiac"):
				if self.tstep > 0.5:
					self.dropto = iname
					self.firstdrop = False
					self.advance()
					view.cutto(dropseedscene, args=(self,))
			else:
				self.tstep = 0
		if self.progress >= 2:
			if self.seed is not None and self.seed.island1 is not None:
				self.advance()
				sound.play("find%d" % (self.progress,))
				self.seed = None
			island = state.getisland(iname)
			if self.seed is None and iname is not None and island.ktree == 1:
				self.seed = thing.Seed(state.getisland("Zodiac"))
				state.effects.append(self.seed)

	def finish(self):
		if self.seed:
			self.seed.alive = False
		for island in state.islands:
			island.grow()
		quests.append(WaterQuest())

	def objective(self):
		if not self.firstseed:
			return "Return to Zodiac Island to retrieve a seed."
		done = max(self.progress - 2, 0)
		return "Bring seeds from Zodiac Island to the other 5 islands (%d/5 done)" % done

def getseedscene(tcut, self):
	island = state.getisland("Zodiac")
	if tcut > 2 and not self.firstseed:
		self.seed = thing.Seed(island)
		self.seed.autodrop = False
		state.effects.append(self.seed)
		self.firstseed = True
	d0, d1 = island.up, state.you.up
	up = math.norm(world.avg(d0, d1))
	y = world.times(up, world.R + 5)
	f = math.norm(world.minus(d1, d0))
	z = math.norm(world.cross(f, y))
	C, S = math.CS(math.fadebetween(tcut, 0, -0.1, 4.5, 0.1), 300)
	camera = world.linsum(y, 1, up, 500, z, C, f, S)
	done = tcut > 4
	return camera, y, up, done

def dropseedscene(tcut, self):
	island = state.getisland(self.dropto)
	if tcut > 2 and not self.firstdrop:
		self.seed.dropto(island)
		self.firstdrop = True
	d0, d1 = island.up, state.you.up
	up = math.norm(world.avg(d0, d1))
	y = world.times(up, world.R + 5)
	f = math.norm(world.minus(d1, d0))
	z = math.norm(world.cross(f, y))
	C, S = math.CS(math.fadebetween(tcut, 0, -0.1, 6, 0.1), 300)
	camera = world.linsum(y, 1, up, 500, z, C, f, S)
	done = tcut > 6
	return camera, y, up, done

def playrumble(self):
	sound.play("rumble")


@Quest()
class WaterQuest:
	shownames = True
	cantab = False
	def __init__(self):
		self.bloomed = set(["Zodiac"])
		self.goal = 6
		self.trodsplash = 0
		self.towed = False
		self.loadmoonrod()
		view.self.cdtarget = 1200
		sound.playmusic(1, 1)
		for island in state.islands:
			island.ztree = 1
			if island.name in self.bloomed:
				island.bloom()
			else:
				island.ktree = 0
				island.bloomed = False
				island.tbloom = 100

	def think(self, dt):
		if self.progress == 0:
			view.cutto(moonrodscene, 1, args=(self,), oncut = playrumble)
			self.advance()
			sound.play("portal")
		else:
			for island in state.islands:
				if island.name not in self.bloomed and island.bloomed:
					self.bloomed.add(island.name)
					self.advance()
					sound.play("whirr")
					sound.play("tree%d" % (self.progress - 1))
		if state.anchored:
			self.towed = True

	def loadmoonrod(self):
		state.moonrod = thing.Moonrod(spot = world.oct0)
		state.moonrod.h = -30

	def controlinfo(self):
		if self.progress < 4:
			if state.anchored:
				return "Space: Release"
			elif state.moonrod is not None and state.moonrod.anchorableto(state.you):
				return "Space: Tow"

	def objective(self):
		if not self.towed:
			return "Press Space near the Tide Summoner to begin towing it. Press Space again to release."
		if self.progress <= 1:
			return "Bring the Tide Summoner to an island to raise the water level. Release it near the island, and then ram into the island to splash water onto its tree."
		done = max(self.progress, 1)
		return "Splash water on each island's tree. (%d/6 done)" % done

	def finish(self):
		quests.append(DiscQuest())

def moonrodscene(tcut, self):
	rod = state.moonrod
	rod.h = math.fadebetween(tcut, 0, -30, 4, 5)
	state.tide = math.fadebetween(tcut, 0, 0, 4, 5)
	while tcut > self.trodsplash:
		spot = rod.forward, rod.left, rod.up
		state.effects.append(thing.Splash(spot, [0, 0, 0], fsplash = 2.5))
		self.trodsplash += 0.05

	y = world.times(rod.up, world.R + 10)
	C, S = math.CS(0.1 * tcut, 300)
	camera = world.linsum(y, 1, rod.up, 500, rod.forward, C, rod.left, S)
	y = world.plus(y, graphics.shake(tcut, 2))
	u = rod.up
	done = tcut > 5
	return camera, y, u, done

@Quest()
class DiscQuest:
	shownames = True
	showtab = True
	def __init__(self):
		self.goal = 2
		self.disc = None
		self.disc3 = None
		view.self.cdtarget = 1200
		sound.playmusic(1, 1)
		for island in state.islands:
			island.grow()
			island.bloom()
		state.tide = 5

	def think(self, dt):
		if self.progress == 0 and not view.pendingcutscene():
			self.loaddisc()
			view.cutto(discscene, 1, args=(self,))
			self.advance()
		if self.progress == 1 and self.tstep > 2 and not view.pendingcutscene():
			if self.disc.touched():
				self.loaddisc3()
				view.cutto(disc3scene, args=(self,))
				self.advance()

	def loaddisc(self):
		if self.disc is None:
			self.disc = thing.Disc(world.oct0, "white")
			state.effects.append(self.disc)
			sound.play("portal")


	def loaddisc3(self):
		if self.disc3 is None:
			self.disc3 = [
				thing.Disc(world.oct1, "red"),
				thing.Disc(world.oct2, "yellow"),
				thing.Disc(world.oct3, "blue"),
			]
			for j, disc in enumerate(self.disc3):
				disc.t = 0.5 * j
				state.effects.append(disc)
			sound.play("portal")

	def objective(self):
		if not self.disc:
			return
		if state.tideat(self.disc.up) < self.disc.h + 1:
			return "Stop your boat on top of the glowing disk now that it's above water."
		return "Lower the water level at the glowing disk, by bringing the Tide Summoner to the opposite side of the planet."

	def finish(self):
		if self.disc3 is None:
			self.loaddisc3()
		quests.append(Act2Quest(self.disc3))
		if self.disc is not None:
			self.disc.fade()

def discscene(tcut, self):
	y = world.times(self.disc.up, world.R)
	across, up = math.CS(math.fadebetween(tcut, 0, 0.2, 6, 1.4), 500)
	C, S = math.CS(1 * tcut, across)
	camera = world.linsum(y, 1, self.disc.up, up, self.disc.forward, C, self.disc.left, S)
	u = self.disc.up
	done = tcut > 6
	return camera, y, u, done

def disc3scene(tcut, self):
	f, l, u = world.oct0
	y = world.times(u, -50)
	u = world.neg(u)
	C, S = math.CS(1 * tcut, 1600)
	camera = world.linsum(y, 1, u, 300, f, C, l, S)
	done = tcut > 8
	return camera, y, u, done



@Quest()
class Act2Quest:
	showtab = True
	def __init__(self, discs):
		self.discs = discs
		self.subquests = [RedQuest(), YellowQuest(), BlueQuest()]
		self.goal = 3
		self.activequest = None
		view.self.cdtarget = 1600
		self.asubquest = None
		self.reset()
		view.self.cdtarget = 1200

	def think(self, dt):
		if state.moonrod is None:
			state.moonrod = thing.Moonrod(spot = world.oct0)
		if self.asubquest is not None and self.asubquest.done:
			self.asubquest = None
			self.advance()
		if self.tstep > 2 and self.asubquest is None:
			for disc, subquest in zip(self.discs, self.subquests):
				if disc.alive and not disc.fading and disc.touched():
					self.activate(disc, subquest)

	def advance(self):
		self.reset()

	def reset(self):
		sound.playmusic(2, 0.7)
		for disc, subquest in zip(self.discs, self.subquests):
			if not subquest.done:
				disc.unfade()
				if disc not in state.effects:
					state.effects.append(disc)
		state.moonrod = thing.Moonrod(spot = world.negspot(world.oct0))
		for island in state.islands:
			island.grow()
			island.bloom()
		state.tide = 5
		if state.anchored is not None:
			state.act()

	
	def activate(self, disc, subquest):
		sound.play("tree1")
		quests.append(subquest)
		for disc in self.discs:
			disc.fade()
		self.asubquest = subquest

	def color0(self):
		return 0, 0, 0

	def objective(self):
		if self.asubquest is not None:
			return None
		return "Stop your boat on top of a glowing disk that's above water. You need to move the Tide Summoner to the opposite side of the planet first."

	def finish(self):
		for disc in self.discs:
			disc.alive = False
		sound.play("win")
		quests.append(Act3Quest())

def introcallback(tcut, self):
	return self.intro(tcut)
def setupcallback(self):
	return self.setup()

class ColorQuest(enco.Component):

	def setup(self):
		sound.playmusic(2, 1)
		for island in state.islands:
			island.ktree = 0
			island.ztree = 1
			island.bloomed = False
			island.tbloom = 0
		self.advance()
		sound.play("rumble")

	def think(self, dt):
		if self.progress == 0 and self.tstep > 1:
			view.cutto(introcallback, oncut=setupcallback, args=(self,))
			self.advance()
		if self.progress == self.goal - 1 and self.exit is None:
			self.exit = thing.Disc(self.getexitspot(), "white")
			state.effects.append(self.exit)
			sound.play("find1")
#			sound.play("portal")
		if self.progress == self.goal - 1 and self.exit.touched():
			self.advance()

	def cleanup(self):
		pass

	def color0(self):
		if self.progress > 0:
			return settings.colors[self.colorname]

	def showexit(self, tcut):
		y = world.times(self.exit.up, world.R)
		across, up = math.CS(math.fadebetween(tcut, 0, 0.2, 6, 1.5), 500)
		C, S = math.CS(1 * tcut, across)
		camera = world.linsum(y, 1, self.exit.up, up, self.exit.forward, C, self.exit.left, S)
		u = self.exit.up
		done = tcut > 3
		return camera, y, u, done

	def finish(self):
		self.cleanup()
		sound.play("portal")
		if self.exit is not None:
			self.exit.fade()


@Quest()
@ColorQuest()
class RedQuest:
	showtab = True
	colorname = "red"
	def __init__(self):
		self.bloomed = set()
		self.goal = 9
		self.exit = None

	def intro(self, tcut):
		f, l, u = world.oct0
		y = 0, 0, 0
		u = world.neg(u)
		C, S = math.CS(1 * tcut, 2400)
		camera = world.linsum(y, 1, f, C, l, S)
		done = tcut > 6
		return camera, y, u, done
	def setup(self):
		state.tide = 4.4
		state.moonrod = thing.Windrod(spot = world.negspot(world.oct1))
	def think(self, dt):
		if self.progress >= 2:
			for island in state.islands:
				if island.name not in self.bloomed and island.bloomed:
					self.bloomed.add(island.name)
					self.advance()
					sound.play("whirr")
					sound.play("find%d" % (self.progress - 2))
	def getexitspot(self):
		return world.negspot(state.moonrod.getspot())

	def objective(self):
		if self.progress < 2:
			return None
		if self.exit is not None:
			return "Stop on the glowing disk when it's above water."
		if self.progress == 2:
			return "Ram into an island to splash water on a tree when the water level at that point is high enough. You will have to move the Tide Summoner to adjust the moon's orbit."
		done = len(self.bloomed)
		return "Splash water on each tree when the water level at that point is high enough. You will have to move the Tide Summoner to adjust the moon's orbit. (%d/6 done)" % done


@Quest()
@ColorQuest()
class YellowQuest:
	showtab = True
	colorname = "yellow"
	def __init__(self):
		self.bloomed = set()
		self.goal = 9
		self.exit = None
	def intro(self, tcut):
		y = world.times(self.raisedisc.up, world.R)
		across, up = math.CS(math.fadebetween(tcut, 0, 0.7, 8, 0.5), math.fadebetween(tcut, 0, 500, 10, 2000))
		C, S = math.CS(0.1 * tcut, across)
		camera = world.linsum(y, 1, self.raisedisc.up, up, self.raisedisc.forward, C, self.raisedisc.left, S)
		u = self.raisedisc.up
		state.tide = math.fadebetween(tcut, 4, 8, 6, 2)
		done = tcut > 8
		return camera, y, u, done
	def setup(self):
		state.tide = 2
		state.moonrod = thing.Moonrod(spot = world.oct0)
		self.raisedisc = thing.Raisedisc(spot = world.negspot(world.oct0))
		state.effects.append(self.raisedisc)
	def think(self, dt):
		if self.progress >= 2:
			for island in state.islands:
				if island.name not in self.bloomed and island.bloomed:
					self.bloomed.add(island.name)
					self.advance()
					sound.play("whirr")
					sound.play("find%d" % (self.progress - 2))
	def getexitspot(self):
		return world.oct0
	def cleanup(self):
		self.raisedisc.fade()
	def objective(self):
		if self.exit is not None:
			return "Stop on the white disk when it's above water. You may need to raise the tide with the black disk first."
		if state.tide < 4.5:
			return "The moon has moved away, weakening the tides. Touch the black disk when it's above water to bring the moon back."
		done = len(self.bloomed)
		return "Splash water on each tree when the water level at that point is high enough. (%d/6 done)" % done

		
	
@Quest()
@ColorQuest()
class BlueQuest:
	colorname = "blue"
	def __init__(self):
		self.bloomed = []
		self.goal = 9
		self.exit = None
	def setup(self):
		view.self.cdtarget = 1200
		state.tide = 5
		state.moonrod = thing.Moonrod(spot = world.oct0)
		self.sequencer = thing.Sequencer(spot = world.negspot(world.oct0))
		state.effects.append(self.sequencer)
		self.sequencer.seq = self.randomseq()
		self.reset()
	def reset(self):
		self.bloomed = []
		self.progress = 2
		for island in state.islands:
			island.ktree = 0
			island.ztree = 1
			island.bloomed = False
			island.tbloom = 0
	def intro(self, tcut):
		y = world.times(self.sequencer.up, world.R)
		across, up = math.CS(math.fadebetween(tcut, 0, 1.4, 10, 0.2), 500)
		C, S = math.CS(0.5 * tcut, across)
		camera = world.linsum(y, 1, self.sequencer.up, up, self.sequencer.forward, C, self.sequencer.left, S)
		u = self.sequencer.up
		done = tcut > 10
		return camera, y, u, done
	def think(self, dt):
		if self.progress >= 2:
			for island in state.islands:
				if island.name not in self.bloomed and island.bloomed:
					self.newbloom(island.name)
		if self.exit is not None:
			self.sequencer.alive = False
	def newbloom(self, name):
		self.bloomed.append(name)
		if seqmatch(self.sequencer.seq, self.bloomed):
			self.advance()
			sound.play("whirr")
			sound.play("find%d" % (self.progress - 2))
		else:
			self.reset()
			sound.play("no")
	def cleanup(self):
		self.sequencer.alive = False
	def getexitspot(self):
		return world.negspot(world.oct0)
	def randomseq(self):
		seq = [island.name for island in state.islands]
		random.shuffle(seq)
		return seq
	def objective(self):
		if self.exit is not None:
			return "Stop on the glowing disk when it's above water."
		done = len(self.bloomed)
		return "Splash water on each tree in order. Follow the sequence shown in the hologram. (%d/6 done)" % done



def seqmatch(seq0, seq):
	for j in range(len(seq0)):
		if [seq0[(j+k)%len(seq0)] for k in range(len(seq))] == seq:
			return True
	return False

class Qhack:
	goal = None
	shownames = False
	showtab = False
	cantab = True
	ending = False
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
	def controlinfo(self):
		return None
	def objective(self):
		return None
	def color0(self):
		return None
	def drawend(self):
		pass
	def titlealpha(self):
		return 0



class Act3Quest(Qhack):
	def __init__(self):
		Qhack.__init__(self)
		self.goal = 4
		self.discs = {
			"white": thing.Disc(world.oct0, "white"),
			"red": thing.Disc(world.oct1, "red"),
			"yellow": thing.Disc(world.oct2, "yellow"),
			"blue": thing.Disc(world.oct3, "blue"),
		}
		for disc in self.discs.values():
			state.effects.append(disc)
		self.seq = self.randomseq(3)
		self.hseq = []
		self.lasttouched = None
		view.self.cdtarget = 1600
		self.rod = thing.Zanyrod(spot = world.oct0)
		state.moonrod = self.rod
		state.tide = 16
		state.dmoon = 20
		state.cfactor = 10
		view.cutto(introcallback, 1, args=(self,))

	def randomseq(self, n):
		seq = []
		while len(seq) < n:
			color = random.choice(list(self.discs))
			if not seq:
				seq.append(color)
			elif color != seq[-1]:
				if len(seq) != n - 1 or color != seq[0]:
					seq.append(color)
		return seq

	def touched(self):
		for color, disc in self.discs.items():
			if disc.touched(vmin = 1000):
				return color
		return None
	
	def newtouched(self):
		color = self.touched()
		if color != self.lasttouched:
			self.lasttouched = color
			return color
		return None

	def intro(self, tcut):
		sound.playmusic(3, 1)
		if tcut < 6:
			if tcut < 1.5:
				obj = self.discs["red"]
				angle = math.fadebetween(tcut, 0, 0.2, 1.5, 0.4)
			elif tcut < 3:
				obj = self.discs["yellow"]
				angle = math.fadebetween(tcut, 1.5, 0.3, 3, 0.5)
			elif tcut < 4.5:
				obj = self.discs["blue"]
				angle = math.fadebetween(tcut, 3, 0.4, 4.5, 0.6)
			else:
				obj = self.discs["white"]
				angle = math.fadebetween(tcut, 4.5, 0.5, 6, 0.7)
			y = world.times(obj.up, world.R)
			across, up = math.CS(angle, 500)
			C, S = math.CS(0.1 * tcut, across)
			camera = world.linsum(y, 1, obj.up, up, obj.forward, C, obj.left, S)
			u = obj.up
			y = world.plus(y, graphics.shake(tcut, math.fadebetween(tcut, 0, 0, 6, 15)))
			done = tcut > 10
			return camera, y, u, done
		f, l, u = world.oct0
		y = 0, 0, 0
		u = world.neg(u)
		C, S = math.CS(1 * tcut, math.fadebetween(tcut, 6, 1600, 10, 2400))
		camera = world.linsum(y, 1, f, C, l, S)
		y = world.plus(y, graphics.shake(tcut, 15))
		done = tcut > 10
		return camera, y, u, done


	def think(self, dt):
		Qhack.think(self, dt)
		state.moonrod = self.rod
		view.self.shake = 10
		color = self.newtouched()
		if color:
			if not (self.hseq and color == self.hseq[-1]):
				self.touch(color)
		a = math.fadebetween(self.t, 0, 0, 1, 0.3)
		for j, island in enumerate(state.islands):
			island.ztree = 1
			island.ktree = 0.7 + a * math.sin(j + (4 + 0.3 * j) * self.t)

	def advance(self):
		Qhack.advance(self)
		self.hseq = []
		self.seq = self.randomseq(self.progress + 3)
		state.tide = 5 + 3 * self.progress
	
	def touch(self, color):
		self.hseq.append(color)
		if seqmatch(self.seq, self.hseq):
			sound.play("find%d" % len(self.hseq))
			if len(self.seq) == len(self.hseq):
				sound.play("portal")
				self.advance()
		else:
			sound.play("noo")
			while not seqmatch(self.seq, self.hseq):
				self.hseq.pop(0)
		
	def color0(self):
		fspeed = [1, 0.8, 0.7, 0.6, 0.5][self.progress]
		return settings.colors[self.seq[int(self.t / fspeed) % len(self.seq)]]

	def objective(self):
		if len(self.seq) == 1:
			return "Touch the disk whose color matches the sky."
		return "Touch the disks in sequence, following the order of colors in the sky. You can start anywhere in the sequence."

	def finish(self):
		Qhack.finish(self)
		view.cutto(outro, 2)
		sound.play("win")
		quests.append(WaitQuest())

def outro(tcut):
	f, l, u = world.oct0
	y = 0, 0, 0
	u = world.neg(u)
	C, S = math.CS(1 * tcut, math.fadebetween(tcut, 0, 2000, 6, 2600))
	camera = world.linsum(y, 1, f, C, l, S)
	y = world.plus(y, graphics.shake(tcut, 15))
	done = tcut > 6
	return camera, y, u, done

@Quest()
class WaitQuest:
	def __init__(self):
		self.goal = 1
	def think(self, dt):
		if self.progress == 0 and not view.pendingcutscene():
			self.advance()
	def finish(self):
		quests.append(EndQuest())

@Quest()
class EndQuest:
	over = False
	ending = True

	def think(self, dt):
		sound.playmusic(3, math.fadebetween(self.t, 0, 1, 12, 0))
		if self.t > 10:
			self.over = True

	def drawend(self):
		if False:
			y = 0, 0, 0
			spot = world.renorm([math.norm([-0.9, 0, -0.1]), [0, -1, 0], math.norm([-0.1, 0, 0.9])])
			f, l, u = spot
			camera = world.times(f, -1000)

			glPushMatrix()
			glDisable(GL_LIGHTING)
			glDisable(GL_TEXTURE_2D)
			view.perspectivestars()
			gluLookAt(*camera, *y, *u)
			glScale(500, 500, 500)
			glCallList(graphics.lists.stars)
			glPopMatrix()

			glClear(GL_DEPTH_BUFFER_BIT)

			glPushMatrix()
			view.perspective()
			gluLookAt(*camera, *y, *u)
			glPushMatrix()
			glTranslate(-5000, 0, 0)
			graphics.draw(youtoo = False)
			glPopMatrix()
			glCallLists(graphics.lists.you)
			glPopMatrix()
		
		alpha = math.fadebetween(self.t, 2, 0, 3, 1)
		if alpha:
			ptextgl.draw("You have successfully escaped from\nthe planet of the Tide Summoner!", center = T(640, 140), fontname = "TradeWinds", fontsize = T(50),
				color = (255, 255, 224), shade = 1.5, alpha = alpha)
		alpha = math.fadebetween(self.t, 3, 0, 4, 1)
		if alpha:
			ptextgl.draw("The question now remains,\nWhere will you wind up next?", midbottom = T(640, 420), fontname = "TradeWinds", fontsize = T(50),
				color = (255, 255, 224), shade = 1.5, alpha = alpha)
		alpha = math.fadebetween(self.t, 4, 0, 5, 1)
		if alpha:
			ptextgl.draw("Thank you for playing!", midbottom = T(640, 600), fontname = "TradeWinds", fontsize = T(50),
				color = (255, 255, 224), shade = 1.5, alpha = alpha)


quests = []

def init():
	state.tide = 0
#	quests.append(HitAllQuest())
#	quests.append(DiscQuest())
#	quests.append(Act3Quest())

	# Act 1
	if True:
		quests.append(HitAllQuest())
	# Jump to Act 2
	if False:
		q = WaterQuest()
		q.loadmoonrod()
		q.trodsplash = 1000
		q.moonrodscene(100)
		q = DiscQuest()
		q.loaddisc3()
		q.finish()
	# Jump to Act 3
	if False:
		quests.append(Act3Quest())

def think(dt):
	for quest in quests:
		quest.think(dt)
	quests[:] = [q for q in quests if not q.done]

def objectives():
	objs = [q.objective() for q in quests]
	return reversed([obj for obj in objs if obj])

def shownames():
	return any(q.shownames for q in quests)

def controlinfo():
	ret = None
	for quest in quests:
		qinfo = quest.controlinfo()
		if qinfo:
			ret = qinfo
			break
	showtab = any(q.showtab for q in quests) and state.ntabs < 5
	if showtab:
		if ret:
			ret += "\nTab: zoom"
		else:
			ret = "Tab: zoom"
	showhint = not settings.easymode and quests and all(quest.tstep > 60 for quest in quests)
	if showhint:
		if ret:
			return ret + "\nHold Ctrl for hint"
		else:
			return "Hold Ctrl for hint"
	
	return ret

def cantab():
	return any(q.cantab for q in quests)

def color0():
	for quest in quests[::-1]:
		color0 = quest.color0()
		if color0:
			return color0
	return 0, 0, 0

def skip():
	if quests:
		quests[-1].finish()

def pourwater(up):
	for island in state.islands:
		if not island.bloomed and state.tideat(island.up) > 4:
			d = world.R * math.length(world.minus(island.up, up))
			if d < 10:
				island.bloom()

def ending():
	return quests and all(q.ending for q in quests)
def drawend():
	for q in quests:
		q.drawend()
def done():
	return ending() and all(q.over for q in quests)

def titlealpha():
	return max(q.titlealpha() for q in quests) if quests else 0


