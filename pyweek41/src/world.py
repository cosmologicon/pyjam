import itertools, math, pygame
from . import fuzz, pview
from . import thing, graphics, view, settings

W, H = 40, 20
Nstar = 100

stars0 = []
stars = {}
links = []
maglimit = 0
score = 0

effects = []


def generate(*seed):
	d = 20
	for n in itertools.count():
		x = fuzz.uniform(-W, W, n, 0.123, *seed)
		y = fuzz.uniform(-H, H, n, 0.234, *seed)
		pos = x, y
		if any(star.distanceto(pos) < d for star in stars0):
			d *= 0.999
			continue
		mag = (len(stars0) / Nstar) ** 0.5 * 6
		cls = fuzz.choice([thing.Star, thing.NoadjStar, thing.BalancedStar], n, 0.345, *seed)
		N = fuzz.choice([1, 2, 3, 4], n, 0.567, *seed)
		stars0.append(cls(pos, mag, N))
		if len(stars0) > Nstar:
			break

if False:
	def generate():
		for n in range(200):
			x, y = math.CS(n * math.phyllo, 4 * math.sqrt(n))
			stars0.append(thing.Star((x, y), 1))


def generate(*seed):
	d = 20
	img = pygame.transform.smoothscale(pygame.image.load("img/starpatch.png").convert_alpha(), settings.size)
	yimg = pygame.transform.smoothscale(pygame.image.load("img/ypatch.png").convert_alpha(), settings.size)
	for n in itertools.count():
		xG = fuzz.uniform(-50, 50, n, 0.123, *seed)
		yG = fuzz.uniform(-30, 30, n, 0.234, *seed)
		if any(star.distanceto((xG, yG)) < d for star in stars0):
			d *= 0.999
			continue
		xW = int(pview.centerx0 + view.camera.WscaleG * xG)
		yW = int(pview.centery0 - view.camera.WscaleG * yG)
		if not img.get_rect().collidepoint((xW, yW)):
			continue
		alpha = img.get_at((xW, yW))[3]
		if alpha < 128:
			continue
		yalpha = yimg.get_at((xW, yW))[3]
		yok = yalpha >= 128
		mag = (len(stars0) / Nstar) ** 0.5 * 6
		if yok and fuzz.flip(0.2, n, 0.678, *seed):
			cls, N = thing.BalancedStar, 3
		else:
			cls = fuzz.choice([thing.Star] * 5 + [thing.NoadjStar], n, 0.345, *seed)
			Ns = [2, 3, 4, 5] if yok else [1, 2, 3]
			N = fuzz.choice(Ns, n, 0.567, *seed)
		stars0.append(cls((xG, yG), mag, N))
		if len(stars0) > Nstar:
			break
	

def advanceto(mag):
	global maglimit
	maglimit = mag
	while len(stars) < len(stars0):
		star = stars0[len(stars)]
		if star.mag <= mag:
			stars[star.pos] = star
		else:
			break

dadvance = 0.5

def advance():
	advanceto(maglimit + dadvance)

def placelink(link):
	global score
	link.place()
	score = sum(star.ok() for star in stars.values())
	if score == len(stars):
		advance()
		score = sum(star.ok() for star in stars.values())

def resolvecon():
	cons = []
	for link in links:
		ps = set(link.ps)
		noncon = []
		for con in cons:
			if ps & con:
				ps |= con
			else:
				noncon.append(con)
		noncon.append(ps)
		cons = noncon
	for con in cons:
		conok = sum(stars[p].islone for p in con) <= 1
		for pos in con:
			stars[pos].conok = conok

startable = [
	("1", thing.Star, 1),
	("2", thing.Star, 2),
	("3", thing.Star, 3),
	("4", thing.Star, 4),
	("5", thing.Star, 5),
	("X", thing.LoneStar, 4),
	("Y", thing.BalancedStar, 3),
]
labels = [label for label, stype, N in startable]

def addstar(pos):
	mag = fuzz.uniform(maglimit - dadvance, maglimit)
	stars[pos] = thing.Star(pos, mag, 1)

def removestar(star):
	for link in star.links:
		link.unplace()
	del stars[star.pos]
	resolvecon()

def cyclestar(star, wheel):
	pos = star.pos
	mag = star.mag
	index = labels.index(star.label)
	index = (index + wheel) % len(labels)
	nlabel, stype, N = startable[index]
	removestar(star)
	stars[pos] = stype(pos, mag, N)

def dumpstars():
	lines = []
	for pos, star in stars.items():
		lines.append((star.mag, pos, star.label))
	print(sorted(lines))

