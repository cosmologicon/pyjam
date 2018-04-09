import pygame, numpy, random, math, os
from . import settings, image, ptext, window
from .util import F

# Channel 0 reserved for dialogue

pygame.mixer.pre_init(settings.mixerfreq, -16, 2, settings.mixerbuffer)

convos = {}
for line in open("data/dialogue.txt"):
	line = line.strip()
	if line.endswith(":"):
		currentconvo = convos[line.rstrip(":")] = []
		convoname = line[:-1]
	elif line:
		words = line.split()
		name = "data/dialogue/%s-%d.%s" % (convoname, 1 + len(currentconvo), settings.dialogueext)
		currentconvo.append((name, words[0], " ".join(words[1:])))


def fakeline(line):
	t = 0.4 + 0.05 * len(line)
	nsamp = int(round(settings.mixerfreq * t))
	freq = random.uniform(0.05, 0.08)
	samples = [14000 * math.sin(freq * j) for j in range(nsamp)]
	sound = pygame.sndarray.make_sound(numpy.int16(numpy.array(zip(samples, samples))))
	return sound

played = set()
playqueue = []
tquiet = 0
currentline = None
def play(dname):
	global tquiet
	tquiet = 0
	playqueue.extend(convos[dname])
	playqueue.append(("end", None, dname))

def playonce(dname):
	if dname in played:
		return
	for who, line in playqueue:
		if who == "end" and line == dname:
			return
	play(dname)

def maybeplay(dname, tsince = 1):
	if tquiet > tsince:
		play(dname)

names = "Mel Scamp Ignatius Ruby Hallan Pax".split()

def think(dt):
	global tquiet, currentline
	channel = pygame.mixer.Channel(0)
	if channel.get_busy():
		tquiet = 0
	else:
		if playqueue:
			fname, who, line = currentline = playqueue.pop(0)
			if fname == "end":
				played.add(line)
				currentline = None
			else:
				from . import state
				if who.startswith("if"):  # only play if a certain character is unlocked
					if any(ship.letter == who[2] for ship in state.state.team):
						who = who[4:]
						currentline = fname, who, line
					else:
						currentline = None
						return
				elif who.startswith("nf"):  # only play if a certain character is not unlocked
					if not any(ship.letter == who[2] for ship in state.state.team):
						who = who[4:]
						currentline = fname, who, line
					else:
						currentline = None
						return

				if os.path.exists(fname):
					sound = pygame.mixer.Sound(fname)
				else:
					sound = fakeline(line)
				sound.set_volume(settings.volumes["dialogue"])
				channel.play(sound)
		else:
			currentline = None
			tquiet += dt

def clear():
	global currentline
	while playqueue:
		fname, who, line = playqueue.pop(0)
		if fname == "end":
			played.add(line)
			currentline = None

def draw():
	if currentline:
		_, who, line = currentline
		n = names.index(who[:-1])
		letter = "ABCDEF"[n]
		rect = pygame.Rect(F(0, 0, 100, 100))
		rect.center = F(100, 420)
		window.screen.fill((0, 0, 0), rect)
		image.draw("avatar-%s" % letter, F(100, 420), size = F(92))
		ptext.draw(who[:-1].upper(), midleft = F(50, 370), fontsize = F(26), color = "yellow",
			fontname = "Oswald", owidth = 2)
		fontname = "PassionOne Salsa FrancoisOne Boogaloo SansitaOne Anton".split()[n]
		ptext.draw(line, bottomleft = F(160, 470), fontsize = F(30), fontname = fontname,
			width = F(540), shadow = (1, 1))

if __name__ == "__main__":
	from . import state, thing
	state.state.team = [thing.ShipA, thing.ShipB, thing.ShipC, thing.ShipD, thing.ShipE, thing.ShipF]
	cnames = sorted(convos)
	current = cnames[0]
	playing = True
	clock = pygame.time.Clock()
	pygame.mixer.init()
	screen = pygame.display.set_mode((854, 900))
	play(current)
	while playing:
		dt = 0.001 * clock.tick()
		think(dt)
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					playing = False
				if event.key == pygame.K_LEFT:
					current = cnames[(cnames.index(current) - 1) % len(cnames)]
					clear()
					play(current)
				if event.key == pygame.K_RIGHT:
					current = cnames[(cnames.index(current) + 1) % len(cnames)]
					clear()
					play(current)
		screen.fill((0, 0, 0))
		ptext.draw("Current dialogue sequence: %s" % current, midtop = (427, 10),
			fontsize = 50)
		y = 60
		for filename, who, text in convos[current]:
			color0, color1 = "yellow", "orange"
			if currentline and who.endswith(currentline[1]) and text == currentline[2]:
				color1 = "white"
			ptext.draw(who, top = y, right = 120, fontsize = 32, color = color0)
			surf, _ = ptext.draw(text, top = y, left = 130, fontsize = 32, color = color1, width = 700)
			y += surf.get_height() + 10
		ptext.draw("Left: previous dialogue\nRight: next dialogue", bottom = 896, right = 850,
			fontsize = 24, color = "gray")
		pygame.display.flip()


