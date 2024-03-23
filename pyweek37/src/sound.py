import pygame, os.path
from functools import cache

pygame.mixer.pre_init(frequency=22050, size=-16, channels=1, buffer=1)

@cache
def load(sname):
	path = f"sound/{sname}.ogg"
	if os.path.exists(path):
		sound = pygame.mixer.Sound(path)
		return sound
	print("Missing sound", sname)


def play(sname):
	sound = load(sname)
	if sound is not None:
		sound.play()

