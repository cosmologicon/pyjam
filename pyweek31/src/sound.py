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
		s.set_volume(settings.soundvolume)
		s.play()

currentsong = None
def playmusic(jsong):
	global currentsong
	settings.mtrack = jsong
	if currentsong is not None:
		currentsong.fadeout(500)
	if jsong is None:
		currentsong = None
		return
	sname = ["ferret", "myst", "builder", "thinking"][jsong]
	fname = os.path.join("music", "%s.ogg" % sname)
	s = getsound(fname)
	if s is not None:
		v = settings.musicvolume
		if sname == "ferret": v *= 0.6
		if sname == "builder": v *= 0.8
		s.set_volume(v)
		s.play(loops = -1, fade_ms = 500)
		currentsong = s

