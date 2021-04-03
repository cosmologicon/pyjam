import os.path, functools, random
import pygame
from . import settings
cache = functools.lru_cache(None)

pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=1)

@cache
def getsound(fname):
	if not os.path.exists(fname):
		print("Missing sound", fname)
		return None
	return pygame.mixer.Sound(fname)


def playsound(sname):
	if sname == "click" or sname == "unclick":
		sname = random.choice(["click0", "click1", "click2"])
	fname = os.path.join("sounds", "%s.ogg" % sname)
	s = getsound(fname)
	if s is not None:
		volume = (settings.soundvolume / 100) ** 1.5
		s.set_volume(volume)
		s.play()

currentsong = None
currentsname = None
def playmusic(jsong):
	global currentsong, currentsname
	settings.mtrack = jsong
	if currentsong is not None:
		currentsong.fadeout(500)
	if jsong is None:
		currentsong = None
		return
	sname = ["ferret", "myst", "builder", "thinking"][jsong]
	currentsname = sname
	fname = os.path.join("music", "%s.ogg" % sname)
	s = getsound(fname)
	s.play(loops = -1, fade_ms = 500)
	currentsong = s
	updatemusicvolume()

def updatemusicvolume():
	if currentsong is not None:
		v = (settings.musicvolume / 100) ** 1.5
		if currentsname == "ferret": v *= 0.5
		if currentsname == "builder": v *= 0.7
		currentsong.set_volume(v)
	

