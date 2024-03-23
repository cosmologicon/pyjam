import random, pygame, math, os, pickle, bisect
from collections import defaultdict, Counter
from functools import cache
from . import settings, grid, view, pview, ptext, graphics, hud, render

def cycle_opts(value, values, reverse = False):
	if value not in values:
		return values[0]
	j = values.index(value)
	return values[(j + (-1 if reverse else 1)) % len(values)]


# s1 <= s2 for multisets as lists
@cache
def issubset(s1, s2):
	return all(s1.count(c) <= s2.count(c) for c in s1)
@cache
def removesymbols(s1, s2):
	s = Counter(s1)
	for c in s2:
		s[c] -= 1
	return "".join(c * n for c, n in sorted(s.items()))
assert removesymbols("aabaacc", "abca") == "aac"

@cache
def symbollit(symbols, lits):
	s = Counter(symbols)
	l = Counter(lits)
	return [(c, j < l[c]) for c, n in sorted(s.items()) for j in range(n)]

class Planet:
	def __init__(self, pH, supply, demand):
		self.pH = pH
		self.supply = "".join(sorted(supply))
		self.demand = "".join(sorted(demand))
		self.tubes = []
		self.supplied = False
		self.t = 0
		self.exports = ""
	# Update the planet's supplied bit and imports/exports based on the resources coming in.
	# Returns a list of tubes that are newly supplied.
	def checksupply(self):
		exports = self.exports
		self.imports = "".join(sorted((tube.supplyto(self) or "") for tube in self.tubes))
		self.supplied = issubset(self.demand, self.imports)
		self.exports0 = removesymbols(self.supply + self.imports, self.demand)
		self.exports = self.exports0 if self.supplied else ""
		ret = []
		if self.exports:
			for tube in self.tubes:
				if tube.supplier is not self: continue
				wassupplied = tube.supplied
				tube.supplied = self.tryclaim(tube.carry)
				if tube.supplied and not wassupplied: ret.append(tube)
		return ret
	# For a newly created tube, recommend an export. Does not claim said export.
	def firstexport(self, consumer):
		if not self.exports:
			return ""
		wanted = removesymbols(consumer.demand, consumer.imports)
		if not wanted:
			return self.exports[0]
		for export in self.exports:
			if export in wanted:
				return export
		return self.exports[0]
	# For a tube for which this is the supplier, try to claim an export.
	# Returns whether successful.
	def tryclaim(self, symbol):
		if symbol in self.exports:
			self.exports = removesymbols(self.exports, symbol)
			return True
		return False
	def think(self, dt):
		self.t += dt
	def draw(self, outline = False):
		color = (160, 200, 240)
		if not self.supplied:
			color = (100, 80, 80)
		graphics.drawdomeatH(self.pH, color, outline = outline)
#		pygame.draw.circle(pview.screen, (255, 0, 255), view.DconvertG(grid.GconvertH(self.pH)), 3)
	def drawbubbles(self):
		symbols = []
		for symbol in self.demand:
			met = symbol in self.imports
			if met and settings.showdemand == "off":
				continue
			strength = 1 if not met or settings.showdemand == "on" else 0.2
			symbols.append((symbol, strength))
		if symbols:
			graphics.drawbubbleatH(self.pH, symbols, False)
		symbols = []
		if self.supplied:
			for symbol, lit in symbollit(self.exports0, self.exports):
				if not lit and settings.showsupply == "off":
					continue
				strength = 1 if lit or settings.showsupply == "on" else 0.2
				symbols.append((symbol, strength))
		else:
			for symbol in self.exports0:
				symbols.append((symbol, 0.2))
		if symbols:
			graphics.drawbubbleatH(self.pH, symbols, True)
	def draw_old(self, glow = False):
		if not self.pH in visible:
			return
		xG, yG = grid.GconvertH(self.pH)
		color = (180, 180, 180) if self.supplied else (60, 60, 60)
		color = math.imix(color, (255, 255, 255), 0.5) if glow else color
		pygame.draw.circle(pview.screen, color, view.DconvertG((xG, yG)), view.DscaleG(0.4))
		for j, symbol in enumerate(reversed(self.demand)):
			beta = 0.3 if symbol in self.imports else 1
			beta *= hud.factor(symbol, "import")
			pG = xG - 0.1 - 0.25 * j, yG + 0.3
			graphics.drawsymbolat(symbol, view.DconvertG(pG), 0.5, beta)
		if not self.supplied:
			symbols = [(symbol, False) for symbol in self.supply]
		else:
			symbols = symbollit(self.exports0, self.exports)
		for j, (symbol, lit) in enumerate(symbols):
			beta = 1 if lit else 0.3
			beta *= hud.factor(symbol, "export")
			pG = xG + 0.1 + 0.25 * j, yG - 0.3
			graphics.drawsymbolat(symbol, view.DconvertG(pG), 0.5, beta)
		
	def info(self):
		return [
			f"posH: {self.pH}",
			f"posG: {grid.GconvertH(self.pH)}",
			f"imports: {self.imports}",
			f"demand: {self.demand}",
			f"supply: {self.supply}",
			f"exports0: {self.exports0}",
			f"exports: {self.exports}",
			f"supplied: {self.supplied}",
		]
		return lines

