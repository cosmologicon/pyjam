import random, pygame, math
from collections import defaultdict, Counter
from functools import cache
from . import settings, grid, view, pview, ptext, graphics, hud

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
	def draw(self, glow = False):
		graphics.drawdomeatH(self.pH)
#		pygame.draw.circle(pview.screen, (255, 0, 255), view.DconvertG(grid.GconvertH(self.pH)), 3)
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
		self.forward = True
		self.carry = ""
		self.supplier = planetat(pH0)
		self.consumer = None
		self.supplied = False
		self.t = 0
		self.dirs = []
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
		straights = [grid.isrowH(self.pHs[j-1], self.pHs[j], self.pHs[j+1])
			for j in range(1, len(self.pHs) - 1)]
		straights = [False] + straights + [False]
		self.straights = dict(zip(self.pHs, straights))
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
			return True
		if len(self.pHs) > 1 and pH == self.pHs[-1]:
			self.pHs.pop()
			self.dirs.pop()
			return True
		return False
	# Drag interface. Either add to the end or back up 1.
	def trydrag(self, pH):
		if self.trybuild(pH):
			return True
		if len(self.pHs) > 1 and pH == self.pHs[-2]:
			self.pHs.pop()
			self.dirs.pop()
			return True
		return False
	def pHalong(self, d):
		n, f = divmod(d, 1)
		n = int(n)
		if not 0 <= n < len(self.pHs) - 1:
			return None
		return math.mix(self.pHs[n], self.pHs[n + 1], f)
	def flip(self):
		self.forward = False
		self.supplier, self.consumer = self.consumer, self.supplier
		resolvenetwork()
	def initializecarry(self):
		self.carry = self.supplier.firstexport(self.consumer)
	def togglecarry(self):
		cancarry = [""] + sorted(set(self.supplier.exports))
		print(f"cancarry {cancarry}, self.carry {self.carry}, {cycle_opts(self.carry, cancarry)}")
		self.carry = cycle_opts(self.carry, cancarry)
		resolvenetwork()
	# What resource, if any, do I supply to this planet?
	def supplyto(self, planet):
		return self.carry if planet is self.consumer and self.supplied and self.carry else None
	def draw(self, glow = False):
		pDs = [view.DconvertG(grid.GconvertH(pH)) for pH in self.pHs]
		color = settings.colorcodes.get(self.carry, (160, 160, 160))
		mix = (255, 255, 255) if glow else (0, 0, 0)
		color = math.imix(color, mix, 0.5)
		if self.dirs:
			pH = math.mix(self.pHs[0], self.pHs[1], 0.5)
			graphics.drawdockatH(pH, self.dirs[0])
		if self.dirs:
			pH = math.mix(self.pHs[-2], self.pHs[-1], 0.5)
			graphics.drawdockatH(pH, (self.dirs[-1] + 3) % 6)
		for j in range(len(self.dirs) - 1):
			graphics.drawtubeatH(self.pHs[j+1], color, self.dirs[j], self.dirs[j+1])
		if self.carry and self.supplied:
			d = self.supplier.t * 3 % 3
			while True:
				pH = self.pHalong(d)
				if pH is None: break
				pD = view.DconvertG(grid.GconvertH(pH))
				beta = hud.factor(self.carry, "tube")
				graphics.drawsymbolat(self.carry, pD, 0.7, beta)
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
		xG, yG = grid.GconvertH(self.pH)
		color = (30, 60, 60)
		color = math.imix(color, (255, 255, 255), 0.5) if glow else color
		pygame.draw.circle(pview.screen, color, view.DconvertG((xG, yG)), view.DscaleG(0.4))
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


board = { pH: None for pH in grid.Hrect(40) }
visible = set()
tubes = []
planets = []
rocks = []


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


