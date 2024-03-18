import random, pygame, math
from collections import defaultdict, Counter
from . import settings, grid, view, pview, ptext

def cycle_opts(value, values, reverse = False):
	if value not in values:
		return values[0]
	j = values.index(value)
	return values[(j + (-1 if reverse else 1)) % len(values)]


class Planet:
	def __init__(self, pH, has, needs):
		self.pH = pH
		self.color = [random.randint(60, 120) for _ in range(3)]
		self.has = has
		self.needs = needs
		self.tubes = []
		self.netsupply = defaultdict(int)
	def draw(self, glow = False):
		xG, yG = grid.GconvertH(self.pH)
		color = math.imix(self.color, (255, 255, 255), 0.5) if glow else self.color
		pygame.draw.circle(pview.screen, color, view.DconvertG((xG, yG)), view.DscaleG(0.4))
		ptext.draw("\n".join(self.info()), center = view.DconvertG((xG, yG)),
			fontsize = view.DscaleG(0.4), owidth = 1)
	def info(self):
		lines = [f"pos: {self.pH}"]
		if self.has:
			hastext = " ".join(f"{n}{x}" for x, n in sorted(self.has.items()))
			lines.append(f"has: {hastext}")
		if self.needs:
			needstext = " ".join(f"{n}{x}" for x, n in sorted(self.needs.items()))
			lines.append(f"needs: {needstext}")
		supplied = all(self.netsupply.get(x, 0) >= self.needs[x] for x in self.needs)
		lines.append(f"supplied: {supplied}")
		return lines

class Tube:
	def __init__(self, pH0):
		self.pHs = [pH0]
		self.forward = True
		self.carry = ""
		self.supplier = planetat(pH0)
		self.consumer = None
		self.supplied = False
	def nexts(self):
		return [pH for pH in grid.HadjsH(self.pHs[-1]) if pH not in self.pHs and isfree(pH)]
	def cango(self, pH):
		return pH in self.nexts()
	def flip(self):
		self.forward = False
		self.supplier, self.consumer = self.consumer, self.supplier
		self.carry = ""
		self.togglecarry()
		resolvenetwork()
	def togglecarry(self):
		cancarry = ["", self.carry]
		cancarry += [x for x, n in self.supplier.netsupply.items() if n > 0]
		cancarry = sorted(set(cancarry))
		self.carry = cycle_opts(self.carry, cancarry)
		resolvenetwork()
	def add(self, pH):
		self.pHs.append(pH)
		if planetat(pH):
			self.consumer = planetat(pH)
	def draw(self, glow = False):
		pDs = [view.DconvertG(grid.GconvertH(pH)) for pH in self.pHs]
		color = settings.colors.get(self.carry, (160, 160, 160))
		mix = (255, 255, 255) if glow else (0, 0, 0)
		color = math.imix(color, mix, 0.5)
		for pD in pDs:
			pygame.draw.circle(pview.screen, color, pD, view.DscaleG(0.2))
		if len(pDs) >= 2:
			pygame.draw.lines(pview.screen, color, False, pDs, view.DscaleG(0.1))
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
		xG, yG = grid.GconvertH(self.pH)
		color = (50, 50, 50)
		color = math.imix(color, (255, 255, 255), 0.5) if glow else color
		pygame.draw.circle(pview.screen, color, view.DconvertG((xG, yG)), view.DscaleG(0.4))
	def info(self):
		return ["Just a rock."]

def resolvenetwork():
	for planet in planets:
		planet.netsupply = defaultdict(int)
		for x, n in planet.has.items():
			planet.netsupply[x] += n
	for tube in tubes:
		tube.supplied = False
	suppliers = list(planets)
	while True:
		updated = False
		nsuppliers = []
		for planet in suppliers:
			for tube in planet.tubes:
				if tube.supplied: continue
				if planet is not tube.supplier: continue
				if planet.netsupply[tube.carry] <= 0: continue
				tube.supplied = True
				tube.consumer.netsupply[tube.carry] += 1
				planet.netsupply[tube.carry] -= 1
				if tube.consumer not in nsuppliers:
					nsuppliers.append(tube.consumer)
				updated = True
		if not updated:
			break
		suppliers = nsuppliers


board = { pH: None for pH in grid.Hrect(60) }

tubes = []
planets = []
rocks = []


def addrock(pH):
	rock = Rock(pH)
	rocks.append(rock)
	board[pH] = rock

def addplanet(pH, has=None, needs=None):
	planet = Planet(pH, (has or {}), (needs or {}))
	planets.append(planet)
	board[pH] = planet

def addrandomplanet(pH, ncolor, nhas, nneeds):
	if nhas + nneeds > ncolor:
		raise ValueError
	colors = list("ROYGBV"[:ncolor])
	random.shuffle(colors)
	has = dict(Counter(colors[:nhas]))
	needs = dict(Counter(colors[nhas:nhas+nneeds]))
	addplanet(pH, has, needs)


def addtube(tube):
	for pH in tube.pHs:
		if not planetat(pH):
			board[pH] = tube
	tube.supplier.tubes.append(tube)
	tube.consumer.tubes.append(tube)
	tube.togglecarry()
	tubes.append(tube)
	resolvenetwork()

def isfree(pH):
	return pH in board and board[pH] is None

def planetat(pH):
	obj = board.get(pH)
	return obj if isinstance(obj, Planet) else None

def objat(pH):
	return board.get(pH)



