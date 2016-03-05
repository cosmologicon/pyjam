import pygame, numpy, random, math, os
from . import settings, image, ptext
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
				print fname, os.path.exists(fname)
				if os.path.exists(fname):
					sound = pygame.mixer.Sound(fname)
				else:
					sound = fakeline(line)
				sound.set_volume(settings.volumes["dialogue"])
				channel.play(sound)
		else:
			currentline = None
			tquiet += dt

def draw():
	if currentline:
		_, who, line = currentline
		n = "Mel Scamp Ignatius Ruby Hallan Pax".split().index(who[:-1])
		letter = "ABCDEF"[n]
		image.draw("avatar-%s" % letter, F(100, 420), size = F(100))
		ptext.draw(who[:-1].upper(), midleft = F(50, 370), fontsize = F(26), color = "yellow", owidth = 2)
		ptext.draw(line, bottomleft = F(160, 470), fontsize = F(30), width = F(540), shadow = (1, 1))




