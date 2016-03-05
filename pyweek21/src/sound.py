import pygame, os
from .util import debug

# Channels 1/2/3 reserved for sound effects

sounds = {}
def getsound(sname):
	if sname not in sounds:
		if os.path.exists("data/" + sname):
			sounds[sname] = pygame.mixer.Sound("data/" + sname)
		else:
			sounds[sname] = None
			debug("Missing sound:", sname)
	return sounds[sname]

def play(sname, channel = None):
	sound = getsound(sname)
	if sound is None:
		return
	if channel is not None:
		pygame.mixer.Channel(channel).play(sound)
	else:
		for channel in (1, 2, 3):
			c = pygame.mixer.Channel(channel)
			if not c.get_busy():
				c.play(sound)
				break
			
