from __future__ import print_function
import pygame, os
from . import settings

if not settings.nosound or not settings.nomusic:
	pygame.mixer.pre_init()

cache = {}
def play(sname):
	if settings.nosound:
		return
	if sname not in cache:
		fname = "sound/%s.ogg" % sname
		if os.path.exists(fname):
			cache[sname] = pygame.mixer.Sound(fname)
		else:
			cache[sname] = None
			print("Missing sound:", sname)
	if settings.DEBUG and cache[sname] is not None:
		cache[sname].play()
	

def playmusic(mname):
	if settings.nomusic:
		return
	pygame.mixer.music.load("sound/%s.ogg" % mname)
	pygame.mixer.music.play(-1)