class Tube:
	def __init__(self, pH0):
		self.pHs = [pH0]
		self.built = False
		self.carry = ""
		self.supplier = planetat(pH0)
		self.consumer = None
		self.supplied = False
		self.t = 0
		self.dirs = []
		self.alongpGs = None
	def think(self, dt):
		self.t += dt
	# Does not check for legality.
	def add(self, pH):
		self.dirs.append(grid.dirH(self.pHs[-1], pH))
		self.pHs.append(pH)
		if planetat(pH):
			self.complete()
	def complete(self):
		self.consumer = planetat(self.pHs[-1])
		self.built = True
		if False:  # Needed for crossing paths feature
			straights = [grid.isrowH(self.pHs[j-1], self.pHs[j], self.pHs[j+1])
				for j in range(1, len(self.pHs) - 1)]
			straights = [False] + straights + [False]
			self.straights = dict(zip(self.pHs, straights))
		self.alongpGs = [
			grid.GconvertH(math.mix(self.pHs[0], self.pHs[1], 0.4)),
			grid.GconvertH(math.mix(self.pHs[0], self.pHs[1], 0.5)),
		]
		for j in range(1, len(self.pHs) - 1):
			if not grid.isrowH(*self.pHs[j-1:j+2]):
				pG0, pG1, pG2 = [grid.GconvertH(pH) for pH in self.pHs[j-1:j+2]]
				xG0, yG0 = pG0
				xG1, yG1 = pG1
				xG2, yG2 = pG2
				dx0, dy0 = math.norm((xG1 - xG0, yG1 - yG0))
				xGc, yGc = xG2 - xG1 + xG0, yG2 - yG1 + yG0
				dx1 = math.mix(xG0, xG1, 0.5) - xGc
				dy1 = math.mix(yG0, yG1, 0.5) - yGc
				for jtheta in range(11):
					C, S = math.CS(jtheta / 12 * math.tau / 6)
					xG = xGc + C * dx1 + S * dx0
					yG = yGc + C * dy1 + S * dy0
					self.alongpGs.append((xG, yG))
			self.alongpGs.append(grid.GconvertH(math.mix(self.pHs[j], self.pHs[j+1], 0.5)))
		self.alongpGs.append(grid.GconvertH(math.mix(self.pHs[-2], self.pHs[-1], 0.6)))
		d = 0
		self.alongds = [d]
		for j in range(1, len(self.alongpGs)):
			d += math.distance(self.alongpGs[j-1], self.alongpGs[j])
			self.alongds.append(d)
	def nexts(self):
		for pH in grid.HadjsH(self.pHs[-1]):
			if pH in self.pHs:
				continue
			if isfree(pH):
				if len(self.pHs) > 1 and grid.issharpH(self.pHs[-2], self.pHs[-1], pH):
					continue
				yield pH
				continue
			obj = objat(pH)
			if isinstance(obj, Planet):
				if obj is not self.supplier and len(self.pHs) > 1:
					if grid.issharpH(self.pHs[-2], self.pHs[-1], pH):
						continue
					yield pH
			elif isinstance(obj, Tube):
				if False:  # Crossing paths feature
					if not obj.straights[pH]:
						continue
					pH2 = tuple(grid.HpastH(self.pHs[-1], pH))
					if pH2 in self.pHs:
						continue
					if isfree(pH2):
						yield pH2
					elif planetat(pH2) not in [None, self.supplier]:
						yield pH2
	def cango(self, pH):
		return pH in self.nexts()
	def trybuild(self, pH):
		if self.cango(pH):
			self.add(pH)
			return True
		return False
	# Click interface. Either add to the end or remove the end.
	def tryclick(self, pH):
		if self.trybuild(pH):
			return 1
		if pH == self.pHs[-1]:
			self.pHs.pop()
			if self.dirs:
				self.dirs.pop()
			if not self.pHs:
				self.supplier = None
			return -1
		return 0
	# Drag interface. Either add to the end or back up 1.
	def trydrag(self, pH):
		if self.trybuild(pH):
			return 1
		if len(self.pHs) > 1 and pH == self.pHs[-2]:
			self.pHs.pop()
			self.dirs.pop()
			return -1
		return 0
	def pGalong(self, d):
		if not self.alongpGs: return None
		if d < 0: return 
		j = bisect.bisect(self.alongds, d) - 1
		if not 0 <= j < len(self.alongpGs) - 1: return None
		return math.interp(d, self.alongds[j], self.alongpGs[j],
			self.alongds[j+1], self.alongpGs[j+1])
	def flip(self):
		self.supplier, self.consumer = self.consumer, self.supplier
		self.pHs = list(reversed(self.pHs))
		self.dirs = [grid.dirH(self.pHs[j], self.pHs[j + 1]) for j in range(len(self.pHs) - 1)]
		resolvenetwork()
	def initializecarry(self):
		self.carry = self.supplier.firstexport(self.consumer)
	def togglecarry(self):
		cancarry = [""] + sorted(set(self.supplier.exports))
		self.carry = cycle_opts(self.carry, cancarry)
		resolvenetwork()
	# What resource, if any, do I supply to this planet?
	def supplyto(self, planet):
		return self.carry if planet is self.consumer and self.supplied and self.carry else None
	def getcolor(self):
		return tuple(settings.getcolor(self.carry) if self.carry else (180, 180, 180))
	def draw(self, mix = None, outline = False):
		pDs = [view.DconvertG(grid.GconvertH(pH)) for pH in self.pHs]
		color = self.getcolor()
		if mix is not None:
			color = math.imix(color, mix, 0.2)
		if not self.supplied:
			color = math.imix((0, 0, 0), color, 0.5)
		if self.dirs:
			pH = math.mix(self.pHs[0], self.pHs[1], 0.5)
			graphics.drawdockatH(pH, self.dirs[0], outline = outline)
		if self.consumer:
			pH = math.mix(self.pHs[-2], self.pHs[-1], 0.5)
			graphics.drawdockatH(pH, (self.dirs[-1] + 3) % 6, outline = outline)
		elif self.dirs:
			graphics.drawbuildatH(self.pHs[-1], color, self.dirs[-1], outline = outline)
		for j in range(len(self.dirs) - 1):
			graphics.drawtubeatH(self.pHs[j+1], color, self.dirs[j], self.dirs[j+1], outline = outline)
	def drawglow(self):
		objs = [self.supplier, self]
		if self.consumer:
			objs.append(self.consumer)
		graphics.renderqueue()
		for obj in objs:
			obj.draw(outline = True)
		graphics.renderqueue()
		for obj in objs:
			obj.draw()
		graphics.renderqueue()
	def drawcarry(self):
		if not self.carry:
			return
		speed = 3 if self.supplied else 1
		symbol = "X" if not self.supplied and self.supplier.t % 1 < 0.5 else self.carry
		strength = hud.factor(self.carry, "tube")
		d = self.supplier.t * speed % 3
		size = 0.4 * (view.VscaleG / 40) ** -0.4
		while True:
			pG = self.pGalong(d)
			if pG is None: break
			pD = view.DconvertG(pG, zG = render.rtube)
			graphics.drawsymbolat(symbol, pD, size, strength)
			d += 3
	def draw_old(self, glow = False):
		pDs = [view.DconvertG(grid.GconvertH(pH)) for pH in self.pHs]
		color = settings.colorcodes.get(self.carry, (160, 160, 160))
		mix = (255, 255, 255) if glow else (0, 0, 0)
		color = math.imix(color, mix, 0.5)
		for pD in pDs:
			pygame.draw.circle(pview.screen, color, pD, view.DscaleG(0.2))
		if len(pDs) >= 2:
			pygame.draw.lines(pview.screen, color, False, pDs, view.DscaleG(0.1))
		if self.carry and self.supplied:
			d = self.supplier.t * 3 % 3
			while True:
				pH = self.pHalong(d)
				if pH is None: break
				pD = view.DconvertG(grid.GconvertH(pH))
				beta = hud.factor(self.carry, "tube")
				graphics.drawsymbolat(self.carry, pD, 0.7, beta)
				d += 3
				
	def info(self):
		return [
			f"length: {len(self.pHs) - 1}",
			f"Carry {self.carry}",
			f"From {self.supplier.pH} to {self.consumer.pH}",
			f"Supplied {self.supplied}",
		]

