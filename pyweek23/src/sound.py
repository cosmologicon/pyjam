import pygame, os
from . import settings

pygame.mixer.pre_init(22050, -16, 2, 0)

path = os.path.join("data", "dialog", "%%s.%s" % settings.soundext)

sounds = {}
def get(sname):
	if sname in sounds:
		return sname
	s = pygame.mixer.Sound(path % sname)
	return s

def play(sname):
	get(sname).play()

		
