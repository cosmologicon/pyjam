import pygame, math
from functools import cache

pygame.mixer.pre_init(frequency=22050, size=-16, channels=1, buffer=4096)

def init():
	pygame.mixer.init()
	pygame.mixer.music.load("sound/lightless-dawn.ogg")
	pygame.mixer.music.play(-1)

@cache
def getsound(sname):
	sound = pygame.mixer.Sound("sound/%s.ogg" % sname)
	sound.set_volume(1)
	return sound

lastplay = {}
def getvolume(sname):
	now = 0.001 * pygame.time.get_ticks()
	if sname not in lastplay:
		volume = 1
	else:
		dt = now - lastplay[sname]
		volume = 1 - math.exp(-0.3 * dt)
	lastplay[sname] = now
	return volume * 0.8


def play(sname):
	sound = getsound(sname)
	sound.set_volume(getvolume(sname))
	sound.play()

