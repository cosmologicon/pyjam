import itertools
from . import fuzz
from . import thing

W, H = 40, 20
Nstar = 100

stars0 = []
stars = []
links = []
maglimit = 0
score = 0


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
		stars0.append(thing.Star(pos, mag))
		if len(stars0) > Nstar:
			break

def advanceto(mag):
	global maglimit
	maglimit = mag
	while len(stars) < len(stars0):
		star = stars0[len(stars)]
		if star.mag <= mag:
			stars.append(star)
		else:
			break

def placelink(link):
	global score
	link.place()
	score = sum(star.ok() for star in stars)

