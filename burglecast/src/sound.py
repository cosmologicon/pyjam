import pygame, os.path
from functools import cache

pygame.mixer.pre_init(frequency=22050, size=-16, channels=1, buffer=0)

def init():
	pygame.mixer.init()

@cache
def loadsound(sname):
	path = os.path.join("sound", f"{sname}.ogg")
	if not os.path.exists(path):
		print("MISSING SOUND", sname)
		return None
	sound = pygame.mixer.Sound(path)
	sound.set_volume({
		"grab": 0.2,
		"claim": 0.4,
		"place": 0.2,
	}.get(sname, 1))
	return sound


def play(sname):
	sound = loadsound(sname)
	if sound is not None:
		sound.play()

currentmusic = None
def playmusic(mname):
	global currentmusic
	if mname == currentmusic:
		return
	path = os.path.join("sound", f"{mname}.ogg")
	pygame.mixer.music.set_volume({
		"fearless-first": 0.15,
		"spy-glass": 0.5,
	}[mname])
	pygame.mixer.music.load(path)
	pygame.mixer.music.play(-1)
	currentmusic = mname

