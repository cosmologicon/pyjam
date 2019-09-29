import math,random
import pygame, os.path
from . import settings

pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=1000)


def init():
	global rush
	pygame.mixer.init()
	rush = getsound("time_stop")
	rush.set_volume(0)
	rush.play(-1)

def setrushvolume(volume):
	if not settings.sound: return
	rush.set_volume(volume)

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
		sounds[sname] = pygame.mixer.Sound(os.path.join("sound", sname + ".ogg"))
	return sounds[sname]


def playsound(sname):
	if not settings.sound: return
	getsound(sname).play()