class Rock:
	def __init__(self, pH):
		self.pH = pH
	def draw(self, glow = False):
		if not self.pH in visible:
			return
		graphics.drawrockatH(self.pH)
#		color = (30, 60, 60)
#		color = math.imix(color, (255, 255, 255), 0.5) if glow else color
#		graphics.drawcircleH(self.pH, color, 0.4)
	def info(self):
		return ["Just a rock."]

def resolvenetwork():
	# Shut down everything.
	for tube in tubes:
		tube.supplied = False
#	for planet in planets:
#		planet.checksupply()
	# Planets with unaccounted for exports.
	suppliers = [planet for planet in planets if planet.supplied]
	suppliers = list(planets)
	while suppliers:
		newsuppliers = []
		for planet in suppliers:
			for tube in planet.checksupply():
				if tube.consumer not in newsuppliers:
					newsuppliers.append(tube.consumer)
		suppliers = newsuppliers

def aimcamera():
	from . import view
	if not visible:
		view.xG0, view.yG0 = 0, 0
		view.zoomto(40)
		return
	xGs, yGs = zip(*[grid.GconvertH(pG) for pG in visible])
	view.xG0, view.yG0 = sum(xGs) / len(xGs), sum(yGs) / len(yGs)
	# The scale that would fit everything to the screen.
	scale = pview.s0 / math.hypot(max(xGs) - min(xGs), max(yGs) - min(yGs))
	# Bias toward medium values.
	scale = 40 * (scale / 40) ** 0.7
	view.zoomto(scale)
	

