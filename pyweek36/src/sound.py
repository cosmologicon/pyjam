import pygame, os.path
from functools import cache
from . import settings

pygame.mixer.pre_init(22050, -16, 1, 1)

@cache
def load(sname):
	path = os.path.join("sfx", "%s.ogg" % sname)
	if not os.path.exists(path):
		print(f"MISSING SFX {sname}")
		return None
	return pygame.mixer.Sound(path)

def play(sname):
	sound = load(sname)
	if sound is not None:
		sound.set_volume(settings.sfxvolume)
		sound.play()



