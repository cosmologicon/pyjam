import pygame, numpy, random, math
from . import settings, image, ptext
from .util import F

pygame.mixer.pre_init(settings.mixerfreq, -16, 2, settings.mixerbuffer)

convos = {}
for line in open("data/dialogue.txt"):
	line = line.strip()
	if line.endswith(":"):
		currentconvo = convos[line.rstrip(":")] = []
	elif line:
		words = line.split()
		currentconvo.append((words[0], " ".join(words[1:])))


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
	playqueue.append(("end", dname))

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

def think(dt):
	global tquiet, currentline
	channel = pygame.mixer.Channel(0)
	if channel.get_busy():
		tquiet = 0
	else:
		if playqueue:
			who, line = currentline = playqueue.pop(0)
			if who == "end":
				played.add(line)
				currentline = None
			else:
				sound = fakeline(line)
				channel.play(sound)
		else:
			currentline = None
			tquiet += dt

def draw():
	if currentline:
		who, line = currentline
		image.draw("avatar-%s" % who, F(100, 420), size = F(100))
		ptext.draw(line, F(160, 370), fontsize = F(30), width = F(640), shadow = (1, 1))

