import itertools, math
from . import fuzz
from . import thing

W, H = 40, 20
Nstar = 100

stars0 = []
stars = []
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
			d *= 0.99
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

def advanceto(mag):
	global maglimit
	maglimit = mag
	while len(stars) < len(stars0):
		star = stars0[len(stars)]
		if star.mag <= mag:
			stars.append(star)
		else:
			break

def advance():
	advanceto(maglimit + 0.2)

def placelink(link):
	global score
	link.place()
	score = sum(star.ok() for star in stars)
	if score >= 0.9 * len(stars):
		advance()
		score = sum(star.ok() for star in stars)

