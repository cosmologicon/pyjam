import pygame, os.path
from functools import cache
from . import settings

pygame.mixer.pre_init(22050, -16, 1, 1)

def init():
	pygame.mixer.init()

@cache
def load(sname):
	path = os.path.join("sound", "%s.ogg" % sname)
	if not os.path.exists(path):
		print(f"MISSING SFX {sname}")
		return None
	return pygame.mixer.Sound(path)

def play(sname):
	sound = load(sname)
	if sound is not None:
		sound.set_volume(settings.sfxvolume)
		sound.play()

currentmname = None
def playmusic(mname, volume = 1):
	global currentmname
	pygame.mixer.music.set_volume(settings.musicvolume * volume)
	if mname == currentmname:
		return
	currentmname = mname
	pygame.mixer.music.load(os.path.join("sound", "%s.ogg" % mname))
	pygame.mixer.music.play(-1)

