import pygame, os.path
from . import settings

pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=0)

musicplaying = None
def playmusic(mname):
	global musicplaying
	if not settings.music or mname == musicplaying:
		return
	musicplaying = mname
	pygame.mixer.music.load(os.path.join("music", mname + ".ogg"))
	pygame.mixer.music.play(-1)

sounds = {}
def getsound(sname):
	if sname not in sounds:
		sounds[sname] = pygame.mixer.Sound(os.path.join("sfx", sname + ".ogg"))
	return sounds[sname]

def playsound(sname):
	if not settings.sfx:
		return
	getsound(sname).play()

