import pygame, os.path, functools
cache = functools.lru_cache(None)

pygame.mixer.pre_init(frequency=22050, size=16, channels=1, buffer=512)

def init():
	pygame.mixer.init()

@cache
def getsound(sname):
	path = os.path.join("sound", f"{sound}.ogg")
	if not os.path.exists(path):
		print(f"Missing sound: {path}")
		return None
	return pygame.mixer.Sound(path)

def play(sname):
	sound = getsound(sname)
	if sound is None: return
	sound.set_volume(settings.soundvolume)
	sound.play()

currentmusic = None
def playmusic(mname):
	global currentmusic
	music = getsound(mname)
	if music is currentmusic:
		return
	if currentmusic is not None:
		currentmusic.stop()
	currentmusic = music
	if currentmusic is not None:
		currentmusic.play(-1)