def init():
	from . import quest
	global board, visible, tubes, planets, rocks
	board = { pH: None for pH in grid.Hrect(20) }
	visible = set()
	tubes = []
	planets = []
	rocks = []
	if level == "tutorial":
		quest.quests.append(quest.TutorialQuest())
	if level == "easy":
		quest.quests.append(quest.EasyQuest())
	if level == "hard":
		quest.quests.append(quest.HardQuest())
	aimcamera()


def setvisibility(R):
	global visible
	visible = set(pH for pH in board if math.length(grid.GconvertH(pH)) <= R)

def addvisibility(R, pH0 = (0, 0)):
	global visible
	pG0 = grid.GconvertH(pH0)
	visible |= set(pH for pH in board if math.distance(grid.GconvertH(pH), pG0) <= R)


def addrock(pH):
	rock = Rock(pH)
	rocks.append(rock)
	board[pH] = rock

def addplanet(pH, supply="", demand = ""):
	planet = Planet(pH, supply, demand)
	planets.append(planet)
	board[pH] = planet

def addrandomplanet(pH, ncolor, nsupply, ndemand):
	if nsupply + ndemand > ncolor:
		raise ValueError
	colors = list("ROYGBV"[:ncolor])
	random.shuffle(colors)
	supply = colors[:nsupply]
	demand = colors[nsupply:nsupply+ndemand]
	addplanet(pH, supply, demand)


def addtube(tube):
	for pH in tube.pHs:
		if not planetat(pH):
			board[pH] = tube
	tube.supplier.tubes.append(tube)
	tube.consumer.tubes.append(tube)
	tube.initializecarry()
	tubes.append(tube)
	resolvenetwork()

def removetube(tube):
	for pH in tube.pHs:
		if board[pH] is tube:
			board[pH] = None
	tube.supplier.tubes.remove(tube)
	tube.consumer.tubes.remove(tube)
	tubes.remove(tube)
	resolvenetwork()

def isfree(pH):
	return pH in visible and board[pH] is None

def planetat(pH):
	if pH not in visible:
		return None
	obj = board.get(pH)
	return obj if isinstance(obj, Planet) else None

def allsupplied():
	return all(planet.supplied for planet in planets)

def objat(pH):
	if pH not in visible:
		return None
	return board.get(pH)

def toobj():
	from . import quest
	return board, visible, tubes, planets, rocks, quest.quests

def fromobj(obj):
	from . import quest
	global board, visible, tubes, planets, rocks
	board, visible, tubes, planets, rocks, quest.quests = obj

def savename():
	return settings.savefile.format(mode = level)

def save():
	pickle.dump(toobj(), open(savename(), "wb"))

def load():
	if os.path.exists(savename()):
		fromobj(pickle.load(open(savename(), "rb")))
		aimcamera()
	else:
		init()

def removesave():
	if os.path.exists(savename()):
		os.remove(savename())





