import random, pygame, math
from collections import defaultdict, Counter
from . import settings, grid, view, pview, ptext

def cycle_opts(value, values, reverse = False):
	if value not in values:
		return values[0]
	j = values.index(value)
	return values[(j + (-1 if reverse else 1)) % len(values)]


def drawsymbolat(symbol, pD, fontsizeG, dim = 0):
	color = math.imix(settings.colorcodes[symbol], (0, 0, 0), dim)
	ptext.draw(symbol, center = pD, color = color,
		fontsize = view.DscaleG(fontsizeG), owidth = 2)


class Planet:
	def __init__(self, pH, has, needs):
		self.pH = pH
		self.has = has
		self.needs = needs
		self.tubes = []
		self.netsupply = defaultdict(int)
		self.t = 0
	def think(self, dt):
		self.t += dt
	def draw(self, glow = False):
		if not self.pH in visible:
			return
		xG, yG = grid.GconvertH(self.pH)
		supplied = all(self.netsupply.get(x, 0) >= self.needs[x] for x in self.needs)
		color = (180, 180, 180) if supplied else (60, 60, 60)
		color = math.imix(color, (255, 255, 255), 0.5) if glow else color
		pygame.draw.circle(pview.screen, color, view.DconvertG((xG, yG)), view.DscaleG(0.4))
		for j, symbol in enumerate(sorted(self.needs.keys())):
			dim = 0.9 if self.netsupply[symbol] < 0 else 0
			dim = 0
			drawsymbolat(symbol, view.DconvertG((xG - 0.1 - 0.25 * j, yG + 0.3)), 0.5, dim)
		for j, symbol in enumerate(sorted(self.has.keys())):
			dim = 0.9 if self.netsupply[symbol] > 0 else 0
			dim = 0
			drawsymbolat(symbol, view.DconvertG((xG + 0.1 + 0.25 * j, yG - 0.3)), 0.5, dim)
		
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
		self.built = False
		self.forward = True
		self.carry = ""
		self.supplier = planetat(pH0)
		self.consumer = None
		self.supplied = False
		self.t = 0
	def think(self, dt):
		self.t += dt
	# Does not check for legality.
	def add(self, pH):
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
				yield pH
				continue
			obj = objat(pH)
			if isinstance(obj, Planet):
				if obj is not self.supplier and len(self.pHs) > 1:
					yield pH
			elif isinstance(obj, Tube):
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
			return True
		return False
	# Drag interface. Either add to the end or back up 1.
	def trydrag(self, pH):
		if self.trybuild(pH):
			return True
		if len(self.pHs) > 1 and pH == self.pHs[-2]:
			self.pHs.pop()
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
		self.carry = ""
		self.togglecarry()
		resolvenetwork()
	def togglecarry(self):
		cancarry = ["", self.carry]
		cancarry += [x for x, n in self.supplier.netsupply.items() if n > 0]
		cancarry = sorted(set(cancarry))
		self.carry = cycle_opts(self.carry, cancarry)
		resolvenetwork()
	def draw(self, glow = False):
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
				drawsymbolat(self.carry, pD, 0.7)
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


board = { pH: None for pH in grid.Hrect(20) }
R = 10
visible = set(pH for pH in board if math.length(grid.GconvertH(pH)) <= R)

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

def objat(pH):
	if pH not in visible:
		return None
	return board.get(pH)



