import pygame, os
from functools import lru_cache

pygame.mixer.pre_init(22050, -16, 2, 1)

@lru_cache(100)
def loadsound(sfxname):
	path = os.path.join("sound", f"{sfxname}.ogg")
	if os.path.exists(path):
		return pygame.sound.Sound(path)
	else:
		print(f"SFX not found: {sfxname}")
		return None


def play(sfxname):
	sfx = loadsound(sfxname)
	if sfx is not None:
		sfx.play()

	
