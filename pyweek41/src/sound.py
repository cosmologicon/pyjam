import pygame, random, math
from functools import cache

pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=4096)

@cache
def load(sname):
	filename = f"sound/{sname}.ogg"
	sfx = pygame.mixer.Sound(filename)
	if "strum" in sname:
		sfx.set_volume(0.2)
	if "chime" in sname:
		sfx.set_volume(0.1)
	if "bell" in sname:
		sfx.set_volume(0.3)
	return sfx

playqueue = []
def play(sname, delay = 0):
	if delay:
		playqueue.append((delay, sname))
	else:
		load(sname).play()

def think(dt):
	qnew = []
	for delay, sname in playqueue:
		delay = math.approach(delay, 0, dt)
		if delay == 0:
			play(sname)
		else:
			qnew.append((delay, sname))
	playqueue[:] = qnew

def playmusic():
	pygame.mixer.music.load("sound/organic-meditations-three.ogg")
	pygame.mixer.music.play(-1)


cnames = ["chime-C", "chime-D", "chime-E", "chime-G", "chime-A"]

def playchime():
	return
	play("chime-C")
	return
	for delay in (0, random.uniform(0.3, 0.6)):
		cname = random.choice(cnames[:-2])
		play(cname, delay)
		cnames.remove(cname)
		cnames.append(cname)

bnames = ["bell-C", "bell-D", "bell-E", "bell-G", "bell-A"]

def playbell():
	for delay in (0, random.uniform(0.2, 0.4), random.uniform(0.4, 0.7)):
		bname = random.choice(bnames[:-2])
		play(bname, delay)
		bnames.remove(bname)
		bnames.append(bname)

snames = ["strum-C", "strum-D", "strum-E", "strum-G", "strum-A"]

def playstrum():
	for delay in (0,):
		sname = random.choice(snames[:-2])
		play(sname, delay)
		snames.remove(sname)
		snames.append(sname)

