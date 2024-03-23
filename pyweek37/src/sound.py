import pygame, os.path
from functools import cache
from . import settings

pygame.mixer.pre_init(frequency=22050, size=-16, channels=1, buffer=1)

def init():
	pygame.mixer.init()

@cache
def load(sname):
	path = f"sound/{sname}.ogg"
	if os.path.exists(path):
		sound = pygame.mixer.Sound(path)
		return sound
	print("Missing sound", sname)

def getvolume(sname):
	return {
		"buildup": 0.4,
	}.get(sname, 0.8) * settings.sfxvolume ** 1.8

def play(sname):
	sound = load(sname)
	if sound is not None:
		sound.set_volume(getvolume(sname))
		sound.play()

currentmusic = None
def playmusic(mname):
	global currentmusic
	if mname == currentmusic:
		return
	pygame.mixer.music.load(f"sound/{mname}.ogg")
	pygame.mixer.music.set_volume(0.8 * settings.musicvolume ** 1.8)
	pygame.mixer.music.play(-1)
	
	
