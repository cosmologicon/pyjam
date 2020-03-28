import pygame, os.path
from functools import lru_cache
from . import settings

pygame.mixer.init()

@lru_cache(None)
def getsound(filename):
	path = "sound/{}.wav".format(filename)
	if os.path.exists(path):
		sound = pygame.mixer.Sound(path)
		sound.set_volume(settings.soundvolume)
		return sound
	else:
		print("missing sound:", path)
		return None

def play(sname):
	sound = getsound(sname)
	if sound:
		sound.play()

pygame.mixer.music.set_volume(settings.musicvolume)
def playmusic(track):
	pygame.mixer.music.load("music/{}.ogg".format(track))
	pygame.mixer.music.play(-1)

