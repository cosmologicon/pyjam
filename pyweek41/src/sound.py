import pygame, random, math
from functools import cache

pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=4096)

@cache
def load(sname):
	filename = f"sound/{sname}.ogg"
	sfx = pygame.mixer.Sound(filename)
	if "strum" in sname:
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


cnames = ["chime-C", "chime-D", "chime-E", "chime-G", "chime-A"]

def playchime():
	for delay in (0, random.uniform(0.1, 0.4)):
		cname = random.choice(cnames[:-2])
		play(cname, delay)
		cnames.remove(cname)
		cnames.append(cname)

snames = ["strum-C", "strum-D", "strum-E", "strum-G", "strum-A"]

def playstrum():
	for delay in (0,):
		sname = random.choice(snames[:-2])
		play(sname, delay)
		snames.remove(sname)
		snames.append(sname)

