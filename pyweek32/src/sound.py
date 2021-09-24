from . import settings, util

def get_sfxvolume():
	return (settings.sfxvolume / 100) ** settings.volumegamma

def get_musicvolume():
	return (settings.musicvolume / 100) ** settings.volumegamma

def cycle_sfxvolume():
	settings.sfxvolume = util.cycle(settings.sfxvolume, settings.volumes)
	settings.save()

def cycle_musicvolume():
	settings.musicvolume = util.cycle(settings.musicvolume, settings.volumes)
	settings.save()

