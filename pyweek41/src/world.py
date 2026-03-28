import itertools, math, pygame
from . import fuzz, pview
from . import thing, graphics, view, settings, sound

W, H = 40, 20
Nstar = 100

stars0 = []
stars = {}
links = []
maglimit = 1
maxmag = 6
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
	

worldspec = [(0.5564299120596843, (19.857142857142858, -4.142857142857143), '2'), (0.6782790594775179, (-28.357142857142858, 7.071428571428571), '2'), (0.8709800059041299, (20.928571428571427, 14.214285714285714), '2'), (1.28717972101731, (-6.857142857142857, -4.928571428571429), '3'), (1.3921731517912121, (-6.571428571428571, 17.642857142857142), '3'), (1.8483254480015603, (10.142857142857142, 5.785714285714286), '4'), (2.02742650568689, (-37.857142857142854, 16.428571428571427), '1'), (2.239199353103686, (-7.214285714285714, 11.714285714285714), 'Y'), (2.526390549581265, (19.428571428571427, 4.142857142857143), 'Y'), (2.7394865733367624, (-4.428571428571429, -16.785714285714285), '1'), (2.7437424091694993, (31.071428571428573, 19.285714285714285), '2'), (3.0649243347033917, (3.0714285714285716, 22.142857142857142), '1'), (3.067767760814604, (30.214285714285715, 0.5), '3'), (3.2525883253401844, (39.92857142857143, 15.071428571428571), '1'), (3.3062764954956947, (-4.5, 3.7857142857142856), '3'), (3.3407340823687264, (6.0, -5.642857142857143), 'X'), (3.4604997759961407, (-13.214285714285714, 3.2857142857142856), 'X'), (3.505292209883919, (4.428571428571429, 10.357142857142858), '3'), (3.51301784721727, (14.5, -15.642857142857142), '2'), (3.579025385650766, (-12.928571428571429, -3.5714285714285716), '3'), (3.595377434641705, (-39.857142857142854, 9.285714285714286), '1'), (3.621571997558931, (-36.0, -7.214285714285714), '2'), (3.6680560056411196, (-23.142857142857142, 2.4285714285714284), '1'), (3.6928771527600475, (-21.428571428571427, 18.5), 'X'), (3.8247200847254135, (-17.5, 11.142857142857142), '3'), (3.8504050837509567, (3.0714285714285716, 16.071428571428573), '3'), (3.9631355429610267, (-20.0, -8.214285714285714), '4'), (4.173205837279966, (-13.214285714285714, 23.142857142857142), '2'), (4.221121865448367, (-8.071428571428571, -9.071428571428571), 'Y'), (4.456933182354078, (-14.5, 16.214285714285715), '1'), (4.485208939469885, (20.214285714285715, 22.214285714285715), '4'), (4.505242271901807, (10.642857142857142, 18.857142857142858), 'X'), (4.585524654306937, (29.571428571428573, 11.071428571428571), '2'), (4.6589420680693365, (-2.7142857142857144, 22.214285714285715), '2'), (4.764636461455666, (-1.5714285714285714, -5.642857142857143), '2'), (4.780819405832972, (24.428571428571427, 3.7142857142857144), '2'), (4.790949984650069, (13.571428571428571, -1.7142857142857142), '2'), (5.01364119034406, (-2.2142857142857144, 8.357142857142858), '3'), (5.060977114135312, (-26.714285714285715, -4.5), '2'), (5.079733435966773, (-12.285714285714286, -6.785714285714286), '3'), (5.098106043215466, (-8.928571428571429, 21.714285714285715), '3'), (5.1082939811603865, (-0.14285714285714285, 0.07142857142857142), '2'), (5.130649171755067, (13.857142857142858, 14.642857142857142), '2'), (5.164433660414943, (-32.214285714285715, 21.5), '1'), (5.172500327224043, (8.071428571428571, -12.571428571428571), '3'), (5.196993952664343, (11.928571428571429, -6.714285714285714), 'Y'), (5.212611271086644, (-22.142857142857142, 8.357142857142858), '1'), (5.233584195593721, (-1.5714285714285714, 13.571428571428571), '2'), (5.277412308892963, (-21.071428571428573, -1.5), '2'), (5.2789112261228865, (-41.285714285714285, -2.7857142857142856), '1'), (5.288531232323294, (-23.857142857142858, 23.428571428571427), '3'), (5.297074475969566, (15.071428571428571, 10.285714285714286), '1'), (5.3151635947033355, (33.0, 6.642857142857143), 'X'), (5.322720848445897, (26.928571428571427, 14.785714285714286), '3'), (5.334667929811985, (-33.07142857142857, -1.9285714285714286), 'Y'), (5.385397048659797, (1.1428571428571428, -11.428571428571429), '2'), (5.398026104901874, (7.714285714285714, 14.571428571428571), 'Y'), (5.419360720101395, (-10.428571428571429, -13.857142857142858), '3'), (5.452608034043806, (6.714285714285714, 0.5714285714285714), '1'), (5.486056070993072, (-29.428571428571427, 14.428571428571429), 'Y')]


def generate():
	for mag, pos, label in worldspec:
		_, ctype, N = startable[labels.index(label)]
		stars0.append(ctype(pos, mag, N))

def advanceto(mag):
	global maglimit
	maglimit = min(mag, maxmag)
	while len(stars) < len(stars0):
		star = stars0[len(stars)]
		if star.mag <= mag:
			stars[star.pos] = star
		else:
			break

dadvance = 0.5

def advance():
	advanceto(maglimit + dadvance)
	sound.playbell()

def checkadvance():
	if max(star.mag for star in stars.values()) < sky - dadvance:
		return
	if score == len(stars):
		advance()
		setscore()

def setscore():
	global score
	score = sum(star.ok() for star in stars.values())


def placelink(link):
	link.place()
	setscore()
	checkadvance()
	graphics.dellinkimg()

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
	assert pos not in stars
	mag = fuzz.uniform(maglimit - dadvance, maglimit, 0.384, *pos)
	stars[pos] = thing.Star(pos, mag, 1)

def removestar(star):
	assert star is stars[star.pos]
	for link in list(star.links):
		link.unplace(resolve = False)
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

