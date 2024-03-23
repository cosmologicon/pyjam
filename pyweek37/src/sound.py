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
	}.get(sname, 0.2) * settings.sfxvolume ** 0.5

def play(sname):
	sound = load(sname)
	if sound is not None:
		sound.play()

