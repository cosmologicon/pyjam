import pygame, os.path
from . import settings, util

pygame.mixer.pre_init(22050, -16, 1, 0)

def get_sfxvolume():
	return (settings.sfxvolume / 100) ** settings.volumegamma

def get_musicvolume():
	return (settings.musicvolume / 100) ** settings.volumegamma

def cycle_sfxvolume():
	settings.sfxvolume = util.cycle(settings.sfxvolume, settings.volumes)
	settings.save()

def cycle_musicvolume():
	settings.musicvolume = util.cycle(settings.musicvolume, settings.volumes)
	pygame.mixer.music.set_volume(get_musicvolume())
	settings.save()

mcurrent = None
def playmusic(mname):
	global mcurrent
	if mcurrent == mname:
		return
	mcurrent = mname
	pygame.mixer.init()
	pygame.mixer.music.set_volume(get_musicvolume())
	pygame.mixer.music.load(os.path.join("music", "%s.ogg" % mcurrent))
	pygame.mixer.music.play(-1)
	

