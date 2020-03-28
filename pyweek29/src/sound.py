import pygame, os.path, random
from functools import lru_cache
from . import settings

if not settings.noaudio:
	pygame.mixer.init()

jumpsounds = ["jump%d" % j for j in range(5)]

# Mutates the arg to keep state of least recently played
def picksound(slist):
	sound = random.choice(slist[:3])
	slist.remove(sound)
	slist.append(sound)
	return sound

@lru_cache(None)
def getsound(filename):
	path = "sound/{}.wav".format(filename)
	if os.path.exists(path):
		sound = pygame.mixer.Sound(path)
		volume = settings.soundvolume
		if filename == "no":
			volume *= 0.4
		if "jump" in filename:
			volume *= 0.2
		sound.set_volume(volume)
		return sound
	else:
		if settings.DEBUG:
			print("missing sound:", path)
		return None

def play(sname):
	if settings.nosound:
		return
	if sname == "jump":
		sname = picksound(jumpsounds)
	sound = getsound(sname)
	if sound:
		sound.play()

mcurrent = None
if not settings.nomusic:
	pygame.mixer.music.set_volume(settings.musicvolume)
def playmusic(track):
	if settings.nomusic:
		return
	global mcurrent
	if mcurrent == track:
		return
	pygame.mixer.music.load("music/{}.ogg".format(track))
	pygame.mixer.music.play(-1)
	mcurrent = track

