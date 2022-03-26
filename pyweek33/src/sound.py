import pygame, os
from functools import lru_cache

pygame.mixer.pre_init(22050, -16, 2, 1)


def init():
	pygame.mixer.init()
	music = pygame.mixer.Sound(os.path.join("sound", "floating-cities.ogg"))
	music.set_volume(0.2)
	music.play(-1)
	

@lru_cache(100)
def loadsound(sfxname):
	path = os.path.join("sound", f"{sfxname}.ogg")
	if os.path.exists(path):
		return pygame.mixer.Sound(path)
	else:
		print(f"SFX not found: {sfxname}")
		return None


def play(sfxname):
	sfx = loadsound(sfxname)
	if sfx is not None:
		sfx.play()

	
